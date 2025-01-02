from selenium_recaptcha_solver import RecaptchaSolver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import os
import time
from .chromedriver import get_driver

DOWNLOAD_DIR = os.path.join(os.getcwd(), 'downloads')

BCDT_PAGE_URL = 'https://bocaodientu.dkkd.gov.vn/egazette/Forms/Egazette/ANNOUNCEMENTSListingInsUpd.aspx'
publication_type_filter_key = "ctl00$C$ANNOUNCEMENT_TYPE_IDFilterFld"

company_id_key = "ctl00$C$ENT_GDT_CODEFld"
btn_filter_key = "ctl00$C$BtnFilter"
response_pdf_key = "ctl00_C_PnlListResult"


def download_file(link, download_dir, timeout=5):
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

def get_pdfs_from_site(company_tax_id: str, count=1, publication_type="AMEND", download_dir=DOWNLOAD_DIR):
    # Get page contents
    test_driver = get_driver(download_dir)
    test_driver.get(BCDT_PAGE_URL)

    # Fill options
    # Publication type
    pub_type_dropdown = test_driver.find_element(By.NAME, publication_type_filter_key) 
    pub_type_select = Select(pub_type_dropdown)
    pub_type_select.select_by_value(publication_type)
    # Company id (tax id)
    test_driver.find_element(By.NAME, company_id_key).send_keys(company_tax_id)

    # Captcha solver
    solver = RecaptchaSolver(driver=test_driver)
    recaptcha_iframe = test_driver.find_element(By.XPATH, '//iframe[@title="reCAPTCHA"]')
    solver.click_recaptcha_v2(iframe=recaptcha_iframe)

    # token = test_driver.execute_script("return document.getElementById('g-recaptcha-response').value;")
    # print("reCAPTCHA Token:", token)

    # Click search (filter) button
    test_driver.find_element(By.NAME, btn_filter_key).click()

    # Wait 5s for the new page to load or result to appear
    WebDriverWait(test_driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    
    # Response page with table of pdfs to download
    response_table = test_driver.find_element(By.ID, response_pdf_key)
    pdf_links = response_table.find_elements(By.TAG_NAME, "input")

    # Download and return files
    return download_files(pdf_links, download_dir, count)
