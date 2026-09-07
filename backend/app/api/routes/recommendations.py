from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.models.match_result import MatchResult
from app.models.skill_gap import SkillGapResult

from app.services.recommendation_engine import (
    generate_recommendations,
)

from app.services.gemini_service import (
    generate_ai_recommendations,
)


router = APIRouter(
    prefix="/recommendations",
    tags=["Recommendations"],
)


class RecommendationRequest(BaseModel):
    match_result: MatchResult
    skill_gap: SkillGapResult


@router.post("/generate")
async def generate_recommendation_response(
    request: RecommendationRequest,
):
    if request.match_result.overall_score < 0:
        raise HTTPException(
            status_code=400,
            detail="Invalid match score.",
        )

    try:
        result = generate_ai_recommendations(
            request.match_result,
            request.skill_gap,
        )

        return {
            "source": "ai",
            "recommendations": result.model_dump(),
        }

    except Exception:
        result = generate_recommendations(
            request.match_result,
            request.skill_gap,
        )

        return {
            "source": "fallback",
            "recommendations": result.model_dump(),
        }