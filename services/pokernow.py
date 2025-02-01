import json

# Helper Functions
from services.helpers import *


class PokerNowProcessor:
    def __init__(self):
        # Players Information
        self.player_id = None
        self.seats = dict()

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
                if 'seats' in json_obj[1]:
                    self.seats = get_seats(json_obj[1])

                if 'pITT' in json_obj[1] and json_obj[1]['pITT'] is not None:
                    print(get_player_in_turn(json_obj[1]))
