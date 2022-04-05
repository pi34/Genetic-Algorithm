from numpy.random import randint
from numpy.random import rand

def onemax (x):
    return -sum(x)

def selection (pop, scores, k=3):
    selection_ix = randint(len(pop))
    for ix in randint(0, len(pop), k-1):
        if scores[ix] < scores[selection_ix]:
            selection_ix = ix
    return pop[selection_ix]

def crossover (p1, p2, r_cross):
    c1 = p1.copy()
    c2 = p2.copy()

    if rand() < r_cross:
        pt = randint(1, len(p1)-2)
        c1 = p1[:pt] + p2[pt:]
        c2 = p2[:pt] + p1[pt:]
    return [c1, c2]

def mutation (bitstring, r_mut):
    for i in range (len(bitstring)):
        if rand() < r_mut:
            bitstring[i] = 1 - bitstring[i]

def genetic (objective, n_bits, n_iter, n_pop, r_cross, r_mut):
    initPop = [randint(0, 2, n_bits).tolist() for i in range(n_pop)]
    best = 0
    bestEval = objective(initPop[0])

    for gen in range(n_iter):
        scores = [objective(c) for c in initPop]

        for i in range (n_pop):
            if scores[i] < bestEval:
                best = initPop[i]
                bestEval = scores[i]
                print(">%d, new best f(%s) = %.3f" % (gen,  initPop[i], scores[i]))

        selected = [selection(initPop, scores) for _ in range(n_pop)]
        children = list()

        for i in range (0, n_pop, 2):
            p1 = selected[i]
            p2 = selected[i+1]

            for c in crossover(p1, p2, r_cross):
                mutation(c, r_mut)
                children.append(c)

        pop = children
    return best, bestEval

n_iter = 100
n_bits = 20
n_pop = 100
r_cross = 0.9
r_mut = 1.0 / float(n_bits)
best, score = genetic(onemax, n_bits, n_iter, n_pop, r_cross, r_mut)
print('f(%s) = %f' % (best, score))
