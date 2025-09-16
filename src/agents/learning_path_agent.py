from crewai import Agent
from src.tools.resource_finder_tool import ResourceFinderTool
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=os.getenv("GOOGLE_API_KEY"))

resource_finder_tool = ResourceFinderTool()

learning_path_agent = Agent(
    role="Learning Path Agent",
    goal="Generate a personalized learning path with relevant resources based on improvement recommendations.",
    backstory=(
        "As a curriculum developer and content curator, you have a talent for finding the perfect resources "
        "to help someone learn a new skill. You can take a list of improvement areas and find high-quality "
        "articles, videos, and tutorials to create a customized learning plan that guides users on their "
        "journey to mastery."
    ),
    tools=[resource_finder_tool],
    allow_delegation=False,
    verbose=True,
    llm=llm
)
