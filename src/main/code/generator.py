import random

import decoder

"""
Each PatternGene consist of 7 genes
"""

"""
:param
- pattern - the motif, represented by a number, and mapped to the image using decoder.py
- trans1 - first transformation, 0 - 3 are rotation, diagonal, 
           horizontal, and vertical translation respectively
- trans2 - second transformation, coding same as trans1
- frame - the frame of the design pattern, and mapped to the image using decoder.py
- center - the centre element of the design pattern, mapped to the image using decoder.py, 
           default to 0
- angle - angle made with x-axis, ranged between 0 and 90 (int), default to 0
- times - number of repetition, default to 0
"""
class PatternGene():
    # TODO: line - horizontal, vertical, diagonal
    def __init__(self, pattern, trans1, trans2, frame, center=0, angle=0, times=1):
        self.pattern_num = pattern
        self.trans1 = trans1
        self.trans2 = trans2
        self.frame = frame
        self.center = center
        self.angle = angle
        #self.line_trans = line_trans # not useful, determined by angle already
        self.times = times

"""Change datatype from List to PatternGene"""
def fromListToPatternGene(a):
    assert len(a) == 7, "Number of element is 7"
    return PatternGene(a[0], a[1], a[2], a[3], a[4], a[5], a[6])

"""Change datatype from PatternGene to List"""
def fromPatternGeneToList(pg):
    return [pg.pattern_num, pg.trans1, pg.trans2, pg.frame, pg.center, pg.angle, pg.times]

"""Compare 2 PatternGenes, if same return True, else False"""
def compareGene(p1, p2):
    l1 = fromPatternGeneToList(p1)
    l2 = fromPatternGeneToList(p2)
    if l1 == l2:
        return True
    else:
        return False

"""Generate 1 random, new PatternGene"""
def gen_random_pattern():
    # get random pattern
    pattern_range = len(decoder.image_pattern_list)
    # randrange(a, b) -> a <= N < b
    pattern_num = random.randrange(0, pattern_range)

    # get random transformation function
    trans_range = len(decoder.transformation_list)
    trans_func1 = random.randrange(0, trans_range)
    trans_func2 = random.randrange(0, trans_range)

    frame_range = len(decoder.frame_list)
    frame_num = random.randrange(0, frame_range)

    center_range = len(decoder.center_list)
    # 0 for no change, 1 for image replacement
    center_num = random.randrange(0, center_range)

    angle = random.randrange(0, 91, 45)

    #line_trans = random.randrange(0, trans_range)

    # should not repeat more than 9 times,
    # overlapping issues occur
    times = random.randrange(1, 10)

    pattern = PatternGene(pattern_num, trans_func1, trans_func2, frame_num, center_num, angle, times)

    return pattern