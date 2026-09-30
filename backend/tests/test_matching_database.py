import uuid

from fastapi.testclient import TestClient

from app.main import app
from app.database.database import SessionLocal
from app.database.models import User, Resume, JobDescription, Analysis


client = TestClient(app)


def test_matching_result_is_saved_to_database():
    db = SessionLocal()

    user = None
    resume = None
    job_description = None
    analysis = None

    try:
        unique_email = f"matching_test_{uuid.uuid4().hex}@jobjazz.local"

        user = User(
            email=unique_email,
            name="Matching Test User",
        )
        db.add(user)
        db.flush()

        resume = Resume(
            user_id=user.id,
            filename="matching_test_resume.pdf",
            raw_text="Python SQL Machine Learning resume",
            profile_data={
                "name": "Matching Test User",
                "skills": [
                    "Python",
                    "SQL",
                    "Machine Learning",
                ],
                "experience": [],
                "education": [],
                "projects": [],
                "certifications": [],
            },
        )
        db.add(resume)

        job_description = JobDescription(
            user_id=user.id,
            job_title="Machine Learning Engineer",
            raw_text="Python SQL Machine Learning",
            profile_data={
                "job_title": "Machine Learning Engineer",
                "required_skills": [
                    "Python",
                    "SQL",
                    "Machine Learning",
                ],
                "preferred_skills": [],
                "experience_requirement": "",
                "education_requirements": [],
                "keywords": [
                    "Python",
                    "SQL",
                    "Machine Learning",
                ],
            },
        )
        db.add(job_description)

        db.commit()
        db.refresh(resume)
        db.refresh(job_description)

        request_payload = {
            "resume_id": str(resume.id),
            "job_description_id": str(job_description.id),
            "resume": resume.profile_data,
            "job": job_description.profile_data,
        }

        response = client.post(
            "/matching/analyze",
            json=request_payload,
        )

        assert response.status_code == 200

        response_data = response.json()

        assert "match_result" in response_data
        assert response_data["match_result"]["overall_score"] == 100.0

        analysis = (
            db.query(Analysis)
            .filter(
                Analysis.resume_id == resume.id,
                Analysis.job_description_id == job_description.id,
            )
            .first()
        )

        assert analysis is not None
        assert analysis.resume_id == resume.id
        assert analysis.job_description_id == job_description.id
        assert analysis.overall_score == 100.0

        assert analysis.match_data["overall_score"] == 100.0
        assert "Python" in analysis.match_data["matched_required_skills"]
        assert "SQL" in analysis.match_data["matched_required_skills"]
        assert "Machine Learning" in analysis.match_data[
            "matched_required_skills"
        ]

    finally:
        if analysis is not None:
            db.delete(analysis)

        if resume is not None:
            db.delete(resume)

        if job_description is not None:
            db.delete(job_description)

        if user is not None:
            db.delete(user)

        db.commit()
        db.close()