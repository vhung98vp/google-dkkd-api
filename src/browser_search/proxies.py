from dotenv import load_dotenv
import os
import random

def get_proxy():
    # Get env file
    load_dotenv()
    proxies = os.getenv('PROXIES')
    return random.choice(proxies.split(",")) if proxies else None
