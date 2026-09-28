from app.services.job_profile_parser import (
    extract_education_requirements,
    extract_experience_requirement,
    parse_job_description,
)


def test_experience_requirement():
    text = """
    Experience
    2+ years of experience in software development.
    """

    result = extract_experience_requirement(text)

    assert "2+ years" in result


def test_education_requirements():
    text = """
    Education
    Bachelor's degree in Computer Science or related field.
    """

    result = extract_education_requirements(text)

    assert len(result) == 1
    assert "Bachelor's degree" in result[0]


def test_complete_job_profile():
    text = """
    Machine Learning Engineer

    Responsibilities
    Build and deploy machine learning models.

    Requirements
    Python
    SQL
    Machine Learning

    Preferred Qualifications
    Docker
    AWS

    Experience
    2+ years of experience

    Education
    Bachelor's degree in Computer Science
    """

    result = parse_job_description(text)

    assert result.job_title == "Machine Learning Engineer"

    assert "Python" in result.required_skills
    assert "SQL" in result.required_skills
    assert "Machine Learning" in result.required_skills

    assert "Docker" in result.preferred_skills
    assert "AWS" in result.preferred_skills

    assert "2+ years" in result.experience_requirement

    assert len(result.education_requirements) >= 1
    assert "Computer Science" in result.education_requirements[0]

    assert "Python" in result.keywords
    assert "Machine Learning" in result.keywords