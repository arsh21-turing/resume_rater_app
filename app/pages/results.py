"""
Results page for the Resume Rating App.

This module displays the results of the resume analysis compared to the job description.
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from app.utils import load_resume_analysis, get_score_color
import numpy as np

def display_results():
    """Display the resume analysis results compared to the job description."""
    st.title("Resume Analysis Results")
    
    # Check if we have both a job description and resume analysis in session state
    if "job_description_analysis" not in st.session_state or "resume_analysis" not in st.session_state:
        st.warning("Please upload a resume and provide a job description before viewing results.")
        
        # Add a button to go back to the job description page
        if st.button("Enter Job Description"):
            st.session_state.navigation = "Job Description"
            st.rerun()
        
        # Add a button to go to the resume upload page
        if st.button("Upload Resume"):
            st.session_state.navigation = "Resume Upload"
            st.rerun()
        
        return
    
    # Get the analyses from session state
    job_analysis = st.session_state.job_description_analysis
    resume_analysis = st.session_state.resume_analysis
    
    # Display overall match score
    display_overall_score(job_analysis, resume_analysis)
    
    # Display detailed breakdown in tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "Skills Match", 
        "Experience Match", 
        "Education Match", 
        "Improvement Suggestions"
    ])
    
    with tab1:
        display_skills_match(job_analysis, resume_analysis)
    
    with tab2:
        display_experience_match(job_analysis, resume_analysis)
    
    with tab3:
        display_education_match(job_analysis, resume_analysis)
    
    with tab4:
        display_improvement_suggestions(job_analysis, resume_analysis)
    
    # Option to download detailed report
    if st.button("Download Detailed Report"):
        generate_downloadable_report(job_analysis, resume_analysis)

def display_overall_score(job_analysis, resume_analysis):
    """Display the overall match score with visual representation."""
    st.subheader("Overall Match Score")
    
    # Calculate the overall score
    overall_score = resume_analysis.get("overall_score", 0)
    
    # Display the score in a large format
    col1, col2 = st.columns([1, 3])
    
    with col1:
        # Display the score in a big metric
        score_color = get_score_color(overall_score)
        st.markdown(
            f"""
            <div style="background-color: {score_color}; padding: 20px; border-radius: 10px; text-align: center;">
                <h1 style="margin: 0; color: white;">{overall_score}%</h1>
                <p style="margin: 0; color: white; font-weight: 500;">Match Score</p>
            </div>
            """, 
            unsafe_allow_html=True
        )
    
    with col2:
        # Display score breakdown by category
        categories = {
            "Skills Match": resume_analysis.get("skills_match_score", 0),
            "Experience Match": resume_analysis.get("experience_match_score", 0),
            "Education Match": resume_analysis.get("education_match_score", 0)
        }
        
        # Create a DataFrame for the bar chart
        df = pd.DataFrame({
            'Category': list(categories.keys()),
            'Score': list(categories.values())
        })
        
        # Create the bar chart
        fig, ax = plt.subplots(figsize=(10, 3))
        bars = ax.barh(df['Category'], df['Score'], color=['#3b82f6', '#10b981', '#f59e0b'])
        ax.set_xlim(0, 100)
        ax.set_xlabel('Score')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        # Add the scores as text on the bars
        for bar in bars:
            width = bar.get_width()
            label_x_pos = width + 1
            ax.text(label_x_pos, bar.get_y() + bar.get_height()/2, f'{width:.0f}%',
                    va='center')
        
        st.pyplot(fig)

def display_skills_match(job_analysis, resume_analysis):
    """Display the skills match analysis."""
    st.subheader("Skills Match Analysis")
    
    # Get required skills from job description
    required_skills = job_analysis.get("required_skills", [])
    preferred_skills = job_analysis.get("preferred_skills", [])
    all_job_skills = required_skills + preferred_skills
    
    # Get skills from resume
    resume_skills = resume_analysis.get("identified_skills", [])
    
    if not all_job_skills:
        st.warning("No skills were identified in the job description.")
        return
    
    # Calculate matching skills
    matching_skills = [skill for skill in resume_skills if skill in all_job_skills]
    missing_skills = [skill for skill in all_job_skills if skill not in resume_skills]
    
    # Display matching skills percentage
    match_percentage = len(matching_skills) / len(all_job_skills) * 100 if all_job_skills else 0
    st.metric(
        "Skills Match Rate", 
        f"{match_percentage:.0f}%", 
        f"{len(matching_skills)} out of {len(all_job_skills)} skills"
    )
    
    # Create two columns for the skills comparison
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🎯 Matching Skills")
        if matching_skills:
            # Display matched skills with checkmarks
            for skill in matching_skills:
                priority = "Required" if skill in required_skills else "Preferred"
                st.markdown(f"✅ **{skill}** ({priority})")
        else:
            st.warning("No matching skills found.")
    
    with col2:
        st.markdown("#### ❌ Missing Skills")
        if missing_skills:
            # Display missing skills with priority
            for skill in missing_skills:
                priority = "Required" if skill in required_skills else "Preferred"
                st.markdown(f"❌ **{skill}** ({priority})")
        else:
            st.success("No missing skills! Your resume covers all required skills.")
    
    # Skills distribution visualization
    st.subheader("Skills Distribution")
    
    # Create a pie chart for skills distribution
    labels = ['Matching', 'Missing']
    sizes = [len(matching_skills), len(missing_skills)]
    colors = ['#10b981', '#ef4444']
    
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
    
    st.pyplot(fig)

def display_experience_match(job_analysis, resume_analysis):
    """Display the experience match analysis."""
    st.subheader("Experience Match Analysis")
    
    # Get required experience from job description
    required_experience = job_analysis.get("required_experience", {})
    
    # Get experience from resume
    resume_experience = resume_analysis.get("experience", {})
    
    # If no experience data is available
    if not required_experience or not resume_experience:
        st.warning("Experience information is not available for comparison.")
        return
    
    # Experience years comparison
    req_years = required_experience.get("years", 0)
    res_years = resume_experience.get("years", 0)
    
    # Display experience years comparison
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Required Experience", f"{req_years} years")
    with col2:
        year_diff = res_years - req_years
        st.metric("Your Experience", f"{res_years} years", f"{year_diff:+g} years")
    
    # Calculate and display experience match score
    experience_score = resume_analysis.get("experience_match_score", 0)
    
    # Display the score
    score_color = get_score_color(experience_score)
    st.markdown(
        f"""
        <div style="background-color: {score_color}; padding: 10px; border-radius: 5px; margin-top: 20px;">
            <h3 style="margin: 0; color: white; text-align: center;">Experience Match Score: {experience_score}%</h3>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    # Display relevant experience details if available
    if "relevant_experience" in resume_analysis:
        st.subheader("Relevant Experience Highlights")
        
        for exp in resume_analysis["relevant_experience"]:
            with st.expander(f"{exp.get('title', 'Position')} at {exp.get('company', 'Company')}"):
                st.write(f"**Duration:** {exp.get('duration', 'N/A')}")
                st.write(f"**Relevance Score:** {exp.get('relevance_score', 0):.0f}%")
                st.write("**Key Responsibilities:**")
                for resp in exp.get("responsibilities", []):
                    st.write(f"- {resp}")

def display_education_match(job_analysis, resume_analysis):
    """Display the education match analysis."""
    st.subheader("Education Match Analysis")
    
    # Get required education from job description
    required_education = job_analysis.get("required_education", {})
    
    # Get education from resume
    resume_education = resume_analysis.get("education", [])
    
    # If no education data is available
    if not required_education and not resume_education:
        st.warning("Education information is not available for comparison.")
        return
    
    # Display education match score
    education_score = resume_analysis.get("education_match_score", 0)
    score_color = get_score_color(education_score)
    
    st.markdown(
        f"""
        <div style="background-color: {score_color}; padding: 10px; border-radius: 5px;">
            <h3 style="margin: 0; color: white; text-align: center;">Education Match Score: {education_score}%</h3>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    # Display comparison table
    st.subheader("Education Comparison")
    
    # Create comparison table
    data = {
        "Criteria": ["Degree Level", "Field of Study", "Academic Performance"],
        "Required": [
            required_education.get("degree_level", "Not specified"),
            required_education.get("field", "Not specified"),
            required_education.get("min_gpa", "Not specified")
        ],
        "Your Qualification": [
            resume_education[0].get("degree", "Not specified") if resume_education else "Not found",
            resume_education[0].get("field", "Not specified") if resume_education else "Not found",
            resume_education[0].get("gpa", "Not specified") if resume_education else "Not found"
        ]
    }
    
    df = pd.DataFrame(data)
    st.table(df)
    
    # Display all education entries from resume
    if resume_education:
        st.subheader("Your Educational Background")
        
        for edu in resume_education:
            st.markdown(f"**{edu.get('degree', 'Degree')}** in {edu.get('field', 'Field')}")
            st.markdown(f"*{edu.get('institution', 'Institution')}* ({edu.get('year', 'Year')})")
            if "gpa" in edu:
                st.markdown(f"GPA: {edu.get('gpa')}")
            st.markdown("---")

def display_improvement_suggestions(job_analysis, resume_analysis):
    """Display suggestions for improving the resume."""
    st.subheader("Improvement Suggestions")
    
    # Get the improvement suggestions from the analysis
    suggestions = resume_analysis.get("improvement_suggestions", [])
    
    if not suggestions:
        st.warning("No improvement suggestions available.")
        
        # Generate some basic suggestions based on the analysis
        missing_skills = [skill for skill in job_analysis.get("required_skills", []) 
                         if skill not in resume_analysis.get("identified_skills", [])]
        
        if missing_skills:
            st.markdown("### 🚀 Suggested Improvements")
            st.markdown("Based on our analysis, consider the following improvements:")
            
            st.markdown("#### Add Missing Skills")
            st.markdown("Add these required skills to your resume if you possess them:")
            for skill in missing_skills[:5]:  # Show top 5 missing skills
                st.markdown(f"- **{skill}**")
            
            st.markdown("#### Quantify Achievements")
            st.markdown("""
            Enhance your experience descriptions by adding measurable achievements.
            For example:
            - "Increased sales by 20% over 6 months"
            - "Reduced processing time by 35%"
            - "Managed a team of 8 developers"
            """)
            
            st.markdown("#### Tailor Your Resume")
            st.markdown("""
            Customize your resume for this specific position by:
            - Using keywords from the job description
            - Highlighting relevant experience
            - Organizing content with the most relevant information first
            """)
        return
    
    # Display each suggestion with an expander for details
    for i, suggestion in enumerate(suggestions):
        with st.expander(f"Suggestion {i+1}: {suggestion.get('title', 'Improve your resume')}"):
            st.markdown(f"**Priority**: {suggestion.get('priority', 'Medium')}")
            st.markdown(f"**Description**: {suggestion.get('description', '')}")
            
            # If there are specific examples or steps, display them
            if "steps" in suggestion:
                st.markdown("**Steps to Implement:**")
                for step in suggestion["steps"]:
                    st.markdown(f"- {step}")
            
            # If there's a before/after example, display it
            if "example_before" in suggestion and "example_after" in suggestion:
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**Before:**")
                    st.markdown(f"```\n{suggestion['example_before']}\n```")
                with col2:
                    st.markdown("**After:**")
                    st.markdown(f"```\n{suggestion['example_after']}\n```")

def generate_downloadable_report(job_analysis, resume_analysis):
    """Generate and provide a downloadable detailed report."""
    # Create a detailed report as a string
    report = f"""
    # Resume Analysis Detailed Report
    
    ## Overall Match Score: {resume_analysis.get('overall_score', 0)}%
    
    ### Skills Match: {resume_analysis.get('skills_match_score', 0)}%
    - Matching skills: {', '.join(skill for skill in resume_analysis.get('identified_skills', []) if skill in job_analysis.get('required_skills', []) + job_analysis.get('preferred_skills', []))}
    - Missing skills: {', '.join(skill for skill in job_analysis.get('required_skills', []) + job_analysis.get('preferred_skills', []) if skill not in resume_analysis.get('identified_skills', []))}
    
    ### Experience Match: {resume_analysis.get('experience_match_score', 0)}%
    - Required experience: {job_analysis.get('required_experience', {}).get('years', 0)} years
    - Your experience: {resume_analysis.get('experience', {}).get('years', 0)} years
    
    ### Education Match: {resume_analysis.get('education_match_score', 0)}%
    - Required education: {job_analysis.get('required_education', {}).get('degree_level', 'Not specified')} in {job_analysis.get('required_education', {}).get('field', 'Not specified')}
    - Your education: {resume_analysis.get('education', [{}])[0].get('degree', 'Not found')} in {resume_analysis.get('education', [{}])[0].get('field', 'Not found')}
    
    ## Key Improvement Areas
    
    1. Add missing required skills to your resume
    2. Highlight relevant experience more prominently
    3. Quantify your achievements with metrics
    4. Use keywords from the job description
    5. Tailor your resume format for better readability
    
    Generated by Resume Rating App
    """
    
    # Convert to bytes for download
    report_bytes = report.encode()
    
    # Offer the download
    st.download_button(
        label="Download Report as Markdown",
        data=report_bytes,
        file_name="resume_analysis_report.md",
        mime="text/markdown"
    )