
class SearchNode:
    def __init__(self, state, parent):
        self.state = state
        self.parent = parent
        if parent:
            self.initial = parent.initial
        else:
            self.initial = state

    def __str__(self):
        return "<-(" + str(self.state) + "," + str(self.parent) + ") "

    def __lt__(self, other):
        return -1
