from crewai import Agent
from src.tools.response_evaluator_tool import ResponseEvaluatorTool

response_evaluator_tool = ResponseEvaluatorTool()

feedback_analyst_agent = Agent(
    role="Feedback Analyst Agent",
    goal="Analyze the user's responses and provide constructive feedback.",
    backstory=(
        "As an expert in communication and interview coaching, you have a keen eye for "
        "identifying strengths and weaknesses in a candidate's responses. You can "
        "provide actionable feedback to help users improve their interviewing skills."
    ),
    tools=[response_evaluator_tool],
    allow_delegation=False,
    verbose=True
)
