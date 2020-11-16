import pygame as pygame
import numpy as np
import random

class start:
    PYGAMEWIDTH = 300  # 600   # Do not change this: This is window sizing
    PYGAMEHEIGHT = 300  # Do not change this: This is window sizing

    dimension = 0
    original_board_array = np.zeros((dimension, dimension), dtype=int)
    belief_array = np.zeros((dimension, dimension), dtype=float)
    false_negative_Array = np.zeros((dimension, dimension), dtype=float)
    targets = np.zeros((dimension, dimension), dtype=float)
    target_cell = None
    cell_distance_array = np.zeros((dimension, dimension), dtype=float)
    cell_distance_array_cost = np.zeros((dimension, dimension), dtype=float)

    row = 0  # row
    col = 0  # col

    box_width = 12
    box_height = 12

    screen = None   # For Graphical setup for the canvas
    screen_two = None

    list_of_all_rects = []

    total_mines = 0


    row = 0  # row
    col = 0  # col
    board_dimension = None

    def __init__(self, scree_one, r , c, dim):
        self.screen = scree_one
        self.row = r
        self.col = c
        self.board_dimension = dim
        self.dimension = dim
        self.original_board_array = np.zeros((self.board_dimension, self.board_dimension), dtype=float)
        self.belief_array = np.zeros((self.dimension, self.dimension), dtype=float)
        self.false_negative_Array = np.zeros((self.dimension, self.dimension), dtype=float)
        self.targets = np.zeros((self.dimension, self.dimension), dtype=float)
        self.cell_distance_array = np.zeros((self.dimension, self.dimension), dtype=float)
        self.cell_distance_array_cost = np.zeros((self.dimension, self.dimension), dtype=float)


    def get_arr(self):
        return self.board_array

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

    def compute_cell_dist_md(self, arr_cell_distance, arr_cell_cost):
        for i in range(0, len(arr_cell_distance)):
            for j in range(0, len(arr_cell_distance)):
                arr_cell_distance[i][j] = self.belief_array[i][j] * self.targets[i][j] / arr_cell_cost[i][j]

    def get_val(self, array_name,search_i, search_j):
        if search_i>= 0 and search_i<self.dimension and search_j>= 0 and search_j<self.dimension:
            if array_name[search_i][search_j]:
                return array_name[search_i][search_j]
        else:
            return -1000

    def start_rule_md(self):
        # My understanding: Compute manhattan distance and then determine whether you want to search current cell
        # or move in the direction of cell from manhattan distance and choose to move neighboring cell
        # repeat

        iteration_count = 0
        cell_position = [0,0]
        vall = self.get_val(self.belief_array,0, 0)
        max_cell = [vall, cell_position]
        check = 1
        while True:
            iteration_count += 1
            #max_cell = self.get_max_val( self.belief_array )

            # compute cost of travelling in cells
            for i in range( 0 , self.board_dimension):
                for j in range( 0 , self.board_dimension):
                    self.cell_distance_array_cost[i][j] = ( abs(i - cell_position[0]) + abs(j - cell_position[1]) )
            # Setting the value of current cells cost as we do not want to be confused in future computations
            self.cell_distance_array_cost[ cell_position[0] ][ cell_position[1] ] = -9999
            if check == 1:
                print("[CURRENT PROCESSED CELL: " , max_cell[1] , "]")
            if check == 0 :
                print("moving")
            if max_cell[1] == self.target_cell:# and check==1: # checks if highest prob cell is target cell
                if self.cell_obs(max_cell[1],'fneg') == True: #False:
                    print("current cell:  " , cell_position)
                    print("Target Found in Iteration: " , iteration_count)
                    break

                #add code: if else condition runs remove [0] from desc and set max_cell as desc[1]

            else:
                # computing the (manhattan distance from current location)/(probability
                # of finding target in that cell)
                self.compute_cell_dist_md(self.cell_distance_array, self.cell_distance_array_cost)
                self.cell_distance_array[ cell_position[0] ][ cell_position[1] ] = self.belief_array[i][j] * self.targets[i][j]

                # max_cell = self.get_max_val(self.cell_distance_array)
                # print("max: " , max_cell)

                self.bayes_computation(max_cell, "b_Two")
                for i in range(0, len(self.belief_array)):
                    for j in range(0, len(self.belief_array)):
                        self.belief_array[i][j] = self.belief_array[i][j] / np.sum(self.belief_array)  # new_total_val

                cell_position = max_cell[1]

                #max_cell = self.get_max_val(self.belief_array)

                desc = []
                index_i = cell_position[0]
                index_j = cell_position[1]

                current_processed_cell = self.get_val(self.cell_distance_array, index_i,index_j)
                cpc = [ current_processed_cell, [index_i, index_j] ]
                desc.append(cpc)

                cell_up = self.get_val(self.cell_distance_array, index_i-1, index_j)
                cu = [cell_up, [index_i-1, index_j]]
                desc.append(cu)

                cell_down = self.get_val(self.cell_distance_array, index_i+1, index_j)
                cd = [cell_down, [ index_i+1, index_j ]]
                desc.append(cd)

                cell_left = self.get_val(self.cell_distance_array, index_i, index_j-1)
                cl = [cell_left, [index_i, index_j-1]]
                desc.append(cl)

                cell_right = self.get_val(self.cell_distance_array, index_i, index_j+1)
                cr = [cell_right, [index_i, index_j+1]]
                desc.append(cr)


                desc.sort(reverse=True)

                print(desc)
                f = desc[0]
                max_cell = f

                #
                # # check if current cell is highest prob
                # first_val = desc[0]
                # print(desc)
                # # print("FIRST VAL ___________________ : " , first_val)
                # if first_val[1] == [cell_position[0], cell_position[1]]:
                #     print("CURRENT CELL HAS THE HIGHEST PROB")
                #     print("current cell: ", cell_position)
                #     cell_position =[cell_position[0], cell_position[1]]
                #     print("will search this cell: " , cell_position)
                #     vall = self.get_val(self.cell_distance_array, cell_position[0], cell_position[1])
                #     max_cell = [vall , cell_position]
                #     check = 1
                # else:
                #     first_val = desc[0]
                #     print("current cell: " , cell_position)
                #     cell_position = first_val[1]    # [1] is the position, index
                #     print("moving to neighbor cell WE ARE NOT SEARCHING: " , cell_position)
                #     check = 0


                # now check if the prob of current cell is higher or prob of neighboring cells is higher - if higher
                # move to neighboring cells
                # if current cell is higher search


                # for i in range(0 , len(self.cell_distance_array) ):
                #     for j in range(0 , len(self.cell_distance_array) ):
                #         self.cell_distance_array[i][j] = self.belief_array[i][j] * self.targets[i][j] / self.cell_distance_array_cost[i][j]


    def start_algorithm(self, obj):



        self.board_array = np.zeros((self.row, self.col), dtype=int)

        self.board_array_for_agent_info = np.copy(self.board_array)

        pygame.display.set_caption("Search and Destroy", "SD")
        pygame.display.flip()

        self.generate_board()

        # Now that everything is set up for the environment
        random_index_i = random.randint(0,self.dimension)
        if random_index_i == len(self.original_board_array):
            random_index_i = random_index_i - 1
        random_index_j = random.randint(0, self.dimension)
        if random_index_j == len(self.original_board_array):
            random_index_j = random_index_j - 1
        self.set_target_cell(random_index_i , random_index_j)

        #self.start_rule_one()

        #self.start_rule_two()

        self.start_rule_md()

        pygame.display.flip()
