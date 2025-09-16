import random
from src.crews.simulation_crew import simulation_crew
from src.config.config import load_interview_config
from src.agents.feedback_analyst import feedback_analyst_agent
from src.agents.question_generator import question_generator_agent
from src.agents.performance_analysis_agent import performance_analysis_agent
from src.agents.improvement_recommender_agent import improvement_recommender_agent
from src.agents.reporting_agent import reporting_agent
from src.agents.learning_path_agent import learning_path_agent
from crewai import Task, Crew

class SimulationManager:
    def __init__(self):
        self.config = load_interview_config()
        self.interview_finished = False
        self.interviewers = self.config["interviewers"]
        self.current_interviewer_index = 0
        self.questions = []
        self.current_question_index = 0
        self.transcript = []
        self.feedback_crew = Crew(
            agents=[feedback_analyst_agent],
            tasks=[],  # Tasks will be created dynamically
            verbose=2
        )
        self.question_crew = Crew(
            agents=[question_generator_agent],
            tasks=[], # Dynamic tasks
            verbose=2
        )
        self.performance_crew = Crew(
            agents=[performance_analysis_agent],
            tasks=[], # Dynamic tasks
            verbose=2
        )
        self.recommendation_crew = Crew(
            agents=[improvement_recommender_agent],
            tasks=[], # Dynamic tasks
            verbose=2
        )
        self.reporting_crew = Crew(
            agents=[reporting_agent],
            tasks=[], # Dynamic tasks
            verbose=2
        )
        self.learning_path_crew = Crew(
            agents=[learning_path_agent],
            tasks=[], # Dynamic tasks
            verbose=2
        )

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

    def _generate_questions(self):
        """
        Generates a list of interview questions using the question generation crew.
        """
        print("Generating interview questions...")
        question_gen_task = Task(
            description=f"""
                Generate a list of 10 interview questions based on the following details:
                - Company: {self.config['company_name']}
                - Job Role: {self.config['job_role']}
                - Job Description: {self.config['job_description']}
                - Interviewers: {self.config['interviewers']}

                The questions should be diverse, covering technical, behavioral, and situational topics.
                Return ONLY the list of questions, nothing else.
            """,
            agent=question_generator_agent,
            expected_output="A python list of 10 string questions."
        )
        self.question_crew.tasks = [question_gen_task]
        question_list_str = self.question_crew.kickoff()
        
        # The output might be a string representation of a list, so we need to parse it.
        try:
            # A simple eval is risky, but for this controlled environment it's a quick solution.
            # A safer method would be ast.literal_eval.
            import ast
            self.questions = ast.literal_eval(question_list_str)
            print("Questions generated successfully.")
        except (ValueError, SyntaxError):
            print("Error parsing the generated questions. Using fallback questions.")
            # Fallback to a simpler split if eval fails
            self.questions = [q.strip() for q in question_list_str.split('\n') if q.strip()]


    def start_simulation(self):
        """
        Starts and manages the interactive interview simulation.
        """
        print("🚀 Starting Interview Simulation...")
        print("Type 'quit' at any time to end the interview.")
        print("-" * 50)

        self._generate_questions()

        if not self.questions:
            print("Could not generate questions. Aborting simulation.")
            return

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
        
        while not self.interview_finished and self.current_question_index < len(self.questions):
            current_question = self.questions[self.current_question_index]
            print(f"\nQuestion: {current_question}")
            
            user_response = input("Your Answer: ")

            if user_response.lower() == 'quit':
                self.interview_finished = True
                print("AI Interviewer: Thank you for your time. The interview has now concluded.")
                continue

            # Store the interaction in the transcript
            self.transcript.append({"question": current_question, "answer": user_response})

            # Create and run the feedback task
            feedback_task = Task(
                description=f"Evaluate the user's answer to the question: '{current_question}'. The user's answer is: '{user_response}'",
                agent=feedback_analyst_agent,
                expected_output="Constructive feedback on the user's response."
            )

            self.feedback_crew.tasks = [feedback_task]
            feedback_result = self.feedback_crew.kickoff()

            print("\n" + "-"*20 + " FEEDBACK " + "-"*20)
            print(feedback_result)
            print("-" * 50 + "\n")

            self.current_question_index += 1
            if self.current_question_index >= len(self.questions):
                self.interview_finished = True
                print("AI Interviewer: That was the last question. Thank you for your time.")
                continue

            # Move to the next interviewer for the next question
            self.next_interviewer()
            current_interviewer = self.get_current_interviewer()
            print(f"{current_interviewer['name']} ({current_interviewer['role']}): Thank you for that response. Let's move to the next question.")

        self._run_performance_analysis()

    def _run_performance_analysis(self):
        """
        Runs the performance analysis crew on the full interview transcript.
        """
        if not self.transcript:
            print("\nNo transcript was recorded. Skipping performance analysis.")
            return

        print("\n" + "="*20 + " FINAL PERFORMANCE ANALYSIS " + "="*20)
        
        analysis_task = Task(
            description="Analyze the provided interview transcript and give a holistic summary of the user's performance. Identify strengths, weaknesses, and provide actionable recommendations for improvement.",
            agent=performance_analysis_agent,
            expected_output="A comprehensive performance review.",
            inputs={'transcript': self.transcript}
        )

        self.performance_crew.tasks = [analysis_task]
        final_summary = self.performance_crew.kickoff()

        print(final_summary)
        print("=" * 70)

        self._run_improvement_recommendations(final_summary)

    def _run_improvement_recommendations(self, performance_summary: str):
        """
        Runs the improvement recommendation crew based on the performance summary.
        """
        print("\n" + "💡" * 20 + " PERSONALIZED RECOMMENDATIONS " + "💡" * 20)

        recommendation_task = Task(
            description="Based on the provided performance summary, generate a list of personalized, actionable recommendations for the user to improve their interview skills.",
            agent=improvement_recommender_agent,
            expected_output="A list of specific, actionable recommendations.",
            inputs={'performance_summary': performance_summary}
        )

        self.recommendation_crew.tasks = [recommendation_task]
        recommendations = self.recommendation_crew.kickoff()

        print(recommendations)
        print("=" * 70)

        self._generate_report(performance_summary, recommendations)
        self._generate_learning_path(recommendations)

    def _generate_report(self, performance_summary: str, recommendations: str):
        """
        Generates and saves a detailed interview report.
        """
        print("\n" + "📊" * 20 + " GENERATING FINAL REPORT " + "📊" * 20)

        report_task = Task(
            description="Generate a comprehensive, well-structured report based on the interview performance summary, recommendations, and full transcript.",
            agent=reporting_agent,
            expected_output="A confirmation message with the path to the saved report file.",
            inputs={
                'performance_summary': performance_summary,
                'recommendations': recommendations,
                'transcript': self.transcript
            }
        )

        self.reporting_crew.tasks = [report_task]
        report_result = self.reporting_crew.kickoff()

        print(report_result)
        print("=" * 70)

    def _generate_learning_path(self, recommendations: str):
        """
        Generates a learning path with resources based on the recommendations.
        """
        print("\n" + "📚" * 20 + " CUSTOMIZED LEARNING PATH " + "📚" * 20)

        learning_path_task = Task(
            description="Based on the provided improvement recommendations, find relevant articles and videos to create a personalized learning path.",
            agent=learning_path_agent,
            expected_output="A markdown-formatted learning path with links to resources.",
            inputs={'recommendations': recommendations}
        )

        self.learning_path_crew.tasks = [learning_path_task]
        learning_path = self.learning_path_crew.kickoff()

        print(learning_path)
        print("=" * 70)


if __name__ == '__main__':
    manager = SimulationManager()
    manager.start_simulation()
