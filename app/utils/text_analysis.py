"""
Text analysis utilities for processing and analyzing resumes and job descriptions.

This module provides functions for extracting skills, experience, education, and 
other relevant information from text documents for resume matching and evaluation.
"""

import re
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from typing import Dict, List, Set, Tuple, Optional
import string

# Ensure NLTK resources are available
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

# Common technical skills to look for in resumes and job descriptions
COMMON_TECHNICAL_SKILLS = {
    'programming_languages': [
        'python', 'java', 'javascript', 'c++', 'c#', 'ruby', 'go', 'rust', 'php',
        'typescript', 'kotlin', 'swift', 'scala', 'perl', 'sql', 'bash', 'r', 'matlab'
    ],
    'web_development': [
        'html', 'css', 'react', 'angular', 'vue', 'node.js', 'express', 'django',
        'flask', 'spring', 'asp.net', 'jquery', 'bootstrap', 'tailwind', 'laravel',
        'ruby on rails', 'wordpress', 'php', 'gatsby', 'next.js', 'graphql', 'rest api'
    ],
    'databases': [
        'mysql', 'postgresql', 'mongodb', 'sqlite', 'oracle', 'sql server', 'redis',
        'dynamodb', 'cassandra', 'firebase', 'mariadb', 'elasticsearch', 'neo4j'
    ],
    'cloud_platforms': [
        'aws', 'azure', 'google cloud', 'gcp', 'heroku', 'digitalocean', 'firebase',
        'cloudflare', 'vercel', 'netlify', 'alibaba cloud', 'ibm cloud'
    ],
    'devops': [
        'docker', 'kubernetes', 'jenkins', 'gitlab ci', 'github actions', 'travis ci',
        'terraform', 'ansible', 'chef', 'puppet', 'circleci', 'prometheus', 'grafana'
    ],
    'data_science': [
        'pandas', 'numpy', 'scikit-learn', 'tensorflow', 'pytorch', 'keras', 'matplotlib',
        'seaborn', 'tableau', 'power bi', 'hadoop', 'spark', 'nlp', 'machine learning',
        'deep learning', 'computer vision', 'data mining', 'statistics'
    ]
}

# Combine all skills into a single list
ALL_SKILLS = [skill for category in COMMON_TECHNICAL_SKILLS.values() for skill in category]

# Education keywords
EDUCATION_KEYWORDS = [
    'bachelor', 'master', 'phd', 'doctorate', 'mba', 'bs', 'ba', 'ms', 'ma', 'degree', 
    'university', 'college', 'institute', 'certification', 'diploma', 'graduate',
    'undergraduate', 'postgraduate'
]

# Experience level indicators
EXPERIENCE_INDICATORS = {
    'entry_level': ['entry level', 'junior', 'intern', 'internship', '0-1 year', '1 year', 
                    'entry-level', 'graduate', 'fresh graduate', 'trainee'],
    'mid_level': ['mid level', 'mid-level', 'intermediate', '2 years', '3 years', '4 years',
                  '2-4 years', 'experienced'],
    'senior_level': ['senior', 'lead', 'principal', '5+ years', 'expert', 'sr.', 'manager',
                     'architect', '5 years', '6 years', '7 years', '8 years', 'experienced']
}

def preprocess_text(text: str) -> str:
    """
    Preprocess text by converting to lowercase, removing punctuation, etc.
    
    Args:
        text: The text to preprocess.
        
    Returns:
        The preprocessed text.
    """
    # Convert to lowercase
    text = text.lower()
    
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def extract_skills(text: str, custom_skills: Optional[List[str]] = None) -> List[str]:
    """
    Extract skills from the given text.
    
    Args:
        text: The text to extract skills from.
        custom_skills: Optional list of custom skills to look for.
        
    Returns:
        A list of skills found in the text.
    """
    # Preprocess text
    processed_text = preprocess_text(text)
    
    # Skills to search for
    skills_to_search = ALL_SKILLS.copy()
    if custom_skills:
        skills_to_search.extend([skill.lower() for skill in custom_skills])
    
    # Find skills in the text
    found_skills = []
    for skill in skills_to_search:
        skill = skill.lower()
        # Match whole words only
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, processed_text):
            found_skills.append(skill)
    
    return found_skills

def extract_education(text: str) -> List[str]:
    """
    Extract education information from the given text.
    
    Args:
        text: The text to extract education from.
        
    Returns:
        A list of education information found in the text.
    """
    education_info = []
    sentences = sent_tokenize(text)
    
    for sentence in sentences:
        # Check if the sentence contains education-related keywords
        if any(keyword in sentence.lower() for keyword in EDUCATION_KEYWORDS):
            education_info.append(sentence.strip())
    
    return education_info

def extract_experience(text: str) -> Dict[str, List[str]]:
    """
    Extract experience information from the text.
    
    Args:
        text: The text to extract experience from.
        
    Returns:
        A dictionary with experience level and corresponding sentences.
    """
    experience_info = {
        'entry_level': [],
        'mid_level': [],
        'senior_level': []
    }
    
    sentences = sent_tokenize(text)
    
    for sentence in sentences:
        sentence_lower = sentence.lower()
        
        # Check each experience level
        for level, indicators in EXPERIENCE_INDICATORS.items():
            if any(indicator in sentence_lower for indicator in indicators):
                experience_info[level].append(sentence.strip())
    
    # If years of experience found in text
    years_pattern = r'\b(\d+)\s*(?:-\s*\d+)?\s*(?:years|year|yrs|yr)(?:\s+of\s+experience)?\b'
    years_matches = re.findall(years_pattern, text.lower())
    
    return experience_info

def calculate_skill_match_score(job_skills: List[str], resume_skills: List[str]) -> float:
    """
    Calculate the skill match score between job skills and resume skills.
    
    Args:
        job_skills: List of skills required for the job.
        resume_skills: List of skills in the resume.
        
    Returns:
        A score between 0.0 and 1.0 indicating the match quality.
    """
    if not job_skills:
        return 0.0
    
    # Convert to sets and make case insensitive
    job_skills_set = {skill.lower() for skill in job_skills}
    resume_skills_set = {skill.lower() for skill in resume_skills}
    
    # Find matching skills
    matching_skills = job_skills_set.intersection(resume_skills_set)
    
    # Calculate score
    score = len(matching_skills) / len(job_skills_set)
    
    return score

def analyze_job_description(job_description: str) -> Dict[str, any]:
    """
    Analyze a job description to extract key information.
    
    Args:
        job_description: The job description text.
        
    Returns:
        A dictionary containing extracted information including skills, experience, etc.
    """
    result = {}
    
    # Extract skills
    result['required_skills'] = extract_skills(job_description)
    
    # Extract education requirements
    result['education'] = extract_education(job_description)
    
    # Extract experience
    result['experience'] = extract_experience(job_description)
    
    # Extract job title (assuming it's in the first few sentences)
    sentences = sent_tokenize(job_description)
    job_title_patterns = [
        r'job title:?\s*(.*?)(?:\.|$)',
        r'position:?\s*(.*?)(?:\.|$)',
        r'role:?\s*(.*?)(?:\.|$)',
    ]
    
    job_title = None
    for pattern in job_title_patterns:
        for sentence in sentences[:3]:  # Check first 3 sentences only
            match = re.search(pattern, sentence, re.IGNORECASE)
            if match:
                job_title = match.group(1).strip()
                break
        if job_title:
            break
    
    result['job_title'] = job_title
    
    # Extract location (assuming it's in the first few sentences)
    location_patterns = [
        r'location:?\s*(.*?)(?:\.|$)',
        r'based in:?\s*(.*?)(?:\.|$)',
        r'position located in:?\s*(.*?)(?:\.|$)',
    ]
    
    location = None
    for pattern in location_patterns:
        for sentence in sentences[:5]:  # Check first 5 sentences only
            match = re.search(pattern, sentence, re.IGNORECASE)
            if match:
                location = match.group(1).strip()
                break
        if location:
            break
    
    result['location'] = location
    
    return result

def analyze_resume(resume_text: str) -> Dict[str, any]:
    """
    Analyze a resume to extract key information.
    
    Args:
        resume_text: The resume text.
        
    Returns:
        A dictionary containing extracted information including skills, experience, etc.
    """
    result = {}
    
    # Extract skills
    result['skills'] = extract_skills(resume_text)
    
    # Extract education
    result['education'] = extract_education(resume_text)
    
    # Extract experience
    result['experience'] = extract_experience(resume_text)
    
    # Get all sentences with potential contact information
    sentences = sent_tokenize(resume_text)
    
    # Extract email
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, resume_text)
    result['email'] = emails[0] if emails else None
    
    # Extract phone number
    phone_pattern = r'\b(?:\+\d{1,3}[- ]?)?\(?\d{3}\)?[- ]?\d{3}[- ]?\d{4}\b'
    phones = re.findall(phone_pattern, resume_text)
    result['phone'] = phones[0] if phones else None
    
    # Try to extract name from the beginning of the resume
    name_candidate = None
    for sentence in sentences[:3]:  # Check first 3 sentences
        # Simple heuristic: First line with 2-3 words could be a name
        words = sentence.strip().split()
        if 2 <= len(words) <= 3 and all(len(word) > 1 for word in words):
            name_candidate = sentence.strip()
            break
    
    result['name'] = name_candidate
    
    return result

def generate_improvement_suggestions(job_analysis: Dict[str, any], resume_analysis: Dict[str, any]) -> List[str]:
    """
    Generate suggestions to improve the resume based on job requirements.
    
    Args:
        job_analysis: Analysis of the job description.
        resume_analysis: Analysis of the resume.
        
    Returns:
        A list of improvement suggestions.
    """
    suggestions = []
    
    # Check for missing skills
    job_skills = {skill.lower() for skill in job_analysis.get('required_skills', [])}
    resume_skills = {skill.lower() for skill in resume_analysis.get('skills', [])}
    
    missing_skills = job_skills - resume_skills
    if missing_skills:
        suggestions.append(f"Add these missing skills to your resume: {', '.join(missing_skills)}")
    
    # Check for education requirements
    job_education = job_analysis.get('education', [])
    resume_education = resume_analysis.get('education', [])
    
    # Simple check if education keywords are mentioned
    if job_education and not resume_education:
        suggestions.append("Include your education background in your resume.")
    
    # Check for experience level
    job_experience = job_analysis.get('experience', {})
    resume_experience = resume_analysis.get('experience', {})
    
    # If job requires senior experience but resume indicates entry level
    if job_experience.get('senior_level') and resume_experience.get('entry_level') and not resume_experience.get('senior_level'):
        suggestions.append("Emphasize more senior-level experience in your resume.")
    
    return suggestions