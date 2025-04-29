"""
Job Description Component

This module handles the job description input and analysis for the Resume Rating App.
"""
import streamlit as st
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Ensure NLTK data is downloaded
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

def job_description_input():
    """
    Display the job description input section.
    
    Returns:
        tuple: The job description text and extracted requirements
    """
    st.title("Job Description Analysis")
    
    st.markdown("""
    Enter a complete job description to analyze key requirements and skills.
    This will help match resumes to the specific needs of the position.
    """)
    
    # Job description text area
    job_desc = st.text_area(
        "Job Description",
        height=300,
        placeholder="Paste the full job description here...",
        value=st.session_state.get("job_description", "")
    )
    
    # Save to session state
    if job_desc:
        st.session_state.job_description = job_desc
    
    # Analysis button
    requirements = None
    if st.button("Analyze Requirements", type="primary", use_container_width=True):
        with st.spinner("Analyzing job description..."):
            requirements = analyze_job_description(job_desc)
            st.session_state.job_description_analysis = requirements
    
    # Display extracted requirements if available
    if "job_description_analysis" in st.session_state:
        display_requirements(st.session_state.job_description_analysis)
    
    return job_desc, requirements

def analyze_job_description(job_description_text):
    """
    Extract requirements from a job description.
    
    Args:
        job_description_text (str): The full job description text
        
    Returns:
        dict: Structured requirements including skills, experience, and education
    """
    if not job_description_text:
        return None
    
    # Extract skills
    skills = extract_skills(job_description_text)
    
    # Extract experience requirements
    experience = extract_experience(job_description_text)
    
    # Extract education requirements
    education = extract_education(job_description_text)
    
    # Extract priority skills (those mentioned multiple times or emphasized)
    priority_skills = extract_priority_skills(job_description_text, skills)
    
    # Extract responsibilities (for content matching)
    responsibilities = extract_responsibilities(job_description_text)
    
    # Build the requirements dictionary
    requirements = {
        "raw_text": job_description_text,
        "skills": skills,
        "priority_skills": priority_skills,
        "required_skills": skills,  # For compatibility with existing code
        "preferred_skills": priority_skills,  # For compatibility with existing code
        "experience": experience,
        "education": education,
        "responsibilities": responsibilities
    }
    
    return requirements

def extract_skills(text, threshold=0.7):
    """
    Extract skills from the text using keyword matching and NLP techniques.
    
    Args:
        text (str): Input text to analyze
        threshold (float): Confidence threshold for skill extraction
        
    Returns:
        list: Extracted skills from the text
    """
    # Normalize text for better matching
    text_lower = text.lower()
    
    # Extract skills using basic keyword matching
    extracted_skills = []
    for skill in COMMON_TECH_SKILLS:
        # Use word boundary to avoid partial matches
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text_lower):
            extracted_skills.append(skill)
    
    # Clean up and return unique skills
    unique_skills = list(set(extracted_skills))
    return unique_skills

def extract_priority_skills(text, skills):
    """
    Identify priority skills based on frequency, position, and emphasis.
    
    Args:
        text (str): Job description text
        skills (list): All extracted skills
        
    Returns:
        list: Priority skills with higher importance
    """
    if not skills:
        return []
    
    text_lower = text.lower()
    priority_skills = []
    
    # Look for skills that appear multiple times
    skill_counts = {skill: text_lower.count(skill.lower()) for skill in skills}
    
    # Look for skills that appear in the first paragraph or requirements section
    first_paragraph = text_lower.split('\n\n')[0] if '\n\n' in text_lower else text_lower[:500]
    requirements_section = None
    
    # Try to identify a requirements section
    req_patterns = ["requirements", "qualifications", "skills required", "what you'll need"]
    for pattern in req_patterns:
        if pattern in text_lower:
            start_idx = text_lower.find(pattern)
            end_idx = text_lower.find("\n\n", start_idx)
            if end_idx == -1:  # No double newline after requirements
                end_idx = len(text_lower)
            requirements_section = text_lower[start_idx:end_idx]
            break
    
    # Check each skill for priority indicators
    for skill in skills:
        # Priority if mentioned multiple times
        if skill_counts[skill] > 1:
            priority_skills.append(skill)
            continue
            
        # Priority if in first paragraph
        if skill.lower() in first_paragraph:
            priority_skills.append(skill)
            continue
            
        # Priority if in requirements section
        if requirements_section and skill.lower() in requirements_section:
            priority_skills.append(skill)
            continue
            
        # Priority if emphasized (all caps, surrounded by * or _, or preceded by "strong" words)
        if re.search(r'\b' + re.escape(skill.upper()) + r'\b', text):
            priority_skills.append(skill)
            continue
            
        if re.search(r'[\*_]' + re.escape(skill.lower()) + r'[\*_]', text_lower):
            priority_skills.append(skill)
            continue
            
        # Look for patterns that emphasize importance
        emphasis_patterns = [
            r'(strong|excellent|advanced|expert)\s+' + re.escape(skill.lower()),
            r'experience\s+(?:with|in)\s+' + re.escape(skill.lower()),
            r'proficient\s+(?:with|in)\s+' + re.escape(skill.lower())
        ]
            
        for pattern in emphasis_patterns:
            if re.search(pattern, text_lower):
                priority_skills.append(skill)
                break
    
    # Remove duplicates while preserving order
    unique_priority_skills = []
    for skill in priority_skills:
        if skill not in unique_priority_skills:
            unique_priority_skills.append(skill)
            
    return unique_priority_skills

def extract_experience(text):
    """
    Extract experience requirements from the job description.
    
    Args:
        text (str): Job description text
        
    Returns:
        dict: Experience requirements including years and level
    """
    text_lower = text.lower()
    
    # Look for years of experience using regex
    years_patterns = [
        r'(\d+)[\+]?\s*(?:to|-)\s*(\d+)[\+]?\s*years?',  # matches ranges like "3-5 years"
        r'(\d+)[\+]?\s*years?',  # matches like "3+ years" or "3 years"
        r'minimum\s*of\s*(\d+)\s*years?',  # matches "minimum of X years"
        r'at\s*least\s*(\d+)\s*years?'  # matches "at least X years"
    ]
    
    years = {
        "min": 0,
        "max": None
    }
    
    for pattern in years_patterns:
        match = re.search(pattern, text_lower)
        if match:
            # Handle range case ("3-5 years")
            if len(match.groups()) > 1 and match.group(2):
                years["min"] = int(match.group(1))
                years["max"] = int(match.group(2))
                break
            else:
                # Handle single value case ("3+ years")
                years["min"] = int(match.group(1))
                years["max"] = None
                break
    
    # Determine experience level
    level = "Entry Level"
    if years["min"] <= 1:
        level = "Entry Level"
    elif years["min"] <= 3:
        level = "Mid Level"
    elif years["min"] <= 5:
        level = "Senior Level"
    else:
        level = "Expert Level"
    
    # Try to infer from keywords if years aren't mentioned
    level_keywords = {
        "Entry Level": ["entry", "junior", "beginner", "trainee", "internship"],
        "Mid Level": ["mid", "intermediate", "associate"],
        "Senior Level": ["senior", "lead", "experienced", "advanced"],
        "Expert Level": ["expert", "principal", "director", "head", "chief"]
    }
    
    for l, keywords in level_keywords.items():
        if any(keyword in text_lower for keyword in keywords):
            level = l
            break
    
    # Create a description for display
    description = ""
    if years["min"] > 0:
        if years["max"]:
            description = f"{years['min']}-{years['max']} years ({level})"
        else:
            description = f"{years['min']}+ years ({level})"
    else:
        description = level
    
    return {
        "years": years,
        "level": level,
        "description": description
    }

def extract_education(text):
    """
    Extract education requirements from the job description.
    
    Args:
        text (str): Job description text
        
    Returns:
        dict: Education requirements including degree level
    """
    text_lower = text.lower()
    
    # Define degree patterns
    degree_patterns = {
        "high_school": ["high school", "ged", "secondary education"],
        "associate": ["associate", "associate's", "aa", "a.a", "a.s"],
        "bachelor": ["bachelor", "bachelor's", "bachelors", "ba", "b.a", "bs", "b.s", "undergraduate"],
        "master": ["master", "master's", "masters", "ma", "m.a", "ms", "m.s", "mba", "graduate"],
        "phd": ["phd", "ph.d", "doctorate", "doctoral"]
    }
    
    # Find required and preferred education levels
    required = None
    preferred = None
    
    # Look for education requirements
    edu_section = None
    edu_keywords = ["education", "qualification", "degree", "academic"]
    
    for keyword in edu_keywords:
        if keyword in text_lower:
            start_idx = text_lower.find(keyword)
            end_idx = text_lower.find("\n\n", start_idx)
            if end_idx == -1:
                end_idx = min(start_idx + 300, len(text_lower))  # Limit to reasonable section length
            edu_section = text_lower[start_idx:end_idx]
            break
    
    # If no education section found, use whole text
    if not edu_section:
        edu_section = text_lower
    
    # Determine if requirements are required or preferred
    for level, patterns in degree_patterns.items():
        for pattern in patterns:
            # Check for required education
            req_match = re.search(r'(require|must have|necessary)(?:.*?)\b' + re.escape(pattern) + r'\b', 
                                  edu_section, re.IGNORECASE)
            if req_match:
                required = level
                break
                
            # Check for preferred education
            pref_match = re.search(r'(prefer|ideally|nice to have)(?:.*?)\b' + re.escape(pattern) + r'\b', 
                                   edu_section, re.IGNORECASE)
            if pref_match:
                preferred = level
                break
                
            # Check for general mention (assume required if not explicitly preferred)
            if re.search(r'\b' + re.escape(pattern) + r'\b', edu_section, re.IGNORECASE):
                if not required:  # Don't override an already found required level
                    required = level
    
    # Extract fields of study
    fields = []
    field_patterns = [
        r'degree in ([A-Za-z\s,]+)',
        r'background in ([A-Za-z\s,]+)',
        r'([A-Za-z\s,]+) degree',
        r'degree \(([A-Za-z\s,]+)\)'
    ]
    
    for pattern in field_patterns:
        matches = re.findall(pattern, edu_section, re.IGNORECASE)
        for match in matches:
            # Clean up the field
            field = match.strip().strip('.,;()')
            # Skip if it's just a degree level
            if not any(d in field.lower() for d in ["bachelor", "master", "phd", "associate"]):
                fields.append(field)
    
    # Create a description for display
    description = ""
    if required:
        degree_name = required.replace("_", " ").title()
        description = f"Required: {degree_name} degree"
        if preferred and preferred != required:
            pref_name = preferred.replace("_", " ").title()
            description += f", Preferred: {pref_name} degree"
    elif preferred:
        pref_name = preferred.replace("_", " ").title()
        description = f"Preferred: {pref_name} degree"
    else:
        description = "No specific degree requirements mentioned"
    
    if fields:
        description += f" in {', '.join(fields[:3])}"
        if len(fields) > 3:
            description += f" or related field"
    
    return {
        "required": required,
        "preferred": preferred,
        "fields": fields,
        "description": description
    }

def extract_responsibilities(text):
    """
    Extract job responsibilities from the job description.
    
    Args:
        text (str): Job description text
        
    Returns:
        list: Extracted job responsibilities
    """
    text_lower = text.lower()
    responsibilities = []
    
    # Look for responsibilities section
    resp_keywords = ["responsibilities", "duties", "what you'll do", "job description", "the role"]
    resp_section = None
    
    for keyword in resp_keywords:
        if keyword in text_lower:
            start_idx = text_lower.find(keyword)
            end_idx = text_lower.find("\n\n", start_idx)
            if end_idx == -1:
                # Look for next section header
                next_headers = ["requirements", "qualifications", "skills", "what you'll need", 
                                "what we're looking for", "education", "benefits"]
                for header in next_headers:
                    header_idx = text_lower.find(header, start_idx + len(keyword))
                    if header_idx > -1:
                        end_idx = header_idx
                        break
            
            if end_idx == -1:  # Still not found
                end_idx = len(text_lower)
                
            resp_section = text_lower[start_idx:end_idx]
            break
    
    # Parse bullet points or numbered lists
    if resp_section:
        # Split by common bullet point patterns
        bullet_patterns = [
            r'•\s*(.*?)(?=•|\Z)',
            r'-\s*(.*?)(?=-|\Z)',
            r'\*\s*(.*?)(?=\*|\Z)',
            r'\d+\.\s*(.*?)(?=\d+\.|\Z)',
            r'[A-Za-z\)]\)\s*(.*?)(?=[A-Za-z\)]\)|\Z)'
        ]
        
        for pattern in bullet_patterns:
            items = re.findall(pattern, resp_section, re.DOTALL)
            if items:
                for item in items:
                    # Clean up the item
                    clean_item = re.sub(r'\s+', ' ', item.strip())
                    if clean_item and len(clean_item) > 10:  # Avoid very short items
                        responsibilities.append(clean_item)
                break  # Stop after finding matching pattern
        
        # If no bullet points found, try splitting by sentences
        if not responsibilities:
            sentences = re.split(r'(?<=[.!?])\s+', resp_section)
            for sentence in sentences:
                clean_sentence = sentence.strip()
                if clean_sentence and len(clean_sentence) > 15:  # Longer threshold for sentences
                    responsibilities.append(clean_sentence)
    
    # Limit to reasonable number
    return responsibilities[:10]

def display_requirements(job_info):
    """
    Display the analyzed job requirements in a user-friendly format.
    
    Args:
        job_info (dict): Analyzed job description
    """
    st.success("Job description analyzed successfully!")
    
    # Create tabs for different requirement categories
    skills_tab, exp_tab, edu_tab = st.tabs(["Skills", "Experience", "Education"])
    
    with skills_tab:
        st.subheader("Required Skills")
        
        if job_info.get("skills"):
            # Create skill tags with priority highlighting
            priority_skills = job_info.get("priority_skills", [])
            
            # Use columns to create a multi-column display
            cols = st.columns(3)
            
            for i, skill in enumerate(job_info["skills"]):
                is_priority = skill in priority_skills
                with cols[i % 3]:
                    st.markdown(
                        f"{skill}{' ⭐' if is_priority else ''}"
                    )
        else:
            st.info("No specific skills were identified in this job description.")

    with exp_tab:
        st.subheader("Experience Requirements")
        
        experience_info = job_info.get("experience", {})
        if experience_info:
            st.markdown(f"**Level:** {experience_info.get('level', 'Not specified')}")
            years = experience_info.get("years", {})
            if years.get("min", 0) > 0:
                if years.get("max"):
                    st.markdown(f"**Years:** {years['min']} - {years['max']} years")
                else:
                    st.markdown(f"**Years:** {years['min']}+ years")
        else:
            st.info("No specific experience requirements were identified.")

    with edu_tab:
        st.subheader("Education Requirements")
        
        education_info = job_info.get("education", {})
        if education_info:
            required = education_info.get("required")
            preferred = education_info.get("preferred")
            if required:
                st.markdown(f"**Required:** {required.replace('_', ' ').title()} Degree")
            if preferred and preferred != required:
                st.markdown(f"**Preferred:** {preferred.replace('_', ' ').title()} Degree")
            fields = education_info.get("fields", [])
            if fields:
                st.markdown("**Fields of Study:**")
                for field in fields:
                    st.markdown(f"- {field.strip().title()}")
        else:
            st.info("No specific education requirements were identified.")

    # Continue to resume upload
    st.markdown("---")
    if st.button("Continue to Resume Upload", type="primary", use_container_width=True):
        st.session_state.navigation = "Resume Upload"
        st.rerun()
