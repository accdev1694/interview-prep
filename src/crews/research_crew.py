from crewai import Crew, Task
from src.agents.research_agent import research_agent

company_research_task = Task(
    description="Research basic information about {company_name}",
    agent=research_agent,
    expected_output='A brief summary of the company'
)

research_crew = Crew(
    agents=[research_agent],
    tasks=[company_research_task]
)