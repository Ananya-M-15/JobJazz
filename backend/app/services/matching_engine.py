import re
from app.models.resume_profile import ResumeProfile
from app.models.job_profile import JobProfile
from app.models.match_result import MatchResult


def calculate_skill_matches(
    resume_skills: list[str],
    required_skills: list[str],
    preferred_skills: list[str],
) -> tuple[list[str], list[str], list[str], list[str]]:
    resume_skill_set = {skill.lower() for skill in resume_skills}

    matched_required = []
    missing_required = []
    matched_preferred = []
    missing_preferred = []

    for skill in required_skills:
        if skill.lower() in resume_skill_set:
            matched_required.append(skill)
        else:
            missing_required.append(skill)

    for skill in preferred_skills:
        if skill.lower() in resume_skill_set:
            matched_preferred.append(skill)
        else:
            missing_preferred.append(skill)

    return (
        matched_required,
        missing_required,
        matched_preferred,
        missing_preferred,
    )


def calculate_keyword_matches(
    resume_skills: list[str],
    job_keywords: list[str],
) -> tuple[list[str], list[str]]:
    resume_skill_set = {skill.lower() for skill in resume_skills}

    keyword_matches = []
    keyword_gaps = []

    for keyword in job_keywords:
        if keyword.lower() in resume_skill_set:
            keyword_matches.append(keyword)
        else:
            keyword_gaps.append(keyword)

    return keyword_matches, keyword_gaps


def calculate_score(
    matched_required: list[str],
    required_skills: list[str],
    matched_preferred: list[str],
    preferred_skills: list[str],
) -> float:
    required_score = (
        len(matched_required) / len(required_skills)
        if required_skills
        else 1.0
    )

    preferred_score = (
        len(matched_preferred) / len(preferred_skills)
        if preferred_skills
        else 1.0
    )

    overall_score = (
        required_score * 0.75
        + preferred_score * 0.25
    ) * 100

    return round(overall_score, 2)

def extract_years_required(experience_requirement: str) -> float | None:
    if not experience_requirement:
        return None

    match = re.search(
        r"(\d+(?:\.\d+)?)\s*(?:\+)?\s*(?:years?|yrs?)",
        experience_requirement.lower(),
    )

    if not match:
        return None

    return float(match.group(1))


def calculate_experience_match(
    resume: ResumeProfile,
    job: JobProfile,
) -> bool:
    required_years = extract_years_required(
        job.experience_requirement
    )

    if required_years is None:
        return True

    if not resume.experience:
        return False

    total_years = 0.0

    for experience in resume.experience:
        if not experience.start_date:
            continue

        start_match = re.search(
            r"(20\d{2})",
            experience.start_date,
        )

        end_match = re.search(
            r"(20\d{2})",
            experience.end_date or "",
        )

        if not start_match:
            continue

        start_year = int(start_match.group(1))

        if end_match:
            end_year = int(end_match.group(1))
        else:
            end_year = start_year

        total_years += max(0, end_year - start_year)

    return total_years >= required_years


def calculate_education_match(
    resume: ResumeProfile,
    job: JobProfile,
) -> bool:
    if not job.education_requirements:
        return True

    if not resume.education:
        return False

    education_text = " ".join(
        [
            f"{education.degree} "
            f"{education.field_of_study} "
            f"{education.institution}"
            for education in resume.education
        ]
    ).lower()

    for requirement in job.education_requirements:
        requirement_lower = requirement.lower()

        if (
            "bachelor" in requirement_lower
            or "b.tech" in requirement_lower
            or "btech" in requirement_lower
        ):
            if (
                "b.tech" in education_text
                or "btech" in education_text
                or "bachelor" in education_text
            ):
                return True

        if (
            "master" in requirement_lower
            or "m.tech" in requirement_lower
            or "mtech" in requirement_lower
        ):
            if (
                "master" in education_text
                or "m.tech" in education_text
                or "mtech" in education_text
            ):
                return True

        if "degree" in requirement_lower:
            if "b.tech" in education_text or "btech" in education_text:
                return True

    return False

def calculate_match(
    resume: ResumeProfile,
    job: JobProfile,
) -> MatchResult:

    (
        matched_required,
        missing_required,
        matched_preferred,
        missing_preferred,
    ) = calculate_skill_matches(
        resume.skills,
        job.required_skills,
        job.preferred_skills,
    )

    keyword_matches, keyword_gaps = calculate_keyword_matches(
        resume.skills,
        job.keywords,
    )

    overall_score = calculate_score(
        matched_required,
        job.required_skills,
        matched_preferred,
        job.preferred_skills,
    )
    experience_match = calculate_experience_match(
        resume,
        job,
    )

    education_match = calculate_education_match(
        resume,
        job,
    )

    return MatchResult(
        overall_score=overall_score,
        matched_required_skills=matched_required,
        missing_required_skills=missing_required,
        matched_preferred_skills=matched_preferred,
        missing_preferred_skills=missing_preferred,
        keyword_matches=keyword_matches,
        keyword_gaps=keyword_gaps,
        experience_match=experience_match,
        education_match=education_match,
    )