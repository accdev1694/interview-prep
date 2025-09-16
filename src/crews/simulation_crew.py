from crewai import Crew, Task
from ..agents.simulation_conductor import simulation_conductor
from ..agents.question_generator import question_generator
from ..agents.interviewer_profiler import interviewer_profiler

# Define the tasks for the simulation
simulation_task = Task(
    description="Conduct a mock interview session. Start with an introduction, then ask a series of questions, and conclude the interview.",
    agent=simulation_conductor,
    expected_output="A transcript of the mock interview session."
)

# In a more advanced setup, we would have tasks for each interviewer agent
# For now, the conductor will manage the overall flow.

# Assemble the simulation crew
simulation_crew = Crew(
    agents=[simulation_conductor, question_generator, interviewer_profiler],
    tasks=[simulation_task],
    verbose=True
)
