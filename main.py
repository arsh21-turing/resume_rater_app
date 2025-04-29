# main.py
"""
Main entry point for the Resume Rating App.
This script initializes and runs the Streamlit application.
"""

import os
import sys
import streamlit as st
from app.pages.home import display_home
from app.pages.about import display_about
from app.pages.results import display_results
from app.components.job_description import job_description_input
from app.components.resume_upload import resume_upload_and_analysis

APP_TITLE = "Resume Rating App"
APP_ICON = "📄"

def create_navigation_sidebar():
    """Create sidebar navigation using radio buttons instead of multiple buttons to avoid ID conflicts."""
    st.sidebar.title("Navigation")
    
    # Using a radio component instead of multiple buttons
    # This ensures we only have one widget instead of multiple buttons that could conflict
    navigation = st.sidebar.radio(
        "Select a page:",
        ["🏠 Home", "📋 Job Description", "📄 Resume Upload", "📊 Results", "ℹ️ About"],
        key="sidebar_radio",
        label_visibility="collapsed"  # Hide the "Select a page:" label
    )
    
    # Map the selection back to our navigation state
    nav_map = {
        "🏠 Home": "Home",
        "📋 Job Description": "Job Description",
        "📄 Resume Upload": "Resume Upload",
        "📊 Results": "Results",
        "ℹ️ About": "About"
    }
    
    # Update navigation if changed
    if nav_map[navigation] != st.session_state.navigation:
        st.session_state.navigation = nav_map[navigation]
        st.rerun()

def main():
    """Main application entry point."""
    st.set_page_config(
        page_title=APP_TITLE,
        page_icon=APP_ICON,
        layout="wide",
        initial_sidebar_state="expanded"
    )

    if "navigation" not in st.session_state:
        st.session_state.navigation = "Home"

    # Custom CSS
    st.markdown("""
    <style>
    .app-header { color: #3b82f6; font-weight: 600; }
    .metric-card { background-color: #f8fafc; border-radius: .5rem; padding: 1rem; box-shadow: 0 1px 3px rgba(0,0,0,0.1); margin-bottom: 1rem; }
    .stProgress .st-bo { background-color: #3b82f6; }
    /* Make the radio buttons look more like a navigation menu */
    div[data-testid="stRadio"] > div {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
    }
    div[data-testid="stRadio"] label {
        padding: 0.5rem;
        border-radius: 0.3rem;
        cursor: pointer;
        font-weight: 500;
    }
    div[data-testid="stRadio"] label:hover {
        background-color: rgba(59, 130, 246, 0.1);
    }
    </style>
    """, unsafe_allow_html=True)

    # Create sidebar navigation
    create_navigation_sidebar()

    # Page dispatch
    page = st.session_state.navigation
    if page == "Home":
        display_home()
    elif page == "Job Description":
        job_description_input()
    elif page == "Resume Upload":
        resume_upload_and_analysis()
    elif page == "Results":
        display_results()
    elif page == "About":
        display_about()

if __name__ == "__main__":
    main()