// ipek
const COLORS = [
  "#4263eb", "#e8590c", "#2f9e44", "#ae3ec9",
  "#1098ad", "#d6336c", "#5c940d", "#f08c00",
  "#7048e8", "#0b7285", "#c2255c", "#495057"
];

const SAMPLE = [
  { pid: "P1", arrival: 0, burst: 4, priority: 2 },
  { pid: "P2", arrival: 1, burst: 3, priority: 1 },
  { pid: "P3", arrival: 2, burst: 2, priority: 3 }
];

const PX_PER_UNIT = 28;

let processes = SAMPLE.map(p => ({ ...p }));
let lastRun = null;
let activeTab = "fcfs";

const $ = id => document.getElementById(id);

function colorFor(pid) {
  const index = processes.findIndex(p => p.pid === pid);
  return COLORS[(index < 0 ? 0 : index) % COLORS.length];
}

function nextPid() {
  let n = processes.length + 1;
  while (processes.some(p => p.pid === `P${n}`)) n++;
  return `P${n}`;
}

function el(tag, attrs = {}, children = []) {
  const node = document.createElement(tag);
  for (const [key, value] of Object.entries(attrs)) {
    if (key === "class") node.className = value;
    else if (key === "text") node.textContent = value;
    else if (key === "style") node.style.cssText = value;
    else node.setAttribute(key, value);
  }
  for (const child of children) node.append(child);
  return node;
}

// ---- process input table ----

function renderProcesses() {
  const body = $("process-rows");
  body.replaceChildren();

  processes.forEach((p, i) => {
    const field = (key, type) => {
      const input = el("input", {
        type,
        value: p[key],
        "aria-label": `${key} of process ${i + 1}`
      });
      if (type === "number") {
        input.min = key === "arrival" ? 0 : 1;
        input.step = 1;
      }
      input.addEventListener("input", () => {
        p[key] = type === "number" ? toInt(input.value) : input.value;
        if (key === "pid") swatch.style.background = colorFor(p.pid);
      });
      return input;
    };

    const swatch = el("span", { class: "swatch", style: `background:${colorFor(p.pid)}` });
    const remove = el("button", {
      type: "button",
      class: "remove",
      "aria-label": `Remove ${p.pid}`,
      text: "✕"
    });
    remove.addEventListener("click", () => {
      processes.splice(i, 1);
      renderProcesses();
    });

    body.append(el("tr", {}, [
      el("td", {}, [el("div", { class: "pid-cell" }, [swatch, field("pid", "text")])]),
      el("td", {}, [field("arrival", "number")]),
      el("td", {}, [field("burst", "number")]),
      el("td", {}, [field("priority", "number")]),
      el("td", {}, [remove])
    ]));
  });
}

function toInt(value) {
  const n = Number(value);
  return value.trim() !== "" && Number.isInteger(n) ? n : value;
}

function randomProcesses() {
  const count = 3 + Math.floor(Math.random() * 4);
  const rand = (min, max) => min + Math.floor(Math.random() * (max - min + 1));
  return Array.from({ length: count }, (_, i) => ({
    pid: `P${i + 1}`,
    arrival: i === 0 ? 0 : rand(0, 8),
    burst: rand(1, 8),
    priority: rand(1, 5)
  }));
}

// ---- simulation ----

function showError(message) {
  const box = $("error");
  box.textContent = message || "";
  box.hidden = !message;
}

async function run() {
  showError("");
  const quantum = toInt($("quantum").value);

  try {
    const response = await fetch("/api/simulate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ processes, quantum })
    });
    const data = await response.json();

    if (!response.ok) {
      showError(data.error || "Simulation failed.");
      return;
    }

    lastRun = data;
    renderOutput();
  } catch (e) {
    showError("Could not reach the server. Is app.py running?");
  }
}

// ---- output ----

function renderOutput() {
  $("empty-state").hidden = !!lastRun;
  if (!lastRun) return;

  renderTabs();

  const comparing = activeTab === "compare";
  $("algorithm-view").hidden = comparing;
  $("compare-view").hidden = !comparing;

  if (comparing) renderCompare();
  else renderAlgorithm(lastRun.algorithms.find(a => a.key === activeTab));
}

function renderTabs() {
  const tabs = $("tabs");
  tabs.replaceChildren();

  const entries = lastRun.algorithms.map(a => [a.key, a.name]);
  entries.push(["compare", "Compare all"]);

  for (const [key, name] of entries) {
    const tab = el("button", {
      type: "button",
      class: "tab",
      role: "tab",
      "aria-selected": String(key === activeTab),
      text: name
    });
    tab.addEventListener("click", () => {
      activeTab = key;
      renderOutput();
    });
    tabs.append(tab);
  }
}

function renderAlgorithm(algo) {
  renderGantt(algo.timeline);

  $("stat-waiting").textContent = algo.avg_waiting.toFixed(2);
  $("stat-turnaround").textContent = algo.avg_turnaround.toFixed(2);

  const body = $("result-rows");
  body.replaceChildren();

  for (const r of algo.results) {
    const swatch = el("span", { class: "swatch", style: `background:${colorFor(r.PID)}` });
    body.append(el("tr", {}, [
      el("td", {}, [el("div", { class: "pid-cell" }, [swatch, r.PID])]),
      el("td", { text: r.Start }),
      el("td", { text: r.Completion }),
      el("td", { text: r.Waiting }),
      el("td", { text: r.Turnaround })
    ]));
  }
}

function renderGantt(timeline) {
  const total = timeline.length ? timeline[timeline.length - 1].end : 0;
  const pct = t => (total ? (t / total) * 100 : 0);

  const bar = el("div", { class: "gantt-bar" });
  const axis = el("div", { class: "gantt-axis" });
  const ticks = new Set([0]);

  for (const s of timeline) {
    const width = `width:${pct(s.end - s.start)}%`;
    const label = `${s.pid ?? "idle"}: ${s.start}–${s.end}`;

    bar.append(s.pid === null
      ? el("div", { class: "slice idle", style: width, title: label, text: "idle" })
      : el("div", {
          class: "slice",
          style: `${width};background:${colorFor(s.pid)}`,
          title: label,
          text: s.pid
        }));

    ticks.add(s.start);
    ticks.add(s.end);
  }

  for (const t of [...ticks].sort((a, b) => a - b)) {
    axis.append(el("span", { class: "tick", style: `left:${pct(t)}%`, text: t }));
  }

  const inner = el("div", {
    class: "gantt-inner",
    style: `width:${total * PX_PER_UNIT}px`
  }, [bar, axis]);

  $("gantt").replaceChildren(inner);
}

function renderCompare() {
  const algorithms = lastRun.algorithms;
  const max = Math.max(...algorithms.map(a => a.avg_waiting), 1);

  const bars = $("compare-bars");
  const rows = $("compare-rows");
  bars.replaceChildren();
  rows.replaceChildren();

  for (const a of algorithms) {
    const best = a.key === lastRun.best ? " best" : "";

    bars.append(el("div", { class: `bar-row${best}` }, [
      el("span", { text: a.name }),
      el("div", { class: "bar-track" }, [
        el("div", { class: "bar-fill", style: `width:${(a.avg_waiting / max) * 100}%` })
      ]),
      el("span", { class: "bar-value", text: a.avg_waiting.toFixed(2) })
    ]));

    rows.append(el("tr", { class: best.trim() }, [
      el("td", { text: a.name }),
      el("td", { text: a.avg_waiting.toFixed(2) }),
      el("td", { text: a.avg_turnaround.toFixed(2) })
    ]));
  }

  const winner = algorithms.find(a => a.key === lastRun.best);
  const note = $("best-note");
  note.replaceChildren(
    "Lowest average waiting time: ",
    el("strong", { text: winner.name }),
    ` (${winner.avg_waiting.toFixed(2)})`
  );
}

// ---- theme ----

function initTheme() {
  try {
    const saved = localStorage.getItem("brain-os-theme");
    if (saved) document.documentElement.dataset.theme = saved;
  } catch (e) { /* storage unavailable */ }

  $("theme-toggle").addEventListener("click", () => {
    const current = document.documentElement.dataset.theme
      || (matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
    const next = current === "dark" ? "light" : "dark";
    document.documentElement.dataset.theme = next;
    try { localStorage.setItem("brain-os-theme", next); } catch (e) { /* ignore */ }
  });
}

// ---- wiring ----

$("add-process").addEventListener("click", () => {
  processes.push({ pid: nextPid(), arrival: 0, burst: 1, priority: 1 });
  renderProcesses();
});

$("load-sample").addEventListener("click", () => {
  processes = SAMPLE.map(p => ({ ...p }));
  renderProcesses();
  run();
});

$("load-random").addEventListener("click", () => {
  processes = randomProcesses();
  renderProcesses();
  run();
});

$("run").addEventListener("click", run);

document.addEventListener("keydown", e => {
  if (e.key === "Enter" && e.target.tagName === "INPUT") run();
});

initTheme();
renderProcesses();
run();
