from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.database.models import Analysis, SkillGap

from app.models.match_result import MatchResult
from app.services.skill_gap_engine import calculate_skill_gap


router = APIRouter(
    prefix="/skill-gap",
    tags=["Skill Gap"],
)


class SkillGapRequest(BaseModel):
    analysis_id: str
    match_result: MatchResult


@router.post("/analyze")
async def analyze_skill_gap(
    request: SkillGapRequest,
    db: Session = Depends(get_db),
):
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

    analysis = db.query(Analysis).filter(
        Analysis.id == request.analysis_id
    ).first()

    if not analysis:
        raise HTTPException(
            status_code=404,
            detail="Analysis not found.",
        )

    skill_gap = SkillGap(
        analysis_id=analysis.id,
        strengths=result.strengths,
        critical_gaps=result.critical_gaps,
        preferred_gaps=result.preferred_gaps,
        experience_gap=result.experience_gap,
        education_gap=result.education_gap,
    )

    db.add(skill_gap)
    db.commit()
    db.refresh(skill_gap)

    return {
        "skill_gap": result.model_dump(),
    }