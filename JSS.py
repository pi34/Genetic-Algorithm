import random

machNo = 5 # int(input("How many machines do you have? "))
job = 5 # int(input("How many jobs do you have? "))
tasks = 5 #int(input("How many tasks in each job?"))

machines = []
times = []

for i in range(job):
    for j in range(tasks):
        machines[i][j] = int(input())
        times[i][j] = int(input())

randArr = tasks * [i for i in range(job)]

def encode(popSize):
    finPop = []

    for _ in range(popSize):
        finPop.append(random.sample(randArr, job*tasks))

    return finPop


def fitness(chromosome):
    machT = [0 for _ in range(machNo)]
    jobs = [0 for _ in range(tasks)]

    started = []

    for _ in range(job):
        arr = []
        for _ in range(tasks):
            arr.append(0)
        started.append(arr)

    for i in chromosome:
        machine = machines[i][jobs[i]]
        time = times[i][jobs[i]]
        prevTime = times[i][jobs[i]-1]
        if (machT[machine] > started[i][jobs[i]-1]+prevTime):
            started[i][jobs[i]] = machT[machine]
            machT[machine] += time
        else:
            started[i][jobs[i]] = started[i][jobs[i]-1]+prevTime
            machT[machine] = started[i][jobs[i]] + time

    makespan = max(machT)

    return makespan


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

    child1[rand::], child2[rand::] = child2[rand::], child1[rand::]

    return child1, child2


def fixCrossover (child):
    counts = [0 for _ in range(machNo)]

    for i in child:
        counts[i] += 1

    more = []
    less = []

    for i in range(len(counts)):
        if counts[i] > machNo:
            more.append([i, counts[i] - machNo])
        else:
            less.append([i, machNo - counts[i]])

    for i in more:
        while i[1] > 0:
            currInd = child.index(i[0])
            currLess = less[0]
            child[currInd] = currLess[0]
            less[0][1] -= 1
            if (less[0][1] == 0):
                less.pop(0)
            i[1] -= 1

    return child


def mutation (child):
    numMut = random.randint(0, (job*tasks)//2)
    for _ in range(numMut):
        ind1 = random.randint(0, len(child)-1)
        ind2 = random.randint(0, len(child)-1)

        child[ind1], child[ind2] = child[ind2], child[ind1]
        
    return child


# Driver Code

popSize = 30

# Generate Population
genome = encode(popSize)

# Recording the best makespan
bests = []

for _ in range(10):

    # Calculate Fitness
    fitnesses = []

    for i in genome:
        fitnesses.append(fitness(i))

    bests.append(min(fitnesses))

    # Selection
    selected = [rouletteWheel(genome) for _ in range(popSize)]

    # Crossover and Mutation

    childPop = []

    for i in range(0, popSize, 2):
        par1 = selected[i]
        par2 = selected[i+1]

        children = crossover(par1, par2)
        child1 = mutation(fixCrossover(children[0]))
        child2 = mutation(fixCrossover(children[1]))

        childPop.append(child1)
        childPop.append(child2)

    genome = childPop
