"""
Component for uploading and analyzing resumes.

This module contains functions for handling resume file upload 
and performing analysis on the resume content.
"""
import streamlit as st
import os
import io
import re
import PyPDF2
import nltk
from datetime import datetime
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Import required functions from resume_matcher.py
from app.components.resume_matcher import (
    calculate_match_score,
    compare_resume_to_job
)

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

# Common technical skills for extraction
COMMON_TECH_SKILLS = [
    "python", "javascript", "java", "c++", "c#", "ruby", "php", "swift", 
    "kotlin", "go", "rust", "typescript", "sql", "nosql", "mongodb", 
    "postgresql", "mysql", "oracle", "react", "angular", "vue.js", "node.js", 
    "express.js", "django", "flask", "spring", "asp.net", "laravel",
    "aws", "azure", "gcp", "docker", "kubernetes", "terraform", "jenkins",
    "git", "ci/cd", "agile", "scrum", "jira", "rest api", "graphql",
    "machine learning", "deep learning", "ai", "data science", "big data",
    "hadoop", "spark", "kafka", "elasticsearch", "tableau", "power bi",
    "excel", "powerpoint", "word", "html", "css", "bootstrap", "sass",
    "redux", "jquery", "webpack", "babel", "responsive design", "mobile development"
]

def extract_text_from_pdf(file):
    """Extract text content from a PDF file."""
    reader = PyPDF2.PdfReader(io.BytesIO(file.getvalue()))
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def extract_text_from_docx(file):
    """Extract text content from a DOCX file."""
    try:
        import docx2txt
        return docx2txt.process(io.BytesIO(file.getvalue()))
    except ImportError:
        st.error("docx2txt library is not installed. Please install it to process DOCX files.")
        return ""

def extract_text_from_txt(file):
    """Extract text content from a TXT file."""
    return file.getvalue().decode("utf-8")

def extract_resume_text(uploaded_file):
    """
    Extract text from the uploaded resume file based on its type.
    
    Args:
        uploaded_file: The uploaded resume file
        
    Returns:
        str: Extracted text from the resume
    """
    if not uploaded_file:
        return None
        
    file_ext = os.path.splitext(uploaded_file.name)[1].lower()
    
    if file_ext == ".pdf":
        return extract_text_from_pdf(uploaded_file)
    elif file_ext in [".docx", ".doc"]:
        return extract_text_from_docx(uploaded_file)
    elif file_ext == ".txt":
        return extract_text_from_txt(uploaded_file)
    else:
        st.error(f"Unsupported file format: {file_ext}")
        return None

def extract_skills_from_text(text):
    """
    Extract skills from resume text.
    
    Args:
        text (str): Resume text content
        
    Returns:
        list: Extracted skills
    """
    text_lower = text.lower()
    found_skills = []
    
    # Extract skills from our predefined list
    for skill in COMMON_TECH_SKILLS:
        # Use word boundary matching to avoid partial matches
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text_lower):
            found_skills.append(skill)
    
    return found_skills

def extract_education_from_text(text):
    """
    Extract education details from resume text.
    
    Args:
        text (str): Resume text content
        
    Returns:
        list: Education entries
    """
    education_entries = []
    
    # Look for common education section indicators
    education_section = None
    
    # Try to find education section
    edu_headers = ["education", "academic background", "academic qualifications", "qualifications"]
    lines = text.split('\n')
    for i, line in enumerate(lines):
        if any(header in line.lower() for header in edu_headers):
            start_idx = i
            # Find the end of the education section (next header or end of text)
            for j in range(i+1, len(lines)):
                # Assuming headers are capitalized or have special formatting
                if re.match(r'^[A-Z\s]+:?$', lines[j].strip()) or j == len(lines)-1:
                    education_section = '\n'.join(lines[start_idx:j])
                    break
            if education_section:
                break
    
    # If no clear section found, use the whole text
    if not education_section:
        education_section = text
    
    # Extract degree information
    degree_patterns = [
        r'(Bachelor|Master|Ph\.?D\.?|Associate|B\.S\.|B\.A\.|M\.S\.|M\.A\.|MBA)\.?\s+(?:of|in|degree)?\s+([A-Za-z\s,]+)',
        r'([A-Za-z\s]+) (degree|diploma)',
        r'(Bachelor|Master|Ph\.?D\.?|Associate|B\.S\.|B\.A\.|M\.S\.|M\.A\.|MBA)',
    ]
    
    # Extract year
    year_pattern = r'\b(19[8-9]\d|20[0-2]\d)\b'
    
    for pattern in degree_patterns:
        matches = re.findall(pattern, education_section, re.IGNORECASE)
        for match in matches:
            if isinstance(match, tuple):
                degree = match[0].strip()
                field = match[1].strip() if len(match) > 1 else ""
            else:
                degree = match.strip()
                field = ""
            
            # Look for year near this degree mention
            context = education_section[max(0, education_section.find(degree)-50):
                                        min(len(education_section), education_section.find(degree)+100)]
            year_match = re.search(year_pattern, context)
            year = year_match.group(1) if year_match else None
            
            education_entries.append({
                'degree': degree,
                'field': field,
                'year': year
            })
    
    return education_entries

def extract_experience_from_text(text):
    """
    Extract experience details from resume text.
    
    Args:
        text (str): Resume text content
        
    Returns:
        list: Experience entries
    """
    experience_entries = []
    
    # Look for common work experience section indicators
    experience_section = None
    
    # Try to find experience section
    exp_headers = ["experience", "work experience", "employment history", "professional experience"]
    lines = text.split('\n')
    for i, line in enumerate(lines):
        if any(header in line.lower() for header in exp_headers):
            start_idx = i
            # Find the end of the experience section (next header or end of text)
            for j in range(i+1, len(lines)):
                # Assuming headers are capitalized or have special formatting
                if re.match(r'^[A-Z\s]+:?$', lines[j].strip()) or j == len(lines)-1:
                    experience_section = '\n'.join(lines[start_idx:j])
                    break
            if experience_section:
                break
    
    # If no clear section found, use the whole text
    if not experience_section:
        experience_section = text
    
    # Extract job title and company
    job_patterns = [
        r'((?:Sr\.?|Senior|Jr\.?|Junior)?\s*[A-Za-z\s]+(?:Developer|Engineer|Analyst|Manager|Director|Designer|Consultant|Specialist|Coordinator))\s*(?:at|,|-)?\s*([A-Za-z\s&]+)',
        r'([A-Za-z\s]+)\s*(?:-|at|,)\s*([A-Za-z0-9\s&]+)',
    ]
    
    # Extract dates and calculate duration
    date_pattern = r'(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+\d{4}\s*(?:-|to|–)\s*(Present|Current|Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s*\d{0,4}'
    year_pattern = r'(\d{4})\s*(?:-|to|–)\s*(Present|Current|\d{4})'
    
    # Extract titles, companies and dates
    for pattern in job_patterns:
        matches = re.findall(pattern, experience_section, re.IGNORECASE)
        for match in matches:
            title = match[0].strip()
            company = match[1].strip() if len(match) > 1 else ""
            
            # Look for dates near this job mention
            context = experience_section[max(0, experience_section.find(title)-100):
                                         min(len(experience_section), experience_section.find(title)+200)]
            
            # Try specific date formats first, then just years
            date_match = re.search(date_pattern, context, re.IGNORECASE)
            if not date_match:
                date_match = re.search(year_pattern, context)
            
            start_date = None
            end_date = None
            duration = None
            
            if date_match:
                if len(date_match.groups()) >= 2:
                    start_date = date_match.group(1)
                    end_date = date_match.group(2)
                    
                    # Calculate duration for current jobs
                    if end_date in ['Present', 'Current']:
                        # Extract year from start date
                        start_year_match = re.search(r'\b(19[9]\d|20[0-2]\d)\b', start_date)
                        if start_year_match:
                            start_year = int(start_year_match.group(1))
                            current_year = datetime.now().year
                            years = current_year - start_year
                            duration = f"{years} years"
            
            experience_entries.append({
                'title': title,
                'company': company,
                'start_date': start_date,
                'end_date': end_date,
                'duration': duration,
                # Estimate years if we can
                'years': float(duration.split()[0]) if duration and duration.split()[0].isdigit() else 0
            })
    
    return experience_entries

def analyze_resume(resume_text, job_description=None):
    """
    Analyze resume content and extract key information.
    
    Args:
        resume_text (str): The text content of the resume
        job_description (dict or str, optional): Job description data for comparison
        
    Returns:
        dict: Analysis results including skills, education, experience, etc.
    """
    if not resume_text:
        return None
    
    # Extract key components from resume
    skills = extract_skills_from_text(resume_text)
    education = extract_education_from_text(resume_text)
    experience = extract_experience_from_text(resume_text)
    
    # Prepare resume data in the format expected by resume_matcher
    resume_data = {
        'skills': skills,
        'education': education,
        'experience': experience,
        'raw_text': resume_text
    }
    
    # Compare with job description if available
    if job_description:
        # Check if job_description is a dictionary and has the required format
        # If it's a string, we need to convert it to the expected format
        job_desc_for_matcher = job_description
        if isinstance(job_description, dict):
            # Ensure job_description has the required format for resume_matcher
            if 'raw_text' not in job_description:
                # Format expected by compare_resume_to_job
                job_desc_for_matcher = {
                    'skills': job_description.get('required_skills', []),
                    'experience': job_description.get('required_experience', []),
                    'education': job_description.get('required_education', []),
                    'raw_text': job_description.get('description', '')
                }
        elif isinstance(job_description, str):
            # If job_description is a string, create a proper dictionary
            job_desc_for_matcher = {
                'skills': [],  # We don't have extracted skills from a raw string
                'experience': [],
                'education': [],
                'raw_text': job_description
            }
        
        # Use the resume_matcher's compare_resume_to_job function
        match_report = compare_resume_to_job(resume_data, job_desc_for_matcher)
        
        # Combine the resume data with match report
        analysis_results = {
            'identified_skills': skills,
            'education_info': education,
            'experience_info': experience,
            'original_text': resume_text,
            'analyzed_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'match_report': match_report,
            'overall_score': match_report.get('overall_score', 0) * 100,  # Convert to percentage
            'skills_match_score': match_report.get('skill_analysis', {}).get('score', 0) * 100,
            'experience_match_score': match_report.get('experience_analysis', {}).get('score', 0) * 100,
            'education_match_score': match_report.get('education_analysis', {}).get('score', 0) * 100
        }
    else:
        # Just return the extracted information
        analysis_results = {
            'identified_skills': skills,
            'education_info': education,
            'experience_info': experience,
            'original_text': resume_text,
            'analyzed_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    return analysis_results

def resume_upload_and_analysis():
    """Display the resume upload interface and perform analysis."""
    st.title("Resume Upload & Analysis")
    
    st.write("""
    Upload your resume to analyze it and match against job requirements.
    Supported formats: PDF, DOCX, and TXT.
    """)
    
    # Check if job description has been provided
    if "job_description_analysis" not in st.session_state:
        st.warning("Please enter a job description first to get the best matching results.")
        
        # Add a button to go to the job description page
        if st.button("Enter Job Description"):
            st.session_state.navigation = "Job Description"
            st.rerun()
            
    # File upload widget
    uploaded_file = st.file_uploader(
        "Choose a resume file", 
        type=["pdf", "docx", "txt"],
        help="Upload your resume in PDF, DOCX, or TXT format"
    )
    
    if uploaded_file:
        # Process the uploaded file
        st.info(f"Processing {uploaded_file.name}...")
        
        with st.spinner("Extracting text from resume..."):
            resume_text = extract_resume_text(uploaded_file)
            
            if resume_text:
                # Show a preview of the extracted text
                with st.expander("Preview Extracted Text"):
                    st.text(resume_text[:1000] + ("..." if len(resume_text) > 1000 else ""))
                
                # Analyze the resume
                with st.spinner("Analyzing resume content..."):
                    job_description = st.session_state.get("job_description_analysis", None)
                    analysis_results = analyze_resume(resume_text, job_description)
                    
                    if analysis_results:
                        # Store the analysis results in session state
                        st.session_state.resume_analysis = analysis_results
                        
                        # Display a summary of the analysis
                        st.success("Resume successfully analyzed!")
                        
                        # Skills found
                        st.subheader("Skills Identified")
                        if analysis_results["identified_skills"]:
                            st.write(", ".join(analysis_results["identified_skills"]))
                        else:
                            st.warning("No specific skills were identified in your resume.")
                        
                        # If we have job description, show match information
                        if job_description and "overall_score" in analysis_results:
                            st.subheader("Match Overview")
                            
                            # Display the overall match score
                            score = analysis_results["overall_score"]
                            score_color = "green" if score >= 70 else (
                                "orange" if score >= 50 else "red"
                            )
                            
                            st.markdown(
                                f"""
<div>
<h3>Overall Match: {score:.1f}%</h3>
</div>
                                """, 
                                unsafe_allow_html=True
                            )
                        
                        # Continue to results page button
                        if st.button("View Detailed Results", use_container_width=True):
                            st.session_state.navigation = "Results"
                            st.rerun()
                    else:
                        st.error("Failed to analyze resume content. Please try again with a different file.")
            else:
                st.error("Failed to extract text from the uploaded file. Please check the file format and try again.")
    
    # Option to see results if we already have an analysis
    elif "resume_analysis" in st.session_state:
        st.success("A resume has already been analyzed.")
        
        if st.button("View Previous Results", use_container_width=True):
            st.session_state.navigation = "Results"
            st.rerun()