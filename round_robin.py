"""ceyda"""

from collections import deque


def round_robin(processes, quantum=2, timeline=None):
    """timeline: optional list, filled with (pid, start, end) slices."""
    if type(quantum) is not int or quantum <= 0:
        raise ValueError("Quantum must be a positive integer.")

    ordered = sorted(processes, key=lambda p: p.arrival_time)
    remaining = {p.pid: p.burst_time for p in ordered}
    first_start = {}
    completion_times = {}
    ready = deque()

    current_time = 0
    next_index = 0

    while next_index < len(ordered) or ready:
        if not ready:
            current_time = max(
                current_time, ordered[next_index].arrival_time
            )

            while (
                next_index < len(ordered)
                and ordered[next_index].arrival_time <= current_time
            ):
                ready.append(ordered[next_index])
                next_index += 1

        p = ready.popleft()
        first_start.setdefault(p.pid, current_time)

        run_time = min(quantum, remaining[p.pid])
        if timeline is not None:
            timeline.append((p.pid, current_time, current_time + run_time))
        current_time += run_time
        remaining[p.pid] -= run_time

        # add processes that arrived while this process was running.
        while (
            next_index < len(ordered)
            and ordered[next_index].arrival_time <= current_time
        ):
            ready.append(ordered[next_index])
            next_index += 1

        if remaining[p.pid] > 0:
            ready.append(p)
        else:
            completion_times[p.pid] = current_time

    results = []

    for p in ordered:
        turnaround = completion_times[p.pid] - p.arrival_time
        waiting = turnaround - p.burst_time

        results.append({
            "PID": p.pid,
            "Start": first_start[p.pid],
            "Completion": completion_times[p.pid],
            "Waiting": waiting,
            "Turnaround": turnaround
        })

    return results

