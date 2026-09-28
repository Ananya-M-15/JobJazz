from app.services.job_description_parser import (
    extract_job_sections,
    extract_job_title,
)


def test_job_section_extraction():
    text = """
    Machine Learning Engineer

    Responsibilities
    Build and deploy machine learning systems.

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

    sections = extract_job_sections(text)

    assert "Python" in sections["required"]
    assert "SQL" in sections["required"]
    assert "Machine Learning" in sections["required"]

    assert "Docker" in sections["preferred"]
    assert "AWS" in sections["preferred"]

    assert "2+ years" in sections["experience"]

    assert "Bachelor's degree" in sections["education"]


def test_job_title_extraction():
    text = """
    Job Description

    Machine Learning Engineer

    Responsibilities
    Build machine learning systems.
    """

    assert extract_job_title(text) == "Machine Learning Engineer"