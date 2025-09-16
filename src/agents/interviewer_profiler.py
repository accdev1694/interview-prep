from crewai import Agent
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from ..tools.web_search_tool import search_company_info
from ..tools.job_description_analyzer import analyze_job_description

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=os.getenv("GOOGLE_API_KEY"))

interviewer_profiler = Agent(
    role= 'Interviewer Background Analyst',
    goal= 'Research interviewer backgrounds, styles, and likely questioning approaches',
    backstory= """You are a specialist in analyzing interviewer profiles, their professional 
    backgrounds, and interview styles. You help candidates understand who they'll be meeting 
    and what types of questions to expect based on the interviewer's role and experience.""",
    tools = [search_company_info, analyze_job_description],
    allow_delegation = False,
    verbose=True,
    llm=llm
)