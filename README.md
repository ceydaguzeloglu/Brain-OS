# Brain OS — CPU Scheduling Simulator

Simulates and compares CPU scheduling algorithms:

- **FCFS** — First Come, First Served
- **SJF** — Shortest Job First (non-preemptive)
- **Priority** — non-preemptive, 1 = highest priority
- **Round Robin** — configurable time quantum

For every algorithm it reports start, completion, waiting and turnaround
times per process, plus the averages.

## Web interface

```bash
pip install -r requirements.txt
python app.py
```

Then open http://127.0.0.1:5000.

- Edit the process table, or load the sample / random processes
- Set the Round Robin time quantum
- See a Gantt chart (with idle time) and the results table for each algorithm
- **Compare all** shows the average waiting / turnaround times side by side
  and highlights the algorithm with the lowest average waiting time

## Command line

```bash
python main.py
```

## Project structure

| File | Description |
| --- | --- |
| `process.py` | `Process` class and terminal input |
| `fcfs.py`, `sjf.py`, `priority.py`, `round_robin.py` | Scheduling algorithms |
| `calculations.py` | Averages and terminal output |
| `main.py` | Command-line menu |
| `app.py` | Flask server and `POST /api/simulate` endpoint |
| `templates/`, `static/` | Web interface (HTML, CSS, JavaScript) |

### API

`POST /api/simulate`

```json
{
  "processes": [
    { "pid": "P1", "arrival": 0, "burst": 4, "priority": 2 }
  ],
  "quantum": 2
}
```

Returns the results, Gantt timeline and averages for every algorithm, and
the key of the algorithm with the lowest average waiting time (`best`).
