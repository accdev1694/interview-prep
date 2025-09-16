from src.crews.interview_prep_crew import interview_prep_crew
from src.config.config import load_interview_config

print("🚀 Starting comprehensive interview preparation...")
print("This will take 2-3 minutes as all agents work together...")
print()

# Load the interview configuration from the config.json file
config = load_interview_config()

# Extract the interviewer names from the config
interviewer_names = ", ".join([interviewer['name'] for interviewer in config['interviewers']])

result = interview_prep_crew.kickoff(
    inputs={
        'company_name': config['company_name'],
        'interviewer_names': interviewer_names,
        'job_role': config['job_role'],
        'job_description': config['job_description']
    }
)
