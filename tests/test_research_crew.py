from src.crews.research_crew import company_research_task, research_crew

print("Research Crew Loaded Succesfully")
print(f"Crew Task 1: {company_research_task.description}")

print(f"Crew has {len(research_crew.agents)} agent(s)")
print(f"Crew has {len(research_crew.tasks)} task(s)")
print(f"Agent name: {research_crew.agents[0].role}")
print(f"Task description: {research_crew.tasks[0].description}")
print("✅ Crew structure looks good!")