from dotenv import load_dotenv
import os
from queue import Queue
from threading import Thread
from .chromedriver import get_driver, reset_driver
from .proxies import get_proxy, reset_proxy
from ..logger_config import get_logger

logger = get_logger(__name__)


def get_driver_pool():
    load_dotenv()
    try:
        POOL = int(os.getenv('DRIVER_POOL'))
    except (TypeError, ValueError):
        POOL = 2

    driver_pool = Queue()

    for i in range(POOL):
        logger.info(f"Creating driver #{i} and add to pool...")
        proxy = get_proxy()
        driver = get_driver(proxy=proxy)
        driver_pool.put((driver, proxy))
    return driver_pool


def reset_driver_async(driver_pool: Queue, app_driver, current_proxy):
    def reset():
        new_proxy = reset_proxy(current_proxy=current_proxy)
        new_driver = reset_driver(app_driver, new_proxy)
        driver_pool.put((new_driver, new_proxy))
    Thread(target=reset).start()
