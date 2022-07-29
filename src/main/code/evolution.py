import random
import numpy as np
from time import time
import generator
from variation import crossover, mutation, choose_parent

"""
Evolve, give the chosen patterns a higher probability 
of being chosen to be in the next generation
"""
def base_evolve(population, prefPattern1, prefPattern2):
    # probability of each user preferred pattern to be chosen
    size = population.size

    probi = 1/size
    #evo_probability = get_evo_probi(population, prefPattern1, prefPattern2)
    evo_probability = np.array([probi for i in range(size)])

    half_size = int(size / 2)

    # crossover, mutation
    for i in range(half_size):
        index1 = choose_parent(size, evo_probability)
        index2 = choose_parent(size, evo_probability)
        # ensure choosing 2 different parents
        while index1 == index2:
            index2 = choose_parent(size, evo_probability)

        parent1 = population.patterns[index1]
        parent2 = population.patterns[index2]

        child1, child2 = crossover(parent1, parent2)
        child1 = mutation(child1)
        child2 = mutation(child2)

        population.add_pattern(child1)
        population.add_pattern(child2)

    return population


"""
Only use for population of size 8
Behaves like evolve without preference when preference is not specified
"""
def pref_evolve(population, prefPattern1, prefPattern2):
    size = population.size
    times = 2
    lpref1 = prefPattern1
    lpref2 = prefPattern2
    for i in range(times):
        parent1 = population.patterns[random.randrange(0, size)]
        parent2 = population.patterns[random.randrange(0, size)]

        p1_lst = generator.fromPatternGeneToList(parent1)
        p2_lst = generator.fromPatternGeneToList(parent2)

        if prefPattern1 != -1 and prefPattern2 != -1:
            pref1_lst = generator.fromPatternGeneToList(prefPattern1)
            pref2_lst = generator.fromPatternGeneToList(prefPattern2)
        elif prefPattern1 != -1:
            #print("HI")
            pref1_lst = generator.fromPatternGeneToList(prefPattern1)
            lpref2 = prefPattern1
            pref2_lst = generator.fromPatternGeneToList(prefPattern1)
        else:
            lpref1 = population.patterns[random.randrange(0, size)]
            pref1_lst = generator.fromPatternGeneToList(lpref1)
            lpref2 = population.patterns[random.randrange(0, size)]
            pref2_lst = generator.fromPatternGeneToList(lpref2)
        """
        if prefPattern2 != -1:
            pref2_lst = generator.fromPatternGeneToList(prefPattern2)
        else:
            lpref2 = population.patterns[random.randrange(0, size)]
            pref2_lst = generator.fromPatternGeneToList(lpref2)
        """
        if(p1_lst == pref1_lst or p1_lst == pref2_lst):
            parent1 = population.patterns[random.randrange(0, size)]

        child1, child2 = crossover(lpref1, parent1)
        child1 = mutation(child1, 0.01)
        child2 = mutation(child2, 0.01)
        child3 = mutation(parent1, 0.45)
        population.add_pattern(child1)
        population.add_pattern(child2)
        population.add_pattern(child3)

        if p2_lst == pref1_lst or p2_lst == pref2_lst:
            parent2 = population.patterns[random.randrange(0, size)]

        child1, child2 = crossover(lpref2, parent2)
        child1 = mutation(child1, 0.01)
        child2 = mutation(child2, 0.01)
        child3 = mutation(parent2, 0.45)
        population.add_pattern(child1)
        population.add_pattern(child2)
        population.add_pattern(child3)

    iter = int(population.size/4)
    for i in range(iter):
        parent1 = population.patterns[random.randrange(0, population.size)]
        parent2 = population.patterns[random.randrange(0, population.size)]
        child1, child2 = crossover(parent1, parent2)
        child1 = mutation(child1)
        child2 = mutation(child2)
        population.add_pattern(child1)
        population.add_pattern(child2)

    return population

"""Evolve by crossover of 2 parents to get prefSize"""
def evolve_with_pref2(population, prefPattern1, prefPattern2):
    prefSize = population.prefSize
    #parent1 = population.patterns[prefPattern1]
    #parent2 = population.patterns[prefPattern2]
    parent1 = prefPattern1
    parent2 = prefPattern2

    iter = round(prefSize/2)

    for i in range(iter):
        child1, child2 = crossover(parent1, parent2)
        child1 = mutation(child1, 0.08 * (i + 1))
        child2 = mutation(child2, 0.08 * (i + 1))

        #evaluation is quite wrong
        occured = (child1 in population.pattern_dict.values()) or (child2 in population.pattern_dict.values())

        """never gets in here"""
        while occured == True:
            #print("HII " + str(child1 in population.pattern_dict.values()) + " " + str(generator.fromPatternGeneToList(child1)))
            child1, child2 = crossover(parent1, parent2)
            child1 = mutation(child1, 0.08 * (i + 1))
            child2 = mutation(child2, 0.08 * (i + 1))
        population.add_pattern(child1)
        population.add_pattern(child2)
        population.update_dict()

    parent1 = population.patterns[random.randrange(0, population.size)]
    parent2 = population.patterns[random.randrange(0, population.size)]
    child1, child2 = crossover(parent1, parent2)
    child1 = mutation(child1)
    child2 = mutation(child2)
    population.add_pattern(child1)
    population.add_pattern(child2)

    return population

def evolve_with_pref3(population, prefPopulation, prefPattern1, prefPattern2):
    #t1 = time()
    if prefPattern1 == -1 or prefPattern2 == -1:
        prefSize = prefPopulation.size
        for i in range(prefSize):
            child = prefPopulation.patterns[random.randrange(0, prefSize)]
            child = mutation(child, 0.08)

            prefPopulation.add_pattern(child)
        new_population = evolve(population, prefPattern1, prefPattern2)
    else: # 2 patterns are chosen
        #size = population.size
        iter = int(population.prefSize/2)
        if prefPattern1 < population.prefSize:
            parent1 = population.patterns[prefPattern1]
        else:
            parent1 = prefPopulation.patterns[prefPattern1 - population.prefSize]

        if prefPattern2 < population.prefSize:
            parent2 = population.patterns[prefPattern2]
        else:
            parent2 = prefPopulation.patterns[prefPattern2 - population.prefSize]


        for i in range(iter):
            #print(prefPattern1)
            child1, child2 = crossover(parent1, parent2)
            child1 = mutation(child1, 0.1 * (i + 1))
            child2 = mutation(child2, 0.1 * (i + 1))

            """
            exist = child1 in prefPopulation.pattern_dict.values()
            while exist == True:
                child1 = mutation(child1, 0.08 * (i + 1))
                exist = child1 in prefPopulation.pattern_dict.values()

            exist = child2 in prefPopulation.pattern_dict.values()
            while exist == True:
                child2 = mutation(child2, 0.08 * (i + 1))
                exist = child2 in prefPopulation.pattern_dict.values()
            """
            prefPopulation.add_pattern(child1)
            prefPopulation.add_pattern(child2)
        new_population = evolve(population, -1, -1)
        prefPopulation.update_dict()
    #print("Pref Pop Size: " + str(prefPopulation.patterns.size))
    #t2 = time()
    #print("Evo w pref: " + str(t2 - t1))
    #print("Pref Pop Size: " + str(prefPopulation.patterns.size))
    return new_population, prefPopulation