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


def deduplicate_skills(skills: list[str]) -> list[str]:
    """Deduplicate skills by normalized form to avoid duplicate inflation."""
    seen = set()
    unique = []
    for skill in skills:
        norm = normalize_skill(skill)
        if norm not in seen:
            seen.add(norm)
            unique.append(skill)
    return unique


def calculate_skill_matches(
    resume_skills: list[str],
    required_skills: list[str],
    preferred_skills: list[str],
) -> tuple[list[str], list[str], list[str], list[str]]:
    resume_skill_set = {
        normalize_skill(skill)
        for skill in resume_skills
    }

    unique_required = deduplicate_skills(required_skills)
    unique_preferred = deduplicate_skills(preferred_skills)

    matched_required = []
    missing_required = []
    matched_preferred = []
    missing_preferred = []

    for skill in unique_required:
        if normalize_skill(skill) in resume_skill_set:
            matched_required.append(skill)
        else:
            missing_required.append(skill)

    for skill in unique_preferred:
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
    has_required = bool(required_skills)
    has_preferred = bool(preferred_skills)

    if not has_required and not has_preferred:
        return 0.0

    required_ratio = (
        len(matched_required) / len(required_skills)
        if has_required
        else 0.0
    )

    preferred_ratio = (
        len(matched_preferred) / len(preferred_skills)
        if has_preferred
        else 0.0
    )

    if has_required and has_preferred:
        overall_score = (
            required_ratio * 0.75
            + preferred_ratio * 0.25
        ) * 100
    elif has_required:
        overall_score = required_ratio * 100
    else:
        overall_score = preferred_ratio * 100

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


def evaluate_experience(
    resume: ResumeProfile,
    job: JobProfile,
) -> tuple[bool, str, str]:
    """
    Evaluate experience requirement.
    Returns: (is_match, status, notes)
    status is one of: 'met', 'gap', 'unspecified'
    """
    required_years = extract_years_required(
        job.experience_requirement
    )

    if required_years is None:
        notes = (
            f"Stated requirement: '{job.experience_requirement}'."
            if job.experience_requirement
            else "No minimum years of experience specified in the job description."
        )
        return True, "unspecified", notes

    total_years = calculate_experience_years(resume)

    if total_years >= required_years:
        notes = (
            f"Requires {required_years:g}+ years; "
            f"candidate documents approximately {total_years:g} years of experience."
        )
        return True, "met", notes
    else:
        gap = round(required_years - total_years, 1)
        if total_years == 0:
            notes = (
                f"Requires {required_years:g}+ years of experience; "
                f"no dated work experience found in candidate profile."
            )
        else:
            notes = (
                f"Requires {required_years:g}+ years of experience; "
                f"candidate documents approximately {total_years:g} years "
                f"(gap of ~{gap:g} years)."
            )
        return False, "gap", notes


def calculate_experience_match(
    resume: ResumeProfile,
    job: JobProfile,
) -> bool:
    is_match, _, _ = evaluate_experience(resume, job)
    return is_match


def evaluate_education(
    resume: ResumeProfile,
    job: JobProfile,
) -> tuple[bool, str, str]:
    """
    Evaluate education requirement.
    Returns: (is_match, status, notes)
    status is one of: 'met', 'gap', 'unspecified'
    """
    if not job.education_requirements:
        return (
            True,
            "unspecified",
            "No specific degree or education requirements stated in the job description.",
        )

    req_summary = "; ".join(job.education_requirements)

    if not resume.education:
        return (
            False,
            "gap",
            f"Job specifies: {req_summary}; no formal education credentials found in candidate profile.",
        )

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
            (
                "b.tech" in requirement_lower
                or "btech" in requirement_lower
            )
            and (
                "b.tech" in resume_text
                or "btech" in resume_text
            )
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
            return (
                True,
                "met",
                f"Candidate's degree satisfies the requirement ({requirement}).",
            )

        if any(
            field in resume_text
            for field in requested_fields
        ):
            return (
                True,
                "met",
                f"Candidate's degree and field satisfy the requirement ({requirement}).",
            )

    return (
        False,
        "gap",
        f"Candidate credentials do not clearly match the stated requirement: {req_summary}.",
    )


def calculate_education_match(
    resume: ResumeProfile,
    job: JobProfile,
) -> bool:
    is_match, _, _ = evaluate_education(resume, job)
    return is_match


def calculate_match(
    resume: ResumeProfile,
    job: JobProfile,
) -> MatchResult:
    unique_required = deduplicate_skills(job.required_skills)
    unique_preferred = deduplicate_skills(job.preferred_skills)

    (
        matched_required,
        missing_required,
        matched_preferred,
        missing_preferred,
    ) = calculate_skill_matches(
        resume.skills,
        unique_required,
        unique_preferred,
    )

    keyword_matches, keyword_gaps = (
        calculate_keyword_matches(
            resume.skills,
            deduplicate_skills(job.keywords),
        )
    )

    overall_score = calculate_score(
        matched_required,
        unique_required,
        matched_preferred,
        unique_preferred,
    )

    experience_match, experience_status, experience_notes = evaluate_experience(
        resume,
        job,
    )

    education_match, education_status, education_notes = evaluate_education(
        resume,
        job,
    )

    # Human-readable factual score breakdown
    parts = []
    if unique_required:
        parts.append(
            f"{len(matched_required)} of {len(unique_required)} required skills matched"
        )
    if unique_preferred:
        parts.append(
            f"{len(matched_preferred)} of {len(unique_preferred)} preferred skills matched"
        )
    if not parts:
        score_breakdown = "No specific skills were extracted from this job description."
    else:
        score_breakdown = ", ".join(parts) + f". Overall score: {overall_score}%."

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
        experience_status=experience_status,
        education_status=education_status,
        experience_notes=experience_notes,
        education_notes=education_notes,
        score_breakdown=score_breakdown,
        total_required_skills=len(unique_required),
        total_preferred_skills=len(unique_preferred),
        candidate_skills_detected=len(resume.skills),
    )