import json
import websocket
import ssl
import time
import threading
import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Access the values of npt and apt keys
npt_key = os.getenv('npt')
apt_key = os.getenv('apt')

WEB_SOCKET_URL_PATTERN = 'wss://www.pokernow.club/socket.io/?gameID=${game_id}&EIO=3&transport=websocket'
TAKE_SEAT_URL = 'https://www.pokernow.club/games/${game_id}/request_ingress'


class PokernowClient:
    def __init__(self, game_id, cookies, name='BOT_' + str(time.time())[-8:], initial_stack=2000, seat=9):
        self.game_id = game_id
        self.cookies = cookies  # Use both npt and apt cookies
        self.ping_interval = 20000
        self.self_player_id = None
        self.ws = None
        self.name = name
        self.initial_stack = initial_stack
        self.seat = seat

        # Headers with the provided cookies
        self.headers = {
            'Cookie': self.cookies,
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'no-cache',
            'Connection': 'Upgrade',
            'Host': 'www.pokernow.club',
            'Origin': 'https://www.pokernow.club',
            'Pragma': 'no-cache',
            'Sec-WebSocket-Extensions': 'permessage-deflate; client_max_window_bits',
            'Sec-WebSocket-Version': '13',
            'Upgrade': 'websocket',
        }

    def ping(self):
        '''Send periodic pings to keep the WebSocket connection alive.'''
        try:
            if self.ws:
                self.ws.send('2')
                threading.Timer(self.ping_interval / 1000, self.ping).start()
        except Exception as e:
            print(f'Ping failed: {e}')

    def listen_on_web_socket(self):
        '''Listen for incoming WebSocket messages and handle them.'''
        while True:
            try:
                result = self.ws.recv()
                self.handle_message(result)
            except websocket.WebSocketConnectionClosedException:
                print('WebSocket connection lost. Reconnecting...')
                self.connect_room(self.game_id)
            except Exception as e:
                print(f'Error in WebSocket: {e}')
                time.sleep(5)

    def handle_message(self, raw_message):
        '''Process received WebSocket messages.'''
        print(raw_message)
        if raw_message.startswith('0'):
            message = raw_message[1:]
            json_obj = json.loads(message)
            # print(json_obj)
            self.self_player_id = json_obj.get('sid')
            self.ping_interval = json_obj.get('pingInterval', 20000)
            self.ping()
            # print(f'Self player ID: {self.self_player_id}')

    def connect_room(self, game_id):
        '''Establish a WebSocket connection to the PokerNow game.'''
        self.game_id = game_id
        url = WEB_SOCKET_URL_PATTERN.replace('${game_id}', game_id)

        try:
            self.ws = websocket.create_connection(
                url, header=self.headers, sslopt={'cert_reqs': ssl.CERT_NONE}
            )
            threading.Thread(target=self.listen_on_web_socket,
                             daemon=True).start()
            print('Connected to room successfully!')
        except Exception as e:
            print(f'Failed to connect to WebSocket: {e}')

    def take_seat(self):
        '''Send a request to take a seat in the PokerNow game.'''
        url = TAKE_SEAT_URL.replace('${game_id}', self.game_id)
        data = {
            'allowSpectator': False,
            'playerName': self.name,
            'stack': self.initial_stack,
            'seat': self.seat,
        }

        try:
            response = requests.post(url, json=data, headers=self.headers)
            print(response.text)
            print(f'Requested to take seat {self.seat} successfully!')
        except Exception as e:
            print(f'Failed to take seat: {e}')

    def run(self):
        '''Keep the client running.'''
        while True:
            time.sleep(1)


if __name__ == '__main__':
    # Replace with your actual game ID and cookies
    GAME_ID = 'pglgVYsmd4xjGX_eTgvIKbFjZ'
    COOKIES = (
        f'npt={npt_key}; '
        f'apt={apt_key}; '
    )

    client = PokernowClient(game_id=GAME_ID, cookies=COOKIES)
    client.connect_room(GAME_ID)
    client.run()
