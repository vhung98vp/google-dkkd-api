from flask import Flask, request, jsonify
from src.browser_search.bcdt_search import get_pdfs_from_site
from src.browser_search.google_search import get_company_identity
# from src.google_search.search import get_company_identity
# from src.chromedriver.chromedriver import get_driver, reset_driver
from src.chromedriver.driver_pool import get_driver_pool, reset_driver_async, add_driver_to_pool_async
from src.chromedriver.simulate_browsing import simulate_browsing
# from src.ocr.extract_data import extract_data_from_pdfs
from src.gemini_api.gemini import extract_data_from_pdfs
from src.mst.company_data import get_company_info_from_site
from src.logger_config import get_logger
import time
import random


logger = get_logger(__name__)

ANNOUNCEMENT_TYPE = ["NEW", "AMEND", "CORP", "OTHER", "CHANTC", "REVOKE"]
# ĐK mới, ĐK thay đổi, Giải thể, Loại khác, TB thay đổi, Vi phạm/Thu hồi


driver_pool = get_driver_pool()

def retry_request(func, max_retries=1, delay_in_seconds=2):
    for attempt in range(max_retries + 1):
        try:
            if attempt > 0:
                logger.info(f"Try again, attempt {attempt}...")
            return func()
        except Exception as e:
            if attempt < max_retries and "Google has detected automated queries" not in str(e):
                logger.error(f"Exception while processing {func.__name__}: {e}")
                time.sleep(delay_in_seconds * (2 ** attempt))  # Exponential backoff (2s, 4s, 8s)
            else:
                raise e


app = Flask(__name__)

def response_error(message, code=400):
    return jsonify({"error": message}), code


@app.route('/manage/health', methods=['GET'])
def manage_health():
    return jsonify({"message": "Service is working"}), 200


@app.route('/driver/get', methods=['GET'])
def manage_driver():
    current_size = driver_pool.qsize()
    return jsonify({"message": f"Total driver is working: {current_size}"}), 200


@app.route('/driver/add', methods=['GET'])
def add_driver():
    add_size = add_driver_to_pool_async(driver_pool)
    return jsonify({"message": f"Total driver is adding to pool: {add_size}"}), 201


@app.route('/search', methods=['GET'])
def search_company():
    # global app_driver
    get_exception = False

    try:
        # Site and company for searching
        site_url = "masothue.com"
        company_name = request.args.get('company_name')
        if not company_name:
            return response_error("Company name is required")

        # Other params
        search_type = request.args.get('type', 'quick')
        search_engine = request.args.get('engine', 'google')
        ann_type = request.args.get('ann_type', 'AMEND')
        app_driver, current_proxy = driver_pool.get()
        logger.info(f"Searching for company {company_name} with driver session {app_driver.session_id}...")
        start = time.time()

        # Simulate browsing before load google
        simulate_browsing(app_driver, random.randint(0, 2))

        # Cases for params
        if search_engine == 'google':   # Using google-mst
            if search_type == 'quick':
                company_idt = retry_request(lambda: get_company_identity(app_driver, company_name, site_url))
                if not company_idt:
                    return response_error(f"No results found for {company_name} on {site_url}", 204)
                
                logger.info(f'Quick search google for {company_name} in time (s): {time.time() - start:.6f}')
                return company_idt
            elif search_type == 'full':
                company_idt = retry_request(lambda: get_company_identity(app_driver, company_name, site_url))
                if not company_idt:
                    return response_error(f"No results found for {company_name} on {site_url}", 204)
                
                company_info = get_company_info_from_site(company_idt["url"], app_driver)
                logger.info(f'Full search google & mst for {company_name} in time (s): {time.time() - start:.6f}')
                return jsonify(company_info)
            else:
                return response_error("Invaid search type")
        
        elif search_engine == 'dkkd':   # Using google-mst-dkkd
            if search_type == 'quick':
                count = 1
            elif search_type == 'full':
                count = 10
            else:
                return response_error("Invaid search type")
            if ann_type not in ANNOUNCEMENT_TYPE:
                return response_error("Invaid announcement type")
            
            company_idt = retry_request(lambda: get_company_identity(app_driver, company_name, site_url))
            if not company_idt:
                return response_error(f"No results found for {company_name} on {site_url}", 204)
            
            tax_id = company_idt["company_tax_id"].split('-')[0]
            logger.info(f'Get company tax id {tax_id} in time (s): {time.time() - start:.6f}')
            
            simulate_browsing(app_driver, random.randint(0, 2))
            simulate_browsing(app_driver, random.randint(1, 3), True)
            logger.info(f"Receiving PDFs from site dkkd with tax_id {tax_id}...")
            pdfs = retry_request(lambda: get_pdfs_from_site(app_driver, tax_id, count, ann_type))

            # Try again with type as new announcement
            if not pdfs and ann_type == 'AMEND':
                logger.info(f"PDFs not found, try again with NEW announcement...")
                pdfs = retry_request(lambda: get_pdfs_from_site(app_driver, tax_id, count, 'NEW'))

            if not pdfs:
                return response_error(f"Request empty. Check type and company tax id: {tax_id}", 204)
            else:
                logger.info(f'Received {len(pdfs)} PDF(s) from site dkkd in time (s): {time.time() - start:.6f}')
                extracted_data = extract_data_from_pdfs(pdfs)
                logger.info(f'Extracted data in time (s): {time.time() - start:.6f}')
                return jsonify(extracted_data)
        else:
            return response_error("Invaid search engine")        
    except Exception as e:
        logger.error(f"Exception while processing request for company {company_name}: {e}")
        reset_driver_async(driver_pool, app_driver, current_proxy)
        get_exception = True
        return response_error(f"An error occurred: {e}", 500)
    finally:
        if not get_exception:
            driver_pool.put((app_driver, current_proxy))

if __name__ == "__main__":
    app.run(debug=True)