import random
from src.crews.simulation_crew import simulation_crew
from src.config.config import load_interview_config
from src.agents.feedback_analyst import feedback_analyst_agent
from src.agents.question_generator import question_generator as question_generator_agent
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


    def start_simulation(self, on_question, on_feedback, on_finish):
        """
        Starts and manages the interactive interview simulation, using callbacks for UI updates.
        """
        print("🚀 Starting Interview Simulation...")
        on_finish("🚀 Starting Interview Simulation...")

        self._generate_questions()

        if not self.questions:
            on_finish("Could not generate questions. Aborting simulation.")
            return

        current_interviewer = self.get_current_interviewer()
        intro_message = f"{current_interviewer['name']} ({current_interviewer['role']}): Hello, thank you for coming in today. Let's start with a few questions."
        on_question(intro_message, is_intro=True)

    def ask_next_question(self, user_response=None):
        """
        Asks the next question or provides feedback based on the user's response.
        """
        if user_response:
            # Provide feedback on the previous answer
            last_question = self.questions[self.current_question_index -1]
            self.transcript.append({"question": last_question, "answer": user_response})
            
            feedback_task = Task(
                description=f"Evaluate the user's answer to the question: '{last_question}'. The user's answer is: '{user_response}'",
                agent=feedback_analyst_agent,
                expected_output="Constructive feedback on the user's response."
            )
            self.feedback_crew.tasks = [feedback_task]
            feedback_result = self.feedback_crew.kickoff()
            yield {"type": "feedback", "content": f"--- FEEDBACK ---\n{feedback_result}\n"}

        if self.current_question_index < len(self.questions):
            current_question = self.questions[self.current_question_index]
            self.current_question_index += 1
            
            current_interviewer = self.get_current_interviewer()
            self.next_interviewer()
            
            yield {"type": "question", "content": f"{current_interviewer['name']} ({current_interviewer['role']}): {current_question}"}
        else:
            self.interview_finished = True
            yield {"type": "analysis_started", "content": "AI Interviewer: That was the last question. Thank you for your time. Analyzing your performance..."}
            
            # Run post-interview analysis
            final_summary = self._run_performance_analysis()
            recommendations = self._run_improvement_recommendations(final_summary)
            report_result = self._generate_report(final_summary, recommendations)
            learning_path = self._generate_learning_path(recommendations)

            report_path = None
            if "Report saved to:" in report_result:
                report_path = report_result.split("Report saved to:")[-1].strip()

            yield {
                "type": "final_results",
                "report_path": report_path,
                "learning_path": learning_path
            }

    def _run_performance_analysis(self):
        """
        Runs the performance analysis crew on the full interview transcript.
        """
        if not self.transcript:
            return "No transcript recorded."

        analysis_task = Task(
            description="Analyze the provided interview transcript and give a holistic summary of the user's performance.",
            agent=performance_analysis_agent,
            expected_output="A comprehensive performance review.",
            inputs={'transcript': self.transcript}
        )
        self.performance_crew.tasks = [analysis_task]
        return self.performance_crew.kickoff()

    def _run_improvement_recommendations(self, performance_summary: str):
        """
        Runs the improvement recommendation crew.
        """
        recommendation_task = Task(
            description="Based on the performance summary, generate personalized recommendations.",
            agent=improvement_recommender_agent,
            expected_output="A list of actionable recommendations.",
            inputs={'performance_summary': performance_summary}
        )
        self.recommendation_crew.tasks = [recommendation_task]
        return self.recommendation_crew.kickoff()

    def _generate_report(self, performance_summary: str, recommendations: str):
        """
        Generates and saves a detailed interview report.
        """
        report_task = Task(
            description="Generate a comprehensive report based on the summary and recommendations.",
            agent=reporting_agent,
            expected_output="A confirmation message with the path to the saved report file.",
            inputs={
                'performance_summary': performance_summary,
                'recommendations': recommendations,
                'transcript': self.transcript
            }
        )
        self.reporting_crew.tasks = [report_task]
        return self.reporting_crew.kickoff()

    def _generate_learning_path(self, recommendations: str):
        """
        Generates a learning path with resources.
        """
        learning_path_task = Task(
            description="Generate a learning path based on the recommendations.",
            agent=learning_path_agent,
            expected_output="A markdown-formatted learning path.",
            inputs={'recommendations': recommendations}
        )
        self.learning_path_crew.tasks = [learning_path_task]
        return self.learning_path_crew.kickoff()


if __name__ == '__main__':
    manager = SimulationManager()
    manager.start_simulation()
