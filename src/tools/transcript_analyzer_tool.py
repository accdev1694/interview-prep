from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type, List, Dict

class TranscriptAnalyzerToolSchema(BaseModel):
    """Input schema for TranscriptAnalyzerTool."""
    transcript: List[Dict[str, str]] = Field(..., description="The full transcript of the interview, with each entry being a dictionary containing a 'question' and 'answer'.")

class TranscriptAnalyzerTool(BaseTool):
    name: str = "Transcript Analyzer Tool"
    description: str = "Analyzes a full interview transcript and provides a summary of performance."
    args_schema: Type[BaseModel] = TranscriptAnalyzerToolSchema

    def _run(self, transcript: List[Dict[str, str]]) -> str:
        """
        Analyzes the interview transcript to provide a holistic performance summary.
        This is a placeholder. A real implementation would use an LLM to analyze
        the content for themes, consistency, and overall quality.
        """
        summary = "Overall Interview Performance Summary:\n\n"
        
        num_questions = len(transcript)
        if num_questions == 0:
            return "The transcript is empty. No analysis can be provided."

        total_answer_length = 0
        filler_words_count = 0
        
        for entry in transcript:
            answer = entry.get("answer", "")
            total_answer_length += len(answer.split())
            filler_words_count += answer.lower().count("um")
            filler_words_count += answer.lower().count("uh")

        avg_answer_length = total_answer_length / num_questions if num_questions > 0 else 0

        summary += f"- You answered {num_questions} questions.\n"
        summary += f"- Average answer length was approximately {int(avg_answer_length)} words.\n"
        
        if avg_answer_length < 30:
            summary += "  - Your answers were generally concise. Consider providing more detail and context where appropriate.\n"
        elif avg_answer_length > 150:
            summary += "  - Your answers were quite detailed. Ensure you are staying on topic and not rambling.\n"
        else:
            summary += "  - Your answer length seems appropriate for most interview questions.\n"

        if filler_words_count > 5:
            summary += f"- You used {filler_words_count} filler words ('um', 'uh'). This is an area for improvement to sound more confident.\n"
        else:
            summary += "- You did a good job of avoiding filler words.\n"

        summary += "\nRecommendation: Review your answers to ensure they align with the STAR method (Situation, Task, Action, Result) for behavioral questions. This will add structure and impact to your responses."

        return summary
