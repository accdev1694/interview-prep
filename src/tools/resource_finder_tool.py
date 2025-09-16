from crewai_tools import BaseTool
from pydantic.v1 import BaseModel, Field
from typing import Type

class ResourceFinderToolSchema(BaseModel):
    """Input schema for ResourceFinderTool."""
    recommendations: str = Field(..., description="The list of improvement recommendations.")

class ResourceFinderTool(BaseTool):
    name: str = "Resource Finder Tool"
    description: str = "Finds relevant learning resources (articles, videos) based on improvement recommendations."
    args_schema: Type[BaseModel] = ResourceFinderToolSchema

    def _run(self, recommendations: str) -> str:
        """
        Finds learning resources based on the provided recommendations.
        This is a placeholder. A real implementation would use a search API
        (like Google Search, YouTube Search, etc.) to find actual resources.
        """
        learning_path = "### Personalized Learning Path\n\n"

        if "STAR method" in recommendations:
            learning_path += "**Topic: Mastering the STAR Method**\n"
            learning_path += "- **Article:** [How to Use the STAR Interview Response Technique](https://www.thebalancecareers.com/what-is-the-star-interview-response-technique-2061629)\n"
            learning_path += "- **Video:** [The STAR Method by CareerVidz](https://www.youtube.com/watch?v=g_a0d9K9g6k)\n\n"

        if "concise" in recommendations.lower() or "direct" in recommendations.lower():
            learning_path += "**Topic: Improving Conciseness**\n"
            learning_path += "- **Article:** [How to Be More Concise in Your Professional Communication](https://hbr.org/2018/07/how-to-be-more-concise)\n"
            learning_path += "- **Video:** [Think Fast, Talk Smart: Communication Techniques](https://www.youtube.com/watch?v=HAnw168huqA)\n\n"

        if "filler words" in recommendations.lower():
            learning_path += "**Topic: Eliminating Filler Words**\n"
            learning_path += "- **Article:** [7 Ways to Stop Using Filler Words Like 'Um' and 'Ah'](https://www.inc.com/carmine-gallo/7-ways-to-stop-using-filler-words-like-um-and-ah.html)\n"
            learning_path += "- **Video:** [How to Stop Saying 'Um' and 'Ah' When You Speak](https://www.youtube.com/watch?v=Fw7_p2rV3j8)\n\n"

        if learning_path == "### Personalized Learning Path\n\n":
            return "No specific learning resources were identified. Continue practicing and refining your skills!"

        return learning_path
