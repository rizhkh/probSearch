import pygame as pygame
import startprgm
import tkinter as tk
import numpy as np
import time
import genData
from ast import literal_eval

row = 10  # row
col = 10  # col
mine_density = 20

if __name__ == '__main__':
    pygame.init()  # initializes the pygame object - Required to run the window on screen
    resolution = (500,500) #(420, 420)  # screen resolution
    mine_density = 20

    row = int(row)
    col = row
    mine_density = int(mine_density)

    flags = pygame.DOUBLEBUF
    ThingsToAppearOnScreen_Display = pygame.display.set_mode(resolution,flags)  # This sets the width and height of the screen that pops up
    ThingsToAppearOnScreen_Display_2 = pygame.display.set_mode(resolution, flags)
    m = startprgm.start(ThingsToAppearOnScreen_Display, row, col, mine_density)
    m.start_algorithm(m)
    window_display_status = True


    #mls = m.get_all_rects()
    # Keeps the window running unless specifically you hit the x to close it
    while window_display_status:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                window_display_status = False
                pygame.quit()
                exit()
            # if event.type == pygame.MOUSEBUTTONDOWN:
            #
            #             # functionality: Click functionality for the first click
            #             # 20 is for the GUI setup
            #             for i in mls:
            #                 next_i = i[0] + 20
            #                 next_j = i[1] + 20
            #                 x = event.pos[0]
            #                 y = event.pos[1]
            #                 if ( x >= i[0] ) and ( x < next_i) :
            #                     if ( y >= i[1] ) and ( y < next_j) :
            #                         m.click_cell(m, i[1],i[0])
            #                         #m.rect_clicked( (150,150,150) , i[1],i[0]) # the reason [1] [0] are in reverse (it should be [0][1] is because pygame is storing index in reverse
            #                         #print(event.pos)


    # #To generate graphs
    # g = genData.generateData()
    # g.strategy_one()
    # g.strategy_Two()
    # # g.strategy_Own()
    # # g.avg_of_all()