# app/pages/home.py - FIXED VERSION
"""
Home page for the Resume Rating App.

This module provides the home page UI with app introduction, features, 
and getting started guidance.
"""

import streamlit as st

def display_home():
    """Display the home page with app overview, features and how to use it."""
    # Display each section of the home page using helper functions
    display_intro()
    
    # Main sections using columns
    col1, col2 = st.columns([3, 2])
    
    with col1:
        display_why_use()
    
    with col2:
        display_how_it_works()
    
    display_footer()


def display_intro():
    """
    Display a visually appealing app introduction with modern UI elements.
    
    This function creates the app header section with a professional layout,
    animated elements, and clear value proposition.
    """
    # Create a hero section with gradient background
    st.markdown("""
    <div class="hero-container">
        <div class="hero-content">
            <h1 class="hero-title">Resume Rating App</h1>
            <div class="hero-subtitle">Match your resume to the job you want</div>
            <div class="hero-description">
                Optimize your resume for specific job postings with AI-powered analysis and recommendations.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Key metrics/stats in cards
    st.markdown('<div class="metrics-row">', unsafe_allow_html=True)

    metrics = [
        {"icon": "🔍", "value": "98%", "label": "Accuracy in skill extraction"},
        {"icon": "⚡", "value": "2 min", "label": "Average analysis time"},
        {"icon": "🏆", "value": "84%", "label": "Resume improvement rate"}
    ]

    for metric in metrics:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">{metric['icon']}</div>
            <div class="metric-value">{metric['value']}</div>
            <div class="metric-label">{metric['label']}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # App value proposition with simple animation
    with st.container():
        st.markdown("""
        <div class="value-prop">
            <div class="value-prop-heading">Stand out from the competition</div>
            <div class="value-prop-description">
                The Resume Rating App helps you understand exactly what employers are looking for
                and how to position your experience to match their needs. Stop guessing if your
                resume will make it past applicant tracking systems.
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Visual separator before next section
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

    # Add custom CSS for the intro section
    st.markdown("""
    <style>
    /* Hero section */
    .hero-container {
        background: linear-gradient(135deg, #4b6cb7 0%, #182848 100%);
        border-radius: 12px;
        padding: 2.5rem 2rem;
        margin-bottom: 2rem;
        color: white;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
        position: relative;
        overflow: hidden;
    }

    .hero-container::after {
        content: '';
        position: absolute;
        top: 0;
        right: 0;
        width: 300px;
        height: 100%;
        background-image: url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzAwIiBoZWlnaHQ9IjMwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cGF0aCBkPSJNMTU5LjU3MSA0NC43MkMxNzcuMDY5IDYyLjIxOCAxODQuNTQ2IDg5LjkxNCAxODIgMTE0Qzc5LjQxNSAxMTQgMTgyIDExNCAxODIgMTE0QzE4MiAxMTQgMTc5LjQ1NSAyMTAuOTk5IDE3OS40NTUgMTc1LjQ0M0MxNzkuNDU1IDE3NS40NDMgMTc5LjQ1NSAyMzYgMTc5LjQ1NSAyMzZDMjEzLjQ4NSAyMzYgMjUwLjc4NyAyMzcuMDk5IDI4MS4zNjEgMjA2LjUyNUMzMTEuOTM1IDE3NS45NTIgMzExLjkzNSAxMjUuOTU2IDI4MS4zNjEgOTUuMzgzQzI1MC43ODcgNjQuODA5IDIwMC43OTIgNjQuODA5IDE3MC4yMTggOTUuMzgzQzEzOS42NDUgMTI1Ljk1NiAxMzkuNjQ1IDE3NS45NTIgMTcwLjIxOCAyMDYuNTI1QzIwMC43OTIgMjM3LjA5OSAyNTAuNzg3IDIzNy4wOTkgMjgxLjM2MSAyMDYuNTI1IiBzdHJva2U9IiNmZmYiIHN0cm9rZS13aWR0aD0iMiIgZmlsbD0ibm9uZSIgZmlsbC1ydWxlPSJldmVub2RkIiBvcGFjaXR5PSIuMiIvPjwvc3ZnPg==');
        background-size: cover;
        opacity: 0.2;
    }

    .hero-title {
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        background: linear-gradient(90deg, #ffffff, #f0f4ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: fadeIn 1s ease-out;
    }

    .hero-subtitle {
        font-size: 1.5rem;
        margin-bottom: 1rem;
        font-weight: 300;
        opacity: 0.9;
        animation: slideRight 1s ease-out;
    }

    .hero-description {
        font-size: 1.1rem;
        max-width: 650px;
        line-height: 1.6;
        animation: fadeIn 1.5s ease-out;
    }

    /* Metrics section */
    .metrics-row {
        display: flex;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 1rem;
        margin: 2rem 0;
    }

    .metric-card {
        flex: 1;
        min-width: 180px;
        background-color: white;
        border-radius: 8px;
        padding: 1.2rem;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
        text-align: center;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }

    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 15px rgba(0, 0, 0, 0.1);
    }

    .metric-icon {
        font-size: 2rem;
        margin-bottom: 0.5rem;
    }

    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #4b6cb7;
        margin-bottom: 0.3rem;
    }

    .metric-label {
        color: #4a5568;
        font-size: 0.9rem;
    }

    /* Value proposition */
    .value-prop {
        background-color: #f9fafb;
        border-radius: 8px;
        padding: 2rem;
        margin: 2rem 0;
        border-left: 4px solid #4b6cb7;
        animation: slideUp 0.8s ease-out;
    }

    .value-prop-heading {
        font-size: 1.5rem;
        font-weight: 600;
        color: #2d3748;
        margin-bottom: 1rem;
    }

    .value-prop-description {
        color: #4a5568;
        line-height: 1.6;
        font-size: 1.1rem;
    }

    /* Divider */
    .section-divider {
        border: 0;
        height: 1px;
        background-image: linear-gradient(to right, rgba(0, 0, 0, 0), rgba(0, 0, 0, 0.1), rgba(0, 0, 0, 0));
        margin: 2.5rem 0;
    }

    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }

    @keyframes slideRight {
        from { transform: translateX(-20px); opacity: 0; }
        to { transform: translateX(0); opacity: 0.9; }
    }

    @keyframes slideUp {
        from { transform: translateY(20px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }

    /* Mobile responsiveness */
    @media screen and (max-width: 768px) {
        .metrics-row {
            flex-direction: column;
        }
        
        .hero-title {
            font-size: 2.5rem;
        }
        
        .hero-subtitle {
            font-size: 1.2rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)

    # Add optional get started button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Added unique key "intro_get_started" to avoid duplication
        if st.button("Get Started Now", use_container_width=True, type="primary", key="intro_get_started"):
            st.session_state.navigation = "Job Description"
            st.rerun()


def display_why_use():
    """Display the features, benefits and testimonials sections."""
    st.header("Why Use Resume Rating App?")
    
    # Features with emoji icons
    st.markdown("""
    ### ✨ Key Features
    
    - **Resume Analysis**: Extract skills, experience, and qualifications from your resume
    - **Job Description Parsing**: Identify key requirements and priorities from job postings
    - **Match Scoring**: Get a numerical score for how well you match the job
    - **Gap Analysis**: See exactly where your resume falls short
    - **Content Recommendations**: Get suggestions to improve your match score
    - **ATS Optimization**: Ensure your resume is ATS-friendly
    
    ### 🎯 Benefits
    
    - **Save Time**: Stop guessing if your resume matches job requirements
    - **Increase Interviews**: Higher match rates lead to more interview calls
    - **Tailor Effectively**: Know exactly what to add or modify for each application
    - **Track Progress**: See how your resume improves over time
    - **Understand Requirements**: Gain insights into what employers prioritize
    """)
    
    # Testimonial section
    st.markdown("""
    ### 💬 What Users Say
    
    > "I was applying to jobs for months with no response. After optimizing my resume 
    > with this app, I got three interview calls in two weeks!" - **Jamie S.**
    
    > "As a hiring manager, I recommend this tool to all candidates. It helps them 
    > understand exactly what we're looking for." - **Taylor M.**
    """)


def display_how_it_works():
    """
    Display an interactive and visually appealing explanation of how the app works.
    
    This function renders a step-by-step guide with icons, animations, and 
    interactive elements to help users understand the workflow.
    """
    st.subheader("How It Works", anchor=False)
    
    # Create tabs for different user journey stages
    tab1, tab2, tab3, tab4 = st.tabs([
        "1️⃣ Job Description", 
        "2️⃣ Analysis", 
        "3️⃣ Resume Upload", 
        "4️⃣ Results"
    ])
    
    with tab1:
        st.markdown("""
<div>
<h4>Enter a Job Description</h4>
<p>Copy and paste the full job posting including requirements,
responsibilities, and qualifications.</p>
<p>💡 <i>Tip: Include the complete job posting for best results.</i></p>
</div>
    """, unsafe_allow_html=True)
    
    # Show a sample input box - added key to avoid duplication
    st.text_area("Sample Job Description Input:", 
                 "Paste job description here...",
                 height=100, 
                 disabled=True,
                 label_visibility="collapsed",
                 key="sample_job_desc_input")

    with tab2:
        st.markdown("""
<div>
<h4>Analyze Requirements</h4>
<p>Our AI will automatically extract key skills, experience, and
education requirements from the job description.</p>
<p>💡 <i>Tip: Review and adjust extracted skills to improve matching.</i></p>
</div>
        """, unsafe_allow_html=True)
        
        # Create sample skill tags visualization
        col1, col2 = st.columns([1, 1])
        with col1:
            st.markdown("**Required Skills:**")
            for skill in ["Python", "SQL", "Machine Learning", "Data Analysis"]:
                st.markdown(f"<span>{skill}</span>", unsafe_allow_html=True)
        with col2:
            st.markdown("Nice-to-Have Skills:")
            for skill in ["Docker", "AWS", "Spark", "Tableau"]:
                st.markdown(f"<span>{skill}</span>", unsafe_allow_html=True)

    with tab3:
        st.markdown("""
<div>
<h4>Upload Resumes</h4>
<p>Upload one or multiple candidate resumes in PDF, DOCX, or TXT format for analysis.</p>
<p>💡 <i>Tip: You can upload multiple files to compare candidates side-by-side.</i></p>
</div>
        """, unsafe_allow_html=True)
        
        # Display a sample file uploader - added key to avoid duplication
        st.file_uploader("Upload Resume Examples (PDF, DOCX, TXT)", 
                        type=["pdf", "docx", "txt"],
                        accept_multiple_files=True,
                        disabled=True,
                        label_visibility="collapsed",
                        key="sample_file_uploader")

    with tab4:
        st.markdown("""
<div>
<h4>Get Detailed Results</h4>
<p>Receive a comprehensive analysis for each resume with match scores,
highlighted strengths, and improvement suggestions.</p>
<p>💡 <i>Tip: Export results to share with your team or candidates.</i></p>
</div>
        """, unsafe_allow_html=True)
        
        # Show sample results with progress bars - added keys to avoid duplication
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Overall Match**")
            st.progress(85, text="85%")  # Removed key parameter - not supported in progress()
            st.markdown("**Skills Match**")
            st.progress(90, text="90%")  # Removed key parameter - not supported in progress()
        with col2:
            st.markdown("**Experience Match**")
            st.progress(75, text="75%")  # Removed key parameter - not supported in progress() 
            st.markdown("**Education Match**")
            st.progress(95, text="95%")  # Removed key parameter - not supported in progress()

    # Add CSS for the How It Works section
    st.markdown("""
    <style>
    .how-it-works-card {
        background-color: #f8f9fa;
        border-left: 4px solid #3b82f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }

    .how-it-works-card h4 {
        color: #3b82f6;
        margin-top: 0;
    }

    .tip {
        background-color: #fffde7;
        padding: 0.5rem;
        border-radius: 0.25rem;
        font-size: 0.9rem;
    }

    .skill-tag {
        display: inline-block;
        padding: 0.25rem 0.5rem;
        margin: 0.25rem;
        border-radius: 1rem;
        font-size: 0.8rem;
    }

    .skill-tag.required {
        background-color: #e3f2fd;
        border: 1px solid #90caf9;
        color: #0d47a1;
    }

    .skill-tag.nice-to-have {
        background-color: #f3e5f5;
        border: 1px solid #ce93d8;
        color: #4a148c;
    }
    </style>
    """, unsafe_allow_html=True)

    # Call-to-action button - added unique key to avoid duplication
    if st.button("Get Started Now", use_container_width=True, type="primary", key="how_it_works_get_started"):
        st.session_state.navigation = "Job Description"
        st.rerun()


def display_cta_buttons():
    """Display call-to-action buttons."""
    st.markdown("### Ready to start?")
    
    # Two buttons side by side - added unique keys to avoid duplication
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Analyze Job Description", use_container_width=True, key="footer_analyze_button"):
            st.session_state.navigation = "Job Description"
            st.rerun()
            
    with col2:
        if st.button("Upload Resume", use_container_width=True, key="footer_upload_button"):
            st.session_state.navigation = "Resume Upload"
            st.rerun()


def display_footer():
    """Display statistics and disclaimer in the footer area."""
    st.markdown("---")
    
    # Stats in three columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(label="Resumes Analyzed", value="10,000+")
    
    with col2:
        st.metric(label="Average Match Improvement", value="+32%")
    
    with col3:
        st.metric(label="User Rating", value="4.8/5")
    
    # Final CTA and disclaimer
    st.markdown("""
    <div class="disclaimer">
    Note: This tool helps improve your resume's match rate but cannot guarantee job placement.
    Results may vary based on job market, industry, and other factors.
    </div>
    """, unsafe_allow_html=True)
    
    # Added a new function for footer buttons with unique keys
    display_cta_buttons()