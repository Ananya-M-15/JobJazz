"""
Phase 13.1 Regression Tests - JobJazz Skill Matching Correctness & Empty-State Scenarios.
Tests offline parser output, normalization parity, deduplication, and matching edge cases.
"""
import pytest

from app.models.resume_profile import (
    ResumeProfile,
    Experience,
    Education,
)
from app.models.job_profile import JobProfile
from app.services.resume_parser import parse_resume_text
from app.services.job_profile_parser import parse_job_description
from app.services.job_description_parser import extract_job_sections
from app.services.matching_engine import (
    calculate_match,
    normalize_skill,
    deduplicate_skills,
)
from app.services.skill_gap_engine import calculate_skill_gap


# Case 1: All required skills match (100% genuine match)
def test_case_1_all_required_skills_match():
    resume_text = """
    Jane Doe
    jane@example.com
    Software Engineer with expertise in Python, SQL, and Docker.
    
    Education
    BS in Computer Science
    
    Experience
    Software Engineer at TechCo
    Jan 2022 - Jan 2024
    """
    jd_text = """
    Backend Developer
    Requirements:
    - Python
    - SQL
    - Docker
    """
    resume = parse_resume_text(resume_text)
    job = parse_job_description(jd_text)
    result = calculate_match(resume, job)

    assert result.total_required_skills == 3
    assert set(result.matched_required_skills) == {"Python", "SQL", "Docker"}
    assert result.missing_required_skills == []
    assert result.overall_score == 100.0
    assert result.candidate_skills_detected >= 3


# Case 2: Some required skills match and others are missing (Partial match)
def test_case_2_partial_required_skills_match():
    resume_text = """
    John Smith
    john@example.com
    Developer skilled in Python and SQL.
    """
    jd_text = """
    Full Stack Developer
    Core Competencies:
    - Python
    - SQL
    - React
    - TypeScript
    """
    resume = parse_resume_text(resume_text)
    job = parse_job_description(jd_text)
    result = calculate_match(resume, job)

    assert result.total_required_skills == 4
    assert set(result.matched_required_skills) == {"Python", "SQL"}
    assert set(result.missing_required_skills) == {"React", "TypeScript"}
    assert result.overall_score == 50.0


# Case 3: No required skills match (0% genuine zero match - no false celebration)
def test_case_3_zero_required_skills_match():
    resume_text = """
    Alice Wonderland
    alice@example.com
    Data Analyst with strong experience in Python and Pandas.
    """
    jd_text = """
    Frontend Specialist
    What You'll Need:
    - React
    - TypeScript
    - HTML
    - CSS
    """
    resume = parse_resume_text(resume_text)
    job = parse_job_description(jd_text)
    result = calculate_match(resume, job)

    assert result.total_required_skills == 4
    assert result.matched_required_skills == []
    assert set(result.missing_required_skills) == {"React", "TypeScript", "HTML", "CSS"}
    assert result.overall_score == 0.0


# Case 4: No required skills detected in JD (Empty state - must NOT claim 100% or all matched)
def test_case_4_no_required_skills_detected_in_jd():
    resume_text = """
    Bob Builder
    bob@example.com
    Software Engineer with Python, Docker, SQL.
    """
    jd_text = """
    Regional Operations Director
    Manage regional warehouse facilities, oversee daily logistical schedules,
    and lead operational planning meetings with field leadership.
    """
    resume = parse_resume_text(resume_text)
    job = parse_job_description(jd_text)
    result = calculate_match(resume, job)

    assert job.required_skills == []
    assert result.total_required_skills == 0
    assert result.matched_required_skills == []
    assert result.missing_required_skills == []
    assert result.overall_score == 0.0
    assert "No specific skills were extracted" in result.score_breakdown


# Case 5: Resume skills empty or insufficient
def test_case_5_resume_skills_empty_or_insufficient():
    resume_text = """
    Chris Nontech
    chris@example.com
    Experienced store supervisor with five years coordinating shifts,
    managing team rosters, and assisting retail customers.
    """
    jd_text = """
    Software Engineer
    Technical Skills:
    - Python
    - SQL
    """
    resume = parse_resume_text(resume_text)
    job = parse_job_description(jd_text)
    result = calculate_match(resume, job)

    assert len(resume.skills) == 0
    assert result.candidate_skills_detected == 0
    assert result.matched_required_skills == []
    assert set(result.missing_required_skills) == {"Python", "SQL"}
    assert result.overall_score == 0.0


# Case 6: Equivalent aliases match across resume and JD
def test_case_6_equivalent_aliases_match():
    resume_text = """
    Deep Learning Researcher
    Expert in Natural Language Processing, Fast API, Amazon Web Services, Postgres, and k8s.
    """
    jd_text = """
    AI Engineer
    Requirements:
    - NLP
    - FastAPI
    - AWS
    - PostgreSQL
    - Kubernetes
    """
    resume = parse_resume_text(resume_text)
    job = parse_job_description(jd_text)
    result = calculate_match(resume, job)

    # In both resume and JD, canonical names must align
    assert set(result.matched_required_skills) == {"NLP", "FastAPI", "AWS", "PostgreSQL", "Kubernetes"}
    assert result.missing_required_skills == []
    assert result.overall_score == 100.0


# Case 7: Similar but distinct skills do not match incorrectly (no false positives)
def test_case_7_similar_distinct_skills_do_not_match_incorrectly():
    resume_text = """
    Backend Developer
    Primary language: Java. Database: SQL. Systems: C++.
    """
    jd_text = """
    Web Developer
    Requirements:
    - JavaScript
    - PostgreSQL
    """
    resume = parse_resume_text(resume_text)
    job = parse_job_description(jd_text)
    result = calculate_match(resume, job)

    # Java must NOT match JavaScript; SQL must NOT match PostgreSQL
    assert "JavaScript" not in result.matched_required_skills
    assert "PostgreSQL" not in result.matched_required_skills
    assert set(result.missing_required_skills) == {"JavaScript", "PostgreSQL"}
    assert result.overall_score == 0.0


# Case 8: Duplicate skills do not inflate counts or score
def test_case_8_duplicate_skills_do_not_inflate_result():
    resume_skills = ["Python", "FastAPI"]
    # JD with duplicate entries in varied cases/aliases
    job_required = ["Python", "python", "FastAPI", "fast api", "SQL"]
    
    unique_req = deduplicate_skills(job_required)
    assert len(unique_req) == 3

    job = JobProfile(
        job_title="Python Developer",
        required_skills=job_required,
        preferred_skills=[],
    )
    resume = ResumeProfile(name="Dev", skills=resume_skills)
    result = calculate_match(resume, job)

    assert result.total_required_skills == 3
    assert set(result.matched_required_skills) == {"Python", "FastAPI"}
    assert result.missing_required_skills == ["SQL"]
    assert result.overall_score == round((2 / 3) * 100, 2)


# Case 9: JD parser handles varied headings, markdown, and does not bleed contextual text
def test_case_9_jd_headings_and_contextual_boundaries():
    jd_text = """
    Senior Cloud Architect
    
    About Us:
    We are a leading consulting firm founded in 2010. We leverage AWS and Docker daily.
    
    ## Core Competencies:
    - Python
    - Kubernetes
    
    Bonus:
    - MLOps
    
    Benefits & Perks:
    - Health insurance, 401(k), paid parental leave.
    """
    sections = extract_job_sections(jd_text)
    assert "Python" in sections["required"]
    assert "Kubernetes" in sections["required"]
    assert "MLOps" in sections["preferred"]
    # AWS from "About Us" should NOT bleed into required section
    assert "AWS" not in sections["required"]

    job = parse_job_description(jd_text)
    assert set(job.required_skills) == {"Python", "Kubernetes"}
    assert job.preferred_skills == ["MLOps"]


# Case 10: Fresh analysis does not carry over stale JD results
def test_case_10_fresh_analysis_independence():
    resume = ResumeProfile(
        name="Candidate",
        skills=["Python", "SQL"],
    )
    jd_1 = JobProfile(
        job_title="Data Engineer",
        required_skills=["Python", "SQL"],
        preferred_skills=[],
    )
    jd_2 = JobProfile(
        job_title="ML Engineer",
        required_skills=["PyTorch", "TensorFlow"],
        preferred_skills=[],
    )

    result_1 = calculate_match(resume, jd_1)
    gap_1 = calculate_skill_gap(result_1)

    result_2 = calculate_match(resume, jd_2)
    gap_2 = calculate_skill_gap(result_2)

    assert result_1.overall_score == 100.0
    assert result_1.matched_required_skills == ["Python", "SQL"]
    assert gap_1.critical_gaps == []

    assert result_2.overall_score == 0.0
    assert result_2.matched_required_skills == []
    assert set(result_2.missing_required_skills) == {"PyTorch", "TensorFlow"}
    assert set(gap_2.critical_gaps) == {"PyTorch", "TensorFlow"}
