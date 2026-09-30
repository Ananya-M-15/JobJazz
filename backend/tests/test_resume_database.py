import uuid

from fastapi.testclient import TestClient

from app.main import app
from app.database.database import SessionLocal
from app.database.models import User, Resume
import app.api.routes.resume as resume_route


client = TestClient(app)


class FakeResumeProfile:
    def model_dump(self):
        return {
            "name": "Test User",
            "email": "test@example.com",
            "skills": ["Python", "SQL"],
            "education": [],
            "experience": [],
            "projects": [],
            "certifications": [],
        }


def test_resume_is_saved_to_database(monkeypatch):
    filename = f"database_test_{uuid.uuid4().hex}.pdf"

    fake_pdf = b"%PDF-1.4 fake test pdf"

    def fake_extract_document_text(file_bytes, file_type):
        return {
            "text": "Test resume content for database persistence.",
            "method": "test",
            "ocr_used": False,
            "ocr_pages": [],
            "quality": "high",
        }

    def fake_parse_resume_text(text):
        return FakeResumeProfile()

    monkeypatch.setattr(
        resume_route,
        "extract_document_text",
        fake_extract_document_text,
    )

    monkeypatch.setattr(
        resume_route,
        "parse_resume_text",
        fake_parse_resume_text,
    )

    response = client.post(
        "/resume/extract",
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

    assert response_data["filename"] == filename
    assert response_data["profile"]["name"] == "Test User"
    assert response_data["profile"]["skills"] == ["Python", "SQL"]

    db = SessionLocal()

    try:
        user = (
            db.query(User)
            .filter(User.email == "development@jobjazz.local")
            .first()
        )

        assert user is not None

        saved_resume = (
            db.query(Resume)
            .filter(Resume.filename == filename)
            .first()
        )

        assert saved_resume is not None
        assert saved_resume.user_id == user.id
        assert saved_resume.raw_text == (
            "Test resume content for database persistence."
        )
        assert saved_resume.profile_data["name"] == "Test User"
        assert saved_resume.profile_data["skills"] == ["Python", "SQL"]

    finally:
        if saved_resume is not None:
            db.delete(saved_resume)
            db.commit()

        db.close()