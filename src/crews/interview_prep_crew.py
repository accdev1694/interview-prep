from crewai import Crew, Task
from ..agents.research_agent import research_agent
from ..agents.interviewer_profiler import interviewer_profiler
from ..agents.question_generator import question_generator

company_research_task = Task(
    description = 'Research comprehensive information about {company_name} including recent developments, culture, business focus, current market challenges, competitive pressures, and strategic obstacles they are facing',
    agent = research_agent,
    expected_output = 'Detailed company profile including recent news, market challenges, competitive threats, and strategic obstacles'
)

interviewer_profiling_task = Task(
    description = 'Research the professional backgrounds, career paths, expertise areas, and management styles of {interviewer_names} at {company_name}. Based on their roles and experience, predict specific types of questions they are likely to ask',
    agent = interviewer_profiler,
    expected_output = 'Detailed interviewer profiles with predicted questions each interviewer is likely to ask based on their background and role'
)

question_generation_task = Task(
    description = 'Generate relevant interview questions for {job_role} position at {company_name} based on company research',
    agent = question_generator,
    expected_output = 'List of tailored interview questions'
)


interview_prep_crew = Crew(
    agents = [research_agent, interviewer_profiler, question_generator],
    tasks = [company_research_task, interviewer_profiling_task, question_generation_task],
    verbose = True
)