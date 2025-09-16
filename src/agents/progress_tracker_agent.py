from crewai import Agent
from src.tools.session_saver_tool import SessionSaverTool
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=os.getenv("GOOGLE_API_KEY"))

session_saver_tool = SessionSaverTool()

progress_tracker_agent = Agent(
    role="Progress Tracker Agent",
    goal="Save the user's interview performance data to track progress over time.",
    backstory=(
        "As a meticulous archivist and data manager, you are responsible for maintaining a record of all "
        "interview simulations. You ensure that every session's performance summary and recommendations "
        "are saved correctly, creating a valuable history for users to review their journey and "
        "see how they've improved."
    ),
    tools=[session_saver_tool],
    allow_delegation=False,
    verbose=True,
    llm=llm
)
