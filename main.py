from services.pokernow import PokerNowProcessor
from services.websocket import WebSocketClient
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Access the values of npt and apt keys
npt_key = os.getenv('npt')
apt_key = os.getenv('apt')

if __name__ == '__main__':
    # Access the values of npt and apt keys
    npt_key = os.getenv('npt')
    apt_key = os.getenv('apt')

    GAME_ID = 'pglWZjE5GYa11MdbdtRxgHaj3'
    COOKIES = (
        f'npt={npt_key}; '
        f'apt={apt_key}; '
    )

    print(apt_key, npt_key)
    processor = PokerNowProcessor()

    client = WebSocketClient(
        game_id=GAME_ID, cookies=COOKIES, message_handler=processor.process_message)
    client.connect_room(GAME_ID)
    client.run()
