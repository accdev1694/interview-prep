from crewai.tools import tool

@tool
def analyze_job_description(job_description: str):
    """Analyze job description to extract key requirements, skills, and responsibilities"""
    key_skills = "extract skills from description"
    responsibilities = "extract main duties"
    requirements = "extract must-haves"