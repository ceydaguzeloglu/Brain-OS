"""ipek"""
from flask import Flask, jsonify, render_template, request

from process import Process
from fcfs import fcfs
from sjf import sjf
from priority import priority_scheduling
from round_robin import round_robin
from calculations import average_waiting_time, average_turnaround_time

MAX_PROCESSES = 26
MAX_TIME = 1000

app = Flask(__name__)


def parse_processes(data):
    """build Process objects from the JSON request body."""
    items = data.get("processes")

    if not isinstance(items, list) or not items:
        raise ValueError("At least one process is required.")
    if len(items) > MAX_PROCESSES:
        raise ValueError(f"At most {MAX_PROCESSES} processes are allowed.")

    processes = []

    for item in items:
        p = Process(
            str(item.get("pid", "")),
            item.get("arrival"),
            item.get("burst"),
            item.get("priority", 1)
        )

        if any(other.pid == p.pid for other in processes):
            raise ValueError("Process IDs must be unique.")
        if p.arrival_time > MAX_TIME or p.burst_time > MAX_TIME:
            raise ValueError(f"Times must be at most {MAX_TIME}.")

        processes.append(p)

    return processes


def parse_quantum(data):
    quantum = data.get("quantum", 2)

    if type(quantum) is not int or quantum <= 0:
        raise ValueError("Quantum must be a positive integer.")

    return quantum


def with_idle(slices):
    """turn (pid, start, end) slices into a gantt timeline with idle gaps."""
    timeline = []
    current_time = 0

    for pid, start, end in sorted(slices, key=lambda s: s[1]):
        if start > current_time:
            timeline.append({"pid": None, "start": current_time,
                             "end": start})

        timeline.append({"pid": pid, "start": start, "end": end})
        current_time = end

    return timeline


def run_all(processes, quantum):
    rr_slices = []

    runs = [
        ("fcfs", "FCFS", fcfs(processes)),
        ("sjf", "SJF", sjf(processes)),
        ("priority", "Priority", priority_scheduling(processes)),
        ("rr", f"Round Robin (q={quantum})",
         round_robin(processes, quantum, rr_slices))
    ]

    algorithms = []

    for key, name, results in runs:
        if key == "rr":
            slices = rr_slices
        else:
            # non-preemptive: each process runs once, start to completion.
            slices = [(r["PID"], r["Start"], r["Completion"])
                      for r in results]

        algorithms.append({
            "key": key,
            "name": name,
            "results": results,
            "timeline": with_idle(slices),
            "avg_waiting": average_waiting_time(results),
            "avg_turnaround": average_turnaround_time(results)
        })

    best = min(algorithms, key=lambda a: a["avg_waiting"])

    return {"algorithms": algorithms, "best": best["key"]}


@app.route("/")
def index():
    return render_template("index.html")


@app.post("/api/simulate")
def simulate():
    data = request.get_json(silent=True) or {}

    try:
        processes = parse_processes(data)
        quantum = parse_quantum(data)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    return jsonify(run_all(processes, quantum))


if __name__ == "__main__":
    app.run(debug=True)
