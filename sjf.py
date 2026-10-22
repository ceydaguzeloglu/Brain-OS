"""ceyda"""
def sjf(processes):
    remaining = list(processes)
    current_time = 0
    results = []

    while remaining:
        available = [
            p for p in remaining
            if p.arrival_time <= current_time
        ]

        if not available:
            current_time = min(p.arrival_time for p in remaining)
            continue

        p = min(
            available,
            key=lambda p: (p.burst_time, p.arrival_time, p.pid)
        )

        start = current_time
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
        remaining.remove(p)

    return results

