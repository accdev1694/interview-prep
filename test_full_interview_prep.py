from src.crews.interview_prep_crew import interview_prep_crew

print("🚀 Starting comprehensive interview preparation...")
print("This will take 2-3 minutes as all agents work together...")
print()

result = interview_prep_crew.kickoff(
    inputs={
        'company_name': 'SAS International', 
        'interviewer_names': 'HR Manager, Technical Lead, Department Head', 'job_role': 'CAD Automation Developer'}
)