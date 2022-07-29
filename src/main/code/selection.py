import random
import numpy as np
from time import time

from evaluate import evaluation, evaluation_only_pref, evaluation_with_pref, evaluation_with_pref3
import generator

"""
Find index i of the probability that is 
lst[i - 1] < r <= lst[i]
:param
- lst - list of probability
- r - the random number generated
:returns - index of the searched probability 
"""
def probi_get_index(r, lst):
    if r == 0:
        return 0
    if len(lst) == 1:
        return 0
    mid  = round(len(lst) / 2)
    if mid > 0:
        if lst[mid - 1] <= r < lst[mid]:
            return (mid)
        elif r < lst[mid]:
            return probi_get_index(r, lst[:mid])
        else:
            return (mid + probi_get_index(r, lst[mid:]))

"""
Performs environmental selection using the fitness score as evaluated
using hamming distance. A candidate solution is chosen and removed in 
each loop. With each removal, the fitness of each candidate solution 
has to be re-evaluated since fitness scores depends on all other candidate 
solutions in the population. This process repeats until the population 
shrinks to the original size before evolution.

:param
- population - Population, the population to go through selection
- prefPattern1 - PatternGene, the first preferred pattern, default to -1
- prefPattern2 - PatternGene, the second preferred pattern, default to -1

:returns
- population - Population, the population after selection
"""
def environmental_selection(population, prefPattern1, prefPattern2):
    pop_size = population.size
    for i in range(pop_size):
        _, fitness_list = evaluation(population, prefPattern1, prefPattern2)
        #min_value = min(fitness_list)
        #min_index = fitness_list.index(min_value)
        r = random.uniform(0, 1)
        min_index = np.argmin(fitness_list)
        if r > 0.9:
            f_temp = fitness_list[fitness_list != np.amin(fitness_list)]
            if len(f_temp) > 0:
                snd_min = [np.amin(f_temp)]
                min_index = np.argmin(np.where(fitness_list == snd_min))
        #print("Min_index: " + str(min_index))
        rm = population.remove_pattern(min_index)
        occured = rm in population.archive.values()
        if occured == False:
            population.update_archive(rm)

    # check for duplicate, replace with archive element if 1 exists
    for i in range(pop_size - 1):
        for j in range(i + 1, pop_size):
            if generator.compareGene(population.patterns[i], population.patterns[j]) == True:
                population.remove_pattern(j)
                r = random.randint(1, len(population.archive))
                p = population.archive.get(r)
                population.add_pattern(p)
                j -= 1
    #for i in range(population.size):
     #   print("New_pop " + str(i) + ": " + str(generator.fromPatternGeneToList(population.patterns[i])))
    return population

"""
Performs environmental selection on the preference pool then on the 
out-breeding pool, with procedure as described in environmental_selection(). 
Here a candidate solution is repeatedly removed by probability, where it has 
a larger probability to be remove when it has a lower fitness, and vice versa. 
The population size is maintained before evolution and after environmental selection. 

:param
- population - Population, the population to go through selection
- prefPattern1 - PatternGene, the first preferred pattern, default to -1
- prefPattern2 - PatternGene, the second preferred pattern, default to -1

:returns
- population - Population, the population after selection
"""
def pref_env_selection(population, prefPattern1, prefPattern2):
    pop_size = population.size
    prefSize = population.prefSize
    #min = 3 * 3
    # swap the last 12 to the preferred ones
    for i in range(prefSize * 2):
        p = population.patterns[-(i + 1)]
        population.patterns[-(i + 1)] = population.patterns[i + 8]
        population.patterns[i + 8] = p

    """performs env selection on preference pool"""
    for i in range(prefSize):
        fitness_list = evaluation_only_pref(population) # size of 12
        if len(fitness_list) > 0:
            min_index = np.argmin(fitness_list)

            if fitness_list[min_index] != 0:
                fitness_sum = sum(fitness_list)
                leng = len(fitness_list)
                probi_lst = [((fitness_sum - fitness_list[i]), i) for i in range(leng)]
                probi_lst.sort(key=lambda x: x[0])
                lst = [x for (x, _) in probi_lst]
                scaled_sum = sum(lst)
                lst = [x/scaled_sum for x in lst]
                for i in range(1, len(lst)):
                    lst[i] += lst[i-1]
                lst[len(lst) - 1] = 1.000 # some does not add to 1 due to floating number issues
                r = random.uniform(0, 1)
                idx = probi_get_index(r, lst)
                min_index = probi_lst[idx][1]
        min_index += 12
        rm = population.remove_pattern(min_index)
        occured = rm in population.archive.values()
        if occured == False:
            population.update_archive(rm)
        #print("Fitness: " + str(fitness_list))

    """performs env selection on out-breeding pool"""
    # evaluate only the front part without last 12
    _, fitness_list = evaluation_with_pref(population, prefPattern1, prefPattern2)
    while population.patterns.size > pop_size:
        if len(fitness_list) > 0:
            min_index = np.argmin(fitness_list)
            #print("Fitness list: " + str(fitness_list) + str(min_index))
            if fitness_list[min_index] != 0:
                fitness_sum = sum(fitness_list)
                leng = len(fitness_list)
                probi_lst = [((fitness_sum - fitness_list[i]), i) for i in range(leng)]
                probi_lst.sort(key=lambda x: x[0])
                lst = [x for (x, _) in probi_lst]
                scaled_sum = sum(lst)
                lst = [x / scaled_sum for x in lst]
                for i in range(1, len(lst)):
                    lst[i] += lst[i - 1]
                lst[len(lst) - 1] = 1.000  # some does not add to 1 due to floating number issues
                r = random.uniform(0, 1)
                idx = probi_get_index(r, lst)
                min_index = probi_lst[idx][1]
                #lst = fitness_list[fitness_list != np.amin(fitness_list)]
                #if len(lst) > 0:
                    #snd_min = [np.amin(lst)]
                    #min_index = np.argmin(np.where(fitness_list == snd_min))
        #if min_index < (pop_size - prefSize):
        rm = population.remove_pattern(min_index)
        occured = rm in population.archive.values()
        if occured == False:
            population.update_archive(rm)
        #fitness_list = np.delete(fitness_list, [min_index])

        _, fitness_list = evaluation_with_pref(population, prefPattern1, prefPattern2)

    # check for duplicate, replace with archive element if 1 exists
    for i in range(pop_size - 1):
        for j in range(i + 1, pop_size):
            if generator.compareGene(population.patterns[i], population.patterns[j]) == True:
                population.remove_pattern(j)
                r = random.randint(1, len(population.archive))
                p = population.archive.get(r)
                population.add_pattern(p)
                j -= 1
    #_, overall_fitness_list = evaluation(population, prefPattern1, prefPattern2)
    #print(str(overall_fitness_list))

    #for i in range(population.size):
    #    print("New_pop " + str(i) + ": " + str(generator.fromPatternGeneToList(population.patterns[i])))
    return population

"""
Add candidate solutions to the population from archive and 
new solutions for diversity maintenance before calling 
pref_env_selection().

:param
- population - Population, the population to go through selection
- prefPattern1 - PatternGene, the first preferred pattern, default to -1
- prefPattern2 - PatternGene, the second preferred pattern, default to -1

:returns
- population - Population, the population after selection
"""
def archive_env_selection(population, prefPattern1, prefPattern2):
    num = int(population.size/2)
    archive_size = len(population.archive)
    if archive_size < num:
        num = archive_size
    # sample without replacement
    rand_lst = random.sample(range(1, len(population.archive) + 1), num)

    for i in range(num):
        p = population.archive.get(rand_lst[i])
        if p != None:
            population.add_pattern(p)

        n = generator.gen_random_pattern()
        population.add_pattern(n)

    #print("Pop size: " + str(population.patterns.size) + " Archive size: " + str(len(population.archive)))
    return pref_env_selection(population, prefPattern1, prefPattern2)

"""
This method operates on 2 population, the main population and the 
preference population, the sizes of the 2 populations are maintained
before evolution and after environmental selection. 
"""
def env_selection_with_pref2(population, prefPopulation, prefPattern1, prefPattern2):
    t1 = time()
    pop_size = population.size
    pref_size = prefPopulation.size

    #if prefPattern1 == -1 and prefPattern2 == -1:
    #    new_population = env_selection(population, prefPattern1, prefPattern2)
    #    return new_population, prefPopulation
    #else:
    while prefPopulation.patterns.size > pref_size:
        fitness_list, pref_fitness_list = evaluation_with_pref3(population, prefPopulation, prefPattern1, prefPattern2)
        #print("Pref fitness " + str(pref_fitness_list))

        r = random.uniform(0, 1)
        min_index = np.argmin(pref_fitness_list)

        if r > 0.7:
            snd_min = [np.amin(pref_fitness_list[pref_fitness_list != np.amin(pref_fitness_list)])]
            min_index = np.argmin(np.where(pref_fitness_list == snd_min))

        rm = prefPopulation.remove_pattern(min_index)
        occured = rm in prefPopulation.archive.values()
        if occured == False:
            population.update_archive(rm)

        if population.patterns.size > pop_size:
            min_index = np.argmin(fitness_list)
            rm = population.remove_pattern(min_index)
            occured2 = rm in population.archive.values()
            if occured2 == False:
                population.update_archive(rm)

    while population.patterns.size > pop_size:
        fitness_list, _ = evaluation_with_pref3(population, prefPopulation, prefPattern1, prefPattern2)
        min_index = np.argmin(fitness_list)
        rm = population.remove_pattern(min_index)
        occured2 = rm in population.archive.values()
        if occured2 == False:
            population.update_archive(rm)

    population.update_dict()
    prefPopulation.update_dict()
    t2 = time()
    #print("Env select w pref: " + str(t2 - t1))
    return population, prefPopulation