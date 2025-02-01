from services.pokernow import PokerNowClient
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

    GAME_ID = 'pglCEu6SWiAfNg59eVkmL-J06'
    COOKIES = (
        f'npt={npt_key}; '
        f'apt={apt_key}; '
    )

    print(apt_key, npt_key)

    client = PokerNowClient(game_id=GAME_ID, cookies=COOKIES)
    client.connect_room(GAME_ID)
    client.run()
