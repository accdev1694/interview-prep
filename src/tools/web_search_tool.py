from crewai.tools import tool
import requests
from bs4 import BeautifulSoup

@tool
def search_company_info(company_name: str):
    """Search for basic information about a company"""
    search_query = f"{company_name} company information"
    search_url = f"https://www.google.com/search?q={search_query}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

    try:
        response = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        snippets = soup.find_all('span', class_='aCOpRe')
        if not snippets: snippets = soup.find_all('div', class_='VwiC3b')
        info = ' '.join([snippet.get_text() for snippet in snippets[:3]])
        return f"Company: {company_name}. Information found: {info}"
    except:
        return f"Could not fetch Information for {company_name}. Please Check mannually." 
