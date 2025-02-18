class Player:
    def __init__(self, id):
        self.id = id

        self.stack = 0
        self.hand_count = 0
        self.vpip_count = 0
        self.pfr_count = 0
        self.three_bet_count = 0
        self.c_bet_count = 0

    def update_stack(self, stack):
        self.stack = stack

    def increment_hand_count(self):
        self.hand_count += 1

    def increment_vpip_count(self):
        self.vpip_count += 1

    def increment_pfr_count(self):
        self.pfr_count += 1

    def increment_three_bet_count(self):
        self.three_bet_count += 1

    def increment_c_bet_count(self):
        self.c_bet_count += 1
