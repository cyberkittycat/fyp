import numpy as np

import generator

penalty = -7
"""
Calculates fitness based on the number of different elements
"""
def hamming_distance(pattern1, pattern2):
    p1 = generator.fromPatternGeneToList(pattern1)
    p2 = generator.fromPatternGeneToList(pattern2)

    ham_dis = 0

    length = len(p1)
    for i in range(length):
        if p1[i] != p2[i]:
            # +1 distance if not equal
            ham_dis += 1

    return ham_dis

"""
Evaluates the population using the hamming distance as fitness function.
The fitness value of each candidate solution is the sum of its hamming distances
with all other candidate solutions in the population.
"""
def evaluation(population, prefPattern1, prefPattern2):
    size = population.patterns.size # take into account that it is now evaluating both parent gen and child gen
    size_minus_one = size - 1
    ham_dis_list = []
    fitness_list = np.zeros(size)
    remove_list = []

    #if prefPattern1 == -1 and prefPattern2 == -1:
    for i in range(size_minus_one):  # run for 1 times less than size, nothing to compare with for the last element
        """
        If an the index of the element is in remove_list then this is 
        a duplicate to be removed, no further evaluation required.
        """
        exists = i in remove_list
        if exists == False:
            for j in range(i, size_minus_one):  # i starts from 0
                dis = hamming_distance(population.patterns[i], population.patterns[j + 1])
                if dis == 0:
                    """If a duplicate is found add its index to remove_list"""
                    remove_list += [j+1]
                else:
                    ham_dis_list += [dis]
                    fitness_list[i] += dis
                    fitness_list[j + 1] += dis
    #for k in remove_list:
    #    if population.patterns.size > 8:
    #        population.remove_pattern(k)
    #        fitness_list.pop(k)
    """
    else:
        for i in range(size_minus_one): # run for 1 times less than size, nothing to compare with for the last element
            if i == prefPattern1 or i == prefPattern2:
                fitness_list[i] += 10
            for j in range(i, size_minus_one): # i starts from 0
                dis = hamming_distance(population.patterns[i], population.patterns[j+1])
                ham_dis_list += [dis]
                fitness_list[i] += dis
                fitness_list[j+1] += dis
        if prefPattern1 == size_minus_one or prefPattern2 == size_minus_one: # last element
            fitness_list[size_minus_one] += 10
    """
    return ham_dis_list, fitness_list

"""
Gets called when preferences are considered, only evaluates the fitness
of the offspring generated using preference input as parents, i.e. evaluates
fitness of preference pool.
"""
def evaluation_only_pref(population):
    # evaluate last 12
    #size = population.patterns.size - 12
    size = 12
    size_minus_one = size - 1
    ham_dis_list = []
    fitness_list = np.zeros(size)
    # find the start and end index of the offspring generated using preference
    start = population.patterns.size - 12
    end = start + size_minus_one
    remove_list = []

    for i in range(start, end):  # run for 1 times less than size, nothing to compare with for the last element
        exists = i in remove_list
        if exists == False:
            for j in range(i, end):  # i starts from 0
                dis = hamming_distance(population.patterns[i], population.patterns[j + 1])
                if dis == 0:
                    remove_list += [j + 1]
                else:
                    ham_dis_list += [dis]
                    fitness_list[i - start] += dis
                    fitness_list[j + 1 - start] += dis

    return fitness_list

"""
Evaluate_only_pref should be called before calling this.
This evaluates the fitness of the candidate solutions in the
out-breeding pool, where each candidate is compared with the
solutions chosen from the preference pool, then the fitness 
is summed up. 
"""
def evaluation_with_pref(population, prefPattern1, prefPattern2):
    size = population.patterns.size # last few patterns are from pref,
    prefSize = population.prefSize

    size = size - (prefSize)
    size_minus_one = size - 1
    ham_dis_list = []
    fitness_list = np.zeros(size)
    remove_list = []

    for i in range(prefSize):
        exists = i in remove_list
        if exists == False:
            for j in range(size):
                # i + size is the preferred pattern at the end 6 of the list
                dis = hamming_distance(population.patterns[i + size], population.patterns[j])
                if dis == 0:
                    remove_list += [j]
                else:
                    # ham_dis_list += [dis]
                    fitness_list[j] += dis
    return ham_dis_list, fitness_list

"""
Another method of calculating fitness for preferred patterns.
An optimal amount for the number of genes that remain the same 
is defined, then the fitness value is calculated according to 
the distance to the optimal amount. If the 2 PatternGenes compared
are exactly the same or are entirely different, then the pattern 
is penalised with a predefined penalty. 
"""
def sim_fitness_with_pref_pattern(pattern, prefPattern1, prefPattern2):
    #t1 = time()
    fitness = 0
    leng = len(generator.fromPatternGeneToList(pattern))
    # find starting position of the patterns to be evaluated
    optimal = round(leng * 0.65)
    start_to_op = optimal
    end_to_op = leng - start_to_op

    if prefPattern1 != -1 and prefPattern2 != -1:
        sim1 = hamming_distance(pattern, prefPattern1)
        sim2 = hamming_distance(pattern, prefPattern2)
        penalty = 0.1
        if sim1 == 0 or sim2 == 0:
            fitness = -penalty # exactly the same, largely penalised
        elif sim1 == leng and sim2 == leng:
            fitness = -penalty # nothing is the same, largely penalised
        elif sim1 == leng or sim2 == leng:
            fitness = -penalty  # could be similar to only 1 of the pref
        else: # assign a positive fitness
            score = 0.1
            if sim1 == optimal:
                fitness += score
            elif sim1 > optimal:
                # scale the fitness scores
                fitness += round(score * sim1 / end_to_op)
            elif sim1 < optimal:
                fitness += round(score * sim1 / start_to_op)
            else:
                fitness += 0

            if sim2 == optimal:
                fitness += score
            elif sim2 > optimal:
                fitness += round(score * sim2 / end_to_op)
            elif sim2 < optimal:
                fitness += round(score * sim2 / start_to_op)
            else:
                fitness += 0
    #t2 = time()
    #print("Sim w pref: " + str(t2 - t1))
    return fitness

"""
The matching evaluation method that uses sim_fitness_with_pref_pattern()
for calculating fitness of preferred patterns. 
"""
def evaluation_with_pref3(population, prefPopulation, prefPattern1, prefPattern2):
    #t1 = time()
    prefSize = prefPopulation.patterns.size
    prefSize_minus_one = prefSize - 1
    size = population.patterns.size
    #size_minus_one = size - 1
    pref_ham_dis_list = []
    pref_fitness_list = np.zeros(prefSize)
    #ham_dis_list = []
    fitness_list = np.zeros(size)
    if prefPattern1 < population.prefSize:
        parent1 = population.patterns[prefPattern1]
    else:
        parent1 = prefPopulation.patterns[prefPattern1 - population.prefSize]

    if prefPattern2 < population.prefSize:
        parent2 = population.patterns[prefPattern2]
    else:
        parent2 = prefPopulation.patterns[prefPattern2 - population.prefSize]

    for i in range(prefSize_minus_one):
        for j in range(i, prefSize_minus_one):
            dis = hamming_distance(prefPopulation.patterns[i], prefPopulation.patterns[j + 1])
            pref_ham_dis_list += [dis]
            pref_fitness_list[i] += dis + sim_fitness_with_pref_pattern(prefPopulation.patterns[i], parent1, parent2)
            pref_fitness_list[j + 1] += dis + sim_fitness_with_pref_pattern(prefPopulation.patterns[j + 1], parent1, parent2)

    # measure distance between out-breeding pop pattern and existing prefPopulation, i.e. first prefSize
    for i in range(prefSize):
        for j in range(size):
            dis = hamming_distance(prefPopulation.patterns[i], population.patterns[j])
            #ham_dis_list += [dis]
            fitness_list[j] += dis
    #t2 = time()
    #print("Evaluation w pref: " + str(t2 - t1))
    return fitness_list, pref_fitness_list
