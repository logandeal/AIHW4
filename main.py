# 2d array state
# class node
# successors (valid only)
# hold path in a set
# minimax-decision (heuristic calculation) -> one looks 4 ahead, one looks 2 ahead
    # max-value
    # min-value
# terminal-test

class Node:
    def __init__(self, state, depth):
        self.state = state
        self.depth = depth
        self.next = None
    
    def setNext(self, next):
        self.next = next

def minimaxDecision():
    pass

if __name__ == "__main__":
    state = [
        [0, 0, 0, 0, 0, 0],
        [0, "O", "X", 0, "X", 0],
        [0, "O", "O", "X", 0, 0],
        ["O", "X", "X", "O", 0, 0],
        [0, "X", 0, 0, 0, 0]]

    root = Node(state, 0)






