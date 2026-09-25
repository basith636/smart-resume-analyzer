from flask import Flask, render_template, request, jsonify
from analyzer import analyze_resume
from pathlib import Path
import sqlite3
import uuid

app = Flask(__name__)
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)
DB_PATH = "resume_analyzer.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""CREATE TABLE IF NOT EXISTS analyses (
        id TEXT PRIMARY KEY,
        filename TEXT,
        target_role TEXT,
        score INTEGER,
        ats_score INTEGER,
        missing_skills TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")
    conn.commit()
    conn.close()

init_db()

@app.route("/")
def index():
    return render_template("index.html")

@app.post("/api/analyze")
def analyze():
    uploaded = request.files.get("resume")
    role = request.form.get("role", "AI Engineer")
    if not uploaded or not uploaded.filename:
        return jsonify({"error": "Please upload a PDF or DOCX resume."}), 400

    suffix = Path(uploaded.filename).suffix.lower()
    if suffix not in {".pdf", ".docx"}:
        return jsonify({"error": "Only PDF and DOCX files are supported."}), 400

    file_id = f"{uuid.uuid4().hex}{suffix}"
    path = UPLOAD_DIR / file_id
    uploaded.save(path)

    try:
        result = analyze_resume(path, role)
        conn = sqlite3.connect(DB_PATH)
        conn.execute(
            "INSERT INTO analyses VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)",
            (
                file_id,
                uploaded.filename,
                role,
                result["resume_score"],
                result["ats_score"],
                ", ".join(result["missing_skills"])
            )
        )
        conn.commit()
        conn.close()
        return jsonify(result)
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500
    finally:
        try:
            path.unlink()
        except OSError:
            pass

if __name__ == "__main__":
    app.run(debug=True)
