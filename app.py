import streamlit as st
from src.simulation_manager import SimulationManager
import json
import os

def save_config(config_data):
    """Saves the configuration data to src/config/config.json"""
    config_path = os.path.join("src", "config", "config.json")
    with open(config_path, "w") as f:
        json.dump(config_data, f, indent=4)

def main():
    st.set_page_config(page_title="AI Interview Prep Assistant", layout="wide")

    st.title("AI Interview Preparation Assistant 🤖")
    st.write("Welcome! Configure your interview details below and start the simulation.")

    # --- Configuration Section ---
    st.header("1. Interview Configuration")

    company_name = st.text_input("Company Name", "Google")
    job_role = st.text_input("Job Role", "Software Engineer")
    job_description = st.text_area("Job Description", "As a Software Engineer at Google, you will...", height=200)

    st.subheader("Interviewer Profiles")
    
    if 'interviewers' not in st.session_state:
        st.session_state.interviewers = [
            {"name": "Alice", "role": "Hiring Manager", "linkedin": "https://www.linkedin.com/in/alice/"},
            {"name": "Bob", "role": "Senior Software Engineer", "linkedin": "https://www.linkedin.com/in/bob/"}
        ]

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

    if st.button("Start Interview Simulation"):
        # --- Validation Step ---
        error = False
        if not job_description or job_description == "As a Software Engineer at Google, you will...":
            st.error("Please provide a detailed job description.")
            error = True
        
        if not st.session_state.interviewers:
            st.error("Please add at least one interviewer.")
            error = True
        else:
            for i, interviewer in enumerate(st.session_state.interviewers):
                if not interviewer['name'] or not interviewer['role'] or not interviewer['linkedin']:
                    st.error(f"Please fill in all fields for Interviewer {i+1}.")
                    error = True
        
        if error:
            return # Stop execution if there are validation errors

        # 1. Save the configuration
        config_data = {
            "company_name": company_name,
            "job_role": job_role,
            "job_description": job_description,
            "interviewers": st.session_state.interviewers
        }
        save_config(config_data)
        st.success("Configuration saved! Starting simulation...")

        # Initialize session state for the interview
        st.session_state.manager = SimulationManager()
        st.session_state.messages = []
        st.session_state.interview_started = True

        # Start the simulation and get the first question
        st.session_state.manager.start_simulation(
            on_question=lambda msg, is_intro: st.session_state.messages.append({"role": "assistant", "content": msg}),
            on_feedback=lambda msg: st.session_state.messages.append({"role": "assistant", "content": msg}),
            on_finish=lambda msg: st.session_state.messages.append({"role": "assistant", "content": msg})
        )
        st.rerun()

    if st.session_state.get('interview_started', False):
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
                    # Check for errors from the backend
                    if response_part.get("type") == "error":
                        st.error(response_part["content"])
                    else:
                        # Append the actual content to messages
                        st.session_state.messages.append({"role": "assistant", "content": response_part["content"]})
                        with st.chat_message("assistant"):
                            st.markdown(response_part["content"])
            st.rerun()



if __name__ == "__main__":
    main()
