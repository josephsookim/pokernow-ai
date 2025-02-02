class GameState:
    def __init__(self):
        self.seats = dict()
        self.player_in_turn = None

    def update_seats(self, seats):
        self.seats = seats

    def update_player_in_turn(self, player_in_turn):
        self.player_in_turn = player_in_turn
        print(self.seats, self.player_in_turn)
