from crewai import Agent
from dotenv import load_dotenv
from ..tools.web_search_tool import search_company_info

load_dotenv()

research_agent = Agent(
    role='Company Research Specialist',
    goal='Gather comprehensive information about companies and job roles',
    backstory="""You are an expert researcher who specializes in analyzing 
    companies, their culture, recent developments, and job requirements. 
    You help interview candidates prepare by providing deep insights.""",
    verbose=True,
    allow_delegation=False,
    tools=[search_company_info]
)