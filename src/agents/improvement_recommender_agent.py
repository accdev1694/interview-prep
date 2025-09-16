from crewai import Agent
from src.tools.skill_gap_analyzer_tool import SkillGapAnalyzerTool

skill_gap_analyzer_tool = SkillGapAnalyzerTool()

improvement_recommender_agent = Agent(
    role="Improvement Recommender Agent",
    goal="Analyze a performance summary and provide personalized recommendations for improvement.",
    backstory=(
        "As a dedicated career development coach, you excel at turning feedback into actionable steps. "
        "You can take a performance analysis, identify the key areas that need work, and suggest "
        "concrete resources, exercises, or strategies to help a candidate improve. Your recommendations "
        "are practical, encouraging, and tailored to the individual's needs."
    ),
    tools=[skill_gap_analyzer_tool],
    allow_delegation=False,
    verbose=True
)
