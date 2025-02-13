from dotenv import load_dotenv
import os
from queue import Queue
from threading import Thread
from .chromedriver import get_driver, reset_driver
from .proxies import get_proxy, reset_proxy
from ..logger_config import get_logger

logger = get_logger(__name__)


def get_driver_pool_size():
    load_dotenv()
    try:
        pool = int(os.getenv('POOL_SIZE'))
    except (TypeError, ValueError):
        pool = 2
    return pool


def add_driver_to_pool(driver_pool):
    proxy = get_proxy()
    driver = get_driver(proxy=proxy)
    driver_pool.put((driver, proxy))


def get_driver_pool():
    POOL_SIZE = get_driver_pool_size()
    driver_pool = Queue()

    for i in range(POOL_SIZE):
        logger.info(f"Creating driver #{i+1} and add to pool...")
        add_driver_to_pool(driver_pool)
    return driver_pool


def add_driver_to_pool_async(driver_pool):
    add_size = get_driver_pool_size() - driver_pool.qsize()

    def add():
        for i in range(add_size):
            logger.info(f"Creating new driver #{i+1} and add to pool...")
            add_driver_to_pool(driver_pool=driver_pool)
        
    Thread(target=add).start()
    return add_size


def reset_driver_async(driver_pool: Queue, app_driver, current_proxy):
    def reset():
        logger.info(f"Reseting driver and proxy...")
        new_proxy = reset_proxy(current_proxy=current_proxy)
        new_driver = reset_driver(app_driver, new_proxy)
        if new_driver:
            driver_pool.put((new_driver, new_proxy))
    Thread(target=reset).start()
