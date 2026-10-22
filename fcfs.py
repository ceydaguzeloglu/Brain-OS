"""ceyda"""

def fcfs(processes):
    ordered = sorted(processes, key=lambda p: p.arrival_time)
    current_time = 0
    results = []

    for p in ordered:
        start = max(current_time, p.arrival_time)
        completion = start + p.burst_time
        turnaround = completion - p.arrival_time
        waiting = turnaround - p.burst_time

        results.append({
            "PID": p.pid,
            "Start": start,
            "Completion": completion,
            "Waiting": waiting,
            "Turnaround": turnaround
        })

        current_time = completion

    return results
