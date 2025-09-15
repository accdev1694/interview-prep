from crewai.tools import tool
import requests

@tool
def search_company_info(company_name: str):
    """Search for basic information about a company"""
    return f"""Company: {company_name}. 
    Industry: Technology. Founded: 1998. 
    Headquarters: Mountain View, CA. 
    Known for: Search engine, Cloud services, Android OS. 
    Recent news: Focus on AI development."""