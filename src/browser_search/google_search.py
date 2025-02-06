import re
import time
from selenium.webdriver.common.by import By
from selenium_recaptcha_solver import RecaptchaSolver
from .simulate_interaction import simulate_interaction
from ..logger_config import get_logger

logger = get_logger(__name__)


xpath_list = [
    "//hr[@size='1']", 
    "//div[contains(., 'https://www.google.com/search')]"
]

def get_company_identity(driver, company_name, site_url):
    start = time.time()
    
    # query = f"{company_name} site:{site_url}"
    query = f"{company_name} {site_url}"
    driver.get(f"https://www.google.com/search?q={query}&hl=vi")
    logger.info(f'Load google in time (s): {time.time() - start:.6f}')

    # Get search result
    def get_first_url():
        try:
            match_url = driver.find_element(By.XPATH, "//a[contains(@href, '%s')]" % f"https://{site_url}")
            return match_url.get_attribute("href")
        except Exception as e:
            logger.error(f"Exception when get first url while searching google: {e}")
            return ""
    
    company_url = get_first_url()
    # Captcha solver if exist
    if not company_url:
        logger.info("Solving captcha while searching google...")
        try:
            simulate_interaction(driver, xpath_list)
            logger.info(f'Simulated interaction in time (s): {time.time() - start:.6f}')
            solver = RecaptchaSolver(driver)
            recaptcha_iframe = driver.find_element(By.XPATH, '//iframe[@title="reCAPTCHA"]')
            solver.click_recaptcha_v2(iframe=recaptcha_iframe)
            logger.info(f"Solved captcha in time (s): {time.time() - start:.6f}")
            company_url = get_first_url()
        except Exception as e:
            logger.error(f"Exception when trying to solve captcha on site google: {e}")
            if "Google has detected automated queries" in str(e):
                raise e
            elif "Unable to locate element" in str(e):
                return {"search.html": driver.page_source}

    if not company_url:
        return {"search.html": driver.page_source}
    
    logger.info(f'Get first url in time (s): {time.time() - start:.6f}')
    company_tax_search_id = re.search(r'(\d{10}(?:-\d{3})?)', company_url)
    if not company_tax_search_id:
        return None

    return {
        "company_tax_id": company_tax_search_id.group(),
        "url": company_url
    }
