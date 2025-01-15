from flask import Flask, request, jsonify
from src.captcha.captcha_solver import get_pdfs_from_site
# from src.ocr.extract_data import extract_data_from_pdfs
from src.gemini_api.gemini import extract_data_from_pdfs
from src.mst.company_data import get_company_info_from_site
from src.google.company_search import get_company_identity
import time

def retry_request(func, max_retries=3, delay_in_seconds=2):
    for attempt in range(max_retries + 1):
        try:
            if attempt > 0:
                print(f"Try again, attempt {attempt}...")
            
            result = func()
            if result != None:
                return result
            else:
                raise ValueError("Function return None")
        except ValueError:
            if attempt < max_retries:
                time.sleep(delay_in_seconds * (2 ** attempt))  # Exponential backoff (2s, 4s, 8s)
            else:
                return None
        except Exception as e:
            if attempt < max_retries:
                time.sleep(delay_in_seconds * (2 ** attempt))  # Exponential backoff (2s, 4s, 8s)
            else:
                raise e

PUBLICATION_TYPE = ["NEW", "AMEND", "CORP", "OTHER", "CHANTC", "REVOKE"]
# ĐK mới, ĐK thay đổi, Giải thể, Loại khác, TB thay đổi, Vi phạm/Thu hồi

app = Flask(__name__)

def response_error(message, code=400):
    return jsonify({"error": message}), code

@app.route('/search', methods=['GET'])
def search_company():
    try:
        # Site and company for searching
        site_url = "masothue.com"
        company_name = request.args.get('company_name')
        if not company_name:
            return response_error("Company name is required")

        # Other params
        search_type = request.args.get('type', 'quick')
        search_engine = request.args.get('engine', 'google')
        pub_type = request.args.get('pub_type', 'AMEND')

        print(f"Searching company {company_name}...")

        # Cases for params
        if search_engine == 'google':   # Using google-mst
            if search_type == 'quick':
                tax_id = retry_request(lambda: get_company_identity(company_name, site_url))
                if not tax_id:
                    return response_error(f"No results found for {company_name} on {site_url}")
                
                return {'company_tax_id': tax_id}
            elif search_type == 'full':
                company_url = retry_request(lambda: get_company_identity(company_name, site_url, False))
                if not company_url:
                    return response_error(f"No results found for {company_name} on {site_url}")
                
                company_info = get_company_info_from_site(company_url)
                return jsonify(company_info)
            else:
                return response_error("Invaid search type")
        
        elif search_engine == 'dkkd':   # Using google-mst-dkkd
            tax_id = retry_request(lambda: get_company_identity(company_name, site_url))
            if not tax_id:
                return response_error(f"No results found for {company_name} on {site_url}")
            
            if search_type == 'quick':
                count = 1
            elif search_type == 'full':
                count = 10
            else:
                return response_error("Invaid search type")
            if pub_type not in PUBLICATION_TYPE:
                return response_error("Invaid publication type")
            
            print(f"Getting PDFs from site with tax_id {tax_id}...")
            pdfs = retry_request(lambda: get_pdfs_from_site(tax_id, count, pub_type))
            if not pdfs:
                return response_error(f"Request empty. Check type and company tax id: {tax_id}", 404)
            else:
                extracted_data = extract_data_from_pdfs(pdfs)
                return jsonify(extracted_data)
        else:
            return response_error("Invaid search engine")
    except Exception as e:
        return response_error(f"An error occurred: {e}", 500)

if __name__ == "__main__":
    app.run(debug=True)