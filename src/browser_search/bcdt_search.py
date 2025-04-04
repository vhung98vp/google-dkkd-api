from selenium_recaptcha_solver import RecaptchaSolver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import os
import time
from .simulate_interaction import simulate_interaction
from ..logger_config import get_logger

logger = get_logger(__name__)

DOWNLOAD_DIR = os.path.join(os.getcwd(), 'downloads')

BCDT_PAGE_HOME = 'https://bocaodientu.dkkd.gov.vn/egazette'
BCDT_PAGE_URL = 'https://bocaodientu.dkkd.gov.vn/egazette/Forms/Egazette/ANNOUNCEMENTSListingInsUpd.aspx'
announcement_type_filter_key = "ctl00$C$ANNOUNCEMENT_TYPE_IDFilterFld"

company_id_key = "ctl00$C$ENT_GDT_CODEFld"
btn_filter_key = "ctl00$C$BtnFilter"
response_pdf_key = "ctl00_C_PnlListResult"
xpath_list = [
        "//input[@id='ctl00_C_ENT_CODEFilterFld']", 
        "//input[@id='ctl00_C_ENT_GDT_CODEFld']",
        "//input[@id='ctl00_C_ENT_NAMEFilterFld']",
        "//input[@id='ctl00_C_WebTextBox1']",
        "//input[@id='ctl00_C_PUBLISH_DATEFilterFldFrom']",
        "//input[@id='ctl00_C_PUBLISH_DATEFilterFldTo']",        
    ]

def download_file(link, download_dir, timeout=15):
    # Get the current list of files in the directory
    before_files = set(os.listdir(download_dir))

    # Start download
    link.click()
    start_time = time.time()
    while True:
        # Get the current list of files in the directory
        current_files = set(os.listdir(download_dir))
        new_files = current_files - before_files

        # Check for a new file that is fully downloaded
        for file in new_files:
            #if not (file.endswith(".crdownload") or file.endswith(".tmp")):  # Exclude temporary files
            if file.endswith(".pdf"):  # Get only PDFs
                return os.path.join(download_dir, file)

        # Check for timeout
        if time.time() - start_time > timeout:
            return None
        # Waiting
        time.sleep(1)


def download_files(links, download_dir, count):
    if links:  
        downloaded_files = []
        for pdf_link in links[:count]:
            downloaded_file = download_file(pdf_link, download_dir)
            if downloaded_file:
                downloaded_files.append(downloaded_file)
        return downloaded_files
    else: # Not found links
        return []

def get_pdfs_from_site(driver, company_tax_id: str, count=1, announcement_type="AMEND", download_dir=DOWNLOAD_DIR):
    # Get page contents
    start = time.time()

    driver.get(BCDT_PAGE_HOME)
    time.sleep(2)
    
    retry = 0
    while retry < 3:
        driver.get(BCDT_PAGE_URL)
        try:
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
        except TimeoutException as e:
            logger.error(f"Timeout while loading dkkd page: {e}")
            retry += 1
            continue
        except Exception as e:
            logger.error(f"Error while loading dkkd page: {e}")
            raise e

        # Avoid redirect to login page
        if driver.current_url != BCDT_PAGE_URL:
            break
        retry += 1
        time.sleep(1)
    
    if driver.current_url != BCDT_PAGE_URL:
        raise Exception(f"Cannot load site dkkd, current url: {driver.current_url}")

    logger.info(f'Load site dkkd in time (s): {time.time() - start:.6f} after {retry} time(s)')

    simulate_interaction(driver, xpath_list)
    simulate_interaction(driver, xpath_list)
    logger.info(f'Simulated interaction in time (s): {time.time() - start:.6f}')
    ## Fill options
    # Announcement type
    ann_type_dropdown = driver.find_element(By.NAME, announcement_type_filter_key) 
    ann_type_select = Select(ann_type_dropdown)
    ann_type_select.select_by_value(announcement_type)

    # Captcha solver
    try:
        solver = RecaptchaSolver(driver=driver)
        recaptcha_iframe = driver.find_element(By.XPATH, '//iframe[@title="reCAPTCHA"]')
        solver.click_recaptcha_v2(iframe=recaptcha_iframe)
        logger.info(f'Solved captcha on site dkkd in time (s): {time.time() - start:.6f}')
    except Exception as e:
        logger.error(f"Exception when trying to solve captcha on site dkkd: {e}")
        if "Google has detected automated queries" in str(e):
            raise e
    
    # Company id (tax id)
    company_input = driver.find_element(By.NAME, company_id_key)
    company_input.send_keys(Keys.CONTROL + "a")  # Select all text to replace
    company_input.send_keys(company_tax_id)

    # Click search (filter) button
    driver.find_element(By.NAME, btn_filter_key).click()

    # Wait 10s for the new page to load or result to appear
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, response_pdf_key)))
    
    # Response page with table of pdfs to download
    response_table = driver.find_element(By.ID, response_pdf_key)
    pdf_links = response_table.find_elements(By.TAG_NAME, "input")
    logger.info(f'Get download links in time (s): {time.time() - start:.6f}')

    # Download and return files
    return download_files(pdf_links, download_dir, count)
