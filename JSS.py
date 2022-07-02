import random

machNo = 5
job = 5
tasks = 5

machines = []
times = []

def encode(popSize):
    finPop = []

    for _ in range(popSize):
        finPop.append(random.sample(range(job*tasks), job*tasks))

    return finPop

genome = encode(30)

def fitness(chromosome):
    machT = [0 for _ in range(machNo)]
    jobs = [0 for _ in range(tasks)]

    started = [[]]

    for i in chromosome:
        index = (i-1)//jobs
        machine = machines[index][jobs[index]]
        time = times[index][jobs[index]]
        machT[machine] += time
        prevMach = machines[index][jobs[index]-1]
        prevTime = times[index][jobs[index]-1]
        if (machT[machine] + 1 > started[index][jobs[index]-1]+prevTime):
            started[index][jobs[index]] = machT[machine] + 1
            machT[machine] += time
        else:
            started[index][jobs[index]] = machT[prevMach] + 1
            machT[machine] = machT[prevMach] + time

    makespan = max(machT)

    return makespan

fitnesses = []

for i in genome:
    fitnesses.append(fitness(i))

def rouletteWheel (pop):
    sm = sum(fitnesses)
    chosen = random.uniform(0, sm)
    curr = 0
    for i in range(len(pop)):
        curr += fitnesses[i]
        if (curr > chosen):
            return pop[i]

def crossover (par1, par2):
    child1 = list(par1)
    child2 = list(par2)

    rand = random.randint(25)

    for i in range(rand, len(par1)):
        child1[i], child2[i] = child2[i], child1[i]
    
    child1 = ''.join(child1)
    child2 = ''.join(child2)

    return child1, child2
