import os
from datetime import datetime
from crewai_tools import BaseTool
from pydantic.v1 import BaseModel, Field
from typing import Type

class SessionSaverToolSchema(BaseModel):
    """Input schema for SessionSaverTool."""
    performance_summary: str = Field(..., description="The final performance summary from the analysis agent.")
    recommendations: str = Field(..., description="The personalized recommendations for improvement.")

class SessionSaverTool(BaseTool):
    name: str = "Session Saver Tool"
    description: str = "Saves the interview performance summary and recommendations to a file."
    args_schema: Type[BaseModel] = SessionSaverToolSchema

    def _run(self, performance_summary: str, recommendations: str) -> str:
        """
        Saves the session summary and recommendations to a timestamped markdown file.
        """
        sessions_dir = "data/sessions"
        os.makedirs(sessions_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(sessions_dir, f"interview_session_{timestamp}.md")

        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write("# Interview Session Summary\n\n")
                f.write(f"**Session Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                f.write("## Overall Performance Analysis\n")
                f.write(performance_summary)
                f.write("\n\n")
                f.write("## Personalized Recommendations\n")
                f.write(recommendations)

            return f"Session successfully saved to {filename}"
        except Exception as e:
            return f"Error saving session: {e}"
