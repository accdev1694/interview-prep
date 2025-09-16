from crewai import Agent
from src.tools.response_evaluator_tool import ResponseEvaluatorTool
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=os.getenv("GOOGLE_API_KEY"))

response_evaluator_tool = ResponseEvaluatorTool()

feedback_analyst_agent = Agent(
    role="Feedback Analyst Agent",
    goal="Analyze the user's responses and provide constructive feedback.",
    backstory=(
        "As an expert in communication and interview coaching, you have a keen eye for "
        "identifying strengths and weaknesses in a candidate's responses. You can "
        "provide actionable feedback to help users improve their interviewing skills."
    ),
    tools=[response_evaluator_tool],
    allow_delegation=False,
    verbose=True,
    llm=llm
)
