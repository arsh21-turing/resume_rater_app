# app/components/resume_matcher.py
"""
Resume Matching Module for Resume Rating App

This module provides functions to compare resumes against job descriptions
and calculate comprehensive match scores with detailed analysis.
"""

import re
import math
import numpy as np
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_match_score(resume_data, job_analysis, config=None):
    """
    Calculate a comprehensive match score between a resume and job description.
    
    Args:
        resume_data (dict): Parsed resume data containing skills, experience, etc.
        job_analysis (dict): Analyzed job description with requirements
        config (dict, optional): Configuration parameters for scoring weights
        
    Returns:
        dict: Comprehensive match report with overall score and category breakdowns
    """
    # Use default config if none provided
    if config is None:
        config = {
            'skill_weight': 0.5,
            'priority_skill_bonus': 2.0,
            'experience_weight': 0.3,
            'education_weight': 0.2,
            'skill_match_threshold': 0.7,
        }
    
    # Initialize scores
    skill_score = calculate_skill_match(resume_data.get('skills', []), 
                                        job_analysis.get('skills', []),
                                        job_analysis.get('priority_skills', []),
                                        config)
    
    experience_score = calculate_experience_match(resume_data.get('experience', []),
                                                job_analysis.get('experience', ''),
                                                config)
    
    education_score = calculate_education_match(resume_data.get('education', []),
                                             job_analysis.get('education', []),
                                             config)
    
    # Calculate overall score with weighted average
    overall_score = (
        skill_score['score'] * config['skill_weight'] +
        experience_score['score'] * config['experience_weight'] +
        education_score['score'] * config['education_weight']
    ) / (config['skill_weight'] + config['experience_weight'] + config['education_weight'])
    
    # Round to 2 decimal places
    overall_score = round(overall_score, 2)
    
    # Calculate category percentile rankings
    if overall_score >= 0.9:
        ranking = "Excellent Match"
        percentile = "Top 10%"
    elif overall_score >= 0.8:
        ranking = "Strong Match"
        percentile = "Top 20%"
    elif overall_score >= 0.7:
        ranking = "Good Match"
        percentile = "Top 30%"
    elif overall_score >= 0.6:
        ranking = "Fair Match"
        percentile = "Top 40%"
    else:
        ranking = "Needs Improvement"
        percentile = "Below Average"
    
    # Generate improvement suggestions
    improvement_suggestions = generate_improvement_suggestions(
        resume_data, 
        job_analysis,
        skill_score,
        experience_score,
        education_score
    )
    
    # Create comprehensive match report
    match_report = {
        'overall_score': overall_score,
        'ranking': ranking,
        'percentile': percentile,
        'skill_analysis': skill_score,
        'experience_analysis': experience_score,
        'education_analysis': education_score,
        'improvement_suggestions': improvement_suggestions,
        'keyword_density': calculate_keyword_density(resume_data.get('raw_text', ''), 
                                                  job_analysis.get('skills', [])),
        'content_similarity': calculate_content_similarity(resume_data.get('raw_text', ''),
                                                          job_analysis)
    }
    
    return match_report

def calculate_skill_match(resume_skills, job_skills, priority_skills, config):
    """
    Calculate the skill match score between resume and job requirements.
    
    Args:
        resume_skills (list): Skills extracted from the resume
        job_skills (list): Skills required in the job description
        priority_skills (list): Priority skills with higher importance
        config (dict): Scoring configuration parameters
        
    Returns:
        dict: Skill match analysis with scores and detailed breakdown
    """
    if not job_skills:
        return {
            'score': 1.0,  # If no skills required, perfect match
            'matched_skills': [],
            'missing_skills': [],
            'priority_matched': [],
            'priority_missing': [],
            'match_percentage': 100,
            'details': "No specific skills required in job description."
        }
    
    # Convert to lowercase for case-insensitive matching
    resume_skills_lower = [skill.lower() for skill in resume_skills]
    job_skills_lower = [skill.lower() for skill in job_skills]
    priority_skills_lower = [skill.lower() for skill in priority_skills]
    
    # Find matched and missing skills
    matched_skills = []
    missing_skills = []
    
    for skill in job_skills:
        skill_lower = skill.lower()
        if skill_lower in resume_skills_lower or any(skill_lower in rs for rs in resume_skills_lower):
            matched_skills.append(skill)
        else:
            missing_skills.append(skill)
    
    # Find priority skills matches
    priority_matched = [skill for skill in priority_skills if skill.lower() in resume_skills_lower]
    priority_missing = [skill for skill in priority_skills if skill.lower() not in resume_skills_lower]
    
    # Calculate match percentages
    total_skills = len(job_skills)
    matched_count = len(matched_skills)
    match_percentage = (matched_count / total_skills * 100) if total_skills > 0 else 100
    
    # Calculate priority skill match with bonus
    priority_bonus = config.get('priority_skill_bonus', 2.0)
    priority_match_score = 0
    
    if priority_skills:
        priority_total = len(priority_skills)
        priority_matched_count = len(priority_matched)
        priority_match_score = (priority_matched_count / priority_total) * priority_bonus
    
    # Calculate the final skill score
    base_score = matched_count / total_skills if total_skills > 0 else 1.0
    
    # Add priority bonus (weighted by priority skill proportion of total skills)
    priority_weight = len(priority_skills) / total_skills if total_skills > 0 else 0
    skill_score = base_score * (1 - priority_weight) + priority_match_score * priority_weight
    
    # Cap at 1.0
    skill_score = min(1.0, skill_score)
    
    # Create detailed analysis
    return {
        'score': round(skill_score, 2),
        'matched_skills': matched_skills,
        'missing_skills': missing_skills,
        'priority_matched': priority_matched,
        'priority_missing': priority_missing,
        'match_percentage': round(match_percentage, 1),
        'details': f"Matched {matched_count} of {total_skills} required skills ({match_percentage:.1f}%)."
    }

def calculate_experience_match(resume_experience, job_experience, config):
    """
    Calculate the experience match score between resume and job requirements.
    
    Args:
        resume_experience (list): Experience entries from the resume
        job_experience (str): Experience requirement from job description
        config (dict): Scoring configuration parameters
        
    Returns:
        dict: Experience match analysis with scores and detailed breakdown
    """
    # If no specific experience mentioned in job, default to full score
    if not job_experience:
        return {
            'score': 1.0,
            'years_required': None,
            'years_matched': None,
            'match_percentage': 100,
            'details': "No specific experience requirements in job description."
        }
    
    # Extract years of experience from job requirement
    job_years = extract_years_from_experience(job_experience)
    
    # If no specific years mentioned, check if its seniority-based
    if job_years is None:
        # Check if this is a seniority level match
        seniority_score = match_seniority_level(resume_experience, job_experience)
        return {
            'score': seniority_score,
            'years_required': None,
            'years_matched': None,
            'match_percentage': round(seniority_score * 100, 1),
            'details': f"Seniority level match: {seniority_score:.2f}"
        }
    
    # Calculate total years of experience from resume
    resume_years = calculate_total_experience_years(resume_experience)
    
    # Calculate match percentage
    if job_years > 0:
        if resume_years >= job_years:
            match_score = 1.0
            match_percentage = 100
        else:
            # Partial credit based on percentage of required experience
            match_score = resume_years / job_years
            match_percentage = (resume_years / job_years * 100)
    else:
        match_score = 1.0
        match_percentage = 100
    
    return {
        'score': round(match_score, 2),
        'years_required': job_years,
        'years_matched': resume_years,
        'match_percentage': round(match_percentage, 1),
        'details': f"Job requires {job_years} years of experience. Resume shows {resume_years} years."
    }

def calculate_education_match(resume_education, job_education, config):
    """
    Calculate the education match score between resume and job requirements.
    
    Args:
        resume_education (list): Education entries from the resume
        job_education (list): Education requirements from job description
        config (dict): Scoring configuration parameters
        
    Returns:
        dict: Education match analysis with scores and detailed breakdown
    """
    # If no specific education requirements in job, default to full score
    if not job_education:
        return {
            'score': 1.0,
            'degree_required': None,
            'degree_matched': True,
            'field_match': None,
            'match_percentage': 100,
            'details': "No specific education requirements in job description."
        }
    
    # Extract degree requirements from job description
    required_degrees = extract_degree_requirements(job_education)
    required_fields = extract_field_requirements(job_education)
    
    # Extract degrees from resume
    resume_degrees = extract_degrees_from_resume(resume_education)
    resume_fields = extract_fields_from_resume(resume_education)
    
    # Calculate degree match score
    degree_match_score = 0.0
    matched_degrees = []
    
    for req_degree in required_degrees:
        for res_degree in resume_degrees:
            match_score = calculate_degree_match_score(res_degree, req_degree)
            if match_score > 0:
                degree_match_score = max(degree_match_score, match_score)
                matched_degrees.append(req_degree)
    
    # Calculate field match score
    field_match_score = 0.0
    matched_fields = []
    
    for req_field in required_fields:
        for res_field in resume_fields:
            if field_similarity(res_field, req_field) >= 0.7:  # Threshold for field match
                field_match_score = 1.0
                matched_fields.append(req_field)
    
    # If no fields specified in job, give full score for fields
    if not required_fields:
        field_match_score = 1.0
    
    # Combined score: 70% degree type, 30% field of study
    combined_score = (0.7 * degree_match_score) + (0.3 * field_match_score)
    match_percentage = round(combined_score * 100, 1)
    
    # Create detailed analysis
    details = []
    if required_degrees:
        degrees_str = ", ".join(required_degrees)
        matched_str = ", ".join(matched_degrees) if matched_degrees else "None"
        details.append(f"Required degree(s): {degrees_str}. Matched: {matched_str}")
    
    if required_fields:
        fields_str = ", ".join(required_fields)
        matched_fields_str = ", ".join(matched_fields) if matched_fields else "None"
        details.append(f"Required field(s): {fields_str}. Matched: {matched_fields_str}")
    
    return {
        'score': round(combined_score, 2),
        'degree_required': required_degrees,
        'degree_matched': bool(matched_degrees) if required_degrees else True,
        'field_match': matched_fields,
        'match_percentage': match_percentage,
        'details': " ".join(details) if details else "Education requirements are not specific enough to evaluate."
    }

def calculate_keyword_density(resume_text, job_keywords):
    """
    Calculate keyword density and distribution in the resume.
    
    Args:
        resume_text (str): Full text of the resume
        job_keywords (list): Keywords from job description
        
    Returns:
        dict: Keyword density analysis
    """
    if not resume_text or not job_keywords:
        return {
            'score': 0,
            'keyword_count': {},
            'density': 0,
            'distribution': 0
        }
    
    # Count total words in resume
    words = re.findall(r'\b\w+\b', resume_text.lower())
    total_words = len(words)
    
    if total_words == 0:
        return {
            'score': 0,
            'keyword_count': {},
            'density': 0,
            'distribution': 0
        }
    
    # Count occurrences of each keyword
    keyword_count = {}
    for keyword in job_keywords:
        pattern = r'\b' + re.escape(keyword.lower()) + r'\b'
        matches = re.findall(pattern, resume_text.lower())
        if matches:
            keyword_count[keyword] = len(matches)
    
    # Calculate overall keyword density
    total_keywords = sum(keyword_count.values())
    density = total_keywords / total_words
    
    # Calculate distribution score (how many sections contain keywords)
    sections = re.split(r'\n\s*\n|\r\n\s*\r\n', resume_text)  # Split by empty lines
    sections_with_keywords = 0
    
    for section in sections:
        has_keyword = False
        for keyword in job_keywords:
            if re.search(r'\b' + re.escape(keyword.lower()) + r'\b', section.lower()):
                has_keyword = True
                break
        if has_keyword:
            sections_with_keywords += 1
    
    distribution = sections_with_keywords / len(sections) if sections else 0
    
    # Calculate overall score
    score = (0.7 * min(density * 50, 1)) + (0.3 * distribution)  # Cap density score at 1.0
    
    return {
        'score': round(score, 2),
        'keyword_count': keyword_count,
        'density': round(density * 100, 2),  # As percentage
        'distribution': round(distribution * 100, 2)  # As percentage
    }

def calculate_content_similarity(resume_text, job_analysis):
    """
    Calculate semantic similarity between resume and job description.
    
    Args:
        resume_text (str): Full text of the resume
        job_analysis (dict): Analyzed job description
        
    Returns:
        dict: Content similarity analysis
    """
    # Extract responsibilities from job description for semantic comparison
    job_responsibilities = " ".join(job_analysis.get('responsibilities', []))
    
    if not resume_text or not job_responsibilities:
        return {
            'score': 0,
            'similarity': 0,
            'top_matching_sections': []
        }
    
    # Split resume into sections
    sections = re.split(r'\n\s*\n|\r\n\s*\r\n', resume_text)
    
    # Calculate similarity for each section
    vectorizer = TfidfVectorizer(stop_words='english')
    
    try:
        # Add job responsibilities to documents for vectorization
        documents = [job_responsibilities] + sections
        
        # Create TF-IDF matrix
        tfidf_matrix = vectorizer.fit_transform(documents)
        
        # Calculate cosine similarity between job description and each resume section
        similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
        
        # Get top 3 matching sections
        top_indices = similarities.argsort()[-3:][::-1]
        top_matching_sections = [(sections[i][:100] + "..." if len(sections[i]) > 100 else sections[i], 
                                 round(similarities[i] * 100, 1)) 
                                for i in top_indices if similarities[i] > 0]
        
        # Calculate overall similarity score
        max_similarity = similarities.max() if similarities.size > 0 else 0
        avg_similarity = similarities.mean() if similarities.size > 0 else 0
        
        overall_score = (0.7 * max_similarity) + (0.3 * avg_similarity)
        
        return {
            'score': round(overall_score, 2),
            'similarity': round(max_similarity * 100, 1),  # As percentage
            'top_matching_sections': top_matching_sections
        }
        
    except Exception as e:
        # Fallback if vectorization fails
        return {
            'score': 0,
            'similarity': 0,
            'top_matching_sections': [],
            'error': str(e)
        }

def generate_improvement_suggestions(resume_data, job_analysis, skill_score, experience_score, education_score):
    """
    Generate specific improvement suggestions based on match analysis.
    
    Args:
        resume_data (dict): Parsed resume data
        job_analysis (dict): Analyzed job description
        skill_score (dict): Skill match analysis
        experience_score (dict): Experience match analysis
        education_score (dict): Education match analysis
        
    Returns:
        list: Specific improvement suggestions
    """
    suggestions = []
    
    # Skill improvement suggestions
    if skill_score['missing_skills']:
        if len(skill_score['missing_skills']) <= 3:
            skills_to_add = ", ".join(skill_score['missing_skills'])
            suggestions.append(f"Add missing skills: {skills_to_add}")
        else:
            priority_missing = skill_score['priority_missing'] if 'priority_missing' in skill_score else []
            if priority_missing:
                priority_to_add = ", ".join(priority_missing[:3])
                suggestions.append(f"Focus on adding these priority skills: {priority_to_add}")
            else:
                skills_to_add = ", ".join(skill_score['missing_skills'][:3])
                suggestions.append(f"Add key missing skills: {skills_to_add}")
            
            suggestions.append(f"Work on developing {len(skill_score['missing_skills'])} missing skills identified in the job description")
    
    # Experience improvement suggestions
    years_required = experience_score.get('years_required')
    years_matched = experience_score.get('years_matched')
    
    if years_required and years_matched and years_matched < years_required:
        gap = years_required - years_matched
        if gap <= 2:
            suggestions.append(f"Highlight relevant projects or additional responsibilities to compensate for the {gap} year experience gap")
        else:
            suggestions.append(f"Consider roles requiring less experience or emphasize rapid skill acquisition and relevant achievements")
    
    # Education improvement suggestions
    if not education_score.get('degree_matched', True):
        required_degrees = education_score.get('degree_required', [])
        if required_degrees:
            degree_str = ", ".join(required_degrees)
            suggestions.append(f"The job requires {degree_str}. Consider highlighting equivalent experience or continuing education")
    
    # Add general suggestions if few specific ones
    if len(suggestions) < 2:
        # Check resume length
        if resume_data.get('raw_text') and len(resume_data['raw_text'].split()) < 300:
            suggestions.append("Your resume appears brief. Consider adding more detail about your achievements and responsibilities")
        
        # Keyword optimization
        if skill_score['matched_skills']:
            suggestions.append("Optimize keyword placement by ensuring skills appear in both your summary and work experience sections")
        
        # Achievements
        suggestions.append("Quantify your achievements with metrics and specific results to stand out from other candidates")
    
    return suggestions

# Helper functions for calculating scores

def extract_years_from_experience(experience_text):
    """
    Extract required years from experience text.
    
    Args:
        experience_text (str or dict): Experience text or structured data
        
    Returns:
        int or None: Number of years required, or None if not specified
    """
    # Handle if we received a dictionary instead of string
    if isinstance(experience_text, dict):
        # Try to extract from description field if available
        if 'description' in experience_text:
            experience_text = experience_text['description']
        # If we have a years field, use that directly
        elif 'years' in experience_text:
            try:
                return int(experience_text['years'])
            except (ValueError, TypeError):
                return None
        else:
            # Try to concatenate all string values in the dict
            text_parts = []
            for value in experience_text.values():
                if isinstance(value, str):
                    text_parts.append(value)
            experience_text = ' '.join(text_parts)
    
    # If we still don't have a string after all that, return None
    if not isinstance(experience_text, str):
        return None
    
    # Look for patterns like "X years"
    year_patterns = [
        r'(\d+)\+?\s*years?',
        r'(\d+)\s*\+\s*years?',
        r'minimum\s*of\s*(\d+)\s*years?',
        r'at\s*least\s*(\d+)\s*years?',
        r'(\d+)[-\s](\d+)\s*years?'  # Range like "3-5 years"
    ]
    
    for pattern in year_patterns:
        match = re.search(pattern, experience_text, re.IGNORECASE)
        if match:
            # If we matched a range (e.g., "3-5 years"), take the lower value
            if len(match.groups()) >= 2 and match.group(2) and match.group(2).isdigit():
                return int(match.group(1))
            return int(match.group(1))
    
    # Check for common experience level phrases
    exp_phrases = {
        'entry level': 0,
        'junior': 1,
        'mid-level': 3,
        'mid level': 3,
        'intermediate': 3,
        'senior': 5,
        'experienced': 4,
        'principal': 8,
        'lead': 6,
        'manager': 5,
        'director': 8,
        'executive': 10
    }
    
    for phrase, years in exp_phrases.items():
        if phrase in experience_text.lower():
            return years
    
    return None

def match_seniority_level(resume_experience, job_experience):
    """Match seniority level when specific years aren't mentioned"""
    job_exp_lower = job_experience.lower() if isinstance(job_experience, str) else ""
    
    # Define seniority levels and their scores
    seniority_levels = {
        'entry': 0.2,
        'junior': 0.4,
        'mid': 0.6,
        'senior': 0.8,
        'lead': 0.9,
        'principal': 1.0,
        'staff': 0.9,
        'manager': 0.9,
        'director': 1.0,
        'vp': 1.0,
        'head': 1.0,
        'chief': 1.0
    }
    
    # Estimate job seniority level
    job_seniority = 0.5  # Default to mid-level
    for level, score in seniority_levels.items():
        if level in job_exp_lower:
            job_seniority = score
            break
    
    # Calculate total years from resume to estimate seniority
    total_years = calculate_total_experience_years(resume_experience)
    
    # Map years to seniority score
    resume_seniority = 0
    if total_years >= 10:
        resume_seniority = 1.0
    elif total_years >= 8:
        resume_seniority = 0.9
    elif total_years >= 5:
        resume_seniority = 0.8
    elif total_years >= 3:
        resume_seniority = 0.6
    elif total_years >= 1:
        resume_seniority = 0.4
    else:
        resume_seniority = 0.2
    
    # Check for seniority terms in resume roles
    for exp in resume_experience:
        if not isinstance(exp, dict):
            continue
            
        title = exp.get('title', '').lower()
        for level, score in seniority_levels.items():
            if level in title:
                resume_seniority = max(resume_seniority, score)
    
    # If resume seniority exceeds job seniority, perfect match
    if resume_seniority >= job_seniority:
        return 1.0
    
    # Otherwise partial credit
    return resume_seniority / job_seniority if job_seniority > 0 else 1.0

def calculate_total_experience_years(experience_entries):
    """Calculate total years of experience from resume entries"""
    total_years = 0
    
    if not experience_entries:
        return total_years
        
    # Ensure we're working with a list
    if not isinstance(experience_entries, list):
        if isinstance(experience_entries, dict):
            experience_entries = [experience_entries]
        else:
            return total_years
            
    for entry in experience_entries:
        if not isinstance(entry, dict):
            continue
            
        # Each entry expected to have a 'duration' or 'years' field
        if 'years' in entry:
            try:
                total_years += float(entry['years'])
            except (ValueError, TypeError):
                pass
        elif 'duration' in entry:
            # Extract years from duration string like "2 years 3 months"
            duration = str(entry['duration']).lower()
            years_match = re.search(r'(\d+)\s*years?', duration)
            months_match = re.search(r'(\d+)\s*months?', duration)
            
            years = float(years_match.group(1)) if years_match else 0
            months = float(months_match.group(1))/12 if months_match else 0
            
            total_years += years + months
        elif 'start_date' in entry and 'end_date' in entry:
            # Calculate duration from start and end dates
            # This is a simplified version, in practice you'd use proper date parsing
            start_year = extract_year_from_date(entry['start_date'])
            end_year = extract_year_from_date(entry.get('end_date', 'Present'))
            
            if start_year and end_year:
                if end_year == 'Present' or end_year == 'Current':
                    # Assume present is current year
                    import datetime
                    end_year = datetime.datetime.now().year
                
                try:
                    years = float(end_year) - float(start_year)
                    total_years += max(0, years)  # Ensure no negative values
                except (ValueError, TypeError):
                    pass
    
    return round(total_years, 1)

def extract_year_from_date(date_str):
    """Extract year from date string"""
    if not date_str:
        return None
    
    # Convert to string if needed
    date_str = str(date_str)
    
    year_match = re.search(r'20\d{2}|19\d{2}', date_str)
    if year_match:
        return year_match.group(0)
    
    return None

def extract_degree_requirements(education_requirements):
    """Extract required degrees from education requirements"""
    degrees = []
    degree_patterns = {
        "bachelor": ["bachelor", "bachelors", "bachelor's", "bs", "ba", "b.s.", "b.a.", "undergraduate"],
        "master": ["master", "masters", "master's", "ms", "ma", "m.s.", "m.a.", "graduate"],
        "doctorate": ["ph.d", "phd", "doctorate", "doctoral", "doctor of philosophy"],
        "associate": ["associate", "associates", "associate's", "aa", "a.a.", "a.s."]
    }
    
    # Handle if we got a string instead of a list
    if isinstance(education_requirements, str):
        education_requirements = [education_requirements]
        
    if not isinstance(education_requirements, list):
        return degrees
    
    for req in education_requirements:
        if not isinstance(req, str):
            continue
            
        req_lower = req.lower()
        for degree, patterns in degree_patterns.items():
            if any(pattern in req_lower for pattern in patterns):
                degrees.append(degree)
    
    return list(set(degrees))  # Remove duplicates

def extract_field_requirements(education_requirements):
    """Extract required fields of study from education requirements"""
    common_fields = [
        "computer science", "information technology", "software engineering",
        "data science", "mathematics", "statistics", "engineering",
        "business", "finance", "economics", "marketing", "accounting",
        "biology", "chemistry", "physics", "psychology", "sociology",
        "communications", "english", "history", "arts", 
        "healthcare", "nursing", "medicine", "pharmacy"
    ]
    
    fields = []
    
    # Handle if we got a string instead of a list
    if isinstance(education_requirements, str):
        education_requirements = [education_requirements]
        
    if not isinstance(education_requirements, list):
        return fields
    
    for req in education_requirements:
        if not isinstance(req, str):
            continue
            
        req_lower = req.lower()
        for field in common_fields:
            if field in req_lower:
                fields.append(field)
    
    return list(set(fields))  # Remove duplicates

def extract_degrees_from_resume(education_entries):
    """Extract degrees from resume education entries"""
    degrees = []
    
    # Handle if we got a string instead of a list
    if isinstance(education_entries, str):
        education_entries = [{"degree": education_entries}]
        
    if not isinstance(education_entries, list):
        return degrees
    
    for entry in education_entries:
        if not isinstance(entry, dict):
            continue
            
        degree = str(entry.get('degree', '')).lower()
        
        if 'bachelor' in degree or ' bs ' in f" {degree} " or ' ba ' in f" {degree} " or 'b.s' in degree or 'b.a' in degree:
            degrees.append('bachelor')
        elif 'master' in degree or ' ms ' in f" {degree} " or ' ma ' in f" {degree} " or 'm.s' in degree or 'm.a' in degree:
            degrees.append('master')
        elif 'phd' in degree or 'ph.d' in degree or 'doctor' in degree:
            degrees.append('doctorate')
        elif 'associate' in degree or 'a.a' in degree or 'a.s' in degree:
            degrees.append('associate')
    
    return list(set(degrees))  # Remove duplicates

def extract_fields_from_resume(education_entries):
    """Extract fields of study from resume education entries"""
    fields = []
    
    # Handle if we got a string instead of a list
    if isinstance(education_entries, str):
        education_entries = [{"field": education_entries}]
        
    if not isinstance(education_entries, list):
        return fields
    
    for entry in education_entries:
        if not isinstance(entry, dict):
            continue
            
        field = str(entry.get('field', ''))
        if field:
            fields.append(field.lower())
        
        # Sometimes field is in degree text
        degree_text = str(entry.get('degree', ''))
        if 'in ' in degree_text.lower():
            field_match = re.search(r'in\s+([A-Za-z\s]+)', degree_text, re.IGNORECASE)
            if field_match:
                fields.append(field_match.group(1).lower())
    
    return list(set(fields))  # Remove duplicates

def calculate_degree_match_score(resume_degree, required_degree):
    """Calculate match score between resume degree and required degree"""
    # Define degree hierarchy
    degree_hierarchy = {
        'associate': 1,
        'bachelor': 2,
        'master': 3,
        'doctorate': 4
    }
    
    # Get numeric values for comparison
    resume_level = degree_hierarchy.get(resume_degree, 0)
    required_level = degree_hierarchy.get(required_degree, 0)
    
    # Exact match
    if resume_degree == required_degree:
        return 1.0
    
    # Higher degree than required
    if resume_level > required_level:
        return 1.0
    
    # Lower degree than required
    if resume_level > 0 and required_level > 0:
        # Partial credit based on how close the degrees are
        return resume_level / required_level
    
    # No match
    return 0.0

def field_similarity(resume_field, required_field):
    """Calculate similarity between fields of study"""
    # Direct match
    if resume_field == required_field:
        return 1.0
    
    # Define related fields with similarity scores
    related_fields = {
        'computer science': {
            'software engineering': 0.9,
            'information technology': 0.8,
            'data science': 0.8,
            'information systems': 0.7,
            'mathematics': 0.6,
            'engineering': 0.6
        },
        'data science': {
            'statistics': 0.9,
            'mathematics': 0.8,
            'computer science': 0.8,
            'analytics': 0.9,
            'machine learning': 0.9
        },
        'business': {
            'finance': 0.8,
            'marketing': 0.7,
            'economics': 0.8,
            'management': 0.9,
            'accounting': 0.7,
            'mba': 0.9
        },
        'engineering': {
            'mechanical engineering': 0.9,
            'electrical engineering': 0.8,
            'civil engineering': 0.7,
            'computer engineering': 0.8,
            'software engineering': 0.7
        }
    }
    
    # Check if we have similarity data for the required field
    if required_field in related_fields:
        # Check if resume field is in the related fields
        if resume_field in related_fields[required_field]:
            return related_fields[required_field][resume_field]
    
    # Check the reverse relation
    if resume_field in related_fields:
        if required_field in related_fields[resume_field]:
            return related_fields[resume_field][required_field]
    
    # Check if the fields contain each other
    if required_field in resume_field or resume_field in required_field:
        return 0.7
    
    # Default low similarity for unrelated fields
    return 0.2

# Add this function to integrate the matching
def compare_resume_to_job(resume_data, job_analysis):
    """
    Compare the resume to the job description and calculate match scores.
    
    Args:
        resume_data (dict): The parsed resume data
        job_analysis (dict): The analyzed job description
        
    Returns:
        dict: Match report with scores and analysis
    """
    # Call the main matching function
    match_report = calculate_match_score(resume_data, job_analysis)
    return match_report