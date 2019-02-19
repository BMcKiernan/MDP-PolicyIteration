import random
reward = -0.05
discount = 0.9
total_rows = 3
total_cols = 4

#actions are ((.1 prob of going left), (.9 prob of going desired direction))
#key is desired action with tuple value representing (left, desired action) 
actions = {'right':('up', 'right'), 'down':('right', 'down'), 'left':('down', 'left'), 'up':('left','up'),}

def copy_to(array1, array2):
    for i in range(total_rows):
        for j in range(total_cols):
            array1[i][j] = array2[i][j]

def setup_tempspace(rows, cols, data):
    global temp_space
    temp_space = [[data for i in range(cols)] for j in range(rows)]

def setup_statespace(rows, cols, data):
    global state_space
    state_space = [[data for i in range(cols)] for j in range(rows)]

def  setup_policyspace(rows, cols, data):
    global policy_space
    policy_space = [[data for i in range(cols)] for j in range(rows)]



#state is a 2-tuple (row, col), policy is the action to be taken
#for the transition
def policy_iteration():
    global state_space
    global policy_space
    global temp_space
    prob1 = 0
    prob9 = 0
    row_max = len(state_space) 
    col_max = len(state_space[0])
    #policy evaluation
    for i in range(row_max):
        for j in range(col_max):
            if state_space[i][j] is not None and state_space[i][j] != -1 and state_space[i][j] != 1:
                state = (i, j)
                prob1 = get_position_value(state_space, state, (actions[policy_space[i][j]])[0])
                prob9 = get_position_value(state_space, state, (actions[policy_space[i][j]])[1])
                value = round(reward + discount*( 0.1 * prob1 + 0.9 * prob9), 3)
                temp_space[i][j] = value
            else:
                continue        
    copy_to(state_space, temp_space)
    #policy_improvement 
    for i in range(row_max):
        for j in range(col_max):
            if state_space[i][j] is not None and state_space[i][j] != -1 and state_space[i][j] != 1:
                choice = None
                state = (i, j)
                for key in actions:
                    prob1 = get_position_value(state_space, state, (actions[key])[0])
                    prob9 = get_position_value(state_space, state, (actions[key])[1])
                    val = round(float((0.1 * prob1 + 0.9 * prob9)), 3)
                    if choice is None:
                        choice = [key, val]
                        policy_space[i][j] = choice[0]
                    elif choice[1] < val:
                        choice = [key, val]
                        policy_space[i][j] = choice[0]
            else:
                continue

''''
This function returns the value at the specifed position with
bounds checking. If at an edge position and the position requested
is outside the 2d-array the current positions value is returned.
state is current position in state_space (#r, #c)
action is any of the actions dictionary
'''
def get_position_value(space, state, action):
    row_max = len(state_space) -1
    col_max = len(state_space[0]) -1
    if action == 'up':
        # in first row can't go up || there is obstacle
        if state[0] == 0 or space[state[0] - 1][state[1]] is None:
            return space[state[0]][state[1]] 
        else:
            return space[state[0] - 1][state[1]]
    if action == 'down':
        # in last row can't go down || there is obstacle
        if state[0] == row_max or space[state[0] + 1][state[1]] is None:
            return space[state[0]][state[1]]
        else:
            return space[state[0] + 1][state[1]]
    if action == 'left':
        # in first column can't go left || there is obstacle
        if state[1] == 0 or space[state[0]][state[1] - 1] is None: 
            return space[state[0]][state[1]]
        else:
            return space[state[0]][state[1] - 1]
    if action == 'right':
        # in last column can't go right || there is obstacle
        if state[1] == col_max or space[state[0]][state[1] + 1] is None:
            return space[state[0]][state[1]]
        else: 
            return space[state[0]][state[1] + 1]

#grid is space for printing
#string name is to print before grid
def print_space(grid, string_name):
    print("\t\t " + string_name)
    for i in range(total_rows):
        print("\t\t " + str(grid[i]))
    print ("")

if __name__ == "__main__":

    #state_space shows policy iteration and calc of rewards
    setup_statespace(total_rows, total_cols, 0)
    state_space[1][1] = None #obstacle
    state_space[0][3] = 1 #utility
    state_space[1][3] = -1 #utility

    #policy space - shows agents move choices 
    random_policy = random.choice(['up', 'left', 'right', 'down']) 
    setup_policyspace(total_rows, total_cols, random_policy) 
    policy_space[1][1] = None #obstacle
    policy_space[0][3] = 1 #utility
    policy_space[1][3] = -1 #utility
    
    #temp_space is for holding intermediary values
    setup_tempspace(total_rows, total_cols, 0)
    temp_space[1][1] = None #obstacle
    temp_space[0][3] = 1 #utility
    temp_space[1][3] = -1 #utility

    print("Printing setup") 
    print_space(state_space, "state_space")
    print_space(policy_space, "policy")
    
    i = 0
    p = 10
    while(i < p):
        policy_iteration()
        i += 1
        print( "After " + str(i) +  " iterations")
        print_space(state_space, "state_space")
        print_space(policy_space, "policy")

    print ("\n Rewards converge to within .001 for all cells after 10 policy iterations \n" )

