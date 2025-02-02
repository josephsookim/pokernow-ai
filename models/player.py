class Player:
    def __init__(self, id, stack):
        self.id = id
        self.stack = stack

    def update_stack(self, stack):
        self.stack = stack
