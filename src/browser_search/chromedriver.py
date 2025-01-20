import random
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
from .proxies import get_proxy
from ..logger_config import get_logger

logger = get_logger(__name__)

USER_AGENT_LIST = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Version/14.0.1 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36 Edge/94.0.992.47",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; Trident/7.0; AS; .NET CLR 4.0.30319; InfoPath.3; .NET4.0C; .NET4.0E) like Gecko",
                ]
screen_sizes = ['1920,1080', '1366,768', '1440,900', '1600,900',
                '1280,720', '1024,768', '1536,864', '1280,800', '1093,614', '1280,1024']

DOWNLOAD_DIR = os.path.join(os.getcwd(), 'downloads')


def get_driver(download_dir=DOWNLOAD_DIR, open_gui=True, proxy=get_proxy()):
    options = Options()
    # user_agent = random.choice(USER_AGENT_LIST)
    user_agent = UserAgent(platforms='desktop').random
    
    options.add_experimental_option("prefs", {  # For PDF Download
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "plugins.always_open_pdf_externally": True  # Avoid opening PDF in browser
    })

    if not open_gui:
        options.add_argument("--headless")  # Remove this if you want to see the browser (Headless makes the chromedriver not have a GUI)
    if proxy:
        options.add_argument(f"--proxy-server={proxy}")

    options.add_argument(f'--user-agent={user_agent}')
    options.add_argument(f"--window-size={random.choice(screen_sizes)}")
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-extensions")
    # options.add_argument('--disable-blink-features=AutomationControlled')
    
    # # Custom chromedriver path on windows
    # chromedriver_path = './driver/chromedriver.exe'
    # driver = webdriver.Chrome(options=options, executable_path=chromedriver_path)
    driver = webdriver.Chrome(options=options)

    logger.info(f"Chrome driver has been created with UA {user_agent} and proxy {proxy}")
    return driver

def reset_driver(driver):
    if driver:
        try:
            driver.close()
            driver.quit()
            driver.service.process.kill()  # Deeply kill the process in case Chrome is not responding
        except Exception as e:
            logger.error("Error, Fail to close driver: ", e)
    
    try:
        new_driver = get_driver()
    except Exception as e:
        logger.error("Error, Fail to setup new driver: ", e)

    logger.info("Driver has been reset...")
    return new_driver
