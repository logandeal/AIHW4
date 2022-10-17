import copy, time, sys

class Node:
    def __init__(self, state, depth, prev, turn):
        self.state = state
        self.depth = depth
        self.prev = prev
        self.next = set()
        self.turn = turn
        self.heuristic = None
    
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
                        # give node heuristic value for the last depth
                        child = Node(child_state, node.getDepth()+1, node, cur_turn)
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
    if turn == "x":
        return (200 * num32X) - (80 * num32O) + (150 * num31X) - (40 * num31O) + (20 * num22X) - (15 * num22O) + (5 * num21X) - (2 * num21O)
    else:
        return (200 * num32O) - (80 * num32X) + (150 * num31O) - (40 * num31X) + (20 * num22O) - (15 * num22X) + (5 * num21O) - (2 * num21X)


def heuristic(node, turn):
    found = set()
    num32X = 0
    num32O = 0
    num31X = 0
    num31O = 0
    num22X = 0
    num22O = 0
    num21X = 0
    num21O = 0
    for i in range(len(node.state)):
        for j in range(len(node.state[i])):
            if (node.state[i][j] == "x") or (node.state[i][j] == "o"):
                neighborsList = getNeighbors(node.state, i, j)
                for neighbors in neighborsList:
                    if neighbors not in found:
                        found.add(neighbors)
                        count = len(neighbors)
                        if count == 15:
                            if node.state[i][j] == "x":
                                num32X += 1
                            else:
                                num32O += 1
                        elif count == 12:
                            zeroCount = 0
                            for i in neighbors:
                                if i == '0':
                                    zeroCount += 1
                            if zeroCount == 2:
                                if node.state[i][j] == "x":
                                    num22X += 1
                                else:
                                    num22O += 1
                            else:
                                if node.state[i][j] == "x":
                                    num31X += 1
                                else:
                                    num31O += 1
                        elif count == 9:
                            if node.state[i][j] == "x":
                                num21X += 1
                            else:
                                num21O += 1
    return heuristicCalc(turn, num32X, num32O, num31X, num31O, num22X, num22O, num21X, num21O)


#returns a list of all found strings of characters
def getNeighbors(state, i, j):
    currentChar = state[i][j]
    currentString = "" + currentChar + str(i) + str(j)
    currentStringList = []
    upStop = False
    downStop = False
    #get up and down string
    for index in range(0, 5):
        if i - index > 0:
            if state[i - index - 1][j] != currentChar:
                upStop = True
                if state[i - index - 1][j] == 0:
                    currentString += "0" + str(i - index - 1) + str(j) + " "
            elif (not upStop) and (state[i - index - 1][j] == currentChar):
                currentString += currentChar + str(i - index - 1) + str(j) + " "
        if i + index < 4:
            if state[i + index + 1][j] != currentChar:
                downStop = True
                if state[i + index + 1][j] == 0:
                    currentString += "0" + str(i + index + 1) + str(j) + " "
            elif (not downStop) and (state[i + index + 1][j] == currentChar):
                currentString += currentChar + str(i + index + 1) + str(j) + " "
    #reordering string to ensure that any line of characters generated will always have the same output
    splitString = [sub.split() for sub in currentString]
    splitString.sort()
    newString = ""
    for part in splitString:
        newString += str(part)
    currentStringList.append(newString)
    currentString = "" + currentChar + str(i) + str(j)
    upStop = False
    downStop = False
    #get left and right string
    for index in range(0, 6):
        if j - index > 0:
            if state[i][j - index - 1] != currentChar:
                upStop = True
                if state[i][j - index - 1] == 0:
                    currentString += "0" + str(i) + str(j - index - 1) + " "
            elif (not upStop) and (state[i][j - index - 1] == currentChar):
                currentString += currentChar + str(i) + str(j - index - 1) + " "
        if j + index < 5:
            if state[i][j + index + 1] != currentChar:
                downStop = True
                if state[i][j + index + 1] == 0:
                    currentString += "0" + str(i) + str(j + index + 1) + " "
            elif (not downStop) and (state[i][j + index + 1] == currentChar):
                currentString += currentChar + str(i) + str(j + index + 1) + " "
    #reordering string to ensure that any line of characters generated will always have the same output
    splitString = [sub.split() for sub in currentString]
    splitString.sort()
    newString = ""
    for part in splitString:
        newString += str(part)
    currentStringList.append(newString)
    currentString = "" + currentChar + str(i) + str(j)
    upStop = False
    downStop = False
    
    #get top left to bottom right diagonal string
    for index in range(0, 4):
        if (j - index > 0) and (i - index > 0):
            if state[i - index - 1][j - index - 1] != currentChar:
                upStop = True
                if state[i - index - 1][j - index - 1] == 0:
                    currentString += "0" + str(i - index - 1) + str(j - index - 1) + " "
            elif (not upStop) and (state[i - index - 1][j - index - 1] == currentChar):
                currentString += currentChar + str(i - index - 1) + str(j - index - 1) + " "
        if (j + index < 5) and (i + index < 4):
            if state[i + index + 1][j + index + 1] != currentChar:
                downStop = True
                if state[i + index + 1][j + index + 1] == 0:
                    currentString += "0" + str(i + index + 1) + str(j + index + 1) + " "
            elif (not downStop) and (state[i + index + 1][j + index + 1] == currentChar):
                currentString += currentChar + str(i + index + 1) + str(j + index + 1) + " "
    #reordering string to ensure that any line of characters generated will always have the same output
    splitString = [sub.split() for sub in currentString]
    splitString.sort()
    newString = ""
    for part in splitString:
        newString += str(part)
    currentStringList.append(newString)
    currentString = "" + currentChar + str(i) + str(j)
    upStop = False
    downStop = False

    #get top right to bottom left diagonal string
    for index in range(0, 4):
        if (j + index < 5) and (i - index > 0):
            if state[i - index - 1][j + index + 1] != currentChar:
                upStop = True
                if state[i - index - 1][j + index + 1] == 0:
                    currentString += "0" + str(i - index - 1) + str(j + index + 1) + " "
            elif (not upStop) and (state[i - index - 1][j + index + 1] == currentChar):
                currentString += currentChar + str(i - index - 1) + str(j + index + 1) + " "
        if (j - index > 0) and (i + index < 4):
            if state[i + index + 1][j - index - 1] != currentChar:
                downStop = True
                if state[i + index + 1][j - index - 1] == 0:
                    currentString += "0" + str(i + index + 1) + str(j - index - 1) + " "
            elif (not downStop) and (state[i + index + 1][j - index - 1] == currentChar):
                currentString += currentChar + str(i + index + 1) + str(j - index - 1) + " "
    #reordering string to ensure that any line of characters generated will always have the same output
    splitString = [sub.split() for sub in currentString]
    splitString.sort()
    newString = ""
    for part in splitString:
        newString += str(part)
    currentStringList.append(newString)
    return currentStringList


# recursive function for checking 4 in a row
# return value: [4 in a row found or not, cell empty]
def terminalTestCell(node, i, j, player, prev_move = None, count = 1):
    if node.state[i][j] == 0: return (False, True)
    if node.state[i][j] != player: return (False, False)
    if count == 4: return (True, False)
    if prev_move != None: moves = [prev_move]
    else: 
        moves = [(1,-1), (1,0), (1,1), (0,1)]
        if count == 1 and j < 3: moves.pop(0)
    for move in moves: 
        pos_after = (i+move[0], j+move[1])
        return terminalTestCell(node, pos_after[0], pos_after[1], player, move, count+1)
    
    # optimization: keep track of ones that I already visited
    # keep track of rows and columns to still check
    # once you've checked a row or column, that row or column is dead
    # keep track of moves based on which directions I've cleared
    # true or false for all cells


# checks relevant cells for start to a 4 in a row
def terminalTest(node):
    cells_filled = True
    points_di = {"x": 1000, "o": -1000} # point dictionary
    for i in range(len(node.state)-3): 
        for j in range(len(node.state[i])-3):
            if node.state[i][j] == 0:
                cells_filled = False
                continue
            for player in ["x", "o"]:
                if node.state[i][j] == player: 
                    result = terminalTestCell(node, i, j, player)
                    if result[0]: return points_di.get(player) # if 4 in a row found
                    if result[1]: cells_filled = False # if empty cell found
    if cells_filled: return 0
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


def printInfo(start_time, node, amt_generated):
    print("--- %s seconds ---" % (time.time() - start_time))
    for row in node.state: print(row)
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
    for child in to_begin.getNext():
        if child.getHeuristic() == result:
            to_begin = child
            break

    printInfo(start_time, to_begin, amt_generated)

    # check if game is done
    terminal_result = terminalTest(to_begin)
    if terminal_result != None: return terminal_result
    
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
        [0, 0, 0, "x", 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0]]

    # construct root node
    root = Node(state, 0, None, "x")

    # hold node to begin at
    to_begin = root
    
    # create set of nodes to be expanded and add root
    to_expand = set()
    to_expand.add(root)

    result = minimaxWrapper(to_begin, 0, True)
    print("RESULT =", result)




