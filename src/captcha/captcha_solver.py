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
publication_type_filter_options = ["NEW", "AMEND", "CORP", "OTHER", "CHANTC", "REVOKE"]
# Đăng ký mới, Đăng ký thay đổi, Giải thể, Loại khác, Thông báo thay đổi, Vi phạm/Thu hồi

company_id_key = "ctl00$C$ENT_GDT_CODEFld"
btn_filter_key = "ctl00$C$BtnFilter"
response_pdf_key = "ctl00_C_PnlListResult"

def get_pdfs_from_page(company_tax_id: str, count=1, publication_type="AMEND", download_dir=DOWNLOAD_DIR):
    test_driver = get_driver()
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

    token = test_driver.execute_script("return document.getElementById('g-recaptcha-response').value;")
    print("reCAPTCHA Token:", token)

    test_driver.find_element(By.NAME, btn_filter_key).click()

    # Wait 5s for the new page to load or result to appear
    WebDriverWait(test_driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    if len(os.listdir(download_dir)) == 0:
        last_file = None
    else:
        last_file = max([os.path.join(download_dir, f) for f in os.listdir(download_dir)], key=os.path.getctime)
    
    response_table = test_driver.find_element(By.ID, response_pdf_key)
    pdf_links = response_table.find_elements(By.TAG_NAME, "input")
    if not pdf_links:
        print("Request empty. Check company tax id and type")
        return []
    else:
        pdf_links = pdf_links[:count]
        downloaded_files = []
        for pdf_link in pdf_links:
            pdf_link.click()
            time.sleep(3)  # Wait for downloading
            downloaded_file = max([os.path.join(download_dir, f) for f in os.listdir(download_dir)], key=os.path.getctime)

            if last_file != downloaded_file:
                last_file = downloaded_file
                # downloaded_files.append(os.path.basename(downloaded_file))
                downloaded_files.append(last_file)
                print(f"PDF downloaded: {last_file}")
            else:
                print("No PDF downloaded. Check the button and browser settings.")
        return downloaded_files

# get_pdfs_from_page(company_tax_id='0107694304')
