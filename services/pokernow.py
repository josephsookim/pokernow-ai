import json
import websocket
import ssl
import time
import threading
import requests

WEB_SOCKET_URL_PATTERN = 'wss://www.pokernow.club/socket.io/?gameID=${game_id}&EIO=3&transport=websocket'


class PokerNowClient:
    def __init__(self, game_id, cookies):
        self.game_id = game_id
        self.cookies = cookies  # Use both npt and apt cookies
        self.ping_interval = 20000
        self.player_id = None
        self.ws = None

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
        if raw_message.startswith('0'):
            message = raw_message[1:]
            json_obj = json.loads(message)
            self.ping_interval = json_obj.get('pingInterval', 20000)
            self.ping()

        elif raw_message.startswith('42'):
            message = raw_message[2:]
            json_obj = json.loads(message)
            print(json_obj)
            print('=============================')

            if 'registered' in json_obj[0]:
                self.player_id = json_obj[1]['currentPlayer']['id']

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

    def run(self):
        '''Keep the client running.'''
        while True:
            time.sleep(1)
