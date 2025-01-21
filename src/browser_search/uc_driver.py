import random
import os
import undetected_chromedriver as uc
from fake_useragent import UserAgent
from .proxies import get_proxy
from ..logger_config import get_logger

logger = get_logger(__name__)

screen_sizes = ['1920,1080', '1366,768', '1440,900', '1600,900',
                '1280,720', '1024,768', '1536,864', '1280,800', '1093,614', '1280,1024']

DOWNLOAD_DIR = os.path.join(os.getcwd(), 'downloads')


def get_driver(download_dir=DOWNLOAD_DIR, open_gui=False, proxy=get_proxy()):
    options = uc.ChromeOptions()
    user_agent = UserAgent(platforms='desktop').random

    options.add_experimental_option("prefs", {  # For PDF Download
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "plugins.always_open_pdf_externally": True,  # Avoid opening PDF in browser
    })

    if not open_gui:
        options.add_argument("--headless=new") # Headless makes the chromedriver not have a GUI
    if proxy:
        options.add_argument(f"--proxy-server={proxy}")   

    for _ in range(100):
        width = random.randint(1024, 1920)
        height = random.randint(768, 1080)
        screen_sizes.append(f'{width},{height}')    
    screen_heights = list(range(70, 120))
    screen_widths = list(range(70, 120))

    options.add_argument(f'user-agent={user_agent}')
    options.add_argument(f'--fp-screenheight={random.choice(screen_heights)}')
    options.add_argument(f'--fp-screenwidth={random.choice(screen_widths)}')
    options.add_argument(f"--window-size={random.choice(screen_sizes)}")
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--incognito")
    options.add_argument("--disable-webgl")
    options.add_argument("--disable-webrtc")

    # # Custom chromedriver path on windows
    chromedriver_path = './driver/chromedriver.exe'
    # chromedriver_path = '/usr/local/bin/chromedriver'
    driver = uc.Chrome(options=options, driver_executable_path=chromedriver_path, version_main=130)
    # driver = uc.Chrome(options=options)

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
