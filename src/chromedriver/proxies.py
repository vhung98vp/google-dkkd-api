from dotenv import load_dotenv
import os
import random
import time
import requests
from ..logger_config import get_logger

logger = get_logger(__name__)


def get_proxy():
    # Get env file
    load_dotenv()
    proxy_server = os.getenv('PROXY_SERVER')
    if proxy_server:
        try:
            logger.info(f"Getting proxy list from {proxy_server}...")
            response = requests.get(f"{proxy_server}/proxy_list")
            time.sleep(2)
            if response.status_code == 200:
                proxy_list = response.json()
                if len(proxy_list) > 0:
                    port = random.choice(proxy_list).get("proxy_port")
                    logger.info(f"Get proxy string config: {proxy_server}:{port}")
                    return f"{proxy_server}:{port}"
        except Exception as e:
            logger.error("Error, Fail to get proxy: ", e)

    return None

def reset_proxy(current_proxy):
    if current_proxy:
        try:
            proxy_server, port = current_proxy.split(":")
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
    
    return None