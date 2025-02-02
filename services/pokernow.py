import json

# Helper Functions
from services.helpers import *


class PokerNowProcessor:
    def __init__(self):
        # Player Information
        self.player_id = None

        # Game State
        self.seats = dict()
        self.player_in_turn = None

    def process_message(self, raw_message):
        # Game Information
        if raw_message.startswith('42'):
            message = raw_message[2:]
            json_obj = json.loads(message)
            print('=============================')

            if 'registered' in json_obj[0]:
                self.player_id = json_obj[1]['currentPlayer']['id']
                self.seats = get_seats(json_obj[1]['gameState'])

            else:
                self.update_game_state(json_obj[1])

    def update_game_state(self, game_state):
        # If seats have changed, update the seats dictionary
        if 'seats' in game_state:
            self.seats = get_seats(game_state)

        # If the player in turn has changed, update the player in turn
        if 'pITT' in game_state and game_state['pITT'] is not None:
            self.player_in_turn = get_player_in_turn(game_state)
