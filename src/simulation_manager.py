import random
from src.crews.simulation_crew import simulation_crew
from src.config.config import load_interview_config

class SimulationManager:
    def __init__(self):
        self.config = load_interview_config()
        self.interview_finished = False
        self.interviewers = self.config["interviewers"]
        self.current_interviewer_index = 0

    def get_current_interviewer(self):
        """
        Gets the current interviewer based on the round-robin index.
        """
        return self.interviewers[self.current_interviewer_index]

    def next_interviewer(self):
        """
        Moves to the next interviewer in a round-robin fashion.
        """
        self.current_interviewer_index = (self.current_interviewer_index + 1) % len(self.interviewers)

    def start_simulation(self):
        """
        Starts and manages the interactive interview simulation.
        """
        print("🚀 Starting Interview Simulation...")
        print("Type 'quit' at any time to end the interview.")
        print("-" * 50)

        # Initial context for the simulation crew
        inputs = {
            "company_name": self.config["company_name"],
            "job_role": self.config["job_role"],
            "interviewers": self.interviewers,
            "job_description": self.config["job_description"]
        }

        # This is a simplified loop. In a real scenario, the crew's tasks would generate questions.
        # For now, we'll simulate the flow.
        
        # Kick off the crew to get the first question (or introduction)
        # Note: This is a conceptual step. The actual implementation will depend on how the crew is designed to be interactive.
        # For now, we will mock this behavior.
        
        current_interviewer = self.get_current_interviewer()
        print(f"{current_interviewer['name']} ({current_interviewer['role']}): Hello, thank you for coming in today. Let's start with a few questions.")

        while not self.interview_finished:
            user_response = input("Your Answer: ")

            if user_response.lower() == 'quit':
                self.interview_finished = True
                print("AI Interviewer: Thank you for your time. The interview has now concluded.")
                continue

            # Here, we would send the user's response back to the crew and get the next question.
            # For example: result = simulation_crew.kickoff(inputs={'user_response': user_response})
            # The crew would then process the response and generate a follow-up question.
            
            # For now, we'll just simulate a generic follow-up.
            self.next_interviewer()
            current_interviewer = self.get_current_interviewer()
            print(f"{current_interviewer['name']} ({current_interviewer['role']}): Thank you for that response. My next question is...")


if __name__ == '__main__':
    manager = SimulationManager()
    manager.start_simulation()
