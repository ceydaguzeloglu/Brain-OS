"""
defne - calculations.py
Brain OS - CPU Scheduling Calculations & Display Module
"""

def calculate_turnaround_time(completion_time, arrival_time):
    # Geri dönüş süresini (turnaround) hesaplayan fonksiyon.
    return completion_time - arrival_time

def calculate_waiting_time(turnaround_time, burst_time):
    # Bekleme süresini hesaplar.
    return turnaround_time - burst_time

def average_waiting_time(results):
    if not results:
        return 0
    return sum(r["Waiting"] for r in results) / len(results)

def average_turnaround_time(results):
    if not results:
        return 0
    return sum(r["Turnaround"] for r in results) / len(results)

def cpu_utilization(processes, results):
    if not results:
        return 0
    total_burst = sum(p.burst_time for p in processes)
    max_completion = max(r["Completion"] for r in results)
    if max_completion == 0:
        return 0
    return (total_burst / max_completion) * 100

def throughput(processes, results):
    if not results:
        return 0
    max_completion = max(r["Completion"] for r in results)
    if max_completion == 0:
        return 0
    return len(processes) / max_completion

def display_gantt_chart(results):
    print("\nGantt Chart Execution Order:")
    chart = "|"
    for r in results:
        chart += f" {r['PID']} ({r['Start']}-{r['Completion']}) |"
    print(chart)

def display_results(results, processes=None):
    if not results:
        print("No results to display.")
        return

    print("\n" + "="*65)
    print("                      SCHEDULING RESULTS")
    print("="*65)
    print(
        f"{'PID':<10}{'Start':<10}{'Completion':<15}"
        f"{'Waiting':<12}{'Turnaround':<12}"
    )
    print("-" * 65)

    for r in results:
        print(
            f"{r['PID']:<10}{r['Start']:<10}{r['Completion']:<15}"
            f"{r['Waiting']:<12}{r['Turnaround']:<12}"
        )

    print("-" * 65)
    print(f"Average Waiting Time:    {average_waiting_time(results):.2f}")
    print(f"Average Turnaround Time: {average_turnaround_time(results):.2f}")
    
    if processes:
        print(f"CPU Utilization:         {cpu_utilization(processes, results):.2f}%")
        print(f"Throughput:              {throughput(processes, results):.2f} processes/unit time")
        display_gantt_chart(results)
        
    print("="*65)

def compare_all_algorithms(results_dict, processes):
    """
    Tüm algoritmaların performansını tek bir tabloda karşılaştırır.
    """
    print("\n" + "="*60)
    print("           ALGORITHM PERFORMANCE COMPARISON")
    print("="*60)
    print(f"{'Algorithm':<20}{'Avg Waiting':<18}{'Avg Turnaround':<18}")
    print("-" * 60)
    
    best_algo = None
    min_avg_wait = float('inf')
    
    for algo_name, res in results_dict.items():
        avg_wait = average_waiting_time(res)
        avg_turn = average_turnaround_time(res)
        print(f"{algo_name:<20}{avg_wait:<18.2f}{avg_turn:<18.2f}")
        
        if avg_wait < min_avg_wait:
            min_avg_wait = avg_wait
            best_algo = algo_name
            
    print("-" * 60)
    print(f" Best Algorithm (Lowest Waiting Time): {best_algo}")
    print("="*60)

def safe_int_input(prompt):
    """
    Kullanıcı yanlışlıkla harf veya geçersiz değer girerse programın
    çökmesini önleyen güvenli girdi alma fonksiyonu.
    """
    while True:
        try:
            val = int(input(prompt))
            if val < 0:
                print("Lütfen negatif olmayan bir sayı girin!")
                continue
            return val
        except ValueError:
            print("Geçersiz girdi! Lütfen sadece tam sayı girin.")