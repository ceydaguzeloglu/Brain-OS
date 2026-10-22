"""nada"""
class Process:
    """stores the information of a process."""

    def __init__(self, pid, arrival_time, burst_time, priority=1):
        if not isinstance(pid, str) or not pid.strip():
            raise ValueError("Process ID cannot be empty.")

        if any(type(v) is not int for v in
               (arrival_time, burst_time, priority)):
            raise ValueError("Time and priority must be integers.")

        if arrival_time < 0:
            raise ValueError("Arrival time cannot be negative.")
        if burst_time <= 0:
            raise ValueError("Burst time must be positive.")
        if priority < 1:
            raise ValueError("Priority must be 1 or greater.")

        self.pid = pid.strip()
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority

    def __str__(self):
        return (
            f"{self.pid}: arrival={self.arrival_time}, "
            f"burst={self.burst_time}, priority={self.priority}"
        )


def read_processes():
    """read process information from the terminal."""
    processes = []
    count = int(input("Number of processes: "))

    if count <= 0:
        raise ValueError("The number of processes must be positive.")

    for i in range(count):
        print(f"\nProcess {i + 1}")

        pid = input("Process ID: ").strip()
        if any(p.pid == pid for p in processes):
            raise ValueError("Process IDs must be unique.")

        arrival = int(input("Arrival time: "))
        burst = int(input("Burst time: "))
        priority = int(input("Priority (1 = highest): "))

        processes.append(Process(pid, arrival, burst, priority))

    return processes
