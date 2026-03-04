import simpy as sp
import random 
import statistics

random_seed = 2
#random.seed(random_seed)
interval = 10
NUM_PROCESSES=25
RAM_CAPACITY=100
INSTRUCTIONS_PER_CYCLE = 3
NUM_CPUS=1


env = sp.Environment()


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

avg, std = run_simulation(NUM_PROCESSES, INTERVAL, RAM_CAPACITY, INSTRUCTIONS_PER_CYCLE, NUM_CPUS)
print(f"Procesos: {NUM_PROCESSES} | Promedio: {avg:.2f} | Desviación: {std:.2f}")