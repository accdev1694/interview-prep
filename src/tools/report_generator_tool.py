import os
from datetime import datetime
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type, List, Dict

class ReportGeneratorToolSchema(BaseModel):
    """Input schema for ReportGeneratorTool."""
    performance_summary: str = Field(..., description="The final performance summary from the analysis agent.")
    recommendations: str = Field(..., description="The personalized recommendations for improvement.")
    transcript: List[Dict[str, str]] = Field(..., description="The full interview transcript.")

class ReportGeneratorTool(BaseTool):
    name: str = "Report Generator Tool"
    description: str = "Generates and saves a detailed interview report in Markdown format."
    args_schema: Type[BaseModel] = ReportGeneratorToolSchema

    def _calculate_readiness_score(self, summary: str, transcript: List[Dict[str, str]]) -> int:
        """
        Calculates a readiness score based on performance metrics.
        This is a placeholder logic. A real implementation would be more nuanced.
        """
        score = 70  # Start with a base score

        # Deduct for filler words
        filler_words = sum(entry.get("answer", "").lower().count(word) for entry in transcript for word in ["um", "uh"])
        score -= filler_words * 2

        # Adjust based on summary sentiment
        if "concise" in summary.lower() or "short" in summary.lower():
            score -= 5
        if "ramble" in summary.lower():
            score -= 10
        if "strong" in summary.lower() or "excellent" in summary.lower():
            score += 15
        
        # Ensure score is within bounds
        return max(0, min(100, score))

    def _run(self, performance_summary: str, recommendations: str, transcript: List[Dict[str, str]]) -> str:
        """
        Generates a detailed report and saves it to a file.
        """
        reports_dir = "data/reports"
        os.makedirs(reports_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(reports_dir, f"interview_report_{timestamp}.md")

        readiness_score = self._calculate_readiness_score(performance_summary, transcript)

        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(f"# Interview Performance Report\n\n")
                f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"**Interview Readiness Score:** {readiness_score}/100\n\n")
                
                f.write("## 1. Overall Performance Summary\n")
                f.write(f"{performance_summary}\n\n")
                
                f.write("## 2. Personalized Recommendations\n")
                f.write(f"{recommendations}\n\n")
                
                f.write("---\n\n")
                f.write("## 3. Full Interview Transcript\n\n")
                for i, entry in enumerate(transcript):
                    f.write(f"**Question {i+1}:** {entry.get('question', 'N/A')}\n")
                    f.write(f"**Your Answer:** {entry.get('answer', 'N/A')}\n\n")

            return f"Detailed report successfully generated and saved to {filename}"
        except Exception as e:
            return f"Error generating report: {e}"
