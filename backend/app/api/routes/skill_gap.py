from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.models.match_result import MatchResult
from app.services.skill_gap_engine import calculate_skill_gap


router = APIRouter(
    prefix="/skill-gap",
    tags=["Skill Gap"],
)


class SkillGapRequest(BaseModel):
    match_result: MatchResult


@router.post("/analyze")
async def analyze_skill_gap(request: SkillGapRequest):
    if (
        not request.match_result.matched_required_skills
        and not request.match_result.missing_required_skills
        and not request.match_result.matched_preferred_skills
        and not request.match_result.missing_preferred_skills
    ):
        raise HTTPException(
            status_code=400,
            detail="Match result does not contain skill information.",
        )

    result = calculate_skill_gap(request.match_result)

    return {
        "skill_gap": result.model_dump(),
    }