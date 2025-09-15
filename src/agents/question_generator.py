from crewai import Agent
from dotenv import load_dotenv
from ..tools.web_search_tool import search_company_info

question_generator = Agent(
    role = 'Interview Question Specialist',
    goal = 'Generate relevant interview questions based on company research and role requirements',
    backstory = """You are an expert at creating realistic interview questions tailored to specific companies and roles. You analyze company culture, recent developments, and job requirements to craft questions that interviewers are likely to ask.""",
    tools = [search_company_info],
    verbose = True,
    allow_delegation = False
)