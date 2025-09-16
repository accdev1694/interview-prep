from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type

class ResponseEvaluatorToolSchema(BaseModel):
    """Input schema for ResponseEvaluatorTool."""
    question: str = Field(..., description="The interview question that was asked.")
    answer: str = Field(..., description="The user's answer to the interview question.")

class ResponseEvaluatorTool(BaseTool):
    name: str = "Response Evaluator Tool"
    description: str = "Evaluates a user's answer to an interview question and provides feedback."
    args_schema: Type[BaseModel] = ResponseEvaluatorToolSchema

    def _run(self, question: str, answer: str) -> str:
        """
        Evaluates the user's response to a given interview question.
        This is a placeholder and should be implemented with a more sophisticated
        evaluation logic, potentially using an LLM to grade the response based on
        clarity, relevance, and completeness.
        """
        # Placeholder logic for evaluation
        feedback = f"Feedback for your answer to '{question}':\n"
        if len(answer.split()) < 20:
            feedback += "- Your answer is a bit short. Consider elaborating further.\n"
        if "um" in answer.lower() or "uh" in answer.lower():
            feedback += "- You used filler words like 'um' or 'uh'. Try to speak more confidently.\n"
        if not any(keyword in answer.lower() for keyword in ["experience", "project", "skill", "team"]):
             feedback += "- Consider linking your answer back to your specific experiences, projects, or skills.\n"

        if feedback == f"Feedback for your answer to '{question}':\n":
            return "Great answer! It was clear, concise, and directly addressed the question."
        else:
            return feedback

