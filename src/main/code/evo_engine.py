import numpy as np

import generator
import evolution
import selection

count = 0

"""
Define class Population
:param
- size - population size, decided in correlation with user interface
- patterns - design patterns that are currently in the population
- pattern_dict - dictionary of patterns
- prefSize - size of preference pool
- divSize - size of out-breeding pool
- archive - collection of patterns that previously, but no-longer exist 
            in the population
- max_archive_size - the maximum size the archive should have
- archive_count - the key of the pattern that should be updated in archive
"""
class Population():
    def __init__(self, num):
        #super(self).__init__()
        self.size = num
        self.patterns = self.init_population(num)
        self.pattern_dict = dict.fromkeys([i for i in range(self.size)], [self.patterns[i] for i in range(self.size)])
        self.prefSize = round(num * 0.75)
        self.divSize = self.size - self.prefSize
        # keep archive size <= 100
        self.archive = dict()
        self.max_archive_size = 100
        self.archive_count = 0

    """
    Initialisation of the population
    :param - num (int), population size
    :returns - patterns (np.array), the initial population
    """
    def init_population(self, num):
        patterns = np.array([])
        for i in range(num):
            p = generator.gen_random_pattern()
            patterns = np.append(patterns, p)
        return patterns

    """
    Add pattern to population
    :param - pattern, PatternGene to be added
    """
    def add_pattern(self, pattern):
        self.patterns = np.append(self.patterns, pattern)

    """
    Remove pattern from population
    :param - index, the index of the pattern to be removed in the population
    :returns - the pattern that is removed
    """
    def remove_pattern(self, index):
        rm = self.patterns[index]
        self.patterns = np.delete(self.patterns, index)
        return rm

    def update_dict(self):
        self.pattern_dict = dict.fromkeys([i for i in range(self.patterns.size)], [self.patterns[i] for i in range(self.patterns.size)])

    """
    Update the archive with the newly removed pattern
    :param - rm, the pattern removed from population and to be added in the archive
    """
    def update_archive(self, rm):
        leng = len(self.archive)
        if leng >= self.max_archive_size and self.archive_count >= self.max_archive_size:
            self.archive_count = 1
        else:
            self.archive_count += 1
        self.archive[self.archive_count] = rm

"""
Evolve without preference
:param
- population - Population, the population to be evolved
- prefPattern1 - PatternGene, the first preferred pattern, default to -1
- prefPattern2 - PatternGene, the second preferred pattern, default to -1

:returns
- population - Population, the evolved population
"""
def evolve(population, prefPattern1, prefPattern2):
    return evolution.base_evolve(population, prefPattern1, prefPattern2)

"""
Evolve with preference
:param
- population - Population, the population to be evolved
- prefPattern1 - PatternGene, the first preferred pattern, default to -1
- prefPattern2 - PatternGene, the second preferred pattern, default to -1

:returns
- population - Population, the evolved population
"""
def evolve_with_pref(population, prefPattern1, prefPattern2):
    return evolution.pref_evolve(population, prefPattern1, prefPattern2)

"""
Environmental selection without preference
:param
- population - Population, the population to go through selection
- prefPattern1 - PatternGene, the first preferred pattern, default to -1
- prefPattern2 - PatternGene, the second preferred pattern, default to -1

:returns
- population - Population, the population after selection
"""
def env_selection(population, prefPattern1, prefPattern2):
    return selection.environmental_selection(population, prefPattern1, prefPattern2)

"""
Environmental selection with out-breeding mechanism
:param
- population - Population, the population to go through selection
- prefPattern1 - PatternGene, the first preferred pattern, default to -1
- prefPattern2 - PatternGene, the second preferred pattern, default to -1

:returns
- population - Population, the population after selection
"""
def env_selection_with_archive(population, prefPattern1, prefPattern2):
    return selection.archive_env_selection(population, prefPattern1, prefPattern2)


