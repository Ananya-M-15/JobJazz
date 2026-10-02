import uuid
from fastapi.testclient import TestClient

from app.main import app
from app.database.database import SessionLocal
from app.database.models import User, JobDescription
import app.api.routes.job_description as jd_route


client = TestClient(app)


def test_job_description_is_saved_to_database():
    job_description_text = """
    Machine Learning Engineer

    We are looking for a Machine Learning Engineer with 2+ years
    of experience.

    Required Skills:
    Python, SQL, Machine Learning, Pandas, NumPy

    Preferred Skills:
    Docker, Git, AWS

    Education:
    Bachelor's degree in Computer Science or Engineering.
    """

    response = client.post(
        "/job-description/analyze",
        json={"text": job_description_text},
    )

    assert response.status_code == 200

    response_data = response.json()

    assert response_data["profile"]["job_title"] == "Machine Learning Engineer"

    db = SessionLocal()

    saved_job = None

    try:
        user = (
            db.query(User)
            .filter(User.email == "development@jobjazz.local")
            .first()
        )

        assert user is not None

        saved_job = (
            db.query(JobDescription)
            .filter(
                JobDescription.user_id == user.id,
                JobDescription.raw_text == job_description_text,
            )
            .first()
        )

        assert saved_job is not None
        assert saved_job.job_title == "Machine Learning Engineer"
        assert saved_job.raw_text == job_description_text
        assert saved_job.profile_data["job_title"] == "Machine Learning Engineer"

    finally:
        if saved_job is not None:
            db.delete(saved_job)
            db.commit()

        db.close()


class FakeJobProfile:
    def model_dump(self):
        return {
            "job_title": "Fake PDF Job",
            "required_skills": ["FakeSkill1", "FakeSkill2"],
            "preferred_skills": [],
            "experience_level": "",
            "education": "",
        }
    
    @property
    def job_title(self):
        return "Fake PDF Job"

    @property
    def required_skills(self):
        return ["FakeSkill1", "FakeSkill2"]
        
    @property
    def preferred_skills(self):
        return []
        
    @property
    def experience_requirement(self):
        return ""
        
    @property
    def education_requirements(self):
        return []


def test_job_description_pdf_is_saved_to_database(monkeypatch):
    filename = f"database_test_jd_{uuid.uuid4().hex}.pdf"
    fake_pdf = b"%PDF-1.4 fake test pdf"
    fake_extracted_text = "Fake PDF Job\nRequired Skills: FakeSkill1, FakeSkill2\nThis is a long description to ensure it passes the length check. " * 5

    def fake_extract_document_text(file_bytes, file_type):
        return {
            "text": fake_extracted_text,
            "method": "test",
            "ocr_used": False,
            "ocr_pages": [],
            "quality": "high",
        }

    def fake_parse_job_description(text):
        return FakeJobProfile()

    monkeypatch.setattr(
        jd_route,
        "extract_document_text",
        fake_extract_document_text,
    )

    monkeypatch.setattr(
        jd_route,
        "parse_job_description",
        fake_parse_job_description,
    )

    response = client.post(
        "/job-description/analyze-pdf",
        files={
            "file": (
                filename,
                fake_pdf,
                "application/pdf",
            )
        },
    )

    assert response.status_code == 200

    response_data = response.json()

    assert response_data["profile"]["job_title"] == "Fake PDF Job"
    assert response_data["job_description"] == fake_extracted_text

    db = SessionLocal()

    saved_job = None

    try:
        user = (
            db.query(User)
            .filter(User.email == "development@jobjazz.local")
            .first()
        )

        assert user is not None

        saved_job = (
            db.query(JobDescription)
            .filter(
                JobDescription.user_id == user.id,
                JobDescription.raw_text == fake_extracted_text,
            )
            .first()
        )

        assert saved_job is not None
        assert saved_job.job_title == "Fake PDF Job"
        assert saved_job.raw_text == fake_extracted_text
        assert saved_job.profile_data["job_title"] == "Fake PDF Job"

    finally:
        if saved_job is not None:
            db.delete(saved_job)
            db.commit()

        db.close()