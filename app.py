from flask import Flask, request, jsonify
from src.captcha.captcha_solver import get_pdfs_from_site
# from src.ocr.extract_data import extract_data_from_pdfs
from src.gemini_api.gemini import extract_data_from_pdfs
from src.mst.company_data import get_company_info_from_site
from src.google_search.company_url import get_company_url_from_google
from src.google_search.company_tax_id import get_company_tax_id_from_google


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

        # Cases for params
        if search_engine == 'google':   # Using google-mst
            if search_type == 'quick':
                tax_id = get_company_tax_id_from_google(company_name, site_url)
                return {'company_tax_id': tax_id}
            elif search_type == 'full':
                company_url = get_company_url_from_google(company_name, site_url)
                company_info = get_company_info_from_site(company_url)
                return jsonify(company_info)
            else:
                return response_error("Invaid search type")
        
        elif search_engine == 'dkkd':   # Using google-mst-dkkd
            tax_id = get_company_tax_id_from_google(company_name, site_url)
            if search_type == 'quick':
                count = 1
            elif search_type == 'full':
                count = 10
            else:
                return response_error("Invaid search type")
            if pub_type not in PUBLICATION_TYPE:
                return response_error("Invaid publication type")
            
            pdfs = get_pdfs_from_site(tax_id, count, pub_type)
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