"""ipek"""
from process import Process, read_processes
from fcfs import fcfs
from sjf import sjf
from priority import priority_scheduling
from round_robin import round_robin
from calculations import (
    display_results,
    average_waiting_time,
    average_turnaround_time
)


def sample_processes():
    return [
        Process("P1", 0, 4, 2),
        Process("P2", 1, 3, 1),
        Process("P3", 2, 2, 3)
    ]


def choose_processes():
    print("\nHow do you want to enter the processes?")
    print("1. Use sample processes")
    print("2. Enter processes manually")

    choice = input("Your choice: ").strip()

    if choice == "2":
        try:
            return read_processes()
        except ValueError as e:
            print(f"Invalid input: {e}")
            print("Using sample processes instead.")

    return sample_processes()


def read_quantum():
    value = input("Time quantum for Round Robin (default 2): ").strip()

    if not value:
        return 2

    try:
        quantum = int(value)
    except ValueError:
        print("Invalid quantum. Using default 2.")
        return 2

    if quantum <= 0:
        print("Quantum must be positive. Using default 2.")
        return 2

    return quantum


def compare_all(algorithms):
    print("\nComparison of All Algorithms")
    print("-" * 50)
    print(f"{'Algorithm':<15}{'Avg Waiting':<18}{'Avg Turnaround':<18}")

    averages = []

    for name, run_algorithm in algorithms:
        results = run_algorithm()
        waiting = average_waiting_time(results)
        turnaround = average_turnaround_time(results)
        averages.append((name, waiting))

        print(f"{name:<15}{waiting:<18.2f}{turnaround:<18.2f}")

    print("-" * 50)

    best_name, best_waiting = min(averages, key=lambda a: a[1])
    print(
        f"Lowest average waiting time: {best_name} "
        f"({best_waiting:.2f})"
    )


def main():
    print("Brain OS - CPU Scheduling Simulator")

    processes = choose_processes()
    quantum = read_quantum()

    algorithms = {
        "1": ("FCFS", lambda: fcfs(processes)),
        "2": ("SJF", lambda: sjf(processes)),
        "3": ("Priority", lambda: priority_scheduling(processes)),
        "4": ("Round Robin", lambda: round_robin(processes, quantum))
    }

    print("\nProcesses:")

    for p in processes:
        print(p)

    while True:
        print("\nChoose a scheduling algorithm:")
        print("1. FCFS")
        print("2. SJF (additional)")
        print("3. Priority Scheduling")
        print(f"4. Round Robin (quantum={quantum})")
        print("5. Compare all algorithms")
        print("0. Exit")

        choice = input("Your choice: ").strip()

        if choice == "0":
            print("Goodbye!")
            break

        if choice == "5":
            compare_all(algorithms.values())
            continue

        if choice not in algorithms:
            print("Invalid choice.")
            continue

        name, run_algorithm = algorithms[choice]
        results = run_algorithm()

        print(f"\nSelected algorithm: {name}")
        display_results(results)


if __name__ == "__main__":
    main()
