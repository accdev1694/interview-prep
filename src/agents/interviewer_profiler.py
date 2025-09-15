from crewai import Agent
from dotenv import load_dotenv
from ..tools.web_search_tool import search_company_info
from ..tools.job_description_analyzer import analyze_job_description

load_dotenv()

interviewer_profiler = Agent(
    role= 'Interviewer Background Analyst',
    goal= 'Research interviewer backgrounds, styles, and likely questioning approaches',
    backstory= """You are a specialist in analyzing interviewer profiles, their professional 
    backgrounds, and interview styles. You help candidates understand who they'll be meeting 
    and what types of questions to expect based on the interviewer's role and experience.""",
    tools = [search_company_info, analyze_job_description],
    allow_delegation = False,
    verbose=True    
)