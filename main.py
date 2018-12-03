
reward = -0.05
discount = 0.9

#actions are ((.1 prob of going left), (.9 prob of going desired direction))
actions = {'right':('up', 'right'), 'up':('left', 'up'), 'left':('down', 'left'), 'down':('right','down'),}


def setup_statespace(rows, cols, data):
    global state_space
    state_space = [[data for i in range(cols)] for j in range(rows)]

def  policy_statespace(rows, cols, data):
    global policy_space
    policy_space = [[data for i in range(cols)] for j in range(rows)]

#state is a 2-tuple (row, col), policy is the action to be taken
#for the transition
def transition(state, action):
    prob1 = 0
    prob9 = 0
    rows = len(state_space)     
    cols = len(state_space[0])
    #compute values with random policy all up ^
    row_max = len(state_space) 
    col_max = len(state_space[0])
    #Random Policy Step 1 - Up for all
    for i in range(row_max):
        for j in range(col_max):
            state = (i, j)
            prob1 = get_position_value(state, (actions['up'])[0])
            prob9 = get_position_value(state, (actions['up'])[1])
            value = reward + discount*( 0.1 * prob1 + 0.9 * prob9)
            state_space[i][j] = value
    for i in range(row_max):
        for j in range(col_max):
            for key, value in actions.iteritems():
                state = (i, j)
            prob1 = get_position_value(state, value[0])
            prob9 = get_position_value(state, value[1])



#state is current position in state_space (#r, #c)
#action is any of the actions dictionary  
def get_position_value(state, action):
    val = -99
    row_max = len(state_space) -1 
    col_max = len(state_space[0]) -1 

    if action == 'up':
        if state[0] == 0 or state_space[state[0] - 1][state[1]] is None : # in first row can't go up || there is obstacle
            val = state_space[state[0]][state[1]] 
        else:
            val = state_space[state[0] - 1][state[1]]

    if action == 'down':
        if state[0] == row_max or state_space[state[0] + 1][state[1]] is None: # in last row can't go down || there is obstacle
            val = state_space[state[0]][state[1]]
        else:
            val = state_space[state[0] + 1]][state[1]]

    if action == 'left':
        if state[1] == 0 or state_space[state[0]][state[1] - 1] is None: # in first column can't go left || there is obstacle
            val = state_space[state[0]][state[1]]
        else:
            val = state_space[state[0]][state[1] - 1]
        
    if action == 'right':
        if state[1] == col_max or state_space[state[0]][state[1] + 1] is None: # in last column can't go right || there is obstacle
            val = state_space[state[0]][state[1]]
        else: 
            val = state_space[state[0]][state[1] + 1]

    return val




if __name__ == "__main__":
