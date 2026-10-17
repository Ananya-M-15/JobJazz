"""
Phase 13 Regression Tests - JobJazz Analysis Quality, Reliability & Scenarios.
Tests run offline without live Gemini API or external network.
"""
from unittest.mock import patch
import pytest

from app.models.resume_profile import (
    ResumeProfile,
    Experience,
    Education,
)
from app.models.job_profile import JobProfile
from app.models.match_result import MatchResult
from app.models.skill_gap import SkillGapResult
from app.services.matching_engine import (
    calculate_match,
    calculate_score,
    evaluate_experience,
    evaluate_education,
)
from app.services.job_profile_parser import parse_job_description
from app.services.skill_gap_engine import calculate_skill_gap
from app.services.recommendation_engine import (
    generate_recommendations,
    generate_skill_recommendations,
)


@pytest.fixture
def fixed_backend_resume():
    return ResumeProfile(
        name="Alex Mercer",
        skills=["Python", "FastAPI", "PostgreSQL", "Docker", "Git"],
        experience=[
            Experience(
                company="TechCorp",
                role="Backend Engineer",
                start_date="Jan 2022",
                end_date="Jan 2024",
                description="Built FastAPI services and maintained PostgreSQL databases.",
            )
        ],
        education=[
            Education(
                institution="State University",
                degree="Bachelor's",
                field_of_study="Computer Science",
                start_date="2018",
                end_date="2022",
            )
        ],
    )


def test_three_materially_different_jds_against_fixed_resume(fixed_backend_resume):
    """
    Verify that three distinct job descriptions produce materially different,
    factually derived match results against the exact same resume.
    """
    # JD A: Strong overlap (Python Backend)
    jd_a = JobProfile(
        job_title="Senior Python Backend Developer",
        required_skills=["Python", "FastAPI", "PostgreSQL", "Docker"],
        preferred_skills=["Git", "AWS"],
        experience_requirement="2+ years",
        education_requirements=["Bachelor's degree in Computer Science"],
    )

    # JD B: Partial overlap (Full Stack)
    jd_b = JobProfile(
        job_title="Full Stack Engineer",
        required_skills=["Python", "React", "TypeScript", "PostgreSQL"],
        preferred_skills=["Docker", "Kubernetes"],
        experience_requirement="3+ years",
        education_requirements=["Bachelor's degree in Computer Science"],
    )

    # JD C: Weak overlap (ML / Data Science Specialist)
    jd_c = JobProfile(
        job_title="Machine Learning Scientist",
        required_skills=["Machine Learning", "TensorFlow", "PyTorch", "Pandas"],
        preferred_skills=["Python", "AWS"],
        experience_requirement="4+ years",
        education_requirements=["Master's degree in Artificial Intelligence"],
    )

    result_a = calculate_match(fixed_backend_resume, jd_a)
    result_b = calculate_match(fixed_backend_resume, jd_b)
    result_c = calculate_match(fixed_backend_resume, jd_c)

    # 1. Scores must be distinctly different and strictly ordered: A > B > C
    assert result_a.overall_score > result_b.overall_score > result_c.overall_score
    assert result_a.overall_score == 87.5  # 4/4 req (75%) + 1/2 pref (12.5%) = 87.5%
    assert result_b.overall_score == 50.0  # 2/4 req (37.5%) + 1/2 pref (12.5%) = 50.0%
    assert result_c.overall_score == 12.5  # 0/4 req (0%) + 1/2 pref (12.5%) = 12.5%

    # 2. Missing required skills must reflect distinct requirements
    assert result_a.missing_required_skills == []
    assert set(result_b.missing_required_skills) == {"React", "TypeScript"}
    assert set(result_c.missing_required_skills) == {
        "Machine Learning",
        "TensorFlow",
        "PyTorch",
        "Pandas",
    }

    # 3. Missing preferred skills must be distinct
    assert result_a.missing_preferred_skills == ["AWS"]
    assert result_b.missing_preferred_skills == ["Kubernetes"]
    assert result_c.missing_preferred_skills == ["AWS"]

    # 4. Experience matches must accurately reflect tenure
    assert result_a.experience_match is True
    assert result_a.experience_status == "met"

    assert result_b.experience_match is False
    assert result_b.experience_status == "gap"
    assert "gap of ~1 years" in result_b.experience_notes

    assert result_c.experience_match is False
    assert result_c.experience_status == "gap"
    assert "gap of ~2 years" in result_c.experience_notes

    # 5. Education matches must reflect degree and field criteria
    assert result_a.education_match is True
    assert result_a.education_status == "met"

    assert result_b.education_match is True
    assert result_b.education_status == "met"

    assert result_c.education_match is False
    assert result_c.education_status == "gap"


def test_absent_preferred_skills_does_not_inflate_score():
    """
    Demonstrate that a job with NO preferred skills calculates score solely
    from required skills and does NOT award free bonus points.
    """
    matched_req = ["Python", "Docker"]
    all_req = ["Python", "Docker", "AWS", "SQL"]  # 2 of 4 = 50%
    matched_pref = []
    all_pref = []  # No preferred skills specified

    score = calculate_score(matched_req, all_req, matched_pref, all_pref)
    # Must be exactly 50.0%, NOT 62.5%
    assert score == 50.0

    # 0 of 4 matched must be 0.0%, NOT 25.0%
    zero_score = calculate_score([], all_req, [], [])
    assert zero_score == 0.0


def test_sparse_and_empty_inputs_do_not_produce_100_percent():
    """
    Verify that an empty JD with no recognized skills produces 0%,
    preventing misleading 100% scores.
    """
    score = calculate_score([], [], [], [])
    assert score == 0.0


def test_experience_and_education_uncertainty_communication(fixed_backend_resume):
    """
    Verify that unspecified requirements report 'unspecified' status and clear notes
    rather than declaring a definitive match.
    """
    job_unspecified = JobProfile(
        job_title="Software Developer",
        required_skills=["Python"],
        experience_requirement="",
        education_requirements=[],
    )

    result = calculate_match(fixed_backend_resume, job_unspecified)

    assert result.experience_status == "unspecified"
    assert "No minimum years of experience specified" in result.experience_notes

    assert result.education_status == "unspecified"
    assert "No specific degree or education requirements stated" in result.education_notes


def test_job_description_parser_with_varied_headings():
    """
    Verify that JD parser correctly identifies requirements across different heading styles.
    """
    jd_text_1 = """
    Software Engineer

    Technical Skills:
    - Python
    - Docker

    Bonus Skills:
    - Kubernetes
    """
    profile_1 = parse_job_description(jd_text_1)
    assert "Python" in profile_1.required_skills
    assert "Docker" in profile_1.required_skills
    assert "Kubernetes" in profile_1.preferred_skills

    jd_text_no_headers = """
    Python Developer
    We are looking for an experienced developer with Python, FastAPI, and SQL experience.
    """
    profile_2 = parse_job_description(jd_text_no_headers)
    assert "Python" in profile_2.required_skills
    assert "FastAPI" in profile_2.required_skills
    assert "SQL" in profile_2.required_skills


def test_skill_gap_engine_and_opportunities():
    """
    Verify skill gap engine and recommendation generation produce real
    actionable opportunities and do not drop gaps.
    """
    match_result = MatchResult(
        overall_score=60.0,
        matched_required_skills=["Python"],
        missing_required_skills=["Docker"],
        matched_preferred_skills=[],
        missing_preferred_skills=["AWS"],
        experience_match=False,
        education_match=True,
    )

    skill_gap = calculate_skill_gap(match_result)
    assert skill_gap.critical_gaps == ["Docker"]
    assert skill_gap.preferred_gaps == ["AWS"]
    assert skill_gap.experience_gap is True
    assert skill_gap.education_gap is False

    recs = generate_recommendations(match_result, skill_gap)
    rec_items = recs.recommendations
    assert len(rec_items) >= 3

    # High priority for critical gap
    docker_rec = next(r for r in rec_items if r.skill == "Docker")
    assert docker_rec.priority == "High"
    assert "Docker" in docker_rec.action

    # High priority for experience gap
    exp_rec = next(r for r in rec_items if r.skill == "Experience")
    assert exp_rec.priority == "High"

    # Medium priority for preferred gap
    aws_rec = next(r for r in rec_items if r.skill == "AWS")
    assert aws_rec.priority == "Medium"


def test_deterministic_fallback_on_ai_failure():
    """
    Verify that recommendation generation functions correctly and deterministically
    when AI generation fails or is unavailable.
    """
    match_result = MatchResult(
        overall_score=70.0,
        matched_required_skills=["Python"],
        missing_required_skills=["Docker"],
        matched_preferred_skills=["Git"],
        missing_preferred_skills=["AWS"],
        experience_match=True,
        education_match=True,
    )
    skill_gap = calculate_skill_gap(match_result)

    result = generate_recommendations(match_result, skill_gap)
    assert len(result.recommendations) == 2
    assert result.overall_advice != ""
