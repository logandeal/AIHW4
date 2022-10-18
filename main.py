import copy, time, sys
from turtle import down

class Node:
    def __init__(self, state, depth, prev, turn, row, col):
        self.state = state
        self.depth = depth
        self.prev = prev
        self.next = set()
        self.turn = turn
        self.heuristic = None
        self.row = row
        self.col = col
    
    def setNext(self, next):
        self.next.add(next)

    def setHeuristic(self, heuristic):
        self.heuristic = heuristic

    def getTurn(self): return self.turn

    def getDepth(self): return self.depth

    def getHeuristic(self): return self.heuristic

    def getNext(self): return self.next


def getNextTurn(turn):
    if turn == "x": return "o" 
    return "x"


# generates levels of tree needed
def generateTree(node_to_expand, depth_to_generate):
    amt_generated = 0
    if depth_to_generate < 1: return
    to_expand = set()
    to_expand.add(node_to_expand)
    # get turn of a node to be expanded
    turn = next(iter(to_expand)).getTurn()
    # get turn of child node
    cur_turn = getNextTurn(turn)
    # start relative depth counter
    rel_depth = 1

    while True:
        expand_next = set() # set for updated to_expand
        for node in to_expand:
            for i in range(len(node.state)):
                for j in range(len(node.state[i])): # for each cell
                    if node.state[i][j] == 0: # valid successor state
                        # create successor (child)
                        child_state = copy.deepcopy(node.state) 
                        child_state[i][j] = cur_turn 
                        child = Node(child_state, node.getDepth()+1, node, cur_turn, i, j)
                        node.setNext(child)
                        # if not on final level, add nodes to set to be expanded next
                        if rel_depth != depth_to_generate: expand_next.add(child)
                        amt_generated += 1
        if rel_depth == depth_to_generate: break
        to_expand = expand_next
        cur_turn = getNextTurn(cur_turn)
        rel_depth += 1
    return amt_generated


def heuristicCalc(turn, num32X, num32O, num31X, num31O, num22X, num22O, num21X, num21O):
    #heuristic scores are dependent on which player is using them
    if turn == "x":
        return (200 * num32X) - (80 * num32O) + (150 * num31X) - (40 * num31O) + (20 * num22X) - (15 * num22O) + (5 * num21X) - (2 * num21O)
    else:
        return (200 * num32O) - (80 * num32X) + (150 * num31O) - (40 * num31X) + (20 * num22O) - (15 * num22X) + (5 * num21O) - (2 * num21X)


def heuristic(node, turn):
    #set containing all found strings of interest on the board
    found = set()
    #initialize number of strings of interest
    num32X = 0
    num32O = 0
    num31X = 0
    num31O = 0
    num22X = 0
    num22O = 0
    num21X = 0
    num21O = 0
    #loop through all rows of the board
    for i in range(len(node.state)):
        #loop through all columns of the board
        for j in range(len(node.state[i])):
            #if a space has a value in it
            if (node.state[i][j] == "x") or (node.state[i][j] == "o"):
                #find all strings on he board that could be notable
                neighborsList = getNeighbors(node.state, i, j)
                for neighbors in neighborsList:
                    if neighbors not in found:
                        found.add(neighbors)
                        #get the length of the string, which is garunteed to be of certain sizes depending on what was found
                        count = len(neighbors)
                        #variable to store the number of 'x's or 'o's
                        varCount = 0
                        for l in neighbors:
                            if l == "x":
                                varCount += 1
                        if varCount == 0:
                            for l in neighbors:
                                if l == "o":
                                    varCount += 1
                        #if count is of length 15, we must have a string with 5 locations, meaning it's either 0xxx0 or 0ooo0
                        if count == 15:
                            if node.state[i][j] == "x":
                                num32X += 1
                            else:
                                num32O += 1
                        #if count is of length 12, we must have a string with 4 locations, meaning its 0xx0, 0xxx, 0oo0, or 0ooo
                        elif count == 12:
                            #if number of 'x's or 'o's is 2, it must be either 0xx0 or 0oo0
                            if varCount == 2:
                                if node.state[i][j] == "x":
                                    num22X += 1
                                else:
                                    num22O += 1
                            #else it must be 0xxx or 0ooo
                            else:
                                if node.state[i][j] == "x":
                                    num31X += 1
                                else:
                                    num31O += 1
                        #if count is of length 9, we must have a string with 3 locations, meaning its 0xx, 0x0, 0oo, or 0o0
                        elif count == 9:
                            if node.state[i][j] == "x":
                                #we do not care about 0x0, so we check to make sure it's 0xx
                                if(varCount == 2):
                                    num21X += 1
                            else:
                                #we do not care about 0o0, so we check to make sure it's 0oo
                                if(varCount == 2):
                                    num21O += 1
    #calculate the heuristic with the values we just found
    return heuristicCalc(turn, num32X, num32O, num31X, num31O, num22X, num22O, num21X, num21O)


#returns a list of all found strings of characters and their locations
def getNeighbors(state, i, j):
    #figure out whether we're looking for 'x's or 'o's
    currentChar = state[i][j]
    #string to store elements found in the direction of search
    currentString = "" + currentChar + str(i) + str(j) + " "
    #list of all found strings that will be returned
    currentStringList = []
    #boolean values to tell us when to stop searching in a direction
    upStop = False
    downStop = False
    #get up and down string
    for index in range(0, 5):
        if i - index > 0:
            #if the position above is not our current character and we can keep going up, stop going up and if it's 0, attach it
            if (state[i - index - 1][j] != currentChar) and (not upStop):
                upStop = True
                if state[i - index - 1][j] == 0:
                    currentString += "0" + str(i - index - 1) + str(j) + " "
            #if the position was our current character and we can keep going up, attach it and its current position to the currentString
            elif (not upStop) and (state[i - index - 1][j] == currentChar):
                currentString += currentChar + str(i - index - 1) + str(j) + " "
        if i + index < 4:
            #if the position above is not our current character and we can keep going down, stop going up and if it's 0, attach it
            if (state[i + index + 1][j] != currentChar) and (not downStop):
                downStop = True
                if state[i + index + 1][j] == 0:
                    currentString += "0" + str(i + index + 1) + str(j) + " "
            #if the position was our current character and we can keep going down, attach it and its current position to the currentString
            elif (not downStop) and (state[i + index + 1][j] == currentChar):
                currentString += currentChar + str(i + index + 1) + str(j) + " "
    #reordering string to ensure that any line of characters generated will always have the same output
    splitString = currentString.split()
    splitString.sort()
    newString = ""
    for part in splitString:
        newString += str(part)
    currentStringList.append(newString)
    #reset variables
    currentString = "" + currentChar + str(i) + str(j) + " "
    upStop = False
    downStop = False
    #get left and right string
    for index in range(0, 6):
        if j - index > 0:
            #if the position above is not our current character and we can keep going left, stop going up and if it's 0, attach it
            if (state[i][j - index - 1] != currentChar) and (not upStop):
                upStop = True
                if state[i][j - index - 1] == 0:
                    currentString += "0" + str(i) + str(j - index - 1) + " "
            #if the position was our current character and we can keep going left, attach it and its current position to the currentString
            elif (not upStop) and (state[i][j - index - 1] == currentChar):
                currentString += currentChar + str(i) + str(j - index - 1) + " "
        if j + index < 5:
            #if the position above is not our current character and we can keep going right, stop going up and if it's 0, attach it
            if (state[i][j + index + 1] != currentChar) and (not downStop):
                downStop = True
                if state[i][j + index + 1] == 0:
                    currentString += "0" + str(i) + str(j + index + 1) + " "
            #if the position was our current character and we can keep going right, attach it and its current position to the currentString
            elif (not downStop) and (state[i][j + index + 1] == currentChar):
                currentString += currentChar + str(i) + str(j + index + 1) + " "
    #reordering string to ensure that any line of characters generated will always have the same output
    splitString = currentString.split()
    splitString.sort()
    newString = ""
    for part in splitString:
        newString += str(part)
    currentStringList.append(newString)
    #reset variables
    currentString = "" + currentChar + str(i) + str(j) + " "
    upStop = False
    downStop = False
    
    #get top left to bottom right diagonal string
    for index in range(0, 4):
        if (j - index > 0) and (i - index > 0):
            #if the position above is not our current character and we can keep going up and left, stop going up and if it's 0, attach it
            if (state[i - index - 1][j - index - 1] != currentChar) and (not upStop):
                upStop = True
                if state[i - index - 1][j - index - 1] == 0:
                    currentString += "0" + str(i - index - 1) + str(j - index - 1) + " "
            #if the position was our current character and we can keep going up and left, attach it and its current position to the currentString
            elif (not upStop) and (state[i - index - 1][j - index - 1] == currentChar):
                currentString += currentChar + str(i - index - 1) + str(j - index - 1) + " "
        if (j + index < 5) and (i + index < 4):
            #if the position above is not our current character and we can keep going down and right, stop going up and if it's 0, attach it
            if (state[i + index + 1][j + index + 1] != currentChar) and (not downStop):
                downStop = True
                if state[i + index + 1][j + index + 1] == 0:
                    currentString += "0" + str(i + index + 1) + str(j + index + 1) + " "
            #if the position was our current character and we can keep going down and right, attach it and its current position to the currentString
            elif (not downStop) and (state[i + index + 1][j + index + 1] == currentChar):
                currentString += currentChar + str(i + index + 1) + str(j + index + 1) + " "
    #reordering string to ensure that any line of characters generated will always have the same output
    splitString = currentString.split()
    splitString.sort()
    newString = ""
    for part in splitString:
        newString += str(part)
    currentStringList.append(newString)
    #reset variables
    currentString = "" + currentChar + str(i) + str(j) + " "
    upStop = False
    downStop = False

    #get top right to bottom left diagonal string
    for index in range(0, 4):
        if (j + index < 5) and (i - index > 0):
            #if the position above is not our current character and we can keep going up and right, stop going up and if it's 0, attach it
            if (state[i - index - 1][j + index + 1] != currentChar) and (not upStop):
                upStop = True
                if state[i - index - 1][j + index + 1] == 0:
                    currentString += "0" + str(i - index - 1) + str(j + index + 1) + " "
            #if the position was our current character and we can keep going up and right, attach it and its current position to the currentString
            elif (not upStop) and (state[i - index - 1][j + index + 1] == currentChar):
                currentString += currentChar + str(i - index - 1) + str(j + index + 1) + " "
        if (j - index > 0) and (i + index < 4):
            #if the position above is not our current character and we can keep going down and left, stop going up and if it's 0, attach it
            if (state[i + index + 1][j - index - 1] != currentChar) and (not downStop):
                downStop = True
                if state[i + index + 1][j - index - 1] == 0:
                    currentString += "0" + str(i + index + 1) + str(j - index - 1) + " "
            #if the position was our current character and we can keep going down and left, attach it and its current position to the currentString
            elif (not downStop) and (state[i + index + 1][j - index - 1] == currentChar):
                currentString += currentChar + str(i + index + 1) + str(j - index - 1) + " "
    #reordering string to ensure that any line of characters generated will always have the same output
    splitString = currentString.split()
    splitString.sort()
    newString = ""
    for part in splitString:
        newString += str(part)
    currentStringList.append(newString)
    #return list of found strings
    return currentStringList


# recursive function for checking 4 in a row
def terminalTestCell(node, i, j, player, prev_move = None, count = 1):
    if node.state[i][j] != player: return False
    if count == 4: return True
    if prev_move != None: moves = [prev_move]
    else: 
        moves = [(1,-1), (1,0), (1,1), (0,1)]
        if j < 3: moves.remove((1,-1))
        else: 
            try: moves.remove((1,1))
            except: pass
            moves.remove((0,1))
        if i > 1: 
            try: moves.remove((1,-1))
            except: pass
            try: moves.remove((1,1))
            except: pass
            moves.remove((1,0))
    for move in moves: 
        pos_after = (i+move[0], j+move[1])
        # if pos_after[0] >= len(node.state) or pos_after[1] >= len(node.state[0]): continue
        result = terminalTestCell(node, pos_after[0], pos_after[1], player, move, count+1)
        if result: return result
    return False
    
    # optimization: keep track of ones that I already visited
    # keep track of rows and columns to still check
    # once you've checked a row or column, that row or column is dead
    # keep track of moves based on which directions I've cleared
    # true or false for all cells


# checks relevant cells for start to a 4 in a row
def terminalTest(node):
    points_di = {"x": 1000, "o": -1000} # point dictionary
    for i in range(len(node.state)): 
        for j in range(len(node.state[i])):
            if node.state[i][j] == 0:
                # cells_filled = False
                continue
            for player in ["x", "o"]:
                if node.state[i][j] == player: 
                    result = terminalTestCell(node, i, j, player)
                    if result: return points_di.get(player) # if 4 in a row found
                    # if result[1]: cells_filled = False # if empty cell found
    if "0" not in str(node.state): return 0 # all cells are filled
    return None


# minimax for a specified height, adopted from Sebastian Lague
def minimax(node, rel_height, maximizingPlayer):
    if rel_height == 0 or terminalTest(node) != None: 
        if maximizingPlayer: cur_turn = "x"
        else: cur_turn = "o"
        node.setHeuristic(heuristic(node, cur_turn))
        return node.getHeuristic()

    if maximizingPlayer:
        maxEval = -sys.maxsize
        for child in node.getNext():
            eval = minimax(child, rel_height-1, False)
            maxEval = max(maxEval, eval)
        node.setHeuristic(maxEval)
        return maxEval
    else: 
        minEval = sys.maxsize
        for child in node.getNext():
            eval = minimax(child, rel_height-1, True)
            minEval = min(minEval, eval)
        node.setHeuristic(minEval)
        return minEval


def printState(node):
    for row in node.state: 
        for col in row: print(col, end=' ')
        print("\n", end='')


def printInfo(start_time, node, amt_generated):
    print("--- %s seconds ---" % (time.time() - start_time))
    printState(node)
    print("g:", amt_generated)
    print("*************")


# minimax wrapper function for running minimax until a player wins
def minimaxWrapper(to_begin, depth_generated, maximizingPlayer):
    start_time = time.time()

    if maximizingPlayer: rel_height = 2
    else: rel_height = 4

    levels_needed = rel_height - depth_generated
    amt_generated = 0
    if levels_needed > 0: 
        amt_generated = generateTree(to_begin, levels_needed)

    result = minimax(to_begin, rel_height, maximizingPlayer)
    # advance to_begin
    children_to_tiebreak = []
    for child in to_begin.getNext():
        if child.getHeuristic() == result: children_to_tiebreak.append(child)
    # see if there are children to tiebreak
    if len(children_to_tiebreak) == 1: to_begin = children_to_tiebreak[0]
    elif len(children_to_tiebreak) > 1: # multiple children to tiebreak
        # get min col child
        min_col_i = [0]
        for i in range(1, len(children_to_tiebreak)):
            if children_to_tiebreak[i].col < children_to_tiebreak[min_col_i[0]].col: min_col_i = [i] 
            elif children_to_tiebreak[i].col == children_to_tiebreak[min_col_i[0]].col: min_col_i.append(i)
        if len(min_col_i) == 1: to_begin = children_to_tiebreak[min_col_i[0]]
        else: # min cols the same so multiple children remaining to tiebreak
            # get min row child
            nodes_to_still_tiebreak = []
            for index in min_col_i: nodes_to_still_tiebreak.append(children_to_tiebreak[index])
            min_row_i = [0]
            for i in range(1, len(nodes_to_still_tiebreak)):
                if nodes_to_still_tiebreak[i].row < nodes_to_still_tiebreak[min_row_i[0]].col: min_row_i = [i] 
                elif nodes_to_still_tiebreak[i].row == nodes_to_still_tiebreak[min_row_i[0]].col: min_row_i.append(i)
            to_begin = nodes_to_still_tiebreak[min_row_i[0]]

    printInfo(start_time, to_begin, amt_generated)

    # check if game is done
    # print("TURN MADE:")
    terminal_result = terminalTest(to_begin)
    if terminal_result != None: 
        print("FINAL STATE:")
        printState(to_begin)
        return terminal_result
    
    # if not, recurse to the next player
    return minimaxWrapper(to_begin, rel_height-1, not maximizingPlayer)
    
    # run minimax decision for to_begin for certain depth
    # after, set to_begin = to_expand[0]
    # make recursive call to minimax so that more tree can be generated
    # if terminated, return -1000 if player o won, 0 for tie, and 1000 if player x won


if __name__ == "__main__":
    # 2D array state layout
    state = [
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, "o", "x", 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0]]

    # construct root node
    root = Node(state, 0, None, "o", 2, 2)

    #uncomment all this
    # hold node to begin at
    to_begin = root
    
    # create set of nodes to be expanded and add root
    to_expand = set()
    to_expand.add(root)
    result = minimaxWrapper(to_begin, 0, False)
    print("RESULT =", result)




