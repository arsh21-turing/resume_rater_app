# Resume Rating App

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32.0-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

A powerful application that helps job seekers match their resumes to specific job descriptions, providing automated analysis and tailored recommendations to improve job application success rates.

## Features

- **Job Description Analysis**: Extract key skills, experience requirements, and priorities from job postings
- **Resume Evaluation**: Upload resumes in multiple formats (PDF, DOCX, TXT) for automated analysis
- **Skills Matching**: Identify which required skills are present or missing in your resume
- **Score Visualization**: View interactive charts showing match percentages across different categories
- **Recommendations**: Get actionable suggestions to improve your resume for specific job applications
- **Privacy-Focused**: All processing happens in-browser; no data is stored permanently

## Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/arsh21-turing/resume_rater_app.git
   cd resume_rater_app
   ```

2. Create and activate a virtual environment:
   ```bash
   # For Windows
   python -m venv venv
   venv\Scripts\activate
   
   # For macOS/Linux
   python -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the App

Start the Streamlit application:
```bash
streamlit run main.py
```

The app will open in your default web browser at http://localhost:8501

## Project Structure

```
resume_rater_app/
├── app/
│   ├── __init__.py
│   ├── components/
│   │   ├── __init__.py
│   │   ├── job_description.py
│   │   ├── resume_upload.py
│   │   └── results.py
│   ├── pages/
│   │   ├── home.py
│   │   ├── about.py
│   │   └── results.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── constants.py
│   │   ├── file_processor.py
│   │   ├── resume_utils.py
│   │   └── text_analysis.py
│   └── static/
│       └── css/
│           └── style.css
├── main.py
├── requirements.txt
└── README.md
```

## How It Works

1. Extract Job Requirements: The app parses job descriptions to identify required skills, experience levels, and education requirements
2. Analyze Resume Content: Uploaded resumes are processed to extract their content, skills, and experience
3. Match & Compare: The system compares resume content against job requirements using NLP techniques
4. Generate Recommendations: Based on the comparison, suggestions are provided to improve the resume

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (git checkout -b feature/AmazingFeature)
3. Commit your changes (git commit -m 'Add some AmazingFeature')
4. Push to the branch (git push origin feature/AmazingFeature)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Streamlit - The fastest way to build data apps in Python
- NLTK - For natural language processing capabilities
- PyPDF2 - For PDF parsing functionality
- python-docx - For DOCX file parsing

