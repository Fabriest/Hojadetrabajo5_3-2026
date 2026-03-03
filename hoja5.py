import sympy as sp
import random 

random_seed = 2
#random.seed(random_seed)
interval = 10


env = sp.Enviroment()


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
            event = random.randint(1,10)
            if event == 1:
                yield env.timeout(1)
    
    yield ram.put(memory_requiered)

    finish_time = env.now
    total_time = finish_time - start_time
    time.append(total_time)

env.process()