# Smart Resume Analyzer with AI-Based Feedback

## SkillOrbit AI Capstone Project

A web application that evaluates resumes for structure, ATS keyword compatibility, role-based skills and improvement opportunities.

### Features
- PDF and DOCX resume upload
- Resume text extraction
- Rule-based resume score
- ATS keyword matching for four roles
- Skill-gap identification
- Smart improvement suggestions
- Interactive dashboard
- SQLite storage of analysis summaries

### Technology
- Frontend: HTML, CSS, JavaScript
- Backend: Python Flask
- AI/NLP: spaCy + rule-based keyword analysis
- Database: SQLite
- Document parsing: PyMuPDF and python-docx

### Run locally
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
python -m spacy download en_core_web_sm   # optional
python app.py
```

Open `http://127.0.0.1:5000`.

### Project workflow
1. Upload resume
2. Extract text
3. Process resume data
4. Calculate resume score
5. Match role keywords
6. Generate suggestions
7. Display results on dashboard

### Important
This is an educational prototype, not a production ATS. Scores are heuristic and should be treated as guidance rather than hiring decisions.
