import re
from datetime import date

from app.models.resume_profile import ResumeProfile
from app.models.job_profile import JobProfile
from app.models.match_result import MatchResult
from app.utils.skill_vocabulary import SKILL_VOCABULARY


def normalize_skill(skill: str) -> str:
    """Normalize a skill using the project's canonical skill vocabulary."""
    normalized = skill.strip().lower()

    for canonical_skill, aliases in SKILL_VOCABULARY.items():
        canonical_lower = canonical_skill.lower()

        if normalized == canonical_lower:
            return canonical_lower

        for alias in aliases:
            if normalized == alias.lower():
                return canonical_lower

    return normalized


def calculate_skill_matches(
    resume_skills: list[str],
    required_skills: list[str],
    preferred_skills: list[str],
) -> tuple[list[str], list[str], list[str], list[str]]:
    resume_skill_set = {
        normalize_skill(skill)
        for skill in resume_skills
    }

    matched_required = []
    missing_required = []
    matched_preferred = []
    missing_preferred = []

    for skill in required_skills:
        if normalize_skill(skill) in resume_skill_set:
            matched_required.append(skill)
        else:
            missing_required.append(skill)

    for skill in preferred_skills:
        if normalize_skill(skill) in resume_skill_set:
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
    resume_skill_set = {
        normalize_skill(skill)
        for skill in resume_skills
    }

    keyword_matches = []
    keyword_gaps = []

    for keyword in job_keywords:
        if normalize_skill(keyword) in resume_skill_set:
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


def extract_years_required(
    experience_requirement: str,
) -> float | None:
    if not experience_requirement:
        return None

    match = re.search(
        r"(\d+(?:\.\d+)?)\s*(?:\+)?\s*(?:years?|yrs?)",
        experience_requirement.lower(),
    )

    if not match:
        return None

    return float(match.group(1))


def parse_experience_date(date_text: str) -> tuple[int, int] | None:
    """
    Extract year and month from values such as:
    'May 2026', 'July 2027', or '2026'.
    """
    if not date_text:
        return None

    month_names = {
        "jan": 1,
        "feb": 2,
        "mar": 3,
        "apr": 4,
        "may": 5,
        "jun": 6,
        "jul": 7,
        "aug": 8,
        "sep": 9,
        "oct": 10,
        "nov": 11,
        "dec": 12,
    }

    month_match = re.search(
        r"\b("
        r"jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|"
        r"may|jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:tember)?|"
        r"oct(?:ober)?|nov(?:ember)?|dec(?:ember)?"
        r")\s+(\d{4})",
        date_text,
        re.IGNORECASE,
    )

    if month_match:
        month = month_names[
            month_match.group(1)[:3].lower()
        ]
        year = int(month_match.group(2))
        return year, month

    year_match = re.search(r"\b(20\d{2})\b", date_text)

    if year_match:
        return int(year_match.group(1)), 1

    return None


def calculate_experience_years(
    resume: ResumeProfile,
) -> float:
    """Calculate total non-overlapping experience approximately in years."""

    intervals = []

    for experience in resume.experience:
        start = parse_experience_date(
            experience.start_date
        )

        if not start:
            continue

        end = parse_experience_date(
            experience.end_date
        )

        if not end:
            today = date.today()
            end = (today.year, today.month)

        start_year, start_month = start
        end_year, end_month = end

        start_total_months = (
            start_year * 12 + start_month
        )
        end_total_months = (
            end_year * 12 + end_month
        )

        if end_total_months > start_total_months:
            intervals.append(
                (start_total_months, end_total_months)
            )

    if not intervals:
        return 0.0

    intervals.sort()

    merged = []
    current_start, current_end = intervals[0]

    for start, end in intervals[1:]:
        if start <= current_end:
            current_end = max(current_end, end)
        else:
            merged.append(
                (current_start, current_end)
            )
            current_start, current_end = start, end

    merged.append((current_start, current_end))

    total_months = sum(
        end - start
        for start, end in merged
    )

    return round(total_months / 12, 2)


def calculate_experience_match(
    resume: ResumeProfile,
    job: JobProfile,
) -> bool:
    required_years = extract_years_required(
        job.experience_requirement
    )

    if required_years is None:
        return True

    total_years = calculate_experience_years(
        resume
    )

    return total_years >= required_years


def calculate_education_match(
    resume: ResumeProfile,
    job: JobProfile,
) -> bool:
    if not job.education_requirements:
        return True

    if not resume.education:
        return False

    resume_text = " ".join(
        [
            f"{education.degree} "
            f"{education.field_of_study}"
            for education in resume.education
        ]
    ).lower()

    for requirement in job.education_requirements:
        requirement_lower = requirement.lower()

        degree_match = (
            "bachelor" in requirement_lower
            and (
                "bachelor" in resume_text
                or "b.tech" in resume_text
                or "btech" in resume_text
            )
        ) or (
            "b.tech" in requirement_lower
            or "btech" in requirement_lower
        ) and (
            "b.tech" in resume_text
            or "btech" in resume_text
        )

        master_match = (
            "master" in requirement_lower
            and (
                "master" in resume_text
                or "m.tech" in resume_text
                or "mtech" in resume_text
            )
        )

        if not (degree_match or master_match):
            continue

        # If a specific field is requested, verify it
        # against the candidate's education.
        field_keywords = [
            "computer science",
            "computer engineering",
            "information technology",
            "software engineering",
            "artificial intelligence",
            "data science",
        ]

        requested_fields = [
            field
            for field in field_keywords
            if field in requirement_lower
        ]

        if not requested_fields:
            return True

        if any(
            field in resume_text
            for field in requested_fields
        ):
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

    keyword_matches, keyword_gaps = (
        calculate_keyword_matches(
            resume.skills,
            job.keywords,
        )
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