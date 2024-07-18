import numpy as np
import copy

def find_element(arr, tar):
    """ 
    function used to find the row and column of an element in the 2d matrix (only for searching unique element)
    Input:
        arr (2d array) - the Gridworld map
        tar (char) - character needed to be found, e.g., 'R'
    Output:
        (i, row.index(tar)) - row and column of the input character on the map
    """
    try:
        for i, row in enumerate(arr):
            if tar in row:
                return (i, row.index(tar)) # return the index of the row (i) and column (row.index(tar))
    except ValueError:
        raise ValueError("Value not found !!!!!!!!!!") # if not found, raise the error
        


#################################################
#### Environment of the gridworld for part 1 ####
#################################################
class Environment_1:

    def __init__(self):
        # set up parameters
        self.n_row = 5
        self.n_col = 5
        self.n_state = self.n_row * self.n_col
        self.n_action = 4

        # Available actions
        #                      left      down      right     up
        self.action =       [ [0, -1],  [1, 0],   [0, 1],   [-1, 0]]
        self.action_text =  ['\u2190', '\u2193', '\u2192', '\u2191']  # unicode text used for visualization

        # Gridworld map
        #             0   1   2   3   4
        self.map = [['W','B','W','W','G'], # 0          map[0][4] = 'G'
                    ['W','W','W','W','W'], # 1
                    ['W','W','W','W','W'], # 2      
                    ['W','W','R','W','W'], # 3          map[3][2] = 'R'
                    ['W','W','W','W','Y']] # 4

        # Set up the model, (n_state) by (n_action) by (n) by (3) array, for state s and action a,
        # there are n possibilities for transiting to different next state s_, each row is composed of (p, s_, r)
        # p  - transition probability from (s,a) to (s_)   ### sum of the n p equals 1
        # s_ - next state
        # r  - reward of the transition from (s,a) to (s_)
        self.model = [[[] for _ in range(self.n_action)] for _ in range(self.n_state)]
        for s in range(self.n_state):
            for a in range(self.n_action):
                row, col = np.divmod(s,self.n_row)  # calculate the place on the map based on the state number
                act = self.action[a]  # 0 left, 1 down, 2 right, 3 up
                row_, col_ = row + act[0], col + act[1]  # new positions after action
                state_ = row_ * self.n_row + col_  # calculate the state number based on the place on the map

                # White, Red, Yellow
                if self.map[row][col] == 'W' or self.map[row][col] == 'R' or self.map[row][col] == 'Y':
                    if (row_ < 0) or (col_ < 0) or (row_ > self.n_row - 1) or (col_ > self.n_col - 1):
                        self.model[s][a].append([1.0, s, -0.5])  # if want to move out, stay and -0.5
                    else:
                        self.model[s][a].append([1.0, state_, 0.0])

                # Blue
                elif self.map[row][col] == 'B':  # if B, jump to R
                    row_, col_ = find_element(self.map, 'R')
                    state_ = row_ * self.n_row + col_  # calculate the state number based on the place on the map
                    self.model[s][a].append([1.0, state_, 5.0])

                # Green
                elif self.map[row][col] == 'G':  # if G, jump to R or Y
                    row_, col_ = find_element(self.map, 'R')
                    state_ = row_ * self.n_row + col_  # calculate the state number based on the place on the map
                    self.model[s][a].append([0.5, state_, 2.5])
                    row_, col_ = find_element(self.map, 'Y')
                    state_ = row_ * self.n_row + col_  # calculate the state number based on the place on the map
                    self.model[s][a].append([0.5, state_, 2.5])

                else:
                    raise ValueError("Unknown value !!!!!!!!!!")


#################################################
#### Environment of the gridworld for part 2 ####
#################################################
class Environment_2:

    def __init__(self):
        # set up parameters
        self.n_row = 5
        self.n_col = 5
        self.n_state = self.n_row * self.n_col
        self.n_action = 4

        # Available actions
        #                      left      down      right     up
        self.action =       [ [0, -1],  [1, 0],   [0, 1],   [-1, 0]]
        self.action_text =  ['\u2190', '\u2193', '\u2192', '\u2191']  # unicode text used for visualization

        # Gridworld map
        #             0   1   2   3   4
        self.map = [['W','B','W','W','G'], # 0          map[0][4] = 'G'
                    ['W','W','W','W','W'], # 1
                    ['W','W','W','W','T'], # 2      
                    ['W','W','W','W','W'], # 3
                    ['T','W','R','W','Y']] # 4          map[4][2] = 'R'

        # Set up the model, (n_state) by (n_action) by (n) by (4) array, for state s and action a,
        # there are n possibilities for transiting to different next state s_, each row is composed of (p, s_, r, t)
        # p  - transition probability from (s,a) to (s_)   ### sum of the n p equals 1
        # s_ - next state
        # r  - reward of the transition from (s,a) to (s_)
        # t  - terminal information, a bool value, True/False
        self.model = [[[] for _ in range(self.n_action)] for _ in range(self.n_state)]
        for s in range(self.n_state):
            for a in range(self.n_action):
                row, col = np.divmod(s,self.n_row)  # calculate the place on the map based on the state number
                act = self.action[a]  # 0 left, 1 down, 2 right, 3 up
                row_, col_ = row + act[0], col + act[1]  # new positions after action
                state_ = row_ * self.n_row + col_  # calculate the state number based on the place on the map

                # Blue
                if self.map[row][col] == 'B':  # if B, jump to R
                    row_, col_ = find_element(self.map, 'R')
                    state_ = row_ * self.n_row + col_  # calculate the state number based on the place on the map
                    self.model[s][a].append([1.0, state_, 5.0, False])

                # Green
                elif self.map[row][col] == 'G':  # if G, jump to R or Y
                    row_, col_ = find_element(self.map, 'R')
                    state_ = row_ * self.n_row + col_  # calculate the state number based on the place on the map
                    self.model[s][a].append([0.5, state_, 2.5, False])
                    row_, col_ = find_element(self.map, 'Y')
                    state_ = row_ * self.n_row + col_  # calculate the state number based on the place on the map
                    self.model[s][a].append([0.5, state_, 2.5, False])

                # White, Red, Yellow
                elif self.map[row][col] == 'W' or self.map[row][col] == 'R' or self.map[row][col] == 'Y':
                    if (row_ < 0) or (col_ < 0) or (row_ > self.n_row - 1) or (col_ > self.n_col - 1):
                        self.model[s][a].append([1.0, s, -0.5, False])  # if want to move out, stay and -0.5
                    elif self.map[row_][col_] == 'T':  # if new state is terminal state
                        # self.model[s][a].append([1.0, state_, -0.2, True])
                        self.model[s][a].append([1.0, state_, 0.0, True])
                    else:
                        self.model[s][a].append([1.0, state_, -0.2, False])

                # Terminal (Black)
                elif self.map[row][col] == 'T':  # if current is terminal, just for indexing
                    self.model[s][a].append([1.0, s, 0.0, True])

                else:
                    raise ValueError("Unknown value !!!!!!!!!!")
                

    def permute_G_B(self):
        """ 
        Permute the locations of the green and blue squares
        """

        # find G and B in map
        row_B, col_B = find_element(self.map, 'B')
        state_B = row_B * self.n_row + col_B
        row_G, col_G = find_element(self.map, 'G')
        state_G = row_G * self.n_row + col_G

        # change G and B in map
        self.map[row_G][col_G] = 'B'
        self.map[row_B][col_B] = 'G'

        # change G and B in model
        temp = copy.deepcopy(self.model[state_B])
        self.model[state_B] = copy.deepcopy(self.model[state_G])
        self.model[state_G] = copy.deepcopy(temp)
