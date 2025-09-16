from crewai import Agent
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from ..tools.web_search_tool import search_company_info
from ..tools.job_description_analyzer import analyze_job_description

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=os.getenv("GOOGLE_API_KEY"))

research_agent = Agent(
    role='Company Research Specialist',
    goal='Gather comprehensive information about companies and job roles',
    backstory="""You are an expert researcher who specializes in analyzing 
    companies, their culture, recent developments, and job requirements. 
    You help interview candidates prepare by providing deep insights.""",
    verbose=True,
    allow_delegation=False,
    tools=[search_company_info, analyze_job_description],
    llm=llm
)