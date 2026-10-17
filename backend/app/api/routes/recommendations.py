from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.database.models import Analysis, Recommendation

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
    analysis_id: str
    match_result: MatchResult
    skill_gap: SkillGapResult


@router.post("/generate")
async def generate_recommendation_response(
    request: RecommendationRequest,
    db: Session = Depends(get_db),
):
    if request.match_result.overall_score < 0:
        raise HTTPException(
            status_code=400,
            detail="Invalid match score.",
        )

    analysis = db.query(Analysis).filter(
        Analysis.id == request.analysis_id
    ).first()

    if not analysis:
        raise HTTPException(
            status_code=404,
            detail="Analysis not found.",
        )

    import time
    import logging

    logger = logging.getLogger(__name__)
    start_time = time.perf_counter()

    try:
        result = generate_ai_recommendations(
            request.match_result,
            request.skill_gap,
        )
        source = "ai"
        duration = time.perf_counter() - start_time
        logger.info("AI recommendations generated in %.2fs", duration)
    except Exception as exc:
        duration = time.perf_counter() - start_time
        logger.warning(
            "AI recommendation failed after %.2fs (%s). Using deterministic fallback.",
            duration,
            type(exc).__name__,
        )
        result = generate_recommendations(
            request.match_result,
            request.skill_gap,
        )
        source = "fallback"

    for recommendation in result.recommendations:
        db_recommendation = Recommendation(
            analysis_id=analysis.id,
            skill=recommendation.skill,
            priority=recommendation.priority,
            reason=recommendation.reason,
            action=recommendation.action,
            source=source,
        )

        db.add(db_recommendation)

    db.commit()

    return {
        "source": source,
        "recommendations": [r.model_dump() for r in result.recommendations],
        "overall_advice": result.overall_advice,
    }
