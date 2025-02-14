from dotenv import load_dotenv
import os
import random
import time
import requests
import re
from ..logger_config import get_logger

logger = get_logger(__name__)


def get_proxy():
    # Get env file
    load_dotenv()
    proxy_server = os.getenv('PROXY_SERVER', '')
    match = re.match(r"(http|https)://([^/:]+)", proxy_server)
    if match:
        try:
            logger.info(f"Getting proxy list from {proxy_server}...")
            response = requests.get(f"{proxy_server}/proxy_list")
            time.sleep(2)
            if response.status_code == 200:
                proxy_list = response.json()
                if len(proxy_list) > 0:
                    port = random.choice(proxy_list).get("proxy_port")
                    protocol, ip = match.groups()
                    proxy_string = f"{protocol}://{ip}:{port}"
                    logger.info(f"Get proxy string config: {proxy_string}")
                    return proxy_string
        except Exception as e:
            logger.error("Error, Fail to get proxy: ", e)

    return None

def reset_proxy(current_proxy):
    load_dotenv()
    proxy_server = os.getenv('PROXY_SERVER')
    if current_proxy and proxy_server:
        try:
            port = current_proxy.split(":")[-1]
            response = requests.get(f"{proxy_server}/reset?proxy={port}")
            time.sleep(5)
            if response.status_code == 200:
                if response.json().get("status"):
                    logger.info(f"Proxy port {port} successfully reset...")
                    return current_proxy
                else:
                    logger.info(f"Proxy port {port} not found!")
            else:
                logger.error(f"Proxy port {port} reset fail with error: {response.text}")
        except Exception as e:
            logger.error("Error, Fail to reset proxy: ", e)
    
    logger.error(f"Trying to get a new proxy...")
    return get_proxy()