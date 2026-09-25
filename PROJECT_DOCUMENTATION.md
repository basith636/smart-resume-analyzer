# Project Documentation

## 1. Project Title
Smart Resume Analyzer with AI-Based Feedback

## 2. Purpose
The application helps students understand how resume structure and role-specific keywords affect automated screening.

## 3. Modules
### Module 1 — Resume Upload and Parsing
Accepts PDF/DOCX files and extracts text.

### Module 2 — Resume Score Analyzer
Checks contact information, education, skills, projects and experience, then combines structural and completeness signals into a score out of 100.

### Module 3 — ATS Keyword Checker
Compares extracted resume text against a predefined skill list for the selected role.

### Module 4 — Smart Feedback System
Produces targeted suggestions when important sections or role keywords are absent.

### Module 5 — Dashboard and Report Generation
Presents scores, matched/missing skills, section checks and suggestions in a single dashboard.

## 4. AI/NLP Logic
The prototype uses rule-based evaluation and lightweight NLP keyword processing. spaCy is used for tokenization when available; a regex fallback keeps the application portable.

## 5. Database
SQLite stores the filename, target role, resume score, ATS score, missing skills and timestamp for each analysis.

## 6. Limitations
- Keyword matching is exact/phrase based.
- No deep learning model is trained.
- No production authentication is included.
- Results depend on resume text extraction quality.
- The project does not make real hiring decisions.

## 7. Future Scope
- Semantic similarity using embeddings
- Better entity/skill extraction
- Job-description upload
- Resume version comparison
- Explainable scoring
- Authentication and secure file storage
