import copy, time

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
        self.next = None
        self.turn = turn
        self.heuristic = None
    
    def setNext(self, next):
        self.next = next

    def setHeuristic(self, heuristic):
        self.heuristic = heuristic

    def getTurn(self): return self.turn

    def getDepth(self): return self.depth


def getNextTurn(turn):
    if turn == "x": return "o"
    return "x"


def generateTree(to_expand, depth_to_generate):
    if depth_to_generate < 1: return
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
                        expand_next.add(node)
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




def minimax(to_begin, to_expand):
    # calculate search depth
    search_depth = to_expand[0].getDepth - to_begin[0].getDepth 
    depth_needed = 0
    turn = to_begin[0].getTurn()
    # check if expansion is needed
    if turn == "o": 
        depth_needed = search_depth - 4
    else: 
        depth_needed = search_depth - 2
    if search_depth < 0: generateTree(to_expand, abs(depth_needed))
    
    # for node in to_begin run minimax decision for certain depth
    # after, set to_begin = to_expand
    # make recursive call to minimax so that more tree can be generated


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

    # create set of beginning nodes for minimax algorithm
    to_begin = set()
    to_begin.add(root)
    
    # create set of nodes to be expanded and add root
    # NOT A SET, JUST ONE NODE
    to_expand = set()
    to_expand.add(root)

    generateTree(to_expand, 4)

    minimax(to_begin)







