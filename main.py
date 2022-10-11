import copy, time

# 2d array state
# class node
# successors (valid only)
# hold path in a set, maybe hold path of next nodes to be expanded
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


def minimaxDecision():
    pass


def getNextTurn(turn):
    if turn == "x": return "o"
    return "x"


def generateTree(to_expand, depth, turn):
    rel_depth = 1
    cur_turn = getNextTurn(turn)

    while True:
        for node in to_expand:
            for i in range(5):
                for j in range(6):
                    if node[i][j] == 0:
                        child_state = copy.deepcopy(node.state)
                        child_state[i][j] = cur_turn
                        child = Node(child_state, rel_depth, node, getNextTurn(cur_turn))
                        node.setNext(child)
        if rel_depth == depth: break
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



if __name__ == "__main__":
    # 2D array state layout
    state = [
        [0, 0, 0, 0, 0, 0],
        [0, "o", "x", 0, "x", 0],
        [0, "o", "o", "x", 0, 0],
        ["o", "x", "x", "o", 0, 0],
        [0, "x", 0, 0, 0, 0]]

    # construct root node
    root = Node(state, 0, None, "x")
    
    # create set of nodes to be expanded and add root
    to_expand = set()
    to_expand.add(root)

    generateTree(to_expand, 4)






