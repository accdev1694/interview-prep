# AI Interview Preparation Assistant

This project is a sophisticated, multi-agent AI system designed to help users practice for job interviews. It simulates a realistic interview experience, provides real-time feedback, and delivers a comprehensive performance analysis with a personalized learning path.

## Features

- **Dynamic Interview Simulation**: Generates interview questions based on a specific job description and company profile.
- **Multi-Interviewer Experience**: Simulates a round-robin interview with multiple personas (e.g., Hiring Manager, Senior Engineer).
- **Real-time Feedback**: Provides instant, constructive feedback on user responses.
- **Comprehensive Performance Analysis**: At the end of the interview, it generates a detailed report covering strengths, weaknesses, and a readiness score.
- **Personalized Learning Paths**: Suggests relevant articles and videos to help users improve in specific areas.
- **Interactive Web UI**: A user-friendly Streamlit application for a seamless experience.

## Tech Stack

- **Backend**: Python, CrewAI (Agentic Framework)
- **Frontend**: Streamlit
- **Core Libraries**: LangChain, Pydantic, python-dotenv

## Getting Started

### Prerequisites

- Python 3.8+
- Pip for package management
- A virtual environment tool (e.g., `venv`)

### Setup Instructions

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/accdev1694/interview-prep.git
    cd interview-prep
    ```

2.  **Create and activate a virtual environment:**

    ```bash
    # For Windows
    python -m venv venv
    .\venv\Scripts\activate

    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the required dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure your API Keys:**
    - Create a `.env` file in the root directory of the project.
    - Add your API keys for the language models you intend to use. For example:
      ```
      OPENAI_API_KEY="your_openai_api_key"
      GOOGLE_API_KEY="your_google_api_key"
      TAVILY_API_KEY="your_tavily_api_key"
      ```
      _Note: The application uses Tavily for web searches in the learning path generation._

### Running the Application

1.  **Start the Streamlit application:**

    ```bash
    streamlit run app.py
    ```

2.  **Open your web browser** and navigate to the local URL provided by Streamlit (usually `http://localhost:8501`).

3.  **Configure your interview:**

    - Fill in the Company Name, Job Role, and a detailed Job Description.
    - Add or remove interviewer profiles as needed, providing their name, role, and a LinkedIn URL for persona simulation.

4.  **Start the simulation** and interact with the AI interviewers!

## Project Structure

```
.
├── src/
│   ├── agents/         # Contains all CrewAI agent definitions
│   ├── crews/          # Crew definitions that group agents and tasks
│   ├── tools/          # Custom tools for the agents (e.g., report generation)
│   ├── config/         # Configuration files
│   ├── simulation_manager.py # Core logic for managing the interview flow
│   └── ...
├── app.py              # The main Streamlit application file
├── requirements.txt    # Project dependencies
├── README.md           # This file
└── .env                # For API keys (not included in git)
```
