# app/pages/about.py
import streamlit as st
import graphviz

def display_about():
    """
    Display the About page with information about the application,
    how it works, and credits.
    """
   
    # Center the title using HTML/CSS and make it blue
    st.markdown("<h1 style='text-align: center; color: #3b82f6;'>About Resume Rating App</h1>", unsafe_allow_html=True)
    
    st.markdown("""
    ## Overview
    
    The Resume Rating App is a comprehensive tool designed to help job seekers and recruiters 
    match resumes with job descriptions. By analyzing the content of both documents, 
    the app provides objective measures of compatibility and suggestions for improvement.
    """)
    
    # Create a visual flowchart showing the resume matching process
    st.subheader("How Resume Matching Works")
    
    # Create flowchart using graphviz
    graph = graphviz.Digraph()
    graph.attr(rankdir='TB', size='8,8')
    
    # Add nodes
    graph.node('upload', 'Resume Upload', shape='box', style='filled', fillcolor='lightblue')
    graph.node('parse', 'Text Extraction', shape='box', style='filled', fillcolor='lightblue')
    graph.node('skills', 'Skills Identification', shape='box', style='filled', fillcolor='lightyellow')
    graph.node('exp', 'Experience Analysis', shape='box', style='filled', fillcolor='lightyellow')
    graph.node('edu', 'Education Analysis', shape='box', style='filled', fillcolor='lightyellow')
    graph.node('job', 'Job Description\nRequirements', shape='box', style='filled', fillcolor='lightyellow')
    graph.node('matching', 'Matching Algorithm', shape='box', style='filled', fillcolor='orange')
    graph.node('scoring', 'Score Calculation', shape='box', style='filled', fillcolor='orange')
    graph.node('results', 'Final Match Score', shape='box', style='filled', fillcolor='lightpink')
    graph.node('suggest', 'Improvement\nSuggestions', shape='box', style='filled', fillcolor='lightpink')
    
    # Add edges
    graph.edge('upload', 'parse')
    graph.edge('parse', 'skills')
    graph.edge('parse', 'exp')
    graph.edge('parse', 'edu')
    graph.edge('job', 'matching')
    graph.edge('skills', 'matching')
    graph.edge('exp', 'matching')
    graph.edge('edu', 'matching')
    graph.edge('matching', 'scoring')
    graph.edge('scoring', 'results')
    graph.edge('scoring', 'suggest')
    
    # Render the graph
    st.graphviz_chart(graph)

    st.markdown("""
    ## Technical Details
    
    The app uses natural language processing techniques to understand the content 
    of both job descriptions and resumes. Key technologies include:
    
    - **Text analysis and extraction**: Our system processes both structured and unstructured text from 
      various document formats (PDF, DOCX, TXT), using advanced OCR and text parsing algorithms to 
      extract meaningful content while filtering out irrelevant information.
    
    - **Skills and keyword identification**: The app employs machine learning models to recognize technical 
      skills, soft skills, and industry-specific terminology. It can distinguish between skill levels 
      (beginner, intermediate, expert) and identify both explicit and implicit skill mentions.
    
    - **Experience level matching**: Beyond simple keyword matching, the system analyzes context to 
      determine relevant experience. It evaluates depth and recency of experience, role responsibilities, 
      and achievements to calculate experience compatibility with job requirements.
    
    - **Document structure analysis**: Our algorithms understand document organization, recognizing 
      sections such as education, work history, and certifications. This enables more accurate 
      evaluation of resume components against specific job description criteria.
    """)
    
    st.markdown("""
    ## Privacy
    
    We take your privacy seriously. All document analysis is performed locally, 
    and no data is stored permanently or shared with third parties.
    """)
    
    # Security Practices section
    st.header("Security Practices")
    st.write("""
    We implement robust security measures to protect your data:
    
    - **End-to-End Encryption**: All data transmissions are secured with TLS/SSL encryption
    - **Secure File Handling**: Documents are processed in isolated environments with strict access controls
    - **Data Sanitization**: All uploads undergo validation and sanitization to prevent security vulnerabilities
    - **Regular Security Audits**: We conduct quarterly security reviews and penetration testing
    - **Zero Persistent Storage**: User documents are never stored on disk and are securely erased from memory after processing
    - **Access Controls**: Role-based access controls limit admin access to system components
    - **Compliance**: Our practices adhere to industry standards including GDPR and CCPA requirements
    - **Vulnerability Management**: Regular updates to all dependencies to patch security vulnerabilities
    """)
    
    st.header("Roadmap / Upcoming Features")
    st.write("""
    We're constantly working to improve the Resume Rating App. Here's what we have planned for future releases:
    
    - **AI-Powered Recommendations**: Personalized suggestions for resume improvements based on job requirements
    - **Interview Question Generator**: Custom interview questions based on resume gaps and job requirements
    - **Resume Templates**: Library of ATS-friendly templates optimized for specific industries
    - **Career Path Visualization**: Interactive diagrams showing potential career progression based on skills
    - **Bulk Processing**: Analyze multiple resumes against a job description for efficient candidate screening
    - **Resume Version Control**: Track changes across different versions of your resume
    - **Mobile App**: Native mobile applications for iOS and Android
    - **Integration with Job Boards**: Direct application capabilities with popular job sites
    - **Custom Skill Assessments**: Short tests to verify claimed skills on resumes
    
    Have a feature request? We'd love to hear your ideas at feedback@resumeratingapp.com
    """)
    
    # Version information
    st.markdown("""
    ## Version
    
    Current version: 1.0.0
    """)
    
    # Display contact information in the sidebar
    st.sidebar.markdown("## Contact")
    st.sidebar.markdown("For questions or support, please contact: support@resumeratingapp.com")