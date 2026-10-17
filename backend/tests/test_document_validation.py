import pytest
from fastapi.testclient import TestClient
from app.main import app
import app.api.routes.resume as resume_route
from app.services.document_classifier import classify_document

client = TestClient(app)

SYNTHETIC_VALID_RESUME = """
Alex Morgan
alex.morgan@example.com | (555) 019-2834 | linkedin.com/in/alexmorgan | github.com/alexmorgan

EDUCATION
Bachelor of Science in Computer Science
University of Washington, 2016 – 2020

WORK EXPERIENCE
Senior Software Engineer | CloudTech Solutions
June 2020 – Present
- Architected and built scalable microservices using Python, FastAPI, and PostgreSQL.
- Optimized database query performance and deployed services to AWS ECS.

Software Engineering Intern | DevCore Inc
June 2019 – August 2019
- Built REST APIs and automated unit testing suites with PyTest.

PROJECTS
JobJazz AI Platform
- Built end-to-end skill gap analyzer with FastAPI, React, and SQLAlchemy.

TECHNICAL SKILLS
Languages: Python, JavaScript, TypeScript, SQL
Frameworks & Tools: FastAPI, React, PostgreSQL, Docker, Git, Redis
"""

SYNTHETIC_JOB_DESCRIPTION = """
Senior Backend Engineer — Acme Corp
About the Role:
We are looking for an experienced Senior Backend Engineer to join our core platform engineering team.

Key Responsibilities:
- Design, build, and maintain high-throughput backend services and APIs.
- Collaborate with frontend engineers, product managers, and data scientists.
- Ensure system reliability, observability, and test coverage across distributed environments.

Basic Qualifications & Requirements:
- 4+ years of professional backend software development experience.
- Strong proficiency in Python, FastAPI, and relational databases (PostgreSQL).
- Experience with Docker, container orchestration, and cloud infrastructure (AWS or GCP).

Preferred Qualifications:
- Familiarity with AI integration, vector databases, or asynchronous message queues.

Benefits & Perks:
- Competitive salary, 401(k) matching, comprehensive health coverage, and flexible remote work.

Apply Now:
Submit your application and portfolio to careers@acmecorp.example.com.
"""

SYNTHETIC_UNRELATED_TEXT = """
Classic Homemade Sourdough Bread Recipe
Ingredients:
- 500g bread flour
- 350g lukewarm water
- 100g active sourdough starter
- 10g fine sea salt

Instructions:
1. Whisk the sourdough starter and water together in a large mixing bowl until fully dissolved.
2. Add the bread flour and stir until a shaggy dough forms. Cover with a damp kitchen towel and let rest for 30 minutes.
3. Sprinkle sea salt evenly over the dough and perform stretch-and-folds every 30 minutes for 2 hours.
4. Shape the loaf into a round boule, transfer into a proofing basket, and refrigerate overnight.
5. Bake inside a preheated Dutch oven at 450 degrees Fahrenheit for 25 minutes with the lid on, then 20 minutes uncovered until golden brown.
"""

SYNTHETIC_AMBIGUOUS_TEXT = """
Software Engineering Overview and Candidate Evaluation
We are reviewing Python, FastAPI, and Docker capabilities.
Qualifications include 3 years experience.
Education: BS Computer Science.
Responsibilities: Build web applications and coordinate with engineering teams.
"""


def test_classifier_unit_behavior():
    res_classification = classify_document(SYNTHETIC_VALID_RESUME)
    assert res_classification["document_type"] == "resume"
    assert res_classification["resume_score"] > res_classification["jd_score"]

    jd_classification = classify_document(SYNTHETIC_JOB_DESCRIPTION)
    assert jd_classification["document_type"] == "job_description"
    assert jd_classification["jd_score"] > jd_classification["resume_score"]

    unrelated_classification = classify_document(SYNTHETIC_UNRELATED_TEXT)
    assert unrelated_classification["document_type"] == "unrelated"


def test_resume_endpoint_accepts_valid_resume(monkeypatch):
    def fake_extract(file_bytes, file_type):
        return {"text": SYNTHETIC_VALID_RESUME, "method": "test", "ocr_used": False, "ocr_pages": [], "quality": "high"}

    monkeypatch.setattr(resume_route, "extract_document_text", fake_extract)

    response = client.post(
        "/resume/extract",
        files={"file": ("alex_morgan_resume.pdf", b"%PDF-1.4 test content", "application/pdf")},
    )
    assert response.status_code == 200
    data = response.json()
    assert "resume_id" in data
    assert "profile" in data
    assert "skills" in data["profile"]


def test_resume_endpoint_rejects_job_description(monkeypatch):
    def fake_extract(file_bytes, file_type):
        return {"text": SYNTHETIC_JOB_DESCRIPTION, "method": "test", "ocr_used": False, "ocr_pages": [], "quality": "high"}

    monkeypatch.setattr(resume_route, "extract_document_text", fake_extract)

    response = client.post(
        "/resume/extract",
        files={"file": ("job_posting.pdf", b"%PDF-1.4 test content", "application/pdf")},
    )
    assert response.status_code == 422
    assert "Job Description rather than a candidate resume" in response.json()["detail"]


def test_resume_endpoint_rejects_unrelated_document(monkeypatch):
    def fake_extract(file_bytes, file_type):
        return {"text": SYNTHETIC_UNRELATED_TEXT, "method": "test", "ocr_used": False, "ocr_pages": [], "quality": "high"}

    monkeypatch.setattr(resume_route, "extract_document_text", fake_extract)

    response = client.post(
        "/resume/extract",
        files={"file": ("recipe.pdf", b"%PDF-1.4 test content", "application/pdf")},
    )
    assert response.status_code == 422
    assert "does not appear to be a candidate resume" in response.json()["detail"]


def test_resume_endpoint_rejects_empty_and_corrupt_files():
    # Empty file
    res_empty = client.post(
        "/resume/extract",
        files={"file": ("empty.pdf", b"", "application/pdf")},
    )
    assert res_empty.status_code == 400
    assert "empty" in res_empty.json()["detail"].lower()

    # Corrupt / invalid magic bytes
    res_corrupt = client.post(
        "/resume/extract",
        files={"file": ("corrupt.pdf", b"NOT_A_REAL_PDF_STREAM", "application/pdf")},
    )
    assert res_corrupt.status_code == 400
    assert "not a valid PDF" in res_corrupt.json()["detail"]

    # Unsupported content type
    res_unsupported = client.post(
        "/resume/extract",
        files={"file": ("doc.txt", b"Hello world", "text/plain")},
    )
    assert res_unsupported.status_code == 400


def test_job_description_endpoint_rejects_resume():
    response = client.post(
        "/job-description/analyze",
        json={"text": SYNTHETIC_VALID_RESUME},
    )
    assert response.status_code == 422
    assert "candidate resume rather than a job description" in response.json()["detail"]


def test_job_description_endpoint_rejects_unrelated_text():
    response = client.post(
        "/job-description/analyze",
        json={"text": SYNTHETIC_UNRELATED_TEXT},
    )
    assert response.status_code == 422
    assert "doesn't look like a job description" in response.json()["detail"]


def test_job_description_endpoint_accepts_valid_jd():
    response = client.post(
        "/job-description/analyze",
        json={"text": SYNTHETIC_JOB_DESCRIPTION},
    )
    assert response.status_code == 200
    data = response.json()
    assert "job_description_id" in data
    assert "profile" in data
    assert len(data["profile"]["required_skills"]) > 0
