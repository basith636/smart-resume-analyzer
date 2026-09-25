from pathlib import Path
import re
import sqlite3

ROLE_SKILLS = {
    "Data Analyst": [
        "python", "sql", "excel", "power bi", "tableau",
        "statistics", "pandas", "numpy", "data visualization"
    ],
    "Web Developer": [
        "html", "css", "javascript", "react", "git",
        "rest api", "sql", "responsive design"
    ],
    "AI Engineer": [
        "python", "machine learning", "deep learning", "nlp",
        "pandas", "numpy", "scikit-learn", "tensorflow",
        "pytorch", "git"
    ],
    "Cloud Engineer": [
        "aws", "azure", "gcp", "docker", "kubernetes",
        "linux", "networking", "terraform", "git"
    ]
}

SECTION_PATTERNS = {
    "education": r"\beducation\b",
    "skills": r"\b(skills|technical skills|technologies)\b",
    "projects": r"\b(projects|academic projects)\b",
    "experience": r"\b(experience|internship|work experience)\b",
    "contact": r"(@|linkedin|github|\+?\d[\d\s().-]{8,})"
}

def extract_text(path):
    suffix = Path(path).suffix.lower()
    if suffix == ".pdf":
        import fitz
        doc = fitz.open(path)
        return "\n".join(page.get_text() for page in doc)
    if suffix == ".docx":
        from docx import Document
        doc = Document(path)
        return "\n".join(p.text for p in doc.paragraphs)
    raise ValueError("Unsupported file type.")

def keyword_candidates(text):
    # spaCy is used when available; regex fallback keeps the project easy to run.
    try:
        import spacy
        nlp = spacy.blank("en")
        doc = nlp(text.lower())
        tokens = [
            t.text for t in doc
            if t.is_alpha and len(t.text) > 2 and not t.is_stop
        ]
        return sorted(set(tokens))
    except Exception:
        return sorted(set(re.findall(r"[a-zA-Z][a-zA-Z+#.-]{2,}", text.lower())))

def analyze_resume(path, role):
    text = extract_text(path)
    lower = text.lower()
    required = ROLE_SKILLS.get(role, ROLE_SKILLS["AI Engineer"])

    sections = {}
    for name, pattern in SECTION_PATTERNS.items():
        sections[name] = bool(re.search(pattern, lower))

    matched = [skill for skill in required if skill.lower() in lower]
    missing = [skill for skill in required if skill.lower() not in lower]

    section_points = sum(sections.values()) * 10
    completeness = min(20, max(0, len(text.strip()) // 350))
    resume_score = min(100, section_points + completeness + min(20, len(matched) * 3))

    ats_score = round((len(matched) / len(required)) * 100) if required else 0

    suggestions = []
    if not sections["contact"]:
        suggestions.append("Add clear contact information, LinkedIn, and GitHub links.")
    if not sections["skills"]:
        suggestions.append("Add a dedicated technical skills section.")
    if not sections["projects"]:
        suggestions.append("Include 2–3 relevant technical projects with measurable outcomes.")
    if not sections["education"]:
        suggestions.append("Add a clearly labeled education section.")
    if not sections["experience"]:
        suggestions.append("Add internship or relevant experience where applicable.")
    if missing:
        suggestions.append("Consider adding relevant role keywords: " + ", ".join(missing[:5]) + ".")
    if len(text.strip()) < 900:
        suggestions.append("Add concise evidence of impact, tools used, and measurable results.")

    return {
        "resume_score": resume_score,
        "ats_score": ats_score,
        "target_role": role,
        "matched_skills": matched,
        "missing_skills": missing,
        "sections": sections,
        "suggestions": suggestions,
        "extracted_characters": len(text.strip()),
        "keyword_count": len(keyword_candidates(text))
    }
