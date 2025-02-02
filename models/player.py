class Player:
    def __init__(self, id, stack):
        self.id = id
        self.stack = stack
        self.hand_count = 0
        self.vpip = 0
        self.pfr = 0
        self.three_bet = 0
        self.c_bet = 0

    def update_stack(self, stack):
        self.stack = stack
