from app.models.job_profile import JobProfile
from app.models.resume_profile import (
    Education,
    Experience,
    ResumeProfile,
)
from app.services.matching_engine import (
    calculate_experience_years,
    calculate_match,
    calculate_skill_matches,
)


def test_skill_alias_matching():
    resume_skills = [
        "Python",
        "ML",
        "JavaScript",
    ]

    required_skills = [
        "Python",
        "Machine Learning",
        "JavaScript",
    ]

    preferred_skills = [
        "Docker",
    ]

    (
        matched_required,
        missing_required,
        matched_preferred,
        missing_preferred,
    ) = calculate_skill_matches(
        resume_skills,
        required_skills,
        preferred_skills,
    )

    assert "Python" in matched_required
    assert "Machine Learning" in matched_required
    assert "JavaScript" in matched_required

    assert missing_required == []

    assert matched_preferred == []
    assert missing_preferred == ["Docker"]


def test_experience_calculation():
    resume = ResumeProfile(
        experience=[
            Experience(
                company="HomeSkool",
                role="Tech Intern",
                start_date="May 2026",
                end_date="July 2026",
                description="Backend development.",
            )
        ]
    )

    years = calculate_experience_years(resume)

    assert 0.15 <= years <= 0.25


def test_experience_match():
    resume = ResumeProfile(
        experience=[
            Experience(
                company="Company A",
                role="Developer",
                start_date="Jan 2022",
                end_date="Jan 2024",
                description="Development.",
            )
        ]
    )

    job = JobProfile(
        experience_requirement="2+ years",
        required_skills=["Python"],
    )

    result = calculate_match(resume, job)

    assert result.experience_match is True


def test_education_match():
    resume = ResumeProfile(
        education=[
            Education(
                institution="Manipal University Jaipur",
                degree="B.Tech",
                field_of_study=(
                    "Computer Science Engineering "
                    "(AI & ML)"
                ),
                start_date="Aug 2023",
                end_date="July 2027",
            )
        ],
        skills=["Python"],
    )

    job = JobProfile(
        required_skills=["Python"],
        education_requirements=[
            "Bachelor's degree in Computer Science"
        ],
    )

    result = calculate_match(resume, job)

    assert result.education_match is True


def test_match_score():
    resume = ResumeProfile(
        skills=[
            "Python",
            "SQL",
            "Machine Learning",
        ]
    )

    job = JobProfile(
        required_skills=[
            "Python",
            "SQL",
            "Machine Learning",
            "Docker",
        ],
        preferred_skills=[
            "AWS",
            "Git",
        ],
    )

    result = calculate_match(resume, job)

    assert result.overall_score == 56.25
    assert "Docker" in result.missing_required_skills
    assert "AWS" in result.missing_preferred_skills