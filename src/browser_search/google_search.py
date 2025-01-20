import re
import time
from selenium.webdriver.common.by import By
from selenium_recaptcha_solver import RecaptchaSolver
from ..logger_config import get_logger

logger = get_logger(__name__)

def get_company_identity(driver, company_name, site_url):
    start = time.time()
    
    query = f"{company_name} site:{site_url}"
    driver.get(f"https://www.google.com/search?q={query}&hl=vi")
    logger.info(f'Search google in time (s): {time.time() - start:.6f}')

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
        time.sleep(1)
        solver = RecaptchaSolver(driver)
        recaptcha_iframe = driver.find_element(By.XPATH, '//iframe[@title="reCAPTCHA"]')
        solver.click_recaptcha_v2(iframe=recaptcha_iframe)
        logger.info(f"Solved captcha in time (s): {time.time() - start:.6f}")
        company_url = get_first_url()

    if not company_url:
        return None
    
    logger.info(f'Get first url in time (s): {time.time() - start:.6f}')
    company_tax_id = re.search(r'\d+', company_url).group()
    return {
        "company_tax_id": company_tax_id,
        "url": company_url
    }
