import pygame
import random
import evo_engine as evo
import generator
import transformation

pygame.init()

white = (255,255,255)
lightgrey = (224,224,224)
black = (0,0,0)
lightpurple = (229,204,255)
greyishpurple = (208,186,228)
lightyellow = (253, 246, 225)
lightbrown = (232, 223, 207)

(width, height) = (1300, 770)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('EvoARchitecT')

box_size = 280

"""variables"""
msgBox = False
fstSelected = False
bothSelected = False
gen = 0

"""initialise population"""
size = 8 # ensure size is even number
population = evo.Population(size)
#pattern1_index = random.randrange(0, size)
#pattern2_index = random.randrange(0, size)
prefPattern1 = population.patterns[random.randrange(0, population.size)]
prefPattern2 = population.patterns[random.randrange(0, population.size)]
#prefPopulation = evo.Population(population.prefSize)

trans1_list = [transformation.outer_rotation_trans,
               transformation.outer_diag_trans,
               transformation.outer_horizontal_trans,
               transformation.outer_vertical_trans]

trans2_list = [transformation.rotation_trans,
               transformation.diagonal_trans,
               transformation.horizontal_trans,
               transformation.vertical_trans]

msgWidth = width / 2
msgHeight = height / 5
(xcenter, ycenter) = (width / 2, height / 2)
msgFont = pygame.font.SysFont('timesnewroman', 22)
msg = "You have selected pattern number 0  to be a preferred pattern in the next generation."
msgText = msgFont.render(msg, msgFont, black)
msgTextWidth = msgText.get_width()
msgTextHeight = msgText.get_height()
okBoxWidth = 150
okBoxHeight = 40
xOkBox = xcenter - okBoxWidth / 2
yOkBox = ycenter - okBoxHeight / 2 + msgHeight / 6 + 20

okFont = msgFont
okText = okFont.render("OK", okFont, black)
okTextWidth = okText.get_width()
okTextHeight = okText.get_height()
xOkText = xcenter - okTextWidth / 2
yOkText = ycenter - okTextHeight / 2 + msgHeight / 6 + 20


def select_msg_display(num):
    pygame.draw.rect(screen, lightyellow, (xcenter - msgWidth / 2, ycenter - msgHeight / 2, msgWidth, msgHeight))
    pygame.draw.rect(screen, black, (xcenter - msgWidth / 2, ycenter - msgHeight / 2, msgWidth, msgHeight), width=1)

    if bothSelected == True:
        msg = "Your have already selected 2 preference patterns."
    else:
        #msg = "You have selected pattern number " + str(num) + " to be a preferred pattern in the next generation."
        msg = "You have selected pattern number " + str(num) + " as a preferred pattern."
    msgText = msgFont.render(msg, msgFont, black)
    msgTextWidth = msgText.get_width()
    msgTextHeight = msgText.get_height()
    screen.blit(msgText, (xcenter - msgTextWidth / 2, ycenter - msgHeight / 6 - msgTextHeight / 2))
    # OK box
    pygame.draw.rect(screen, lightbrown, (xOkBox, yOkBox, okBoxWidth, okBoxHeight))
    pygame.draw.rect(screen, black, (xOkBox, yOkBox, okBoxWidth, okBoxHeight), width=1)
    screen.blit(okText, (xOkText, yOkText))

screen.fill(lightgrey)
#screen.fill(white)
pygame.display.flip()

xspace = (width - 20)/4
yspace = height/4

"""draw pattern containers/boxes"""
#x_box_space = 20
x_box_space = 50
y_box_space = 45

box_spacing = (width - x_box_space * 2 - box_size) / 3 - box_size
(x1, y1) = (x_box_space, y_box_space)
# (x2, y2) = (width/4+x_box_space, y_box_space)
(x2, y2) = (x1 + box_spacing + box_size, y_box_space)
# (x3, y3) = (width/2+x_box_space, y_box_space)
(x3, y3) = (x2 + box_spacing + box_size, y_box_space)
# (x4, y4) = (width/4*3+x_box_space, y_box_space)
(x4, y4) = (x3 + box_spacing + box_size, y_box_space)

(x5, y5) = (x1, y_box_space*2 + box_size)
(x6, y6) = (x2, y_box_space*2 + box_size)
(x7, y7) = (x3, y_box_space*2 + box_size)
(x8, y8) = (x4, y_box_space*2 + box_size)

"""draw buttons"""
startButtonWidth = width / 3
startButtonHeight = height / 9

refreshButtonHeight = startButtonHeight
refreshButtonWidth = refreshButtonHeight
refreshButtonImage = pygame.transform.smoothscale(pygame.image.load("../stickers/refresh.png"), (refreshButtonWidth,refreshButtonHeight))

xbutton = width / 2 - startButtonWidth / 2
#ybutton = yspace * 2 + yspace/2 - buttonHeight/2
ybutton = yspace * 3 + yspace/2

displacement = 10

"""start button"""
rg = round(startButtonWidth / 4)
for i in range(rg + 1):
    pygame.draw.rect(screen, (i, i, 255), (xbutton + i * 2, ybutton, 2, startButtonHeight))

for i in range(rg):
    pygame.draw.rect(screen, (rg - i, rg - i, 255), (xbutton + startButtonWidth / 2 + i * 2, ybutton, 2, startButtonHeight))

"""refresh button"""
#pygame.draw.rect(screen, (204, 211, 244), (x1, ybutton, refreshButtonWidth, refreshButtonHeight))
pygame.draw.rect(screen, lightgrey, (x1, ybutton, refreshButtonWidth, refreshButtonHeight))
screen.blit(refreshButtonImage, (x1, ybutton))
#pygame.draw.rect(screen, greyishpurple,(xbutton,ybutton,buttonWidth,buttonHeight))
#pygame.draw.rect(screen, lightpurple,(xbutton+displacement,ybutton+displacement,buttonWidth-displacement*2,buttonHeight-displacement*2))

"""initialise the pattern numberings"""
numFont = pygame.font.SysFont('timesnewroman',25)
oneText = numFont.render("1", numFont, black)
twoText = numFont.render("2", numFont, black)
threeText = numFont.render("3", numFont, black)
fourText = numFont.render("4", numFont, black)
fiveText = numFont.render("5", numFont, black)
sixText = numFont.render("6", numFont, black)
sevenText = numFont.render("7", numFont, black)
eightText = numFont.render("8", numFont, black)
numList = [oneText, twoText, threeText, fourText, fiveText, sixText, sevenText, eightText]

numWidth = oneText.get_width()
numHeight = oneText.get_height()

buttonFont = pygame.font.SysFont('timesnewroman',30, bold=True)
buttonText = buttonFont.render("Start/Evolve", buttonFont, black)
textWidth = buttonText.get_width()
textHeight = buttonText.get_height()
screen.blit(buttonText, (width / 2 - textWidth / 2, ybutton + (startButtonHeight / 2) - (textHeight / 2)))

xbuttonEnd = xbutton + startButtonWidth
ybuttonEnd = ybutton + startButtonHeight

genInfoFont = pygame.font.SysFont('timesnewroman',30)
genInfo = "Gen: " + str(gen)
genInfoText = genInfoFont.render(genInfo, genInfoFont, black)
genInfoWidth = genInfoText.get_width()
genInfoHeight = genInfoText.get_height()
screen.blit(genInfoText, (width - genInfoWidth - 20, height - genInfoHeight - 15))

chooseInfoFont = pygame.font.SysFont('timesnewroman',20)
chooseInfoText = chooseInfoFont.render("or I can choose for you!", chooseInfoFont, black)
chooseInfoWidth = chooseInfoText.get_width()
chooseInfoHeight = chooseInfoText.get_height()
screen.blit(chooseInfoText, (width - chooseInfoWidth - 20, height - genInfoHeight - chooseInfoHeight- 15))

chooseInfoText2 = chooseInfoFont.render("Choose up to 2 interesting patterns every time,", chooseInfoFont, black)
chooseInfoWidth2 = chooseInfoText2.get_width()
chooseInfoHeight2 = chooseInfoText2.get_height()
screen.blit(chooseInfoText2, (width - chooseInfoWidth2 - 20, height - genInfoHeight - chooseInfoHeight - chooseInfoHeight2 - 15))

def draw_cover_rec():
    # left
    pygame.draw.rect(screen, lightgrey, (0, 0, x1, height))
    # bottom
    pygame.draw.rect(screen, lightgrey, (0, y5 + box_size, width, height - y5 - box_size))
    # right
    pygame.draw.rect(screen, lightgrey, (x4 + box_size, 0, width - x4 - box_size, height))

    gap_width = box_spacing
    pygame.draw.rect(screen, lightgrey, (x1 + box_size, 0, box_spacing, height))
    pygame.draw.rect(screen, lightgrey, (x2 + box_size, 0, box_spacing, height))
    pygame.draw.rect(screen, lightgrey, (x3 + box_size, 0, box_spacing, height))

def draw_patterns(population):
    # draw background
    pygame.draw.rect(screen, lightgrey, (0, 0, width, height))

    for i in range(population.size):
        (x, y) = (x1, y1)
        if i == 1:
            (x, y) = (x2, y2)
        elif i == 2:
            (x, y) = (x3, y3)
        elif i == 3:
            (x, y) = (x4, y4)
        elif i == 4:
            (x, y) = (x5, y5)
        elif i == 5:
            (x, y) = (x6, y6)
        elif i == 6:
            (x, y) = (x7, y7)
        elif i == 7:
            (x, y) = (x8, y8)
        """
        0: pattern, 1: trans1, 2: trans2, 3: frame,
        4: centre, 5: line_angle, 6: times
        """
        #print("New_pop " + str(i) + ": " + str(generator.fromPatternGeneToList(population.patterns[i])))
        pygame.draw.rect(screen, white, (x, y, box_size, box_size))
        p = generator.fromPatternGeneToList(population.patterns[i])
        # line
        transformation.line(screen, p[5], x, y, p[6], box_size)
        # pattern
        transformation.basic_pattern(screen, p[0], x, y, p[6], p[5], trans1=p[1], trans2=p[2])
        # frame
        transformation.frame(screen, p[3], x, y)
        # centre
        transformation.center(screen, p[4], x + box_size / 2 - box_size / 6, y + box_size / 2 - box_size / 6)

        # cover overflowing pattern if there is any
        if i == 4:
            pygame.draw.rect(screen, lightgrey, (0, y1 + box_size, width, y5 - y1 - box_size))
        # draw numbers
        num = numList[i]
        numWidth = num.get_width()
        numHeight = num.get_height()
        screen.blit(num, (x + box_size / 2 - numWidth, y - numHeight))

    # draw covers to cover up overflowing elements
    draw_cover_rec()

    #update gen info
    genInfo = "Gen: " + str(gen*10)
    genInfoText = genInfoFont.render(genInfo, genInfoFont, black)
    genInfoWidth = genInfoText.get_width()
    genInfoHeight = genInfoText.get_height()
    pygame.draw.rect(screen, lightgrey, (width - chooseInfoWidth2 - 20, height - genInfoHeight - chooseInfoHeight - chooseInfoHeight2 - 15, chooseInfoWidth2, chooseInfoHeight + genInfoHeight + chooseInfoHeight2))
    screen.blit(genInfoText, (width - genInfoWidth - 20, height - genInfoHeight - 15))
    screen.blit(chooseInfoText, (width - chooseInfoWidth - 20, height - genInfoHeight - chooseInfoHeight - 15))
    screen.blit(chooseInfoText2,
                (width - chooseInfoWidth2 - 20, height - genInfoHeight - chooseInfoHeight - chooseInfoHeight2 - 15))

def draw_patterns_with_pref(population, prefPopulation):
    if gen <= 10:
        draw_patterns(population)
    else:
        # draw background
        pygame.draw.rect(screen, lightgrey, (0, 0, width, height))
        for i in range(population.size):
            (x, y) = (x1, y1)
            if i == 1:
                (x, y) = (x2, y2)
            elif i == 2:
                (x, y) = (x3, y3)
            elif i == 3:
                (x, y) = (x4, y4)
            elif i == 4:
                (x, y) = (x5, y5)
            elif i == 5:
                (x, y) = (x6, y6)
            elif i == 6:
                (x, y) = (x7, y7)
            elif i == 7:
                (x, y) = (x8, y8)
            # 0: pattern, 1: trans1, 2: trans2, 3: frame,
            # 4: centre, 5: line_angle, 6: times
            pygame.draw.rect(screen, white, (x, y, box_size, box_size))

            if i < population.prefSize:
                p = generator.fromPatternGeneToList(prefPopulation.patterns[i])
            else:
                p = generator.fromPatternGeneToList(population.patterns[i-population.prefSize])
            # line
            transformation.line(screen, p[5], x, y, p[6], box_size)
            # pattern
            transformation.basic_pattern(screen, p[0], x, y, p[6], p[5], trans1=p[1], trans2=p[2])
            # frame
            transformation.frame(screen, p[3], x, y)
            # centre
            transformation.center(screen, p[4], x + box_size / 2 - box_size / 6, y + box_size / 2 - box_size / 6)

            #draw numbers
            num = numList[i]
            numWidth = num.get_width()
            numHeight = num.get_height()
            screen.blit(num, (x + box_size / 2 - numWidth, y - numHeight))

            #update gen info
            genInfo = "Gen: " + str(gen*10)
            genInfoText = genInfoFont.render(genInfo, genInfoFont, black)
            genInfoWidth = genInfoText.get_width()
            genInfoHeight = genInfoText.get_height()
            pygame.draw.rect(screen, lightgrey, (width - chooseInfoWidth2 - 20, height - genInfoHeight - chooseInfoHeight - chooseInfoHeight2 - 15, chooseInfoWidth2, chooseInfoHeight + genInfoHeight + chooseInfoHeight2))
            screen.blit(genInfoText, (width - genInfoWidth - 20, height - genInfoHeight - 15))
            screen.blit(chooseInfoText, (width - chooseInfoWidth - 20, height - genInfoHeight - chooseInfoHeight - 15))
            screen.blit(chooseInfoText2,
                        (width - chooseInfoWidth2 - 20, height - genInfoHeight - chooseInfoHeight - chooseInfoHeight2 - 15))

"""include rendering"""
def evo_size8(population, gen):
    # generate population
    if gen <= 1:
        for i in range(10):
            population = evo.evolve(population, prefPattern1, prefPattern2)
            population = evo.env_selection(population, prefPattern1, prefPattern2)
    else:
        for i in range(10):
            # function is similar with evolve when there is not preference pattern
            population = evo.evolve_with_pref(population, prefPattern1, prefPattern2)
            population = evo.env_selection_with_archive(population, prefPattern1, prefPattern2)
    #if gen % 10 == 0:
    #    _, overall_fitness_list = evo.evaluation(population, prefPattern1, prefPattern2)
    #    print(str(overall_fitness_list))
    draw_patterns(population)
    # draw_patterns_with_pref(population, prefPopulation)

running = True
while running:
    mouse = pygame.mouse.get_pos()
    mouse_on_start_button = False
    mouse_on_refresh_button = False
    mouse_on_ok_button = False

    if xOkBox <= mouse[0] <= (xOkBox + okBoxWidth) and mouse[1] >= yOkBox and mouse[1] <= (yOkBox + okBoxHeight):
        #print("Msg Box " + str(msgBox))
        mouse_on_ok_button = True
    else:
        mouse_on_ok_button = False

    if mouse[0] >= xbutton and mouse[0]<= xbuttonEnd and mouse[1] >= ybutton and mouse[1] <=ybuttonEnd:
        mouse_on_start_button = True
        #pygame.draw.rect(screen, lightpurple, (xbutton, ybutton, buttonWidth, buttonHeight))
        for i in range(rg+1):
            pygame.draw.rect(screen, (rg + i, rg + i, 255), (xbutton + i * 2, ybutton, 2, startButtonHeight))

        for i in range(rg):
            pygame.draw.rect(screen, (rg * 2 - i, rg * 2 - i, 255),
                             (xbutton + startButtonWidth / 2 + i * 2, ybutton, 2, startButtonHeight))
        #screen.blit(buttonText, (width/2 - textWidth/2, ybutton + (buttonHeight/2)  - (textHeight/2)))
    else:
        mouse_on_start_button = False
        #pygame.draw.rect(screen, greyishpurple, (xbutton, ybutton, buttonWidth, buttonHeight))
        for i in range(rg+1):
            pygame.draw.rect(screen, (40 + i, 40 + i, 255), (xbutton + i * 2, ybutton, 2, startButtonHeight))

        for i in range(rg):
            pygame.draw.rect(screen, (40 + rg - i, 40 + rg - i, 255),
                             (xbutton + startButtonWidth / 2 + i * 2, ybutton, 2, startButtonHeight))
    screen.blit(buttonText, (width / 2 - textWidth / 2, ybutton + (startButtonHeight / 2) - (textHeight / 2)))

    if mouse[0] >= x1 and mouse[0]<= (x1+refreshButtonWidth) and mouse[1] >= ybutton and mouse[1] <=(ybutton + refreshButtonHeight):
        mouse_on_refresh_button = True
        #pygame.draw.rect(screen, (234,234,234), (x1, ybutton, refreshButtonWidth, refreshButtonHeight))
        pygame.draw.rect(screen, lightgrey, (x1, ybutton, refreshButtonWidth, refreshButtonHeight))
        pygame.draw.rect(screen, black, (x1, ybutton, refreshButtonWidth, refreshButtonHeight), width=1)
        #screen.blit(refreshButtonImage, (x1, ybutton))
    else:
        mouse_on_refresh_button = False
        pygame.draw.rect(screen, lightgrey, (x1, ybutton, refreshButtonWidth, refreshButtonHeight))
    screen.blit(refreshButtonImage, (x1, ybutton))


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if mouse_on_start_button == True:
                if gen <= 1:
                    gen += 1
                    evo_size8(population, gen - 1)
                    fstSelected = False
                    bothSelected = False
                    prefPattern1 = -1
                    prefPattern2 = -1
                else:
                    gen += 1
                    evo_size8(population, gen)
                    fstSelected = False
                    bothSelected = False
                    prefPattern1 = -1
                    prefPattern2 = -1

                """
                if (gen - 1) % 10 == 0: # reset when 1, 11, 21, ...
                    #prefPattern1 = population.patterns[random.randrange(0, population.size)]
                    #prefPattern2 = population.patterns[random.randrange(0, population.size)]
                    prefPattern1 = -1
                    prefPattern2 = -1
                    fstSelected = False
                    bothSelected = False
                """
            elif mouse_on_refresh_button == True:
                # reinitialise population
                gen = 0
                population = evo.Population(size)
                #prefPattern1 = population.patterns[random.randrange(0, population.size)]
                #prefPattern2 = population.patterns[random.randrange(0, population.size)]
                prefPattern1 = -1
                prefPattern2 = -1
                fstSelected = False
                bothSelected = False
                evo_size8(population, gen + 1)
                #gen += 1
            elif msgBox == True and mouse_on_ok_button == True:
                draw_patterns(population)
                #draw_patterns_with_pref(population, prefPopulation)
                msgBox = False
                # checking & debugging
                parent1 = prefPattern1
                #if prefPattern1 == -1:
                #    parent1 = -1
                #elif prefPattern1 < population.prefSize:
                    #parent1 = population.patterns[prefPattern1]
                #else:
                    #parent1 = population.patterns[prefPattern1 - population.prefSize]
                parent2 = prefPattern2
                #if prefPattern2 == -1:
                #    parent2 = -1
                #elif prefPattern2 < population.prefSize:
                #    parent2 = population.patterns[prefPattern2]
                #else:
                    #parent2 = population.patterns[prefPattern2 - population.prefSize]

                #if parent1 != -1 and parent2 != -1:
                #    print("Gen: " + str(gen) + ", Pref 1: " + str(generator.fromPatternGeneToList(parent1)) + ", Pref 2: " + str(generator.fromPatternGeneToList(parent2)))

            #elif gen % 10 == 0 and gen != 0:
            else:
                if mouse[0] >= x1 and mouse[0] <= (x1 + box_size) and mouse[1] >= y1 and mouse[1] <= (y1 + box_size):
                    num = 0
                    msgBox = True
                    select_msg_display(num+1)
                    if fstSelected == False:
                        fstSelected = True
                        prefPattern1 = population.patterns[num]
                    elif fstSelected == True and bothSelected == False:
                        bothSelected = True
                        prefPattern2 = population.patterns[num]
                elif mouse[0] >= x2 and mouse[0] <= (x2 + box_size) and mouse[1] >= y2 and mouse[1] <= (y2 + box_size):
                    num = 1
                    msgBox = True
                    select_msg_display(num+1)
                    if fstSelected == False:
                        fstSelected = True
                        prefPattern1 = population.patterns[num]
                    elif fstSelected == True and bothSelected == False:
                        bothSelected = True
                        prefPattern2 = population.patterns[num]
                elif mouse[0] >= x3 and mouse[0] <= (x3 + box_size) and mouse[1] >= y3 and mouse[1] <= (y3 + box_size):
                    num = 2
                    msgBox = True
                    select_msg_display(num+1)
                    if fstSelected == False:
                        fstSelected = True
                        prefPattern1 = population.patterns[num]
                    elif fstSelected == True and bothSelected == False:
                        bothSelected = True
                        prefPattern2 = population.patterns[num]
                elif mouse[0] >= x4 and mouse[0] <= (x4 + box_size) and mouse[1] >= y4 and mouse[1] <= (y4 + box_size):
                    num = 3
                    msgBox = True
                    select_msg_display(num+1)
                    if fstSelected == False:
                        fstSelected = True
                        prefPattern1 = population.patterns[num]
                    elif fstSelected == True and bothSelected == False:
                        bothSelected = True
                        prefPattern2 = population.patterns[num]
                elif mouse[0] >= x5 and mouse[0] <= (x5 + box_size) and mouse[1] >= y5 and mouse[1] <= (y5 + box_size):
                    num = 4
                    msgBox = True
                    select_msg_display(num+1)
                    if fstSelected == False:
                        fstSelected = True
                        prefPattern1 = population.patterns[num]
                    elif fstSelected == True and bothSelected == False:
                        bothSelected = True
                        prefPattern2 = population.patterns[num]
                elif mouse[0] >= x6 and mouse[0] <= (x6 + box_size) and mouse[1] >= y6 and mouse[1] <= (y6 + box_size):
                    num = 5
                    msgBox = True
                    select_msg_display(num+1)
                    if fstSelected == False:
                        fstSelected = True
                        prefPattern1 = population.patterns[num]
                    elif fstSelected == True and bothSelected == False:
                        bothSelected = True
                        prefPattern2 = population.patterns[num]
                elif mouse[0] >= x7 and mouse[0] <= (x7 + box_size) and mouse[1] >= y7 and mouse[1] <= (y7 + box_size):
                    num = 6
                    msgBox = True
                    select_msg_display(num+1)
                    if fstSelected == False:
                        fstSelected = True
                        prefPattern1 = population.patterns[num]
                    elif fstSelected == True and bothSelected == False:
                        bothSelected = True
                        prefPattern2 = population.patterns[num]
                elif mouse[0] >= x8 and mouse[0] <= (x8 + box_size) and mouse[1] >= y8 and mouse[1] <= (y8 + box_size):
                    num = 7
                    msgBox = True
                    select_msg_display(num+1)
                    if fstSelected == False:
                        fstSelected = True
                        prefPattern1 = population.patterns[num]
                    elif fstSelected == True and bothSelected == False:
                        bothSelected = True
                        prefPattern2 = population.patterns[num]

    pygame.display.update()
    pygame.time.wait(40)

pygame.quit()
quit()