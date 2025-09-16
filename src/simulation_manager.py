import random
import ast
from crewai import Task, Crew
from src.config.config import load_interview_config
from src.agents.feedback_analyst import feedback_analyst_agent
from src.agents.question_generator import question_generator as question_generator_agent
from src.agents.performance_analysis_agent import performance_analysis_agent
from src.agents.improvement_recommender_agent import improvement_recommender_agent
from src.agents.reporting_agent import reporting_agent
from src.agents.learning_path_agent import learning_path_agent

class SimulationManager:
    """
    Manages the entire interview simulation, from question generation to final reporting.
    """
    def __init__(self):
        """Initializes the SimulationManager, loading configuration and setting up all necessary crews."""
        self.config = load_interview_config()
        self.interview_finished = False
        self.interviewers = self.config.get("interviewers", [])
        self.current_interviewer_index = 0
        self.questions = []
        self.current_question_index = 0
        self.transcript = []
        self._initialize_crews()

    def _initialize_crews(self):
        """Initializes all the CrewAI crews with their respective agents."""
        self.question_crew = Crew(agents=[question_generator_agent], tasks=[], verbose=2)
        self.feedback_crew = Crew(agents=[feedback_analyst_agent], tasks=[], verbose=2)
        self.performance_crew = Crew(agents=[performance_analysis_agent], tasks=[], verbose=2)
        self.recommendation_crew = Crew(agents=[improvement_recommender_agent], tasks=[], verbose=2)
        self.reporting_crew = Crew(agents=[reporting_agent], tasks=[], verbose=2)
        self.learning_path_crew = Crew(agents=[learning_path_agent], tasks=[], verbose=2)

    def _run_crew(self, crew, task):
        """A generic method to run a task on a given crew with error handling."""
        try:
            crew.tasks = [task]
            result = crew.kickoff()
            return result
        except Exception as e:
            print(f"An error occurred in {crew.__class__.__name__}: {e}")
            return f"Could not complete the task due to an error: {e}"

    def get_current_interviewer(self):
        """Gets the current interviewer based on a round-robin index."""
        if not self.interviewers:
            return {"name": "Interviewer", "role": "N/A"}
        return self.interviewers[self.current_interviewer_index]

    def next_interviewer(self):
        """Moves to the next interviewer in a round-robin fashion."""
        if self.interviewers:
            self.current_interviewer_index = (self.current_interviewer_index + 1) % len(self.interviewers)

    def _generate_questions(self):
        """Generates a list of interview questions using the question generation crew."""
        print("Generating interview questions...")
        try:
            task = Task(
                description=f"""
                    Generate a list of 10 interview questions based on the following details:
                    - Company: {self.config.get('company_name')}
                    - Job Role: {self.config.get('job_role')}
                    - Job Description: {self.config.get('job_description')}
                    - Interviewers: {self.interviewers}
                    The questions should be diverse, covering technical, behavioral, and situational topics.
                    Return ONLY the list of questions as a Python list of strings.
                """,
                agent=question_generator_agent,
                expected_output="A Python list of 10 string questions."
            )
            question_list_str = self._run_crew(self.question_crew, task)
            
            # The output might be a string representation of a list, so we parse it safely.
            self.questions = ast.literal_eval(question_list_str)
            print("Questions generated successfully.")
        except (ValueError, SyntaxError, TypeError) as e:
            print(f"Error parsing generated questions: {e}. Using fallback split.")
            self.questions = [q.strip() for q in str(question_list_str).split('\n') if q.strip()]
        except Exception as e:
            print(f"An unexpected error occurred during question generation: {e}")
            self.questions = []

    def start_simulation(self, on_question, on_feedback, on_finish):
        """Starts the interview simulation, generates questions, and sends the intro message."""
        print("🚀 Starting Interview Simulation...")
        on_finish("🚀 Starting Interview Simulation...")

        self._generate_questions()

        if not self.questions:
            on_finish("Could not generate questions due to an error. Please check the logs. Aborting simulation.")
            return

        interviewer = self.get_current_interviewer()
        intro = f"{interviewer['name']} ({interviewer['role']}): Hello, thank you for coming in today. Let's start with a few questions."
        on_question(intro, is_intro=True)

    def ask_next_question(self, user_response=None):
        """
        Processes the user's response, provides feedback, and yields the next question or final results.
        """
        try:
            if user_response:
                self._process_user_response(user_response)
                yield from self._get_feedback(user_response)

            if self.current_question_index < len(self.questions):
                yield self._get_next_question()
            else:
                yield from self._finalize_interview()
        except Exception as e:
            print(f"An error occurred in ask_next_question: {e}")
            yield {"type": "error", "content": f"Sorry, an unexpected error occurred: {e}"}

    def _process_user_response(self, user_response):
        """Adds the last question and user's response to the transcript."""
        last_question = self.questions[self.current_question_index - 1]
        self.transcript.append({"question": last_question, "answer": user_response})

    def _get_feedback(self, user_response):
        """Generates and yields feedback for the user's response."""
        last_question = self.transcript[-1]["question"]
        task = Task(
            description=f"Evaluate the user's answer: '{user_response}' for the question: '{last_question}'.",
            agent=feedback_analyst_agent,
            expected_output="Constructive feedback on the user's response."
        )
        feedback_result = self._run_crew(self.feedback_crew, task)
        yield {"type": "feedback", "content": f"--- FEEDBACK ---\n{feedback_result}\n"}

    def _get_next_question(self):
        """Formats and returns the next question in the queue."""
        question = self.questions[self.current_question_index]
        self.current_question_index += 1
        interviewer = self.get_current_interviewer()
        self.next_interviewer()
        return {"type": "question", "content": f"{interviewer['name']} ({interviewer['role']}): {question}"}

    def _finalize_interview(self):
        """Runs all post-interview analysis and yields the final results."""
        self.interview_finished = True
        yield {"type": "analysis_started", "content": "AI Interviewer: That was the last question. Thank you. Analyzing your performance..."}
        
        summary = self._run_performance_analysis()
        recommendations = self._run_improvement_recommendations(summary)
        report_result = self._generate_report(summary, recommendations)
        learning_path = self._generate_learning_path(recommendations)

        report_path = report_result.split("Report saved to:")[-1].strip() if "Report saved to:" in report_result else None

        yield {
            "type": "final_results",
            "report_path": report_path,
            "learning_path": learning_path,
            "summary": summary
        }

    def _run_performance_analysis(self):
        """Runs the performance analysis crew."""
        if not self.transcript: return "No transcript recorded."
        task = Task(
            description="Analyze the interview transcript and provide a holistic performance summary.",
            agent=performance_analysis_agent,
            expected_output="A comprehensive performance review.",
            inputs={'transcript': self.transcript}
        )
        return self._run_crew(self.performance_crew, task)

    def _run_improvement_recommendations(self, summary: str):
        """Runs the improvement recommendation crew."""
        task = Task(
            description="Generate personalized recommendations based on the performance summary.",
            agent=improvement_recommender_agent,
            expected_output="A list of actionable recommendations.",
            inputs={'performance_summary': summary}
        )
        return self._run_crew(self.recommendation_crew, task)

    def _generate_report(self, summary: str, recommendations: str):
        """Generates a detailed interview report."""
        task = Task(
            description="Generate a comprehensive report from the summary and recommendations.",
            agent=reporting_agent,
            expected_output="A confirmation message with the path to the saved report file.",
            inputs={'performance_summary': summary, 'recommendations': recommendations, 'transcript': self.transcript}
        )
        return self._run_crew(self.reporting_crew, task)

    def _generate_learning_path(self, recommendations: str):
        """Generates a learning path with resources."""
        task = Task(
            description="Generate a learning path based on the provided recommendations.",
            agent=learning_path_agent,
            expected_output="A markdown-formatted learning path with relevant resources.",
            inputs={'recommendations': recommendations}
        )
        return self._run_crew(self.learning_path_crew, task)

if __name__ == '__main__':
    # This part is for testing purposes and won't be executed by the Streamlit app.
    manager = SimulationManager()
    # The start_simulation method in the app requires callbacks, so direct execution here is not practical.
    print("SimulationManager is ready for use in the application.")
