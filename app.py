"""ipek - app.py
Brain OS - Web frontend (Streamlit)

Run:  python -m streamlit run app.py

This file only USES the team's modules (process, fcfs, sjf, priority,
round_robin, calculations); it does not change them.
"""

from collections import deque

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from process import Process
from fcfs import fcfs
from sjf import sjf
from priority import priority_scheduling
from round_robin import round_robin
from calculations import (
    average_waiting_time,
    average_turnaround_time,
    cpu_utilization,
    throughput,
)

st.set_page_config(page_title="Brain OS - CPU Scheduler", page_icon="🧠", layout="wide")

ALGORITHMS = {
    "FCFS": "First Come, First Served - processes run in arrival order.",
    "SJF": "Shortest Job First (non-preemptive) - shortest burst among arrived processes runs next.",
    "Priority": "Priority Scheduling (non-preemptive) - 1 = highest priority.",
    "Round Robin": "Each process runs for at most one time quantum, then goes to the back of the queue.",
}

EXAMPLE = pd.DataFrame(
    {
        "Name": ["P1", "P2", "P3"],
        "Arrival": [0, 1, 2],
        "Burst": [4, 3, 2],
        "Priority": [2, 1, 3],
    }
)

PALETTE = ["#4C78A8", "#F58518", "#54A24B", "#E45756", "#72B7B2",
           "#B279A2", "#EECA3B", "#9D755D", "#FF9DA6", "#BAB0AC"]


# ---------------------------------------------------------------- helpers
def build_processes(df):
    """Turn the editor table into the team's Process objects."""
    processes = []
    for i, row in enumerate(df.dropna(how="all").itertuples(index=False)):
        name = str(row.Name).strip() if pd.notna(row.Name) and str(row.Name).strip() else f"P{i + 1}"
        try:
            processes.append(
                Process(f"T{i + 1}", int(row.Arrival), int(row.Burst), int(row.Priority), name)
            )
        except (ValueError, TypeError) as e:
            raise ValueError(f"Row {i + 1} ({name}): {e}") from None
    if not processes:
        raise ValueError("Add at least one process.")
    return processes


def run_algorithm(name, processes, quantum):
    if name == "FCFS":
        return fcfs(processes)
    if name == "SJF":
        return sjf(processes)
    if name == "Priority":
        return priority_scheduling(processes)
    return round_robin(processes, quantum)


def rr_timeline(processes, quantum):
    """Every CPU slice of Round Robin (same queue rules as round_robin.py),
    so the Gantt chart can show P1 -> P2 -> P1 ... instead of one block."""
    ordered = sorted(processes, key=lambda p: p.arrival_time)
    remaining = {p.pid: p.burst_time for p in ordered}
    ready, slices = deque(), []
    t, nxt = 0, 0
    while nxt < len(ordered) or ready:
        if not ready:
            t = max(t, ordered[nxt].arrival_time)
            while nxt < len(ordered) and ordered[nxt].arrival_time <= t:
                ready.append(ordered[nxt]); nxt += 1
        p = ready.popleft()
        run = min(quantum, remaining[p.pid])
        slices.append((p.name, t, t + run))
        t += run
        remaining[p.pid] -= run
        while nxt < len(ordered) and ordered[nxt].arrival_time <= t:
            ready.append(ordered[nxt]); nxt += 1
        if remaining[p.pid] > 0:
            ready.append(p)
    return slices


def timeline(name, processes, results, quantum):
    if name == "Round Robin":
        return rr_timeline(processes, quantum)
    return [(r["PID"], r["Start"], r["Completion"]) for r in results]


def with_idle(slices):
    """Insert IDLE gaps where the CPU waits for the next arrival."""
    out, t = [], 0
    for n, s, e in sorted(slices, key=lambda x: x[1]):
        if s > t:
            out.append(("IDLE", t, s))
        out.append((n, s, e))
        t = e
    return out


def gantt_figure(slices, names):
    colors = {n: PALETTE[i % len(PALETTE)] for i, n in enumerate(names)}
    colors["IDLE"] = "rgba(150,150,150,0.25)"
    fig = go.Figure()
    shown = set()
    for n, s, e in with_idle(slices):
        fig.add_trace(go.Bar(
            x=[e - s], base=[s], y=["CPU"], orientation="h",
            marker=dict(color=colors[n], line=dict(color="white", width=2)),
            text=n, textposition="inside", insidetextanchor="middle",
            name=n, legendgroup=n, showlegend=n not in shown,
            hovertemplate=f"<b>{n}</b><br>{s} → {e}<extra></extra>",
        ))
        shown.add(n)
    end = max(e for _, _, e in slices)
    fig.update_layout(
        barmode="overlay", height=190, margin=dict(l=10, r=10, t=10, b=10),
        xaxis=dict(title="Time", tickmode="linear", dtick=1 if end <= 30 else None,
                   range=[0, end], showgrid=True),
        yaxis=dict(showticklabels=False),
        legend=dict(orientation="h", y=-0.45),
        uniformtext=dict(minsize=10, mode="hide"),
    )
    return fig


def results_table(results, processes):
    by_name = {p.name: p for p in processes}
    rows = []
    for r in results:
        p = by_name[r["PID"]]
        rows.append({
            "Process": r["PID"], "Arrival": p.arrival_time, "Burst": p.burst_time,
            "Priority": p.priority, "Start": r["Start"], "Completion": r["Completion"],
            "Waiting": r["Waiting"], "Turnaround": r["Turnaround"],
        })
    return pd.DataFrame(rows)


# ---------------------------------------------------------------- sidebar
with st.sidebar:
    st.title("🧠 Brain OS")
    st.caption("CPU Scheduling Simulator")
    algo = st.radio("Algorithm", list(ALGORITHMS))
    quantum = st.number_input("Time quantum (Round Robin)", min_value=1, value=2, step=1,
                              disabled=algo != "Round Robin")
    st.info(ALGORITHMS[algo])
    st.divider()
    if st.button("↺ Load example processes", width="stretch"):
        st.session_state.pop("editor", None)
        st.session_state["data"] = EXAMPLE.copy()

# ---------------------------------------------------------------- main
st.title("Brain OS - CPU Scheduler")

st.subheader("1. Processes")
st.caption("Edit the table: add rows with the + at the bottom, delete with the checkbox. Priority 1 = highest.")
data = st.data_editor(
    st.session_state.get("data", EXAMPLE),
    key="editor", num_rows="dynamic", width="stretch", hide_index=True,
    column_config={
        "Name": st.column_config.TextColumn("Name", required=True),
        "Arrival": st.column_config.NumberColumn("Arrival", min_value=0, step=1, required=True),
        "Burst": st.column_config.NumberColumn("Burst", min_value=1, step=1, required=True),
        "Priority": st.column_config.NumberColumn("Priority", min_value=1, step=1, required=True),
    },
)

try:
    processes = build_processes(data)
except ValueError as e:
    st.error(str(e))
    st.stop()

if len({p.name for p in processes}) != len(processes):
    st.error("Process names must be unique.")
    st.stop()

names = [p.name for p in processes]
results = run_algorithm(algo, processes, int(quantum))

tab_run, tab_cmp = st.tabs([f"2. {algo} result", "3. Compare all algorithms"])

with tab_run:
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Avg waiting", f"{average_waiting_time(results):.2f}")
    c2.metric("Avg turnaround", f"{average_turnaround_time(results):.2f}")
    c3.metric("CPU utilization", f"{cpu_utilization(processes, results):.1f}%")
    c4.metric("Throughput", f"{throughput(processes, results):.2f} /unit")

    st.markdown("**Gantt chart**")
    st.plotly_chart(gantt_figure(timeline(algo, processes, results, int(quantum)), names),
                    width="stretch")

    st.markdown("**Process table**")
    st.dataframe(results_table(results, processes), width="stretch", hide_index=True)

with tab_cmp:
    rows = []
    for a in ALGORITHMS:
        r = run_algorithm(a, processes, int(quantum))
        rows.append({
            "Algorithm": a if a != "Round Robin" else f"Round Robin (q={int(quantum)})",
            "Avg waiting": round(average_waiting_time(r), 2),
            "Avg turnaround": round(average_turnaround_time(r), 2),
            "CPU utilization %": round(cpu_utilization(processes, r), 1),
            "Throughput": round(throughput(processes, r), 2),
            "_tl": timeline(a, processes, r, int(quantum)),
        })
    cmp = pd.DataFrame(rows)
    best = cmp.loc[cmp["Avg waiting"].idxmin(), "Algorithm"]
    st.success(f"🏆 Best algorithm (lowest average waiting time): **{best}**")

    fig = go.Figure([
        go.Bar(name="Avg waiting", x=cmp["Algorithm"], y=cmp["Avg waiting"], marker_color="#4C78A8",
               text=cmp["Avg waiting"], textposition="outside"),
        go.Bar(name="Avg turnaround", x=cmp["Algorithm"], y=cmp["Avg turnaround"], marker_color="#F58518",
               text=cmp["Avg turnaround"], textposition="outside"),
    ])
    fig.update_layout(barmode="group", height=360, margin=dict(l=10, r=10, t=30, b=10),
                      yaxis_title="Time", legend=dict(orientation="h", y=1.12))
    st.plotly_chart(fig, width="stretch")
    st.dataframe(cmp.drop(columns="_tl"), width="stretch", hide_index=True)

    st.markdown("**Gantt charts side by side**")
    for _, row in cmp.iterrows():
        st.caption(row["Algorithm"])
        st.plotly_chart(gantt_figure(row["_tl"], names), width="stretch",
                        key=f"g_{row['Algorithm']}")
