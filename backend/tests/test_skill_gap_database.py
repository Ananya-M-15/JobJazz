import uuid

from fastapi.testclient import TestClient

from app.main import app
from app.database.database import SessionLocal
from app.database.models import User, Resume, JobDescription, Analysis, SkillGap


client = TestClient(app)


def test_skill_gap_is_saved_to_database():
    db = SessionLocal()

    user = None
    resume = None
    job_description = None
    analysis = None
    skill_gap = None

    try:
        user = User(
            email=f"skill_gap_test_{uuid.uuid4().hex}@jobjazz.local",
            name="Skill Gap Test User",
        )
        db.add(user)
        db.flush()

        resume = Resume(
            user_id=user.id,
            filename="skill_gap_test_resume.pdf",
            raw_text="Python SQL resume",
            profile_data={
                "name": "Skill Gap Test User",
                "skills": ["Python", "SQL"],
            },
        )
        db.add(resume)

        job_description = JobDescription(
            user_id=user.id,
            job_title="Software Engineer",
            raw_text="Python SQL Docker",
            profile_data={
                "job_title": "Software Engineer",
                "required_skills": ["Python", "SQL", "Docker"],
                "preferred_skills": ["Git"],
            },
        )
        db.add(job_description)

        db.flush()

        analysis = Analysis(
            resume_id=resume.id,
            job_description_id=job_description.id,
            overall_score=66.67,
            match_data={
                "overall_score": 66.67,
                "matched_required_skills": ["Python", "SQL"],
                "missing_required_skills": ["Docker"],
                "matched_preferred_skills": [],
                "missing_preferred_skills": ["Git"],
                "keyword_matches": ["Python", "SQL"],
                "keyword_gaps": ["Docker", "Git"],
                "experience_match": True,
                "education_match": True,
            },
        )
        db.add(analysis)
        db.commit()
        db.refresh(analysis)

        match_result = analysis.match_data

        response = client.post(
            "/skill-gap/analyze",
            json={
                "analysis_id": str(analysis.id),
                "match_result": match_result,
            },
        )

        assert response.status_code == 200

        response_data = response.json()

        assert response_data["skill_gap"]["strengths"] == [
            "Python",
            "SQL",
        ]
        assert response_data["skill_gap"]["critical_gaps"] == [
            "Docker",
        ]
        assert response_data["skill_gap"]["preferred_gaps"] == [
            "Git",
        ]

        skill_gap = (
            db.query(SkillGap)
            .filter(SkillGap.analysis_id == analysis.id)
            .first()
        )

        assert skill_gap is not None
        assert skill_gap.analysis_id == analysis.id
        assert skill_gap.strengths == ["Python", "SQL"]
        assert skill_gap.critical_gaps == ["Docker"]
        assert skill_gap.preferred_gaps == ["Git"]
        assert skill_gap.experience_gap is False
        assert skill_gap.education_gap is False

    finally:
        if skill_gap is not None:
            db.delete(skill_gap)

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
        