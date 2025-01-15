from googlesearch import search
from .proxies import get_proxy
import re


def get_company_identity(company_name, site_url, id_only=True):
    try:
        # Use Google Search to find the site_url link for the company
        query = f"{company_name} site:{site_url}"
        search_results = search(query, num_results=1, lang='vi', proxy=get_proxy())

        # Extract the first search result
        company_url = next(search_results, None)
        if not company_url:
            return None
        
        if id_only: # Take only tax id
            return re.search(r'\d+', company_url).group()
        else:
            return company_url
    
    except Exception as e:
        return f"An error occurred: {e}"