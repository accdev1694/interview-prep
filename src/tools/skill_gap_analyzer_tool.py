from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type

class SkillGapAnalyzerToolSchema(BaseModel):
    """Input schema for SkillGapAnalyzerTool."""
    performance_summary: str = Field(..., description="The performance summary from the analysis agent.")

class SkillGapAnalyzerTool(BaseTool):
    name: str = "Skill Gap Analyzer Tool"
    description: str = "Analyzes a performance summary to identify skill gaps and recommend improvements."
    args_schema: Type[BaseModel] = SkillGapAnalyzerToolSchema

    def _run(self, performance_summary: str) -> str:
        """
        Analyzes the performance summary to generate actionable recommendations.
        This is a placeholder. A real implementation would use an LLM to parse the
        summary and suggest specific, targeted advice.
        """
        recommendations = "Personalized Recommendations for Improvement:\n\n"

        if "concise" in performance_summary.lower() or "short" in performance_summary.lower():
            recommendations += "- Practice expanding on your answers. Use the STAR method (Situation, Task, Action, Result) to structure your responses and provide more depth. Try recording yourself answering common questions to check for length and detail.\n"
        
        if "ramble" in performance_summary.lower() or "detailed" in performance_summary.lower():
            recommendations += "- Work on being more direct. Before answering, take a moment to think about the core of the question and structure your answer around it. Practice summarizing your key points at the end of your response.\n"

        if "filler words" in performance_summary.lower():
            recommendations += "- To reduce filler words, practice speaking more slowly and deliberately. Pause silently instead of using 'um' or 'uh'. Awareness is the first step, so you're already on the right track!\n"

        if "STAR method" in performance_summary:
            recommendations += "- You've received a recommendation to use the STAR method. Focus on practicing this for behavioral questions. For each project on your resume, write down a few STAR-based stories.\n"

        if recommendations == "Personalized Recommendations for Improvement:\n\n":
            return "Your performance was strong! Continue to refine your answers and practice with a variety of questions."
        
        return recommendations
