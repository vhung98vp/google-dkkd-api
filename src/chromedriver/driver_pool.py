from dotenv import load_dotenv
import os
from queue import Queue
from threading import Thread
from .chromedriver import get_driver, reset_driver
from ..logger_config import get_logger

logger = get_logger(__name__)


def get_driver_pool():
    load_dotenv()
    try:
        POOL = int(os.getenv('DRIVER_POOL'))
    except (TypeError, ValueError):
        POOL = 3

    driver_pool = Queue()

    for i in range(POOL):
        logger.info(f"Creating driver #{i} and add to pool...")
        driver_pool.put(get_driver())
    return driver_pool

def reset_driver_async(driver_pool: Queue, app_driver):
    def reset():
        new_driver = reset_driver(app_driver)
        driver_pool.put(new_driver)
    Thread(target=reset).start()