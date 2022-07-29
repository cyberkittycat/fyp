import random
import numpy as np
import generator
import decoder

"""
Helper function for crossover
"""
def choose_parent(size, evo_probability):
    num = random.uniform(0, 1)
    # get the index represented by the random num
    # enumerate through evo_probability
    index = -1 # set to -1 so this returns the last element by default when it is not updated
    for e in range(size):
        # population size will be controlled within 10 for this particular case
        # so nothing fancy is required for optimisation purpose
        # if a larger population size is used for experimental purposes, a binary search would be more efficient
        if num <= evo_probability[e]:
            index = e
            break
    return index

def get_evo_probi(population, pattern1_index, pattern2_index):
    # probability of each user preferred pattern to be chosen
    size = population.size

    if pattern1_index < 0 and pattern2_index < 0:
        pref_probability = 1 / size
        other_probability = 1 / size
    elif pattern1_index < 0 or pattern2_index < 0:
        pref_probability = (1 / 5)  # TODO: experiment with numbers e.g. 3 - 5
        other_probability = (1 - (pref_probability)) / (size - 1)
    else:
        pref_probability = (1 / 4)  # TODO: experiment with numbers e.g. 3 - 5
        other_probability = (1 - (pref_probability * 2)) / (size - 2)

    """
    # Create the evolution probability list in form of range
    # e.g. index 1,2 are chosen, size = 5
    # probability of index 1,2 are each 0.25
    # probability of the rest are each p = 0.5 / 3
    # evo_probability = [p, p + 0.25, p + 0.5, p + 0.5 + p, p + 0.5 + p * 2], note that p + 0.5 + p * 2 == 1
    """
    evo_probability = np.zeros(size)

    # initialise the probabilities
    if 0 == pattern1_index or 0 == pattern2_index:
        evo_probability[0] = pref_probability
    else:
        evo_probability[0] = other_probability

    # the first one is done in initialisation
    for i in range(1, size):
        if i == pattern1_index or i == pattern2_index:
            evo_probability[i] = pref_probability + evo_probability[i - 1]
        else:
            evo_probability[i] = other_probability + evo_probability[i - 1]

    return evo_probability

"""
Swap the genes of the 2 parents at a single point
The 2 parents are chosen with respect to the user choice 
in the last generation, user's preference is given a 
higher probability to be chosen
"""
def swap_crossover(population, pattern1_index, pattern2_index):
    # probability of each user preferred pattern to be chosen
    size = population.size
    new_gen = np.array([])

    evo_probability = get_evo_probi(population, pattern1_index, pattern2_index)

    # Choose parent
    # Generate 1 new pattern each time
    for i in range(size):
        # choose 2 parents (data type: PatternGene)
        parent1 = population[choose_parent(size, evo_probability)]
        parent2 = population[choose_parent(size, evo_probability)]

        # preform crossover
        # done in 1,2,1,2,1,2,... since the first few elements are strictly required
        # while last few elements are not necessary
        new_pattern = generator.PatternGene(parent1.pattern, parent2.trans1, parent1.trans2,
                                            parent2.frame, parent2.center,
                                            parent2.line_angle, parent1.times,
                                            )
        # add to the new generation new_gen
        new_gen = np.append(new_gen, new_pattern)

    population.__setattr__("patterns", new_gen)
    print(new_gen[0])


"""
Uniform Crossover
Perform crossover if probability <= 0.5
"""
def uniform_crossover(parent1, parent2):
    c1 = []
    c2 = []
    p1 = generator.fromPatternGeneToList(parent1)
    p2 = generator.fromPatternGeneToList(parent2)
    size = len(p1)

    for i in range(size):
        r = random.uniform(0, 1)
        if r <= 0.5:
            c1 += [p1[i]]
            c2 += [p2[i]]
        else:
            c1 += [p2[i]]
            c2 += [p1[i]]

    child1 = generator.fromListToPatternGene(c1)
    child2 = generator.fromListToPatternGene(c2)

    return child1, child2

def crossover(parent1, parent2):
    #print("Crossover")
    return uniform_crossover(parent1, parent2)

"""
Polynomial Mutation
"""
def poly_mutation():
    pass

def gaussian_mutation():
    pass

def random_resetting_mutation(mutation_probi, pattern):
    patternAsList = generator.fromPatternGeneToList(pattern)
    # same probabilities as in generator gen_random_pattern
    pattern_range = len(decoder.image_pattern_list)

    # get random transformation function
    trans_range = len(decoder.transformation_list)
    frame_range = len(decoder.frame_list)

    #reflection_range = len(decoder.reflection_list)

    center_range = len(decoder.center_list)

    angle_range = 7
    angle_step = 45

    # should not repeat more than 9 times
    times_range = 10

    rangeList = [pattern_range, trans_range, trans_range, frame_range,
                 center_range, angle_range, times_range]

    length = len(patternAsList)
    for i in range(length):
        r = random.uniform(0, 1)

        if r <= mutation_probi:
            probi_range = rangeList[i]
            new_val = random.randrange(0, probi_range)
            if i == length - 2: # angle
                new_val *= angle_step
            elif i == length - 1: # times
                new_val += 1

            patternAsList[i] = new_val

    new_pattern = generator.fromListToPatternGene(patternAsList)
    return new_pattern

def mutation(pattern, mutation_probi = 0.01):
    #mutation_probi = mutation_probi # changed from 0.005 to 0.01 to ensure diversity
    return random_resetting_mutation(mutation_probi, pattern)
