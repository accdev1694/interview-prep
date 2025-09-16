from src.crews.research_crew import research_crew

print("✈️ Starting Execution")
print("This may take some time...")

result = research_crew.kickoff(
    inputs={"company_name": "SAS International"}
)

print("✅ Crew execution completed!")
f"Result: {result}"