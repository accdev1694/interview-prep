from crewai import Agent
from ..tools.personality_simulator_tool import personality_simulator_tool
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=os.getenv("GOOGLE_API_KEY"))

simulation_conductor = Agent(
    role="Simulation Conductor",
    goal="Orchestrate a realistic and interactive interview simulation",
    backstory=(
        "As a seasoned interview coach and simulation expert, you specialize in creating "
        "immersive and effective practice environments for job candidates. You guide the "
        "interview flow, manage the panel of AI interviewers, and ensure the simulation "
        "runs smoothly from start to finish."
    ),
    tools=[personality_simulator_tool],
    allow_delegation=False,
    verbose=True,
    llm=llm
)
