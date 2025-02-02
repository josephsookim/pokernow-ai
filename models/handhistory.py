class HandHistory:
    def __init__(self):
        self.history = []

    def reset(self):
        self.history = []

    def add_action(self, action):
        self.history.append(action)

    def get_history(self):
        return '\n'.join(self.history)
