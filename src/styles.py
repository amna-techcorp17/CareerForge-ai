import streamlit as st

def apply_custom_css():
    st.markdown("""
        <style>
        .main { background-color: #f8f9fa; }
        .stButton>button {
            width: 100%;
            border-radius: 5px;
            height: 3em;
            background-color: #007bff;
            color: white;
        }
        .stTextInput>div>div>input { border-radius: 5px; }
        </style>
    """, unsafe_allow_html=True)