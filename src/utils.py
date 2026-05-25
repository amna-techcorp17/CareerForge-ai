import streamlit as st

def initialize_session_state():
    """Initializes keys for storing AI results."""
    if 'resume_done' not in st.session_state:
        st.session_state['resume_done'] = False
    if 'generated_resume' not in st.session_state:
        st.session_state['generated_resume'] = ""
    if 'generated_cl' not in st.session_state:
        st.session_state['generated_cl'] = ""


def apply_dark_theme():
    try:
        with open("assets/style.css", "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass
