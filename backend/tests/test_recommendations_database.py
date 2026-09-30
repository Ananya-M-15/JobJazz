import uuid

from fastapi.testclient import TestClient

from app.main import app
from app.database.database import SessionLocal
from app.database.models import (
    User,
    Resume,
    JobDescription,
    Analysis,
    Recommendation,
)


client = TestClient(app)


def test_recommendations_are_saved_to_database(monkeypatch):
    from app.api.routes import recommendations

    db = SessionLocal()

    user = None
    resume = None
    job_description = None
    analysis = None

    try:
        user = User(
            email=f"recommendation_db_{uuid.uuid4().hex}@jobjazz.local",
            name="Recommendation Database Test User",
        )
        db.add(user)
        db.flush()

        resume = Resume(
            user_id=user.id,
            filename="recommendation_db_test.pdf",
            raw_text="Python SQL resume",
            profile_data={
                "name": "Recommendation Database Test User",
                "skills": ["Python", "SQL"],
            },
        )
        db.add(resume)

        job_description = JobDescription(
            user_id=user.id,
            job_title="Machine Learning Engineer",
            raw_text="Python SQL Pandas Docker",
            profile_data={
                "job_title": "Machine Learning Engineer",
                "required_skills": [
                    "Python",
                    "SQL",
                    "Pandas",
                ],
                "preferred_skills": [
                    "Docker",
                ],
            },
        )
        db.add(job_description)

        db.flush()

        analysis = Analysis(
            resume_id=resume.id,
            job_description_id=job_description.id,
            overall_score=48.81,
            match_data={
                "overall_score": 48.81,
            },
        )
        db.add(analysis)
        db.commit()
        db.refresh(analysis)

        def fake_ai_recommendations(
            match_result,
            skill_gap,
        ):
            raise RuntimeError("Gemini unavailable")

        monkeypatch.setattr(
            recommendations,
            "generate_ai_recommendations",
            fake_ai_recommendations,
        )

        payload = {
            "analysis_id": str(analysis.id),
            "match_result": {
                "overall_score": 48.81,
                "matched_required_skills": [
                    "Python",
                    "SQL",
                ],
                "missing_required_skills": [
                    "Pandas",
                ],
                "matched_preferred_skills": [],
                "missing_preferred_skills": [
                    "Docker",
                ],
                "keyword_matches": [
                    "Python",
                    "SQL",
                ],
                "keyword_gaps": [
                    "Pandas",
                    "Docker",
                ],
                "experience_match": False,
                "education_match": True,
            },
            "skill_gap": {
                "strengths": [
                    "Python",
                    "SQL",
                ],
                "critical_gaps": [
                    "Pandas",
                ],
                "preferred_gaps": [
                    "Docker",
                ],
                "experience_gap": True,
                "education_gap": False,
            },
        }

        response = client.post(
            "/recommendations/generate",
            json=payload,
        )

        assert response.status_code == 200

        response_data = response.json()

        assert response_data["source"] == "fallback"

        saved_recommendations = (
            db.query(Recommendation)
            .filter(
                Recommendation.analysis_id == analysis.id
            )
            .all()
        )

        assert len(saved_recommendations) > 0

        skills = [
            recommendation.skill
            for recommendation in saved_recommendations
        ]

        assert "Pandas" in skills

        for recommendation in saved_recommendations:
            assert recommendation.analysis_id == analysis.id
            assert recommendation.source == "fallback"
            assert recommendation.priority
            assert recommendation.reason
            assert recommendation.action

    finally:
        saved_recommendations = (
            db.query(Recommendation)
            .filter(
                Recommendation.analysis_id == analysis.id
            )
            .all()
            if analysis is not None
            else []
        )

        for recommendation in saved_recommendations:
            db.delete(recommendation)

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