"""ipek"""
from process import Process
from fcfs import fcfs
from sjf import sjf
from priority import priority_scheduling
from round_robin import round_robin
from calculations import display_results


def main():
    processes = [
        Process("P1", 0, 4, 2),
        Process("P2", 1, 3, 1),
        Process("P3", 2, 2, 3)
    ]

    algorithms = {
        "1": ("FCFS", lambda: fcfs(processes)),
        "2": ("SJF", lambda: sjf(processes)),
        "3": ("Priority", lambda: priority_scheduling(processes)),
        "4": ("Round Robin", lambda: round_robin(processes, quantum=2))
    }

    print("Brain OS - CPU Scheduling Simulator")
    print("\nSample processes:")

    for p in processes:
        print(p)

    print("\nChoose a scheduling algorithm:")
    print("1. FCFS")
    print("2. SJF (additional)")
    print("3. Priority Scheduling")
    print("4. Round Robin")

    choice = input("Your choice: ").strip()

    if choice not in algorithms:
        print("Invalid choice.")
        return

    name, run_algorithm = algorithms[choice]
    results = run_algorithm()

    print(f"\nSelected algorithm: {name}")
    display_results(results)


if __name__ == "__main__":
    main()
