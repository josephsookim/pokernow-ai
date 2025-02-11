import json

# Models
from models.gamestate import GameState

# Helper Functions
from services.helpers import *


class PokerNowProcessor:
    def __init__(self):
        # Player Information
        self.player_id = None

        # Game State
        self.game_state = GameState()

    def process_message(self, raw_message):
        if raw_message.startswith('42'):
            message = raw_message[2:]
            json_obj = json.loads(message)

            if 'registered' in json_obj[0]:
                self.player_id = json_obj[1]['currentPlayer']['id']
                self.game_state.update_seats(
                    get_seats(json_obj[1]['gameState']))

            elif 'gC' in json_obj[0]:
                print(json_obj[1])
                self.update_game_state(json_obj[1])

                if is_hand_over(json_obj[1]):
                    print('Hand over')

            print('=============================')

    def update_game_state(self, game_state):
        # If seats have changed, update the seats dictionary

        if 'seats' in game_state:
            self.game_state.update_seats(get_seats(game_state))

        # If the player in turn has changed, update the player in turn
        if 'pITT' in game_state and game_state['pITT'] is not None:
            self.game_state.update_player_in_turn(
                get_player_in_turn(game_state))
