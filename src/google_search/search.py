import re
import requests
import random
import os 
from bs4 import BeautifulSoup


# Use text-based user agents
USER_AGENTS = [
    "Lynx/2.8.9rel.1 libwww-FM/2.14",
    "Lynx/2.8.8rel.2 libwww-FM/2.13",
    "w3m/0.5.3+git20220429",
    "w3m/0.5.2+git20190105",
    "Links (2.28; Linux 5.15.0)",
    "Links (2.27; Linux 4.19.0)",
    "ELinks/0.13.1 (textmode; Linux x86_64)",
    "ELinks/0.12pre6 (textmode; FreeBSD)"
]

def get_headers():
    return { "User-Agent": random.choice(USER_AGENTS) } 

def get_proxies():
    return os.getenv('PROXIES')

def get_company_identity(company_name, site_url):
    # Use Google Search to find the site_url link for the company
    query = f"{company_name} site:{site_url}"
    search_url = f"https://www.google.com/search?q={query}&hl=vi"
    response = requests.get(search_url, headers=get_headers(), proxies=get_proxies())

    # Extract first result from response html
    soup = BeautifulSoup(response.text, "html.parser")
    first_result = soup.find("a", class_="fuLhoc")  # CSS selector for the link

    if not first_result:
        return {"search.html": response.text}
    
    company_url = re.search(r"/url\?q=(https://[^\s&]+)", first_result["href"]).group(1)
    company_tax_id = re.search(r'\d+', company_url).group()
    return {
        "company_tax_id": company_tax_id,
        "url": company_url
    }