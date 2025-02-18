class HandHistory:
    def __init__(self):
        self.history = []

    def __str__(self):
        return '\n'.join(self.history)

    def reset(self):
        self.history = []

    def add_action(self, action):
        self.history.append(action)
