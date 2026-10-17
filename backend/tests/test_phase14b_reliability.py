"""
Phase 14B Reliability, Persistence, and API Contract Regression Tests.
Verifies all five fixes:
1. Roadmap preference contract alignment & alias mapping
2. Step completion & progress preservation across regenerations
3. Vetted catalogue Scikit-Learn URL correction
4. Active dashboard recovery endpoint GET /matching/analysis/{analysis_id}
5. Normalized recommendations contract for both AI and fallback
"""
import uuid
from datetime import datetime, timedelta, UTC
from unittest.mock import patch, MagicMock

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.database.database import SessionLocal
from app.database.models import User, Resume, JobDescription, Analysis, SkillGap, Recommendation, Roadmap
from app.models.resume_profile import ResumeProfile
from app.models.job_profile import JobProfile
from app.models.match_result import MatchResult
from app.models.skill_gap import SkillGapResult
from app.models.recommendation import RecommendationResult, SkillRecommendation
from app.schemas.roadmap import (
    RoadmapPreferences,
    ProficiencyLevel,
    ResourceFormat,
    BudgetPreference,
    RoadmapResult,
    RoadmapModule,
    RoadmapStep,
    RoadmapSummary,
    RoadmapStage,
    StepStatus,
    GapType,
)
from app.services.roadmap_generator import (
    generate_deterministic_roadmap,
    merge_roadmap_progress,
)
from app.services.roadmap_vetted_resources import VETTED_CATALOGUE
from app.services.roadmap_schedule_engine import calculate_schedule

client = TestClient(app)


# -------------------------------------------------------------
# Stage 2: Roadmap Preference Contract Tests
# -------------------------------------------------------------
def test_roadmap_preferences_canonical_fields():
    """Verify canonical fields work directly."""
    prefs = RoadmapPreferences(
        proficiency=ProficiencyLevel.ADVANCED,
        hours_per_week=20,
        target_date="2026-11-15",
        resource_format=ResourceFormat.PROJECTS,
        budget=BudgetPreference.ALL,
    )
    assert prefs.proficiency == ProficiencyLevel.ADVANCED
    assert prefs.hours_per_week == 20
    assert prefs.target_date == "2026-11-15"
    assert prefs.resource_format == ResourceFormat.PROJECTS
    assert prefs.budget == BudgetPreference.ALL


def test_roadmap_preferences_legacy_alias_mapping():
    """Verify legacy frontend keys are safely mapped without silent preference loss."""
    raw = {
        "proficiency": "beginner",
        "hours_per_week": 15,
        "target_completion_date": "2026-12-01",
        "preferred_format": "docs",
        "budget_preference": "free_only",
    }
    prefs = RoadmapPreferences.model_validate(raw)
    assert prefs.proficiency == ProficiencyLevel.BEGINNER
    assert prefs.hours_per_week == 15
    assert prefs.target_date == "2026-12-01"
    assert prefs.resource_format == ResourceFormat.DOCS
    assert prefs.budget == BudgetPreference.FREE

    raw_paid = {
        "budget_preference": "free_and_paid",
    }
    prefs_paid = RoadmapPreferences.model_validate(raw_paid)
    assert prefs_paid.budget == BudgetPreference.ALL


def test_roadmap_preferences_defaults():
    """Verify defaults work when optional preferences are omitted."""
    prefs = RoadmapPreferences()
    assert prefs.proficiency == ProficiencyLevel.INTERMEDIATE
    assert prefs.hours_per_week == 10
    assert prefs.target_date is None
    assert prefs.resource_format == ResourceFormat.MIX
    assert prefs.budget == BudgetPreference.FREE


def test_infeasible_target_date_triggers_warning():
    """Verify aggressive target dates produce feasibility warning."""
    step = RoadmapStep(
        id="s1",
        module_id="m1",
        title="Step 1",
        skill="Docker",
        gap_type=GapType.GENUINELY_MISSING,
        stage=RoadmapStage.LEARN,
        why_it_matters="Core skill",
        activities=["Practice"],
        resources=[],
        estimated_hours=40.0,
        dependencies=[],
        measurable_outcome="Done",
    )
    mod = RoadmapModule(
        id="m1",
        title="Module 1",
        skills=["Docker"],
        priority="High",
        why_it_matters="Important",
        estimated_hours=40.0,
        steps=[step],
    )
    # Target date 3 days from today for 40 hours of work at 10h/week is infeasible
    near_target = (datetime.now(UTC) + timedelta(days=3)).strftime("%Y-%m-%d")
    sched = calculate_schedule(
        modules=[mod],
        hours_per_week=10,
        target_date_str=near_target,
    )
    assert sched.is_feasible is False
    assert "At your current pace of 10 hrs/week" in sched.feasibility_notes


# -------------------------------------------------------------
# Stage 3: Learning Progress Preservation Tests
# -------------------------------------------------------------
def test_merge_roadmap_progress_preserves_completed_and_annotated_steps():
    """Verify equivalent completed steps retain completion status, timestamps, and notes."""
    existing_modules = [
        {
            "id": "mod-1",
            "title": "Backend Architecture & API Systems",
            "steps": [
                {
                    "id": "step-1",
                    "skill": "Python",
                    "stage": "Learn",
                    "title": "Master Python Core Fundamentals",
                    "status": "completed",
                    "completed_at": "2026-10-15T12:00:00Z",
                    "user_notes": "Reviewed official tutorial ch 1-5",
                },
                {
                    "id": "step-2",
                    "skill": "Python",
                    "stage": "Practise",
                    "title": "Hands-On Problem Sets in Python",
                    "status": "in_progress",
                    "completed_at": None,
                    "user_notes": "Solved 2 out of 3 exercises",
                },
            ],
        }
    ]

    new_step_1 = RoadmapStep(
        id="new-step-1",
        module_id="new-mod-1",
        title="Master Python Core Fundamentals",
        skill="Python",
        gap_type=GapType.GENUINELY_MISSING,
        stage=RoadmapStage.LEARN,
        why_it_matters="Fundamental",
        activities=["Read docs"],
        resources=[],
        estimated_hours=4.0,
        dependencies=[],
        measurable_outcome="Summary notes",
        status=StepStatus.NOT_STARTED,
    )
    new_step_2 = RoadmapStep(
        id="new-step-2",
        module_id="new-mod-1",
        title="Hands-On Problem Sets in Python",
        skill="Python",
        gap_type=GapType.GENUINELY_MISSING,
        stage=RoadmapStage.PRACTISE,
        why_it_matters="Practice",
        activities=["Solve problems"],
        resources=[],
        estimated_hours=5.0,
        dependencies=["new-step-1"],
        measurable_outcome="Practice repo",
        status=StepStatus.NOT_STARTED,
    )
    new_step_3 = RoadmapStep(
        id="new-step-3",
        module_id="new-mod-1",
        title="Practical Python Application",
        skill="Python",
        gap_type=GapType.GENUINELY_MISSING,
        stage=RoadmapStage.BUILD,
        why_it_matters="Portfolio",
        activities=["Build project"],
        resources=[],
        estimated_hours=8.0,
        dependencies=["new-step-2"],
        measurable_outcome="Published app",
        status=StepStatus.NOT_STARTED,
    )

    new_roadmap = RoadmapResult(
        analysis_id="test-123",
        preferences=RoadmapPreferences(),
        summary=RoadmapSummary(
            target_role="Developer",
            overall_strategy="Plan",
            key_focus_areas=["Python"],
            total_modules=1,
            total_steps=3,
            total_hours=17.0,
            estimated_weeks=2,
            completed_steps=0,
            progress_percentage=0.0,
        ),
        modules=[
            RoadmapModule(
                id="new-mod-1",
                title="Backend Architecture",
                skills=["Python"],
                priority="High",
                why_it_matters="Core",
                estimated_hours=17.0,
                steps=[new_step_1, new_step_2, new_step_3],
            )
        ],
        schedule=calculate_schedule([RoadmapModule(id="m", title="m", skills=["Python"], priority="High", why_it_matters="m", estimated_hours=17.0, steps=[new_step_1, new_step_2, new_step_3])], 10),
        source="deterministic",
        created_at=datetime.now(UTC).isoformat(),
        updated_at=datetime.now(UTC).isoformat(),
    )

    merged = merge_roadmap_progress(new_roadmap, existing_modules)

    # Step 1 was completed in old roadmap -> must be completed in merged roadmap
    assert merged.modules[0].steps[0].status == StepStatus.COMPLETED
    assert merged.modules[0].steps[0].completed_at == "2026-10-15T12:00:00Z"
    assert merged.modules[0].steps[0].user_notes == "Reviewed official tutorial ch 1-5"

    # Step 2 was in progress -> must be in progress
    assert merged.modules[0].steps[1].status == StepStatus.IN_PROGRESS
    assert merged.modules[0].steps[1].user_notes == "Solved 2 out of 3 exercises"

    # Step 3 was new / not started -> must remain NOT_STARTED
    assert merged.modules[0].steps[2].status == StepStatus.NOT_STARTED
    assert merged.modules[0].steps[2].completed_at is None

    # Summary metrics must be updated accurately: 1 completed out of 3 = 33.3%
    assert merged.summary.completed_steps == 1
    assert merged.summary.total_steps == 3
    assert merged.summary.progress_percentage == 33.3


# -------------------------------------------------------------
# Stage 4: Scikit-Learn Vetted URL Test
# -------------------------------------------------------------
def test_scikit_learn_vetted_url_corrected():
    """Verify that Scikit-Learn documentation link in vetted catalogue is corrected."""
    ml_resources = VETTED_CATALOGUE.get("Machine Learning", [])
    assert len(ml_resources) > 0
    sklearn_entry = next((r for r in ml_resources if "scikit-learn" in r["title"].lower()), None)
    assert sklearn_entry is not None
    assert sklearn_entry["url"] == "https://scikit-learn.org/stable/tutorial/"


# -------------------------------------------------------------
# Stage 5: Active Dashboard Recovery Endpoint Tests
# -------------------------------------------------------------
def test_dashboard_recovery_endpoints_and_error_handling():
    """Test GET /matching/analysis/{analysis_id} with valid, invalid, and missing IDs."""
    db = SessionLocal()
    user = None
    resume = None
    job = None
    analysis = None
    try:
        user = User(email=f"recovery_test_{uuid.uuid4().hex[:8]}@example.com", name="Recovery User")
        db.add(user)
        db.flush()

        resume = Resume(
            user_id=user.id,
            filename="recov.pdf",
            raw_text="Python React",
            profile_data={"name": "Recovery User", "skills": ["Python", "React"]},
        )
        db.add(resume)
        job = JobDescription(
            user_id=user.id,
            job_title="Full Stack Dev",
            raw_text="Python React Docker",
            profile_data={"job_title": "Full Stack Dev", "required_skills": ["Python", "Docker"]},
        )
        db.add(job)
        db.flush()

        analysis = Analysis(
            resume_id=resume.id,
            job_description_id=job.id,
            overall_score=75.0,
            match_data={"overall_score": 75.0, "matched_required_skills": ["Python"]},
        )
        db.add(analysis)
        db.flush()

        gap = SkillGap(
            analysis_id=analysis.id,
            strengths=["Python"],
            critical_gaps=["Docker"],
            preferred_gaps=[],
            experience_gap=False,
            education_gap=False,
        )
        db.add(gap)

        rec = Recommendation(
            analysis_id=analysis.id,
            skill="Docker",
            priority="High",
            reason="Containerization",
            action="Learn Dockerfile",
            source="deterministic",
        )
        db.add(rec)
        db.commit()

        # 1. Valid retrieval
        resp = client.get(f"/matching/analysis/{analysis.id}")
        assert resp.status_code == 200
        data = resp.json()
        assert data["analysis_id"] == str(analysis.id)
        assert data["overall_score"] == 75.0
        assert data["candidate_profile"]["name"] == "Recovery User"
        assert data["job_profile"]["job_title"] == "Full Stack Dev"
        assert data["skill_gap"]["critical_gaps"] == ["Docker"]
        assert len(data["recommendations"]["recommendations"]) == 1
        assert data["recommendations"]["recommendations"][0]["skill"] == "Docker"

        # 2. Malformed UUID
        resp_malformed = client.get("/matching/analysis/not-a-valid-uuid")
        assert resp_malformed.status_code == 400
        assert "Invalid analysis ID format" in resp_malformed.json()["detail"]

        # 3. Non-existent UUID
        random_uuid = str(uuid.uuid4())
        resp_missing = client.get(f"/matching/analysis/{random_uuid}")
        assert resp_missing.status_code == 404
        assert "Analysis record not found" in resp_missing.json()["detail"]

    finally:
        if analysis:
            db.delete(analysis)
        if resume:
            db.delete(resume)
        if job:
            db.delete(job)
        if user:
            db.delete(user)
        db.commit()
        db.close()


# -------------------------------------------------------------
# Stage 6: Normalized Recommendations Contract Tests
# -------------------------------------------------------------
def test_normalized_recommendations_endpoint_ai_and_fallback(monkeypatch):
    """Verify single recommendations array and overall_advice contract for both AI and fallback."""
    db = SessionLocal()
    user = None
    resume = None
    job = None
    analysis = None

    try:
        user = User(email=f"rec_norm_{uuid.uuid4().hex[:8]}@example.com", name="Norm Rec")
        db.add(user)
        db.flush()

        resume = Resume(
            user_id=user.id,
            filename="rec.pdf",
            raw_text="Python",
            profile_data={"name": "Norm Rec", "skills": ["Python"]},
        )
        db.add(resume)
        job = JobDescription(
            user_id=user.id,
            job_title="Backend Dev",
            raw_text="Python Docker",
            profile_data={"job_title": "Backend Dev", "required_skills": ["Python", "Docker"]},
        )
        db.add(job)
        db.flush()

        analysis = Analysis(
            resume_id=resume.id,
            job_description_id=job.id,
            overall_score=50.0,
            match_data={"overall_score": 50.0},
        )
        db.add(analysis)
        db.commit()

        payload = {
            "analysis_id": str(analysis.id),
            "match_result": {
                "overall_score": 50.0,
                "matched_required_skills": ["Python"],
                "missing_required_skills": ["Docker"],
                "matched_preferred_skills": [],
                "missing_preferred_skills": [],
                "experience_match": True,
                "education_match": True,
            },
            "skill_gap": {
                "strengths": ["Python"],
                "critical_gaps": ["Docker"],
                "preferred_gaps": [],
                "experience_gap": False,
                "education_gap": False,
            },
        }

        # Case 1: Mocked Successful Gemini AI response
        def mock_ai_recommendations(match_res, gap_res):
            return RecommendationResult(
                recommendations=[
                    SkillRecommendation(
                        skill="Docker",
                        priority="High",
                        reason="Required containerization tool",
                        action="Complete Docker handbook",
                    )
                ],
                overall_advice="Focus on practical Docker containerization.",
            )

        monkeypatch.setattr("app.api.routes.recommendations.generate_ai_recommendations", mock_ai_recommendations)

        resp_ai = client.post("/recommendations/generate", json=payload)
        assert resp_ai.status_code == 200
        data_ai = resp_ai.json()
        assert data_ai["source"] == "ai"
        assert isinstance(data_ai["recommendations"], list)
        assert len(data_ai["recommendations"]) == 1
        assert data_ai["recommendations"][0]["skill"] == "Docker"
        assert data_ai["overall_advice"] == "Focus on practical Docker containerization."

        # Case 2: Mocked AI Failure -> Deterministic Fallback response
        def mock_ai_fail(match_res, gap_res):
            raise RuntimeError("Gemini 503 Service Unavailable")

        monkeypatch.setattr("app.api.routes.recommendations.generate_ai_recommendations", mock_ai_fail)

        resp_fb = client.post("/recommendations/generate", json=payload)
        assert resp_fb.status_code == 200
        data_fb = resp_fb.json()
        assert data_fb["source"] == "fallback"
        assert isinstance(data_fb["recommendations"], list)
        assert len(data_fb["recommendations"]) == 1
        assert data_fb["recommendations"][0]["skill"] == "Docker"
        assert data_fb["overall_advice"] != ""

    finally:
        if analysis:
            db.delete(analysis)
        if resume:
            db.delete(resume)
        if job:
            db.delete(job)
        if user:
            db.delete(user)
        db.commit()
        db.close()


def test_e2e_roadmap_regeneration_preserves_database_progress(monkeypatch):
    """Integration test: marks a step complete in DB, regenerates roadmap, and confirms progress is preserved."""
    db = SessionLocal()
    user = None
    resume = None
    job = None
    analysis = None

    try:
        user = User(email=f"regen_{uuid.uuid4().hex[:8]}@example.com", name="Regen User")
        db.add(user)
        db.flush()

        resume = Resume(
            user_id=user.id,
            filename="regen_res.pdf",
            raw_text="Python",
            profile_data={"name": "Regen User", "skills": ["Python"]},
        )
        db.add(resume)

        job = JobDescription(
            user_id=user.id,
            job_title="DevOps Engineer",
            raw_text="Python Docker Kubernetes",
            profile_data={"job_title": "DevOps Engineer", "required_skills": ["Python", "Docker", "Kubernetes"]},
        )
        db.add(job)
        db.flush()

        analysis = Analysis(
            resume_id=resume.id,
            job_description_id=job.id,
            overall_score=33.3,
            match_data={
                "overall_score": 33.3,
                "matched_required_skills": ["Python"],
                "missing_required_skills": ["Docker", "Kubernetes"],
                "matched_preferred_skills": [],
                "missing_preferred_skills": [],
                "experience_match": True,
                "education_match": True,
            },
        )
        db.add(analysis)
        db.flush()

        skill_gap = SkillGap(
            analysis_id=analysis.id,
            strengths=["Python"],
            critical_gaps=["Docker", "Kubernetes"],
            preferred_gaps=[],
            experience_gap=False,
            education_gap=False,
        )
        db.add(skill_gap)
        db.commit()

        # Mock Gemini client to ensure test runs fast, deterministically and offline without live network calls
        def mock_get_client():
            raise RuntimeError("Offline test fallback")

        monkeypatch.setattr("app.services.roadmap_generator.get_gemini_client", mock_get_client)

        # Step 1: Initial Roadmap Generation
        resp_gen1 = client.post(
            "/roadmap/generate",
            json={
                "analysis_id": str(analysis.id),
                "preferences": {
                    "proficiency": "intermediate",
                    "hours_per_week": 10,
                    "target_date": None,
                    "resource_format": "mix",
                    "budget": "free",
                },
            },
        )
        assert resp_gen1.status_code == 200
        gen1_data = resp_gen1.json()
        assert gen1_data["summary"]["completed_steps"] == 0

        first_step = gen1_data["modules"][0]["steps"][0]
        first_step_id = first_step["id"]

        # Step 2: Mark First Step Completed
        resp_update = client.patch(
            f"/roadmap/{analysis.id}/step/{first_step_id}",
            json={
                "status": "completed",
                "user_notes": "Completed Docker intro walkthrough",
            },
        )
        assert resp_update.status_code == 200
        updated_data = resp_update.json()
        assert updated_data["summary"]["completed_steps"] == 1
        assert updated_data["summary"]["progress_percentage"] > 0

        # Step 3: Regenerate with changed preferences (e.g. 15 hours/week)
        resp_gen2 = client.post(
            "/roadmap/generate",
            json={
                "analysis_id": str(analysis.id),
                "preferences": {
                    "proficiency": "intermediate",
                    "hours_per_week": 15,
                    "target_date": None,
                    "resource_format": "mix",
                    "budget": "free",
                },
            },
        )
        assert resp_gen2.status_code == 200
        gen2_data = resp_gen2.json()

        # Must preserve completed step count and percentage!
        assert gen2_data["summary"]["completed_steps"] == 1
        assert gen2_data["summary"]["progress_percentage"] > 0
        preserved_step = gen2_data["modules"][0]["steps"][0]
        assert preserved_step["status"] == "completed"
        assert preserved_step["user_notes"] == "Completed Docker intro walkthrough"
        assert preserved_step["completed_at"] is not None

        # Step 4: Verify GET /roadmap/{analysis_id} agrees
        resp_get = client.get(f"/roadmap/{analysis.id}")
        assert resp_get.status_code == 200
        get_data = resp_get.json()
        assert get_data["summary"]["completed_steps"] == 1
        assert get_data["modules"][0]["steps"][0]["status"] == "completed"

        # Step 5: Verify GET /roadmap/{analysis_id}/progress agrees
        resp_prog = client.get(f"/roadmap/{analysis.id}/progress")
        assert resp_prog.status_code == 200
        prog_data = resp_prog.json()
        assert prog_data["completed_steps"] == 1
        assert prog_data["progress_percentage"] > 0

    finally:
        if analysis:
            # Delete related roadmap if exists
            db_roadmaps = db.query(Roadmap).filter(Roadmap.analysis_id == analysis.id).all()
            for r in db_roadmaps:
                db.delete(r)
            db.delete(analysis)
        if resume:
            db.delete(resume)
        if job:
            db.delete(job)
        if user:
            db.delete(user)
        db.commit()
        db.close()

