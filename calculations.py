"""defne"""

def calculate_turnaround_time(completion_time, arrival_time):#geridönüş süresini(turnaround) hesaplayan fonksiyon tanımlar. Sürecin bitiş zamanından ,sisteme varış zamanını çıkararak  geri dönüş süresini bulur.
    return completion_time - arrival_time


def calculate_waiting_time(turnaround_time, burst_time):#bekleme süresini hesaplıyor. toplam geridönüş süresinden ,sürecin işlemcide harcadığı gerçek süreyi(burst time)çıkarark, process in ne kadar boş beklediğini hesaplıyor. 
    return turnaround_time - burst_time


def average_waiting_time(results):
    if not results:
        return 0

    return sum(r["Waiting"] for r in results) / len(results)


def average_turnaround_time(results):
    if not results:
        return 0

    return sum(r["Turnaround"] for r in results) / len(results)


def display_results(results):
    if not results:
        print("No results to display.")
        return

    print("\nScheduling Results")
    print("-" * 65)
    print(
        f"{'PID':<10}{'Start':<10}{'Completion':<15}"#metni 10 karakterlik bir alana sola dayalı olarak yerleştirir.
        f"{'Waiting':<12}{'Turnaround':<12}"
    )

    for r in results:
        print(
            f"{r['PID']:<10}{r['Start']:<10}{r['Completion']:<15}"
            f"{r['Waiting']:<12}{r['Turnaround']:<12}"
        )

    print("-" * 65)
    print(f"Average Waiting Time: {average_waiting_time(results):.2f}")
    print(
        "Average Turnaround Time: "
        f"{average_turnaround_time(results):.2f}"
    )
