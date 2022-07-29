import pygame
import math

import decoder

"""
Manually declare these 3 variables with same value as that in main.py
to avoid circular import issue. 
"""
box_size = 280
(width, height) = (1300, 770)
black = (0,0,0)

"""load all images"""
# frame
ui_frame_list = []
frame_list_size = len(decoder.frame_list)
for i in range(frame_list_size):
    ui_frame_list.append(pygame.transform.smoothscale(pygame.image.load(decoder.frame_list[i]), (box_size, box_size)))
# centre
ui_center_list = []
center_list_size = len(decoder.center_list)
for i in range(center_list_size):
    ui_center_list.append(pygame.transform.smoothscale(pygame.image.load(decoder.center_list[i]), (box_size / 3, box_size / 3)))
# motif
ui_pattern_list = []
pattern_list_size = len(decoder.image_pattern_list)
for i in range(pattern_list_size):
    ui_pattern_list.append(pygame.transform.smoothscale(pygame.image.load(decoder.image_pattern_list[i]), (box_size/8,box_size/8)))

"""Draw frame"""
def frame(screen, num, x, y):
    screen.blit(ui_frame_list[num], (x, y))
"""Draw center element"""
def center(screen, num, x, y):
    screen.blit(ui_center_list[num], (x, y))

"""
Define transformation functions.
The input arguments are the same for all first transformation functions 
and are the same for all second transformation for mapping convenience. 
These functions are mapped to transform in function basic_pattern().
"""

"""
Define first transformation of rotation.
:param 
- screen - the screen to build the images on
- pattern (int) - the motif number
- x (int) - x-coordinate of initial position
- y (int) - y-coordinate of initial position 
- times (int) - number of repetition
- angle (int) - angle with x-axis
- trans - function name, second transformation 
"""
def outer_rotation_trans(screen, pattern, x, y, times, angle, trans):
    maxX = x + box_size - (box_size / 8) - 10 # boxsize - patternsize
    maxY = y + box_size - (box_size / 8) - 10
    if times == 0:
        rot_angle = 0
    else:
        rot_angle = 2 * math.pi / times
    radius = box_size / 3
    currX = round(x + box_size/4)
    currX = round(x + box_size/4)
    currY = round(y + box_size/4)
    for i in range(times):
        #print("Curr X: " + str(currX) + ", Curr Y: " + str(currY))
        trans(screen, pattern, currX, currY, times, angle, maxX, maxY)
        currX = currX + round(radius * math.sin(math.pi/2 - i * rot_angle))
        currY = currY + round(radius * math.cos(math.pi/2 - i * rot_angle))

"""
Define second transformation of rotation.
:param 
- screen - the screen to build the images on
- pattern (int) - the motif number
- x (int) - x-coordinate of initial position
- y (int) - y-coordinate of initial position 
- times (int) - number of repetition
- angle (int) - angle with x-axis
- maxX (int) - maximum x-coordinate where beyond that the image should not be built
- maxY (int) - maximum y-coordinate where beyond that the image should not be built
"""
def rotation_trans(screen, pattern, x, y, times, angle, maxX=width, maxY=height):
    centerX = x
    centerY = y
    #w, h = pattern.get_size()
    rotated_pattern = pygame.transform.rotate(pattern, angle)
    if centerX < maxX and centerY < maxY:
        screen.blit(rotated_pattern, (centerX, centerY))
    #for i in range(times):
    #    rotated_pattern = pygame.transform.rotate(pattern, i * angle)
    #    screen.blit(rotated_pattern, (centerX,centerY))

"""
Define first transformation of diagonal translation.
:param 
- screen - the screen to build the images on
- pattern (int) - the motif number
- x (int) - x-coordinate of initial position
- y (int) - y-coordinate of initial position 
- times (int) - number of repetition
- angle (int) - angle with x-axis
- trans - function name, second transformation 
"""
def outer_diag_trans(screen, pattern, x, y, times, angle, trans):
    spacing = (box_size - (box_size / 8)) / (times)
    maxX = x + box_size - (box_size / 8) - 10 # boxsize - patternsize
    maxY = y + box_size - (box_size / 8) - 10
    currX = x
    currY = y
    #print("Max X: " + str(maxX) + ", Max Y: " + str(maxY))
    for i in range(times):
        if currX < maxX and currY < maxY:
            #print("Curr X: " + str(currX) + ", Curr Y: " + str(currY))
            trans(screen, pattern, currX, currY, times, maxX, maxY)
            currX = currX + spacing
            currY = currY + spacing

"""
Define second transformation of diagonal translation.
:param 
- screen - the screen to build the images on
- pattern (int) - the motif number
- x (int) - x-coordinate of initial position
- y (int) - y-coordinate of initial position 
- times (int) - number of repetition
- angle (int) - angle with x-axis
- maxX (int) - maximum x-coordinate where beyond that the image should not be built
- maxY (int) - maximum y-coordinate where beyond that the image should not be built
"""
def diagonal_trans(screen, pattern, x, y, times, angle, maxX=width, maxY=height):
    spacing = (box_size - (box_size / 8)) / (times) # (boxsize - patternsize) /times
    currX = x
    currY = y

    for i in range(times):
        if currX < maxX and currY < maxY:
            screen.blit(pattern, (currX, currY))
            currX = currX + spacing
            currY = currY + spacing

"""
Define first transformation of horizontal translation.
:param 
- screen - the screen to build the images on
- pattern (int) - the motif number
- x (int) - x-coordinate of initial position
- y (int) - y-coordinate of initial position 
- times (int) - number of repetition
- angle (int) - angle with x-axis
- trans - function name, second transformation 
"""
def outer_horizontal_trans(screen, pattern, x, y, times, angle, trans):
    spacing = (box_size - (box_size / 8)) / (times)
    maxX = x + box_size - (box_size / 8) - 10 # boxsize - patternsize
    maxY = y + box_size - (box_size / 8) - 10
    currX = x
    currY = y
    if trans == rotation_trans or trans == horizontal_trans:
        currY = y + (box_size / 2) - (box_size/16)
    for i in range(times):
        if currX < maxX and currY < maxY:
            #print("Curr X: " + str(currX) + ", Curr Y: " + str(currY))
            trans(screen, pattern, currX, currY, times, maxX, maxY)
            currX = currX + spacing

"""
Define second transformation of horizontal translation.
:param 
- screen - the screen to build the images on
- pattern (int) - the motif number
- x (int) - x-coordinate of initial position
- y (int) - y-coordinate of initial position 
- times (int) - number of repetition
- angle (int) - angle with x-axis
- maxX (int) - maximum x-coordinate where beyond that the image should not be built
- maxY (int) - maximum y-coordinate where beyond that the image should not be built
"""
def horizontal_trans(screen, pattern, x, y, times, angle, maxX=width, maxY=height):
    spacing = (box_size - (box_size / 8)) / (times)
    currX = x
    currY = y
    for i in range(times):
        if currX < maxX and currY < maxY:
            screen.blit(pattern, (currX, currY))
            currX = currX + spacing

"""
Define first transformation of vertical translation.
:param 
- screen - the screen to build the images on
- pattern (int) - the motif number
- x (int) - x-coordinate of initial position
- y (int) - y-coordinate of initial position 
- times (int) - number of repetition
- angle (int) - angle with x-axis
- trans - function name, second transformation 
"""
def outer_vertical_trans(screen, pattern, x, y, times, angle, trans):
    spacing = (box_size - (box_size / 8)) / times
    maxX = x + box_size - (box_size / 8) - 10 # boxsize - patternsize
    maxY = y + box_size - (box_size / 8) - 10
    currX = x
    if trans == rotation_trans or trans == vertical_trans:
        currX = x + (box_size / 2) - (box_size/16)
    currY = y
    for i in range(times):
        if currX < maxX and currY < maxY:
            #print("Curr X: " + str(currX) + ", Curr Y: " + str(currY))
            trans(screen, pattern, currX, currY, times, maxX, maxY)
            currY = currY + spacing

"""
Define second transformation of vertical translation.
:param 
- screen - the screen to build the images on
- pattern (int) - the motif number
- x (int) - x-coordinate of initial position
- y (int) - y-coordinate of initial position 
- times (int) - number of repetition
- angle (int) - angle with x-axis
- maxX (int) - maximum x-coordinate where beyond that the image should not be built
- maxY (int) - maximum y-coordinate where beyond that the image should not be built
"""
def vertical_trans(screen, pattern, x, y, times, angle, maxX=width, maxY=height):
    spacing = (box_size - (box_size / 8)) / (times)
    currX = x
    currY = y
    for i in range(times):
        if currX < maxX and currY < maxY:
            screen.blit(pattern, (currX, currY))
            currY = currY + spacing

"""Used in basic_pattern()"""
trans1_list = [outer_rotation_trans,
               outer_diag_trans,
               outer_horizontal_trans,
               outer_vertical_trans]

trans2_list = [rotation_trans,
               diagonal_trans,
               horizontal_trans,
               vertical_trans]

"""
Draw the motif by calling first transformation function and
then calls second transformation in the first transformation 
function.
:param
- screen - the screen to build the images on
- pattern (int) - the motif number
- x (int) - x-coordinate of initial position
- y (int) - y-coordinate of initial position 
- times (int) - number of repetition
- angle (int) - angle with x-axis, default to 0
- trans1 (int) - mapped to 1st transformation using trans1_list, default to 0
- trans2 (int) - mapped to 2nd transformation using trans2_list, default to 0
"""
def basic_pattern(screen, num, x, y, times, angle=0, trans1=0, trans2=0):
    pattern = ui_pattern_list[num]

    fst_trans = trans1_list[trans1]
    snd_trans = trans2_list[trans2]
    fst_trans(screen, pattern, x, y, times, angle, snd_trans)

"""
Draw the lines
:param
- screen - the screen to build the images on
- num (int) - line angle, randrange(0, 91, 45)
- x (int) - x-coordinate of initial position
- y (int) - y-coordinate of initial position  
- times (int) - number of repetition
- len (int) - length of line, should be the same as the box size 
"""
def line(screen, num, x, y, times, len):
    # [(start_pos), (end_pos)]
    line_45 = [[(x + box_size, y), (x, y + box_size)], # right diag
               [(x, y), (x + box_size, y + box_size)], # left diag
               [(x+1, y + (box_size / 2)), (x + box_size-1, y + (box_size / 2))], # horizontal
               [(x + (box_size / 2), y+1), (x + (box_size / 2), y + box_size-1)]] # vertical

    spacing = round(len / (times + 1))
    currX = x
    currY = y
    if num == 0:
        for i in range(times):
            currX = currX + spacing
            pygame.draw.line(screen, color=black, start_pos=(currX, y), end_pos=(currX, y+len-1))
    elif num == 90:
        for i in range(times):
            currY = currY + spacing
            pygame.draw.line(screen, color=black, start_pos=(x, currY), end_pos=(x + len - 1, currY))
    else: # num == 45
        # do nothing for 0
        if times == 1 or times == 3 or times == 4 or times == 5 or times == 7 or times == 9:
            pygame.draw.line(screen, color=black, start_pos=line_45[0][0], end_pos=line_45[0][1], width=2) # right diag

        if times == 2 or times == 3 or times == 4 or times == 5 or times == 8 or times == 9:
            pygame.draw.line(screen, color=black, start_pos=line_45[1][0], end_pos=line_45[1][1], width=2) # left diag

        if times == 4 or times == 6 or times == 7 or times == 8 or times == 9:
            pygame.draw.line(screen, color=black, start_pos=line_45[2][0], end_pos=line_45[2][1], width=2)

        if times == 5 or times == 6 or times == 7 or times == 8 or times == 9:
            pygame.draw.line(screen, color=black, start_pos=line_45[3][0], end_pos=line_45[3][1], width=2)
