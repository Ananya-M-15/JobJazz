import re

from app.models.job_profile import JobProfile
from app.services.job_description_parser import (
    extract_job_sections,
    extract_job_title,
)
from app.services.job_skill_extractor import (
    extract_job_skills,
)


EXPERIENCE_PATTERN = re.compile(
    r"\b(?:"
    r"\d+\+?\s*(?:years?|yrs?)"
    r"(?:\s*[-–]\s*\d+\s*(?:years?|yrs?))?"
    r"|"
    r"entry[- ]level"
    r"|"
    r"fresher"
    r"|"
    r"freshers"
    r"|"
    r"internship"
    r")\b",
    re.IGNORECASE,
)


EDUCATION_KEYWORDS = [
    "bachelor",
    "bachelors",
    "b.tech",
    "btech",
    "master",
    "masters",
    "m.tech",
    "mtech",
    "computer science",
    "engineering degree",
    "degree",
    "diploma",
]


def extract_experience_requirement(text: str) -> str:
    matches = EXPERIENCE_PATTERN.findall(text)

    if not matches:
        return ""

    return matches[0]


def extract_education_requirements(text: str) -> list[str]:
    if not text:
        return []

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    education_requirements = []

    for line in lines:
        lower_line = line.lower()

        if any(
            keyword in lower_line
            for keyword in EDUCATION_KEYWORDS
        ):
            education_requirements.append(line)

    return education_requirements


def parse_job_description(text: str) -> JobProfile:
    if not text or not text.strip():
        return JobProfile()

    sections = extract_job_sections(text)

    required_skills, preferred_skills = extract_job_skills(
        sections["required"],
        sections["preferred"],
    )

    experience_requirement = extract_experience_requirement(
        sections["experience"]
    )

    education_requirements = (
        extract_education_requirements(
            sections["education"]
        )
    )

    # Extract skills from the complete JD for keywords.
    all_skills = extract_job_skills(
        text,
        "",
    )[0]

    return JobProfile(
        job_title=extract_job_title(text),
        required_skills=required_skills,
        preferred_skills=preferred_skills,
        experience_requirement=experience_requirement,
        education_requirements=education_requirements,
        keywords=all_skills,
    )