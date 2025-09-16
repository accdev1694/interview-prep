from crewai import Agent
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from ..tools.web_search_tool import search_company_info
from ..tools.job_description_analyzer import analyze_job_description

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=os.getenv("GOOGLE_API_KEY"))

question_generator = Agent(
    role = 'Interview Question Specialist',
    goal = 'Generate relevant interview questions based on company research and role requirements',
    backstory = """You are an expert at creating realistic interview questions tailored to specific companies and roles. You analyze company culture, recent developments, and job requirements to craft questions that interviewers are likely to ask.""",
    tools = [search_company_info, analyze_job_description],
    verbose = True,
    allow_delegation = False,
    llm=llm
)