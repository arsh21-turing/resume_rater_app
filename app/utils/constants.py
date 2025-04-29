# app/utils/constants.py
"""
Constants for the Resume Rating App.

This module contains all constant values used across the application,
including lists of skills, degree levels, job categories, etc.
"""

# Skills categorization
COMMON_SKILLS = [
    # Technical Skills
    "Python", "JavaScript", "Java", "C++", "C#", "Ruby", "PHP", "Swift", "Kotlin", "Go",
    "React", "Angular", "Vue.js", "Node.js", "Django", "Flask", "Spring", "ASP.NET",
    "SQL", "MongoDB", "PostgreSQL", "MySQL", "Oracle", "NoSQL", "Redis",
    "AWS", "Azure", "Google Cloud", "Kubernetes", "Docker", "Jenkins", "Git", "CI/CD",
    "Machine Learning", "Deep Learning", "AI", "Data Analysis", "Data Science", "Statistics",
    "TensorFlow", "PyTorch", "scikit-learn", "NLP", "Computer Vision",
    "HTML", "CSS", "JavaScript", "TypeScript", "REST API", "GraphQL", "JSON", "XML",
    "Agile", "Scrum", "Jira", "Confluence", "DevOps", "Testing", "QA", "Test Automation",
    
    # Soft Skills
    "Communication", "Leadership", "Teamwork", "Problem Solving", "Critical Thinking", 
    "Time Management", "Adaptability", "Collaboration", "Creativity", "Attention to Detail",
    "Project Management", "Presentation Skills", "Analytical Skills", "Decision Making",
    "Organizational Skills", "Interpersonal Skills", "Negotiation", "Conflict Resolution",
    
    # Business Skills
    "Strategic Planning", "Business Analysis", "Product Management", "Marketing", 
    "Sales", "Customer Service", "Financial Analysis", "Market Research", "Operations",
    "Consulting", "Risk Management", "Compliance", "Legal", "Regulatory"
]

# Education categorization
DEGREE_LEVELS = [
    "Associate's", "Bachelor's", "Master's", "MBA", "PhD", "Doctorate", 
    "Professional Certification", "Diploma", "High School"
]

# Experience level categorization
EXPERIENCE_LEVELS = [
    "Entry Level", "Junior", "Mid-Level", "Senior", "Principal",
    "Manager", "Director", "VP", "C-Level", "Executive"
]

# Job category categorization
JOB_CATEGORIES = [
    "Software Development", "Data Science", "Data Engineering", "Web Development",
    "Mobile Development", "DevOps", "Cloud Engineering", "QA Testing",
    "UI/UX Design", "Product Management", "Project Management",
    "Business Analysis", "Technical Support", "IT Security", "Database Administration",
    "Network Engineering", "Systems Engineering", "Machine Learning Engineering",
    "Technical Writing", "IT Management"
]

# Location type categorization
LOCATION_TYPES = ["On-site", "Remote", "Hybrid"]

# Salary range categorization
SALARY_RANGES = [
    "Under $50,000", "$50,000 - $75,000", "$75,000 - $100,000",
    "$100,000 - $125,000", "$125,000 - $150,000", "$150,000 - $200,000",
    "$200,000+"
]

# Skill categorization for organizing display
SKILL_CATEGORIES = {
    "Programming Languages": [
        "Python", "JavaScript", "Java", "C++", "C#", "Ruby", "PHP", "Swift", 
        "Kotlin", "Go", "TypeScript", "SQL"
    ],
    "Web Development": [
        "HTML", "CSS", "JavaScript", "React", "Angular", "Vue.js", "Node.js", 
        "Django", "Flask", "REST API", "GraphQL", "JSON", "XML"
    ],
    "Database": [
        "SQL", "MongoDB", "PostgreSQL", "MySQL", "Oracle", "NoSQL", "Redis"
    ],
    "DevOps & Cloud": [
        "AWS", "Azure", "Google Cloud", "Kubernetes", "Docker", "Jenkins", 
        "Git", "CI/CD", "DevOps"
    ],
    "Data Science": [
        "Machine Learning", "Deep Learning", "AI", "Data Analysis", "Data Science", 
        "Statistics", "TensorFlow", "PyTorch", "scikit-learn", "NLP", "Computer Vision"
    ],
    "Soft Skills": [
        "Communication", "Leadership", "Teamwork", "Problem Solving", "Critical Thinking",
        "Time Management", "Adaptability", "Collaboration", "Creativity", "Attention to Detail"
    ]
}

# Weight factors for scoring
SCORING_WEIGHTS = {
    "required_skills": 0.5,
    "preferred_skills": 0.2,
    "education": 0.15,
    "experience": 0.15
}

# Analysis settings
SKILL_EXTRACTION_THRESHOLD = 0.7
EXPERIENCE_MATCH_THRESHOLD = 0.8

# File upload settings
ALLOWED_EXTENSIONS = ["pdf", "docx", "txt"]
MAX_FILE_SIZE = 5  # in MB