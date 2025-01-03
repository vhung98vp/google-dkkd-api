from googlesearch import search
from .proxies import get_proxy
import re

def get_company_tax_id(company_name, site_url):
    try:
        # Use Google Search to find the site_url link for the company
        query = f"{company_name} site:{site_url}"
        search_results = search(query, num_results=1, lang='vi', proxy=get_proxy())

        # Extract the first search result
        company_url = next(search_results, None)

        if not company_url:
            return f"No results found for {company_name} on {site_url}"
        tax_id = re.search(r'\d+', company_url).group()
        return tax_id
        
    except Exception as e:
        return f"An error occurred: {e}"
    
def get_company_url(company_name, site_url):
    try:
        # Use Google Search to find the site_url link for the company
        query = f"{company_name} site:{site_url}"
        search_results = search(query, num_results=1, lang='vi', proxy=get_proxy())

        # Extract the first search result
        company_url = next(search_results, None)
        if not company_url:
            return f"No results found for {company_name} on {site_url}"
        return company_url
        
    except Exception as e:
        return f"An error occurred: {e}"
    