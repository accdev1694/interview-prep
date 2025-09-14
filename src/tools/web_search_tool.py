from crewai.tools import tool
import requests

@tool
def search_company_info(company_name: str):
    """Search for basic information about a company"""
    return f"Searching for information about {company_name}..."