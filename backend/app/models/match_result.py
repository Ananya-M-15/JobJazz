from pydantic import BaseModel, Field


class MatchResult(BaseModel):
    overall_score: float = 0.0

    matched_required_skills: list[str] = Field(
        default_factory=list
    )

    missing_required_skills: list[str] = Field(
        default_factory=list
    )

    matched_preferred_skills: list[str] = Field(
        default_factory=list
    )

    missing_preferred_skills: list[str] = Field(
        default_factory=list
    )

    keyword_matches: list[str] = Field(
        default_factory=list
    )

    keyword_gaps: list[str] = Field(
        default_factory=list
    )

    experience_match: bool = False

    education_match: bool = False

    experience_status: str = "unspecified"

    education_status: str = "unspecified"

    experience_notes: str = ""

    education_notes: str = ""

    score_breakdown: str = ""

    total_required_skills: int = 0

    total_preferred_skills: int = 0

    candidate_skills_detected: int = 0