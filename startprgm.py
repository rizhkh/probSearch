import pygame as pygame
import numpy as np
import random

class start:
    PYGAMEWIDTH = 300  # 600   # Do not change this: This is window sizing
    PYGAMEHEIGHT = 300  # Do not change this: This is window sizing

    dimension = 10
    original_board_array = np.zeros((dimension, dimension), dtype=int)
    belief_array = np.zeros((dimension, dimension), dtype=float)
    false_negative_Array = np.zeros((dimension, dimension), dtype=float)
    targets = np.zeros((dimension, dimension), dtype=float)
    target_cell = None

    row = 0  # row
    col = 0  # col

    box_width = 12
    box_height = 12

    board_array = np.zeros((0, 0), dtype=int)
    board_array_2 = np.zeros((0, 0), dtype=int)
    #board_array = np.zeros((0, 0), dtype=object)
    screen = None
    screen_two = None

    list_of_all_rects = []

    recent_clicked_rect_x = None
    recent_clicked_rect_y = None

    environment_class = None
    agent_class = None

    total_mines = 0


    row = 0  # row
    col = 0  # col
    mine_density = None

    def __init__(self, scree_one, r , c, mines):
        self.screen = scree_one
        self.row = r
        self.col = c
        self.mine_density = mines
        orignal_board_array = np.zeros((self.mine_density, self.mine_density), dtype=float)


    def get_arr(self):
        return self.board_array

    # def get_all_rects(self):
    #     return self.environment_class.get_all_rects() #self.list_of_all_rects

    def highlight_board(self,i,j):
        # canvas_arr_i = i * 20  # the reason it is being multiplied is because the cell size is set to 20 - if its the orignal value then it causes GUI problems
        # canvas_arr_j = j * 20
        status = self.environment_class.get_cell_value(self.board_array,i,j)
        if status != 1:
            val = self.environment_class.get_clue(self.board_array,i,j)
            self.environment_class.color_cell(str(val), i, j,0)
        elif status == 1:   # IF THE CELL IS A MINE
            self.total_mines += 1
            self.environment_class.color_cell('', i, j,1)

    def generate_tiles_gui(self, prob, i , j):

        # orignal board array stores 4 values through out its 2d array this vales
        # flat = 1
        # cave = 2
        # hilly = 3
        # forested = 4

        # reason: as prob values are same its confusing with same prob values

        if  prob < 0.5: #prob < 0.3:
            r = random.randint(0,1)
            if r == 0:
                self.original_board_array[i][j] = 1  # Flat
                self.color_cell(i , j, 'Flat')

            if r == 1:
                self.original_board_array[i][j] = 2  # cave
                self.color_cell(i, j, 'Cave')

        if prob >= 0.5: #prob <= 0.1 and prob <= 0.3:
            r = random.randint(0,1)
            if r == 0:
                self.original_board_array[i][j] = 3  # Hilly
                self.color_cell(i, j, 'Hilly')

            if r == 1:
                self.original_board_array[i][j] = 4  # Forested
                self.color_cell(i, j, 'Forested')

    def set_false_negative_vals(self, i , j ):
        terrain_val = self.original_board_array[i][j]

        if terrain_val == 1:
               self.false_negative_Array[i][j] = 0.1    # flat
        if terrain_val == 2:
               self.false_negative_Array[i][j] = 0.9    # caves
        if terrain_val == 3:
               self.false_negative_Array[i][j] = 0.3    # hilly
        if terrain_val == 4:
               self.false_negative_Array[i][j] = 0.7    #forested

    def set_target_cell(self, i ,j):
        self.target_cell = [i,j]

    def get_target_cell(self):
        return self.target_cell

    def generate_board(self):
        for i in range( 0 , self.dimension):
            for j in range(0 , self.dimension):
                self.belief_array[i][j] = 1 / (self.dimension * self.dimension)
                prob = random.random()
                self.generate_tiles_gui(prob , i , j)   # sets prob values of textures on map
                self.set_false_negative_vals(i , j) # sets prob values of textures on map
                self.targets[i][j] = 1 - self.false_negative_Array[i][j]


    def color_cell(self, row_x , col_y, status):
        message = ''
        row_x = row_x * 13
        col_y = col_y * 13

        if status == 'Flat':
            Grid_box_Object = pygame.draw.rect(self.screen, (255,255,255), [col_y, row_x, self.box_width, self.box_height])   # row_x=row and col_y=col is the position where the box will be displayed
            # text = self.font.render(message, True, (255, 255, 255))
            # self.screen.blit(text, Grid_box_Object.midtop)
            pygame.display.flip()
        if status == 'Hilly':
            Grid_box_Object = pygame.draw.rect(self.screen, (192,192,192), [col_y, row_x, self.box_width, self.box_height])   # row_x=row and col_y=col is the position where the box will be displayed
            pygame.display.flip()
        if status == 'Forested':
            Grid_box_Object = pygame.draw.rect(self.screen, (76,153,0), [col_y, row_x, self.box_width, self.box_height])   # row_x=row and col_y=col is the position where the box will be displayed
            pygame.display.flip()
        if status == 'Cave':
            Grid_box_Object = pygame.draw.rect(self.screen, (153,76,0), [col_y, row_x, self.box_width, self.box_height])   # row_x=row and col_y=col is the position where the box will be displayed
            pygame.display.flip()


    # This function works just once - you click once that is it - the rest is auto movement
    def click_cell(self,obj,i,j):
        obj = self.environment_class  # do not remove this - obj variable is being passed the reference of global obj this way the refernce is copied in start_algorithm
        # and we dont have pass any obj in main.py

        # we are dividing by 20 due do GUI dimension for pycharm - its a scaling issue in GUI
        index_board_i= int(i/20)
        index_board_j= int(j/20)
        # after this wherever we send i and j we dont need to worry about rescaling issues

        val = obj.get_clue(self.board_array , index_board_i, index_board_j)
        self.highlight_board(index_board_i,index_board_j)
        # # Note: MAKE SURE TO CHECK IF THE NEIGHBOR LIST HAS ANY CELL THAT HAS BEEN REVEALED OR MARKED AS A MINE/FLAGGED

        # Reveales the cell
        returned_list =  self.agent_class.constraint_cell_processing(index_board_i,index_board_j)

        self.agent_class.var_removed_confirmed([index_board_i,index_board_j])

        # Forms equations of un revealed neighbor cells of current cell and gets stored in Knowledge base
        self.agent_class.form_equation(returned_list, val, [index_board_i,index_board_j])
        safe_cells_to_traverse = []
        safe_cells_to_traverse = self.agent_class.csp_solver(returned_list, [index_board_i,index_board_j])
        for i in safe_cells_to_traverse:
            self.environment_class.color_cell('T', i[0], i[1], 'testing')

        #self.agent_class.traverse_board(safe_cells_to_traverse) # For basic algorithm
        #for advanced algorithm i worte
        self.agent_class.traverse(safe_cells_to_traverse) # for my own aglorithm

    def forSimpleWindow(self):
        for i in range(0 , len( self.board_array_2) ):
            for j in range(0, len( self.board_array_2 )):
                status = self.environment_class.get_cell_value(self.board_array_2,i,j)

    def highlight_board_empty(self,i,j):
        # canvas_arr_i = i * 20  # the reason it is being multiplied is because the cell size is set to 20 - if its the orignal value then it causes GUI problems
        # canvas_arr_j = j * 20
        status = self.environment_class.get_cell_value(self.board_array,i,j)
        if status != 1:
            #color = (150, 150, 150)
            val = self.environment_class.get_clue(self.board_array,i,j)
            #self.environment_class.rect_clicked( str(val) , color, canvas_arr_i,canvas_arr_j)
            if val == 0 :
                self.environment_class.color_cell('', i, j, 0)
            else:
                self.environment_class.color_cell(str(val), i, j,0)
        elif status == 1:   # IF THE CELL IS A MINE
            color = (255, 0, 0)
            self.total_mines += 1
            #self.environment_class.rect_clicked('', color, canvas_arr_i, canvas_arr_j)
            self.environment_class.color_cell('', i, j,1)

    # This function gets max value from any passed array
    def get_max_val(self, passed_array):
        temp = -9
        val = None
        pos = None

        for i in range(0 , len(passed_array)):
            for j in range(0 , len(passed_array)):
                #print(passed_array[i][j])
                if passed_array[i][j] > temp:
                    val = passed_array[i][j]
                    pos = [i,j]
                temp = passed_array[i][j]
        v = [ val, pos ]
        return v

    # This function is used for cell targets and false negs rate for cells observation compute
    def cell_obs(self, pos, status):
        i = pos[0]
        j = pos[1]
        r = random.randint(0, 100)
        if status == 'fneg':
            rand_val_c = r/100
            val = self.false_negative_Array[i,j]
            if val <= rand_val_c:
                return True

        if status == 'prb_tar':
            rand_val_c = r / 100
            if rand_val_c <= self.targets[i][j]:
                return True

        return False

    def recompute_belief(self):
        # print(new_total_val)
        for i in range( 0 , len(self.belief_array) ):
            for j in range(0, len(self.belief_array)):
                self.belief_array[i][j] = self.belief_array[i][j] / np.sum(self.belief_array)#new_total_val

    def bayes_computation(self, max_cell, status):
        pos = max_cell[1]
        i = pos[0]
        j = pos[1]
        if status == "b_One":
            val = max_cell[0]
            self.belief_array[i][j] = self.false_negative_Array[i][j] * self.belief_array[i][j]

        if status == "b_Two":
            val = max_cell[0]
            #self.belief_array[i][j] = (1 - self.false_negative_Array[i][j]) * self.belief_array[i][j]
            # made it look cleaner and did this on the main board generation so dont need it here
            self.belief_array[i][j] = self.targets[i][j] * self.belief_array[i][j]

    # computing the probabilistic chance that the current open cell is in
    def start_rule_one(self):
        iteration_count = 0
        while True:
            iteration_count += 1
            max_cell = self.get_max_val( self.belief_array )
            print(max_cell[1] , " | " , self.target_cell)

            if max_cell[1] == self.target_cell: # checks if highest prob cell is target cell
                if self.cell_obs(max_cell[1],'fneg') == True: #False:
                    print("Target Found in Iteration: " , iteration_count)
                    break
            else:
                self.bayes_computation(max_cell, "b_One")
                # normalize
                for i in range(0, len(self.belief_array)):
                    for j in range(0, len(self.belief_array)):
                        self.belief_array[i][j] = self.belief_array[i][j] / np.sum(self.belief_array)  # new_total_val
                #self.recompute_belief()

    def start_rule_two(self):
        iteration_count = 0
        while True:
            iteration_count += 1
            max_cell = self.get_max_val( self.belief_array )
            print(max_cell[1] , " | " , self.target_cell)
            if max_cell[1] == self.target_cell: # checks if highest prob cell is target cell
                if self.cell_obs(max_cell[1],'prb_tar') == True: #False:
                    print("Target Found in Iteration: " , iteration_count)
                    break
            else:
                self.bayes_computation(max_cell, "b_Two")
                # normalize
                for i in range(0, len(self.belief_array)):
                    for j in range(0, len(self.belief_array)):
                        self.belief_array[i][j] = self.belief_array[i][j] / np.sum(self.belief_array)  # new_total_val
                #self.recompute_belief()

    def start_algorithm(self, obj):



        self.board_array = np.zeros((self.row, self.col), dtype=int)

        self.board_array_for_agent_info = np.copy(self.board_array)

        pygame.display.set_caption("Search and Destroy", "SD")
        pygame.display.flip()
        # self.environment_class = environment(self.screen, self.board_array, obj, self.box_height, self.box_width , self.row , self.col , self.mine_density)
        # self.environment_class.set_mine_count( self.mine_density )
        # self.board_array = self.environment_class.add_mines_randomly(self.board_array)
        # self.environment_class.generate_board(self.board_array)
        # self.board_array_2 = np.copy(self.board_array)
        # print(self.board_array) # shows map where the mines are
        #
        # self.agent_class = Agnt( self.board_array , self.row, self.col, self.box_height, self.box_width)
        # self.agent_class.set_environment_obj(self.environment_class)    # because of this method agent class can use environment methods now
        # self.agent_class.init_all_cells()

        self.generate_board()

        # Now that everything is set up for the environment
        random_index_i = random.randint(0,self.dimension)
        if random_index_i == len(self.original_board_array):
            random_index_i = random_index_i - 1
        random_index_j = random.randint(0, self.dimension)
        if random_index_j == len(self.original_board_array):
            random_index_j = random_index_j - 1
        self.set_target_cell(random_index_i , random_index_j)

        self.start_rule_one()

        pygame.display.flip()
