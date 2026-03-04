import simpy as sp
import random 
import statistics
import matplotlib.pyplot as plt

random_seed = 2
#random.seed(random_seed)
RAM_CAPACITY=100
INSTRUCTIONS_PER_CYCLE = 3
NUM_CPUS=1

def process(env, name, ram, cpu, time, instructions_per_cycle):
    start_time= env.now
    memory_requiered = random.randint(1,10)
    remaining_instructions = random.randint(1,10)

    yield ram.get(memory_requiered)

    while remaining_instructions > 0:
        with cpu.request() as rq:
            yield rq    

            executed = min(instructions_per_cycle, remaining_instructions)
            remaining_instructions -= executed
            yield env.timeout(1)
        
        if remaining_instructions > 0:
            event = random.randint(1,21)
            if event == 1:
                yield env.timeout(random.randint(1,5))
    
    yield ram.put(memory_requiered)

    total_time = env.now - start_time
    time.append(total_time)

def setup(env, num_processes, ram, cpu, times, instructions_per_cycle, interval):
    for i in range(num_processes):
        env.process(process(env, f"Proceso {i}", ram, cpu, times, instructions_per_cycle))
        yield env.timeout(random.expovariate(1.0 / interval))

def run_simulation(num_processes, interval, ram_capacity, instructions_per_cycle, num_cpus):
    random.seed(random_seed)
    times = []

    env = sp.Environment()
    ram = sp.Container(env, init=ram_capacity, capacity=ram_capacity)
    cpu = sp.Resource(env, capacity=num_cpus)

    env.process(setup(env, num_processes, ram, cpu, times, instructions_per_cycle, interval))
    env.run()

    avg = statistics.mean(times)
    std = statistics.stdev(times) if len(times) > 1 else 0
    return avg, std

process_counts = [25, 50, 100, 150, 200]
intervals = [10, 5, 1]

print("=" * 55)
print("PARTE 1 Y 2")
print("=" * 55)

results_by_interval = {}
for interval in intervals:
    avgs = []
    print(f"\nIntervalo = {interval}")
    for n in process_counts:
        avg, std = run_simulation(n, interval, RAM_CAPACITY, INSTRUCTIONS_PER_CYCLE, NUM_CPUS)
        avgs.append(avg)
        print(f"  Procesos: {n:3d} | Promedio: {avg:6.2f} | Desviación: {std:.2f}")
    results_by_interval[interval] = avgs

plt.figure(figsize=(8, 5))
for interval in intervals:
    plt.plot(process_counts, results_by_interval[interval], marker='o', label=f"Intervalo {interval}")
plt.xlabel("Número de procesos")
plt.ylabel("Tiempo promedio")
plt.title("PARTE 1 Y 2")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("grafica_parte1y2.png")
plt.show()

print("\n" + "=" * 55)
print("PARTE 3 — Optimizaciones (intervalo=10)")
print("=" * 55)

optimizations = {
    "Baseline (RAM=100, CPU=3, 1 CPU)":   {"ram": 100, "speed": 3, "cpus": 1},
    "a) RAM=200":                          {"ram": 200, "speed": 3, "cpus": 1},
    "b) CPU rápido (6 instr/ciclo)":       {"ram": 100, "speed": 6, "cpus": 1},
    "c) 2 CPUs":                           {"ram": 100, "speed": 3, "cpus": 2},
}

results_optimizations = {}
for label, params in optimizations.items():
    avgs = []
    print(f"\n{label}")
    for n in process_counts:
        avg, std = run_simulation(n, 10, params["ram"], params["speed"], params["cpus"])
        avgs.append(avg)
        print(f"  Procesos: {n:3d} | Promedio: {avg:6.2f} | Desviación: {std:.2f}")
    results_optimizations[label] = avgs


plt.figure(figsize=(8, 5))
for label, avgs in results_optimizations.items():
    plt.plot(process_counts, avgs, marker='o', label=label)
plt.xlabel("Número de procesos")
plt.ylabel("Tiempo promedio")
plt.title("PARTE 3")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("grafica_parte3.png")
plt.show()


print("\n" + "=" * 55)
print("PARTE 4")
print("=" * 55)

fig, axes = plt.subplots(1, 3, figsize=(16, 5), sharey=True)

for idx, interval in enumerate([10, 5, 1]):
    ax = axes[idx]
    for label, params in optimizations.items():
        avgs = []
        for n in process_counts:
            avg, _ = run_simulation(n, interval, params["ram"], params["speed"], params["cpus"])
            avgs.append(avg)
        ax.plot(process_counts, avgs, marker='o', label=label)
    ax.set_title(f"Intervalo = {interval}")
    ax.set_xlabel("Número de procesos")
    ax.set_ylabel("Tiempo promedio")
    ax.legend(fontsize=7)
    ax.grid(True)

plt.suptitle("PARTE 4")
plt.tight_layout()
plt.savefig("grafica_parte4.png")
plt.show()

print("\nGráficas guardadas")