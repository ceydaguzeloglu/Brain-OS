"""ipek"""

from process import Process
from fcfs import fcfs
from sjf import sjf
from priority import priority_scheduling
from round_robin import round_robin
from calculations import display_results


def choose_algorithm(processes):

    print("\nChoose a CPU Scheduling Algorithm:")
    print("1. FCFS")
    print("2. SJF")
    print("3. Priority Scheduling")
    print("4. Round Robin")

    choice = input("\nYour choice: ")

    if choice == "1":
        results = fcfs(processes)

    elif choice == "2":
        results = sjf(processes)

    elif choice == "3":
        results = priority_scheduling(processes)

    elif choice == "4":
        quantum = int(input("Enter Time Quantum: "))
        results = round_robin(processes, quantum)

    else:
        print("Invalid choice!")
        return

    display_results(results)


def existing_example():

    processes = [
        Process("P1", 0, 4, 2),
        Process("P2", 1, 3, 1),
        Process("P3", 2, 2, 3)
    ]

    print("\nExisting CPU Scheduling Example")

    for p in processes:
        print(p)

    choose_algorithm(processes)


def create_own_schedule():

    processes = []

    count = int(input("\nHow many tasks do you want to enter? "))

    if count <= 0:
        print("Please enter a positive number.")
        return

    for i in range(count):

        print(f"\nTask {i + 1}")

        name = input("Enter task name: ")

        arrival = int(input("Enter Arrival Time (minutes): "))
        burst = int(input("Enter Burst Time (minutes): "))
        priority = int(input("Enter Priority (1 = highest): "))

        if arrival < 0 or burst <= 0 or priority <= 0:
            print("Invalid values!")
            return

        process = Process(
            f"T{i + 1}",
            arrival,
            burst,
            priority,
            name
        )

        processes.append(process)

    print("\nYour Tasks:")

    for p in processes:
        print(p)

    choose_algorithm(processes)


def main():

    print("========================================")
    print("       BRAIN OS - CPU SCHEDULER")
    print("========================================")

    print("\nWelcome to Brain OS!")

    print("\nWhat would you like to do?")

    print("1. Create your own schedule")
    print("2. Explore an existing CPU Scheduling example")

    choice = input("\nEnter your choice: ")

    if choice == "1":
        create_own_schedule()

    elif choice == "2":
        existing_example()

    else:
        print("Invalid choice!")


if __name__ == "__main__":
    main()
