from models.player import Player


class GameState:
    def __init__(self):
        self.players = dict()
        self.seats = dict()
        self.player_in_turn = None

    def update_seats(self, seats):
        self.seats = seats

        # Add new players to the players dictionary
        for player_id in self.seats.values():
            if player_id not in self.players:
                self.players[player_id] = Player(player_id)

    def update_player_in_turn(self, player_in_turn):
        self.player_in_turn = player_in_turn

        print(self.seats, self.player_in_turn)
