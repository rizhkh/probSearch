import pygame as pygame
import startprgm
import tkinter as tk
import numpy as np
import time
from ast import literal_eval

row = 10  # row
col = 10  # col

if __name__ == '__main__':

    pygame.init()  # initializes the pygame object - Required to run the window on screen

    row = int(row)
    col = row

    def open_win(dim):
        if dim == 50 :
            resolution = (650, 650)
        elif dim == 15:
            resolution = (200, 200)
        else:
            resolution = (800, 800)

        dimension_board = dim
        dimension_board = int(dimension_board)
        flags = pygame.DOUBLEBUF
        ThingsToAppearOnScreen_Display = pygame.display.set_mode(resolution,
                                                                 flags)  # This sets the width and height of the screen that pops up
        ThingsToAppearOnScreen_Display_2 = pygame.display.set_mode(resolution, flags)
        m = startprgm.start(ThingsToAppearOnScreen_Display, row, col, dimension_board)
        return m


    def One():
        m = open_win(50)
        m.start_algorithm("One")
        continue_process()

    def Two():
        m = open_win(50)
        m.start_algorithm("Two")
        continue_process()

    def f_One():
        m = open_win(15)
        m.start_algorithm("f_One")
        continue_process()

    def f_Two():
        m = open_win(15)
        m.start_algorithm("f_Two")
        continue_process()

    def f_Three():
        m = open_win(15)
        m.start_algorithm("f_Three")
        continue_process()

    def Own():
        m = open_win(15)
        m.start_algorithm("Own")
        continue_process()


    def continue_process():
        window_display_status = True
        # Keeps the window running unless specifically you hit the x to close it
        while window_display_status:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    window_display_status = False
                    pygame.quit()
                    exit()
    root = tk.Tk()

    f1 = tk.Frame(root)
    b1 = tk.Button(f1, text="Rule One", command=One)
    b2 = tk.Button(f1, text="Rule Two", command=Two)
    b3 = tk.Button(f1, text="Modified Algorithm With Rule One", command=f_One)
    b4 = tk.Button(f1, text="Modified Algorithm With Rule Two", command=f_Two)
    b5 = tk.Button(f1, text="Modified Algorithm With Direct Search", command=f_Three)
    b6 = tk.Button(f1, text="Own Algorithm", command=Own)
    f1.grid(row=1, column=1, sticky="nsew")

    b1.pack(side="top")
    b2.pack(side="top")
    b3.pack(side="top")
    b4.pack(side="top")
    b5.pack(side="top")
    b6.pack(side="top")
    root.mainloop()

    #To generate graphs
    # g = genData.generateData()
    # g.strategy_one()
    # g.strategy_Two()
    # g.strategy_Own()
    # g.avg_of_all()