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
    
    def setNext(self, next):
        self.next = next


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






