"""
Resume Analysis Utilities

This module provides utilities for loading and processing resume analysis data.
"""
import streamlit as st

def load_resume_analysis():
    """
    Load resume analysis data from session state.
    
    Returns:
        dict: Resume analysis data or None if not available
    """
    if "resume_analysis" in st.session_state:
        return st.session_state.resume_analysis
    return None

def get_score_color(score):
    """
    Get color for score visualization based on the score value.
    
    Args:
        score (float): Score value (0-100)
        
    Returns:
        str: HEX color code
    """
    if score >= 80:
        return "#22c55e"  # Green
    elif score >= 60:
        return "#10b981"  # Teal
    elif score >= 40:
        return "#f59e0b"  # Amber
    else:
        return "#ef4444"  # Red