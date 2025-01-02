from flask import Flask, request, jsonify
from src.captcha.company_tax_id import get_company_tax_id_from_google
from src.captcha.captcha_solver import get_pdfs_from_page
# from src.ocr.extract_data import extract_data_from_pdfs
from src.gemeni_api.gemini import extract_data_from_pdfs
from src.mst.company_data import get_company_info_from_site
from src.mst.company_url import get_company_url_from_google
# import re 

# import time

app = Flask(__name__)

# @app.route('/search', methods=['GET'])
# def search_company_data():
#     # Site and company for searching
#     try:
#         site_url = "masothue.com"
#         company_name = request.args.get('company_name')
#         if not company_name:
#             return jsonify({"error": "Company name is required"}), 400
        
#         # Quick search mode - get only first page from first PDF
#         quick_search = request.args.get('quick')
#         quick_search = True if quick_search == None else quick_search.lower() in ['true', '1', 'yes', 'y']

#         time0 = time.time()
#         company_tax_id = get_company_tax_id_from_google(company_name, site_url)
#         print(f"Tax id: {company_tax_id}")

#         if quick_search:
#             # Take only 1 file and get info from first page
#             pdfs = get_pdfs_from_page(company_tax_id)
#             time1 = time.time()
#             print(f"Elapsed get pdfs time: {time1-time0:.6f} seconds")
#         else:
#             pdfs = get_pdfs_from_page(company_tax_id, 10)
#             time1 = time.time()
#             print(f"Elapsed get pdfs time: {time1-time0:.6f} seconds")

#         if pdfs:
#             # extracted_data = extract_data_from_pdfs(pdfs, quick_search)
#             extracted_data = extract_data_from_pdfs(pdfs)
#             time2 = time.time()
#             print(f"Elapsed extract time: {time2-time1:.6f} seconds") 
#             return jsonify(extracted_data)
#         else:
#             return jsonify({"error": "Data not found"})
    
#     except Exception as e:
#         return jsonify({"error": f"An error occurred: {e}"})


# @app.route('/search_google', methods=['GET'])
# def search_company_data_google():
#     # Site and company for searching
#     site_url = "masothue.com"
#     company_name = request.args.get('company_name')
#     if not company_name:
#         return jsonify({"error": "Company name is required"}), 400

#     quick_search = request.args.get('quick')
#     quick_search = True if quick_search == None else quick_search.lower() in ['true', '1', 'yes', 'y']
#     # Get company url site from google, then extract data

#     company_url = get_company_url_from_google(company_name, site_url)
    
#     if quick_search:
#         return {'company_tax_id': re.search(r'\d+', company_url).group()}
#     else:
#         company_info = get_company_info_from_site(company_url)
#         return jsonify(company_info)


@app.route('/search', methods=['GET'])
def search_company():
    try:
        # Site and company for searching
        site_url = "masothue.com"
        company_name = request.args.get('company_name')
        if not company_name:
            return jsonify({"error": "Company name is required"}), 400

        search_type = request.args.get('type', 'quick')
        search_engine = request.args.get('engine', 'google')

        if search_engine == 'google':
            if search_type == 'quick':
                tax_id = get_company_tax_id_from_google(company_name, site_url)
                return {'company_tax_id': tax_id}
            elif search_type == 'full':
                company_url = get_company_url_from_google(company_name, site_url)
                company_info = get_company_info_from_site(company_url)
                return jsonify(company_info)
            else:
                return {'error': "Invaid search type"}
        
        elif search_engine == 'dkkd':
            tax_id = get_company_tax_id_from_google(company_name, site_url)
            if search_type == 'quick':
                count = 1
            elif search_type == 'full':
                count = 10
            else:
                return {'error': "Invaid search type"}
            
            pdfs = get_pdfs_from_page(tax_id, count)
            extracted_data = extract_data_from_pdfs(pdfs)
            return jsonify(extracted_data)
        else:
            return {'error': "Invaid search engine"}
    except Exception as e:
        return jsonify({"error": f"An error occurred: {e}"})

if __name__ == "__main__":
    app.run(debug=True)