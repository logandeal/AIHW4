import copy, time, sys

# 2d array state
# class node
# successors (valid only)
# minimax-decision (heuristic calculation) -> one looks 4 ahead, one looks 2 ahead
    # max-value
    # min-value
# terminal-test

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


def generateTree(node_to_expand, depth_to_generate):
    if depth_to_generate < 1: return
    to_expand = set()
    to_expand.add(node_to_expand)
    # get turn of a node to be expanded
    turn = to_expand[0].getTurn()
    # get turn of child node
    cur_turn = getNextTurn(turn)
    # start relative depth counter
    rel_depth = 1

    while True:
        expand_next = set() # set for updated to_expand
        for node in to_expand:
            for i in range(5):
                for j in range(6): # for each cell
                    if node[i][j] == 0: # valid successor state
                        # create successor (child)
                        child_state = copy.deepcopy(node.state) 
                        child_state[i][j] = cur_turn 
                        # give node heuristic value for the last depth
                        child = Node(child_state, node.getDepth()+1, node, cur_turn)
                        node.setNext(child)
                        # if on final level, set heuristics so that minimax can be performed 
                        if rel_depth == depth_to_generate: child.setHeuristic(heuristic(child, cur_turn))
                        else: expand_next.add(child)
        if rel_depth == depth_to_generate: break
        to_expand = expand_next
        cur_turn = getNextTurn(cur_turn)
        rel_depth += 1


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
    for i in node.state:
        for j in node.state[i]:
            if (node.state[i][j] == "x") or (node.state[i][j] == "o"):
                neighbors = getNeighbors(node.state, i, j)
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


#returns a tuple or set containing found string of same turn type
def getNeighbors(state, i, j):
    currentChar = state[i][j]
    if i > 0:
        if state[i - 1][j] == currentChar:
            return 0


def terminalTestCell(node, row, col, player, count):
    if node.state[row][col] != player: return False
    if count == 4: return True
    moves = [(1,-1), (1,0), (1,1), (0,1)]
    for move in moves: 
        terminalTestCell(node, row+move[0], col+move[1], player, count+1)

def terminalTest(node):
    points_di = {"x": 1000, "o": -1000}
    for i in range(len(node.state)-3): 
        for j in range(len(node.state[i])-3):
            for player in ["x", "o"]:
                if node.state[i][j] == player: 
                    if terminalTestCell(node, i, j, player, 1): return points_di.get(player)
    return -1


def minimax(node, rel_height, maximizingPlayer):
    if rel_height == 0 or terminalTest(node) != -1: return node.getHeuristic()

    if maximizingPlayer:
        maxEval = -sys.maxsize
        for child in node.getNext():
            eval = minimax(child, rel_height-1, False)
            maxEval = max(maxEval, eval)
        return maxEval
    else: 
        minEval = sys.maxsize
        for child in node.getNext():
            eval = minimax(child, rel_height-1, True)
            minEval = min(minEval, eval)
        return minEval


def minimaxWrapper(to_begin, depth_generated, maximizingPlayer):
    if maximizingPlayer:
        rel_height = 2
        maximizingPlayer = True
    else:
        rel_height = 4
        maximizingPlayer = False

    generateTree(to_begin, rel_height - depth_generated)
    result = minimax(to_begin, rel_height, maximizingPlayer)
    
    for child in to_begin.getNext():
        if child.getHeuristic() == result:
            to_begin = child
            break

    terminal_result = terminalTest(to_begin)
    if terminal_result != -1: return terminal_result
    
    minimaxWrapper(to_begin, rel_height-1, not maximizingPlayer)
    
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
    # NOT A SET, JUST ONE NODE
    to_expand = set()
    to_expand.add(root)

    generateTree(to_expand, 4)

    result = minimaxWrapper(to_begin, to_expand, 0)







