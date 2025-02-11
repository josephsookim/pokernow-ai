def get_seats(game_state):
    seats = dict()

    for seat in game_state['seats']:
        seat_number, player_id = seat[0], seat[1]
        seats[seat_number] = player_id

    return seats


def get_player_in_turn(game_state):
    return game_state['pITT']


def is_hand_over(game_state):
    return 'gameResult' in game_state and game_state['gameResult'] != '<D>'
