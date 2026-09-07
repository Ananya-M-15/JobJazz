from app.models.match_result import MatchResult
from app.models.skill_gap import SkillGapResult


def calculate_skill_gap(match_result: MatchResult) -> SkillGapResult:
    strengths = (
        match_result.matched_required_skills
        + match_result.matched_preferred_skills
    )

    critical_gaps = match_result.missing_required_skills

    preferred_gaps = match_result.missing_preferred_skills

    experience_gap = not match_result.experience_match
    education_gap = not match_result.education_match

    return SkillGapResult(
        strengths=strengths,
        critical_gaps=critical_gaps,
        preferred_gaps=preferred_gaps,
        experience_gap=experience_gap,
        education_gap=education_gap,
    )