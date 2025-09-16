from crewai import Agent
from src.tools.report_generator_tool import ReportGeneratorTool

report_generator_tool = ReportGeneratorTool()

reporting_agent = Agent(
    role="Reporting Agent",
    goal="Generate a detailed, structured report of the user's interview performance, including a readiness score.",
    backstory=(
        "As a data visualization and reporting specialist, you are skilled at transforming raw performance "
        "data into beautiful, insightful reports. You create comprehensive summaries that are easy to "
        "understand, highlighting key metrics, performance scores, and actionable feedback to provide a "
        "full picture of a candidate's readiness."
    ),
    tools=[report_generator_tool],
    allow_delegation=False,
    verbose=True
)
