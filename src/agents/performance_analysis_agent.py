from crewai import Agent
from src.tools.transcript_analyzer_tool import TranscriptAnalyzerTool
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=os.getenv("GOOGLE_API_KEY"))

transcript_analyzer_tool = TranscriptAnalyzerTool()

performance_analysis_agent = Agent(
    role="Performance Analysis Agent",
    goal="Provide a comprehensive analysis of the user's interview performance.",
    backstory=(
        "As a seasoned HR analyst and career coach, you specialize in dissecting interview transcripts "
        "to provide a holistic view of a candidate's performance. You can identify patterns in communication, "
        "the quality of responses, and overall alignment with the job role. Your feedback is crucial for "
        "helping candidates understand their strengths and areas for improvement after an interview."
    ),
    tools=[transcript_analyzer_tool],
    allow_delegation=False,
    verbose=True,
    llm=llm
)
