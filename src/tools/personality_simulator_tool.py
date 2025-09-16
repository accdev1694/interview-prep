from crewai_tools import BaseTool
import random

class PersonalitySimulatorTool(BaseTool):
    name: str = "Interviewer Personality Simulator"
    description: str = "Simulates a personality for an interviewer based on their role."

    def _run(self, interviewer_role: str) -> str:
        personalities = {
            "HR Manager": [
                "Friendly and conversational, focused on cultural fit and behavioral questions.",
                "Formal and structured, follows a strict script of questions.",
                "Enthusiastic and energetic, looking for passion and motivation."
            ],
            "Technical Lead": [
                "Direct and to-the-point, focused on technical skills and problem-solving abilities.",
                "Collaborative and curious, interested in your thought process and how you work with others.",
                "Skeptical and challenging, will probe for weaknesses in your knowledge."
            ],
            "Department Head": [
                "Big-picture oriented, focused on strategic thinking and long-term vision.",
                "Pragmatic and results-driven, wants to know how you can add value to the team.",
                "Personable and engaging, looking for leadership potential and team dynamics."
            ],
            "default": [
                "A typical interviewer with a mix of technical and behavioral questions.",
                "A very quiet interviewer who provides little feedback.",
                "A very friendly interviewer who seems more interested in a casual chat."
            ]
        }

        # Get the list of personalities for the given role, or use the default if the role is not found
        personality_list = personalities.get(interviewer_role, personalities["default"])
        
        # Return a random personality from the list
        return random.choice(personality_list)

# Instantiate the tool
personality_simulator_tool = PersonalitySimulatorTool()
