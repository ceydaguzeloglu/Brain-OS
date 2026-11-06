"""nada"""
class Process:
    def __init__(self, pid, arrival_time, burst_time,
                 priority=1, name=None):

        if not pid:
            raise ValueError("Process ID cannot be empty.")

        if any(type(v) is not int for v in
               (arrival_time, burst_time, priority)):
            raise ValueError("Time and priority must be integers.")

        if arrival_time < 0 or burst_time <= 0 or priority < 1:
            raise ValueError("Invalid process values.")

        self.pid = pid
        self.name = name if name else pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority

    def __str__(self):
        return (
            f"{self.name}: "
            f"Arrival={self.arrival_time}, "
            f"Burst={self.burst_time}, "
            f"Priority={self.priority}"
        )