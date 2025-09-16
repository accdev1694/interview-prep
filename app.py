import streamlit as st
from src.simulation_manager import SimulationManager
import json
import os

# --- Constants ---
CONFIG_DIR = os.path.join("src", "config")
CONFIG_PATH = os.path.join(CONFIG_DIR, "config.json")
DEFAULT_JOB_DESC = "As a Software Engineer at Google, you will..."

# --- Helper Functions ---
def save_config(config_data):
    """Saves the configuration data to the config file."""
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(CONFIG_PATH, "w") as f:
        json.dump(config_data, f, indent=4)

def initialize_session_state():
    """Initializes session state variables if they don't exist."""
    if 'interviewers' not in st.session_state:
        st.session_state.interviewers = [
            {"name": "Alice", "role": "Hiring Manager", "linkedin": "https://www.linkedin.com/in/alice/"},
            {"name": "Bob", "role": "Senior Software Engineer", "linkedin": "https://www.linkedin.com/in/bob/"}
        ]
    if 'interview_started' not in st.session_state:
        st.session_state.interview_started = False
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'manager' not in st.session_state:
        st.session_state.manager = None

# --- UI Components ---
def render_config_section():
    """Renders the configuration section of the UI."""
    st.header("1. Interview Configuration")
    company_name = st.text_input("Company Name", "Google")
    job_role = st.text_input("Job Role", "Software Engineer")
    job_description = st.text_area("Job Description", DEFAULT_JOB_DESC, height=200)
    return company_name, job_role, job_description

def render_interviewer_profiles():
    """Renders the UI for managing interviewer profiles."""
    st.subheader("Interviewer Profiles")
    for i, interviewer in enumerate(st.session_state.interviewers):
        with st.container():
            st.write(f"--- Interviewer {i+1} ---")
            cols = st.columns(3)
            interviewer['name'] = cols[0].text_input(f"Name", value=interviewer['name'], key=f"name_{i}")
            interviewer['role'] = cols[1].text_input(f"Role", value=interviewer['role'], key=f"role_{i}")
            interviewer['linkedin'] = cols[2].text_input(f"LinkedIn URL", value=interviewer['linkedin'], key=f"linkedin_{i}")
            if st.button(f"Remove Interviewer {i+1}", key=f"remove_{i}"):
                st.session_state.interviewers.pop(i)
                st.rerun()

    if st.button("Add Interviewer"):
        st.session_state.interviewers.append({"name": "", "role": "", "linkedin": ""})
        st.rerun()

def validate_inputs(job_description, interviewers):
    """Validates user inputs before starting the simulation."""
    error = False
    if not job_description or job_description == DEFAULT_JOB_DESC:
        st.error("Please provide a detailed job description.")
        error = True
    
    if not interviewers:
        st.error("Please add at least one interviewer.")
        error = True
    else:
        for i, interviewer in enumerate(interviewers):
            if not all(interviewer.values()):
                st.error(f"Please fill in all fields for Interviewer {i+1}.")
                error = True
    return not error

def render_simulation_section():
    """Renders the chat interface for the interview simulation."""
    st.header("2. Interview Simulation")

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Your Answer..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.spinner("Thinking..."):
            response_generator = st.session_state.manager.ask_next_question(prompt)
            for response_part in response_generator:
                if response_part.get("type") == "error":
                    st.error(response_part["content"])
                else:
                    content = response_part.get("content", "")
                    st.session_state.messages.append({"role": "assistant", "content": content})
                    with st.chat_message("assistant"):
                        st.markdown(content)
        st.rerun()

# --- Main Application ---
def main():
    """Main function to run the Streamlit application."""
    st.set_page_config(page_title="AI Interview Prep Assistant", layout="wide")
    st.title("AI Interview Preparation Assistant 🤖")
    st.write("Welcome! Configure your interview details below and start the simulation.")

    initialize_session_state()
    
    company_name, job_role, job_description = render_config_section()
    render_interviewer_profiles()

    if st.button("Start Interview Simulation"):
        if validate_inputs(job_description, st.session_state.interviewers):
            config_data = {
                "company_name": company_name,
                "job_role": job_role,
                "job_description": job_description,
                "interviewers": st.session_state.interviewers
            }
            save_config(config_data)
            st.success("Configuration saved! Starting simulation...")

            st.session_state.manager = SimulationManager()
            st.session_state.messages = []
            st.session_state.interview_started = True

            st.session_state.manager.start_simulation(
                on_question=lambda msg, is_intro: st.session_state.messages.append({"role": "assistant", "content": msg}),
                on_feedback=lambda msg: st.session_state.messages.append({"role": "assistant", "content": msg}),
                on_finish=lambda msg: st.session_state.messages.append({"role": "assistant", "content": msg})
            )
            st.rerun()

    if st.session_state.interview_started:
        render_simulation_section()

if __name__ == "__main__":
    main()
