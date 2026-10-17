"""
Phase 13.5 Automated Regression Tests - JobJazz Personalized Learning Roadmap Engine.
Tests run offline without live Gemini API or external network calls.
"""
from datetime import date, timedelta
from unittest.mock import patch, MagicMock
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.database.database import get_db, SessionLocal
from app.database.models import User, Resume, JobDescription, Analysis, SkillGap, Recommendation, Roadmap
from app.models.resume_profile import ResumeProfile, Experience, Project
from app.models.job_profile import JobProfile
from app.models.match_result import MatchResult
from app.models.skill_gap import SkillGapResult
from app.schemas.roadmap import (
    RoadmapPreferences,
    ProficiencyLevel,
    ResourceFormat,
    BudgetPreference,
    RoadmapStage,
    StepStatus,
    GapType,
)
from app.services.roadmap_generator import (
    classify_skill_gap,
    generate_deterministic_roadmap,
    generate_personalized_roadmap,
)
from app.services.roadmap_vetted_resources import (
    validate_and_sanitize_resource,
    get_vetted_resources_for_skill,
)
from app.services.roadmap_schedule_engine import calculate_schedule

client = TestClient(app)


# 1. Skill Gap Classification (Missing vs Partially Demonstrated vs Demonstrated)
def test_skill_gap_classification():
    resume = ResumeProfile(
        name="Alex Candidate",
        skills=["Python", "FastAPI"],
        experience=[
            Experience(
                role="Backend Intern",
                company="StartupCo",
                description="Built Docker containers and wrote SQL queries for reporting.",
            )
        ],
        projects=[
            Project(
                name="CloudApp",
                description="Deployed web service on AWS.",
                technologies=["Python"],
            )
        ],
    )

    # In skills list -> DEMONSTRATED_UNPOLISHED
    assert classify_skill_gap("Python", resume) == GapType.DEMONSTRATED_UNPOLISHED
    assert classify_skill_gap("FastAPI", resume) == GapType.DEMONSTRATED_UNPOLISHED

    # In experience/project description text -> PARTIALLY_DEMONSTRATED
    assert classify_skill_gap("Docker", resume) == GapType.PARTIALLY_DEMONSTRATED
    assert classify_skill_gap("SQL", resume) == GapType.PARTIALLY_DEMONSTRATED
    assert classify_skill_gap("AWS", resume) == GapType.PARTIALLY_DEMONSTRATED

    # Nowhere in resume -> GENUINELY_MISSING
    assert classify_skill_gap("Kubernetes", resume) == GapType.GENUINELY_MISSING
    assert classify_skill_gap("React", resume) == GapType.GENUINELY_MISSING


# 2. Resource Validation and Sanitization (Filtering Hallucinated & Dummy URLs)
def test_resource_validation_and_sanitization():
    # Valid official resource
    valid_raw = {
        "title": "PostgreSQL Documentation",
        "provider": "PostgreSQL.org",
        "url": "https://www.postgresql.org/docs/current/",
        "resource_type": "documentation",
        "skill": "PostgreSQL",
        "pricing": "free",
    }
    sanitized = validate_and_sanitize_resource(valid_raw)
    assert sanitized is not None
    assert sanitized.title == "PostgreSQL Documentation"
    assert sanitized.is_verified is True

    # Invalid scheme
    invalid_scheme = {
        "title": "Fake Python",
        "url": "ftp://files.python.org",
    }
    assert validate_and_sanitize_resource(invalid_scheme) is None

    # Blacklisted/hallucinated domain
    dummy_domain = {
        "title": "Learn AWS fast",
        "url": "https://example.com/learn-aws-course",
    }
    assert validate_and_sanitize_resource(dummy_domain) is None

    # Blank URL or missing title
    assert validate_and_sanitize_resource({"title": "No URL", "url": ""}) is None
    assert validate_and_sanitize_resource({"title": "", "url": "https://valid.com"}) is None


# 3. Schedule Engine Arithmetic, Weekly Capacity Limits, and Categorized Hours
def test_schedule_engine_arithmetic_and_weekly_limits():
    resume = ResumeProfile(skills=["Python"])
    job = JobProfile(job_title="Backend Dev", required_skills=["FastAPI", "Docker"])
    match_result = MatchResult(matched_required_skills=["Python"], missing_required_skills=["FastAPI", "Docker"])
    skill_gap = SkillGapResult(critical_gaps=["FastAPI", "Docker"])

    prefs = RoadmapPreferences(
        proficiency=ProficiencyLevel.INTERMEDIATE,
        hours_per_week=10,
    )
    roadmap = generate_deterministic_roadmap(
        resume=resume,
        job=job,
        match_result=match_result,
        skill_gap=skill_gap,
        recommendations=None,
        preferences=prefs,
    )

    sched = roadmap.schedule
    assert sched.total_hours > 0
    assert sched.hours_per_week == 10.0
    assert sched.total_weeks >= 2

    # Categorized hours must sum to total_hours
    category_sum = sched.learning_hours + sched.practising_hours + sched.building_hours
    assert round(category_sum, 1) == round(sched.total_hours, 1)
    assert sched.learning_hours > 0
    assert sched.practising_hours > 0
    assert sched.building_hours > 0

    # Every week must not exceed the weekly capacity limit
    for week in sched.weekly_schedule:
        assert week.allocated_hours <= sched.hours_per_week


# 4. Feasibility Evaluation for Target Dates
def test_schedule_engine_feasibility_evaluation():
    today = date.today()
    resume = ResumeProfile(skills=[])
    job = JobProfile(job_title="Engineer", required_skills=["FastAPI", "Docker", "PostgreSQL"])
    match_result = MatchResult(missing_required_skills=["FastAPI", "Docker", "PostgreSQL"])
    skill_gap = SkillGapResult(critical_gaps=["FastAPI", "Docker", "PostgreSQL"])

    prefs = RoadmapPreferences(hours_per_week=10)
    roadmap = generate_deterministic_roadmap(resume, job, match_result, skill_gap, None, prefs)
    total_weeks = roadmap.schedule.total_weeks

    # Test 1: Infeasible tight target date (e.g. 1 week from now for a 3-week plan)
    tight_target = (today + timedelta(days=7)).isoformat()
    tight_sched = calculate_schedule(roadmap.modules, hours_per_week=10, target_date_str=tight_target)
    assert tight_sched.is_feasible is False
    assert "To finish by" in tight_sched.feasibility_notes

    # Test 2: Feasible comfortable target date (e.g. 52 weeks from now)
    generous_target = (today + timedelta(days=365)).isoformat()
    generous_sched = calculate_schedule(roadmap.modules, hours_per_week=10, target_date_str=generous_target)
    assert generous_sched.is_feasible is True
    assert "leaving a healthy" in generous_sched.feasibility_notes


# 5. Distinct Target Roles Produce Materially Different Roadmaps
def test_different_roles_produce_different_roadmaps():
    resume = ResumeProfile(name="Alex", skills=["Python", "SQL"])

    # Role 1: Cloud & DevOps Engineer
    job_devops = JobProfile(
        job_title="Cloud & DevOps Engineer",
        required_skills=["Docker", "Kubernetes", "AWS"],
    )
    res_1 = generate_deterministic_roadmap(
        resume=resume,
        job=job_devops,
        match_result=MatchResult(missing_required_skills=["Docker", "Kubernetes", "AWS"]),
        skill_gap=SkillGapResult(critical_gaps=["Docker", "Kubernetes", "AWS"]),
        recommendations=None,
        preferences=RoadmapPreferences(),
    )

    # Role 2: Frontend React Engineer
    job_frontend = JobProfile(
        job_title="Frontend React Engineer",
        required_skills=["React", "TypeScript"],
    )
    res_2 = generate_deterministic_roadmap(
        resume=resume,
        job=job_frontend,
        match_result=MatchResult(missing_required_skills=["React", "TypeScript"]),
        skill_gap=SkillGapResult(critical_gaps=["React", "TypeScript"]),
        recommendations=None,
        preferences=RoadmapPreferences(),
    )

    # Modules and skills must be completely distinct
    skills_1 = {s for m in res_1.modules for s in m.skills}
    skills_2 = {s for m in res_2.modules for s in m.skills}
    assert "Docker" in skills_1 or "AWS" in skills_1
    assert "React" in skills_2
    assert skills_1.isdisjoint(skills_2)
    assert res_1.summary.target_role == "Cloud & DevOps Engineer"
    assert res_2.summary.target_role == "Frontend React Engineer"


# 6. Structured AI Roadmap Generation with Mocked Gemini
def test_ai_roadmap_generation_with_mocked_gemini():
    mock_gemini_json = """{
      "overall_strategy": "Accelerated path to master modern cloud deployment.",
      "modules": [
        {
          "title": "Container Orchestration Mastery",
          "skills": ["Kubernetes"],
          "priority": "High",
          "why_it_matters": "Kubernetes is critical for production deployment.",
          "steps": [
            {
              "title": "Kubernetes Architecture & Pods",
              "skill": "Kubernetes",
              "stage": "Learn",
              "gap_type": "genuinely_missing",
              "why_it_matters": "Core concepts of pods and deployments.",
              "activities": ["Read tutorials", "Launch local cluster"],
              "resources": [
                {
                  "title": "Kubernetes Basics",
                  "provider": "CNCF",
                  "url": "https://kubernetes.io/docs/tutorials/kubernetes-basics/",
                  "resource_type": "documentation",
                  "pricing": "free",
                  "difficulty": "intermediate",
                  "why_relevant": "Official interactive tutorial."
                }
              ],
              "estimated_hours": 8.0,
              "measurable_outcome": "Working local pod deployment."
            }
          ]
        }
      ]
    }"""

    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.text = mock_gemini_json
    mock_client.models.generate_content.return_value = mock_response

    with patch("app.services.roadmap_generator.get_gemini_client", return_value=mock_client):
        resume = ResumeProfile(skills=["Python"])
        job = JobProfile(job_title="DevOps Lead", required_skills=["Kubernetes"])
        res = generate_personalized_roadmap(
            resume=resume,
            job=job,
            match_result=MatchResult(missing_required_skills=["Kubernetes"]),
            skill_gap=SkillGapResult(critical_gaps=["Kubernetes"]),
            recommendations=None,
            preferences=RoadmapPreferences(),
        )

        assert res.source == "ai"
        assert res.summary.target_role == "DevOps Lead"
        assert len(res.modules) == 1
        assert res.modules[0].skills == ["Kubernetes"]
        assert len(res.modules[0].steps[0].resources) == 1
        assert res.modules[0].steps[0].resources[0].is_verified is True


# 7. AI Generation Graceful Fallback on Gemini Error
def test_ai_roadmap_generation_graceful_fallback():
    mock_client = MagicMock()
    mock_client.models.generate_content.side_effect = RuntimeError("Rate limit or network timeout")

    with patch("app.services.roadmap_generator.get_gemini_client", return_value=mock_client):
        resume = ResumeProfile(skills=["Python"])
        job = JobProfile(job_title="Backend Lead", required_skills=["FastAPI"])
        res = generate_personalized_roadmap(
            resume=resume,
            job=job,
            match_result=MatchResult(missing_required_skills=["FastAPI"]),
            skill_gap=SkillGapResult(critical_gaps=["FastAPI"]),
            recommendations=None,
            preferences=RoadmapPreferences(),
        )

        # Must cleanly fall back to deterministic generator
        assert res.source == "deterministic"
        assert len(res.modules) > 0
        assert "FastAPI" in [s for m in res.modules for s in m.skills]


# 8. Database Persistence, Retrieval, and Progress Update End-to-End
def test_roadmap_database_persistence_and_step_update():
    db = SessionLocal()
    try:
        # Create test User, Resume, JD, and Analysis in DB
        user = User(email="roadmap_tester@jobjazz.local", name="Roadmap Tester")
        db.add(user)
        db.flush()

        resume_prof = ResumeProfile(name="Tester", skills=["Python"])
        job_prof = JobProfile(job_title="Cloud Engineer", required_skills=["Docker", "AWS"])

        resume = Resume(
            user_id=user.id,
            filename="tester.pdf",
            raw_text="Python Engineer",
            profile_data=resume_prof.model_dump(),
        )
        job_desc = JobDescription(
            user_id=user.id,
            job_title="Cloud Engineer",
            raw_text="Looking for Docker and AWS.",
            profile_data=job_prof.model_dump(),
        )
        db.add_all([resume, job_desc])
        db.flush()

        match_res = MatchResult(
            overall_score=50.0,
            matched_required_skills=["Python"],
            missing_required_skills=["Docker", "AWS"],
        )
        analysis = Analysis(
            resume_id=resume.id,
            job_description_id=job_desc.id,
            overall_score=50.0,
            match_data=match_res.model_dump(),
        )
        db.add(analysis)
        db.flush()

        skill_gap = SkillGap(
            analysis_id=analysis.id,
            strengths=["Python"],
            critical_gaps=["Docker", "AWS"],
            preferred_gaps=[],
            experience_gap=False,
            education_gap=False,
        )
        db.add(skill_gap)
        db.commit()

        analysis_id_str = str(analysis.id)

        # 1. Generate roadmap via POST /roadmap/generate
        gen_resp = client.post(
            "/roadmap/generate",
            json={
                "analysis_id": analysis_id_str,
                "preferences": {
                    "proficiency": "intermediate",
                    "hours_per_week": 10,
                },
            },
        )
        assert gen_resp.status_code == 200
        gen_data = gen_resp.json()
        assert gen_data["analysis_id"] == analysis_id_str
        assert len(gen_data["modules"]) > 0
        first_step_id = gen_data["modules"][0]["steps"][0]["id"]

        # 2. Retrieve roadmap via GET /roadmap/{analysis_id}
        get_resp = client.get(f"/roadmap/{analysis_id_str}")
        assert get_resp.status_code == 200
        assert get_resp.json()["id"] == gen_data["id"]

        # 3. Update step progress via PATCH /roadmap/{analysis_id}/step/{step_id}
        patch_resp = client.patch(
            f"/roadmap/{analysis_id_str}/step/{first_step_id}",
            json={
                "status": "completed",
                "user_notes": "Completed official tutorials and practice tests.",
            },
        )
        assert patch_resp.status_code == 200
        patch_data = patch_resp.json()
        assert patch_data["summary"]["completed_steps"] == 1
        assert patch_data["summary"]["progress_percentage"] > 0

        # Step itself must be completed
        step_obj = next(s for m in patch_data["modules"] for s in m["steps"] if s["id"] == first_step_id)
        assert step_obj["status"] == "completed"
        assert step_obj["completed_at"] is not None
        assert step_obj["user_notes"] == "Completed official tutorials and practice tests."

        # 4. Check progress summary via GET /roadmap/{analysis_id}/progress
        prog_resp = client.get(f"/roadmap/{analysis_id_str}/progress")
        assert prog_resp.status_code == 200
        prog_data = prog_resp.json()
        assert prog_data["completed_steps"] == 1
        assert prog_data["progress_percentage"] > 0
        assert len(prog_data["completed_skills"]) >= 1

    finally:
        db.rollback()
        # Clean up test user and cascade
        db_user = db.query(User).filter(User.email == "roadmap_tester@jobjazz.local").first()
        if db_user:
            db.delete(db_user)
            db.commit()
        db.close()


# 9. API Error Handling for Nonexistent Analysis
def test_roadmap_api_error_handling():
    fake_uuid = "00000000-0000-0000-0000-000000000000"
    resp = client.get(f"/roadmap/{fake_uuid}")
    assert resp.status_code == 404
    assert "Roadmap not found" in resp.json()["detail"]

    patch_resp = client.patch(
        f"/roadmap/{fake_uuid}/step/step-1",
        json={"status": "completed"},
    )
    assert patch_resp.status_code == 404
