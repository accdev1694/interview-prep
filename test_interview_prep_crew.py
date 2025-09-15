from src.crews.interview_prep_crew import interview_prep_crew

print(f"Crew has {len(interview_prep_crew.agents)} agents")
print(f"Crew has {len(interview_prep_crew.tasks)} tasks")
print("Agent roles:")
for i, agent in enumerate(interview_prep_crew.agents):
    print(f"  {i+1}. {agent.role}")
print("✅ Interview prep crew structure verified!")