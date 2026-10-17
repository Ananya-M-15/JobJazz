import uuid
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.database.models import Analysis, Resume, JobDescription

from app.models.resume_profile import ResumeProfile
from app.models.job_profile import JobProfile
from app.services.matching_engine import calculate_match


router = APIRouter(
    prefix="/matching",
    tags=["Matching"],
)


class MatchingRequest(BaseModel):
    resume_id: str
    job_description_id: str
    resume: ResumeProfile
    job: JobProfile


@router.post("/analyze")
async def analyze_match(
    request: MatchingRequest,
    db: Session = Depends(get_db),
):
    if not request.resume.skills and not request.resume.experience:
        raise HTTPException(
            status_code=400,
            detail="Resume profile cannot be empty.",
        )

    if (
        not request.job.required_skills
        and not request.job.preferred_skills
    ):
        raise HTTPException(
            status_code=400,
            detail="Job profile must contain skills.",
        )

    result = calculate_match(
        request.resume,
        request.job,
    )

    resume = db.query(Resume).filter(
        Resume.id == request.resume_id
    ).first()

    if not resume:
        raise HTTPException(
            status_code=404,
            detail="Resume not found.",
        )

    job_description = db.query(JobDescription).filter(
        JobDescription.id == request.job_description_id
    ).first()

    if not job_description:
        raise HTTPException(
            status_code=404,
            detail="Job description not found.",
        )

    analysis = Analysis(
        resume_id=resume.id,
        job_description_id=job_description.id,
        overall_score=result.overall_score,
        match_data=result.model_dump(),
    )

    db.add(analysis)
    db.commit()
    db.refresh(analysis)

    return {
        "analysis_id": str(analysis.id),
        "match_result": result.model_dump(),
    }


@router.get("/analysis/{analysis_id}")
async def get_analysis_by_id(
    analysis_id: str,
    db: Session = Depends(get_db),
):
    try:
        analysis_uuid = uuid.UUID(analysis_id)
    except (ValueError, TypeError, AttributeError):
        raise HTTPException(
            status_code=400,
            detail="Invalid analysis ID format. Expected a valid UUID.",
        )

    analysis = db.query(Analysis).filter(
        Analysis.id == analysis_uuid
    ).first()

    if not analysis:
        raise HTTPException(
            status_code=404,
            detail="Analysis record not found.",
        )

    resume = analysis.resume
    job = analysis.job_description

    candidate_profile = resume.profile_data if resume else None
    job_profile = job.profile_data if job else None

    skill_gap_data = None
    if analysis.skill_gap:
        skill_gap_data = {
            "strengths": analysis.skill_gap.strengths,
            "critical_gaps": analysis.skill_gap.critical_gaps,
            "preferred_gaps": analysis.skill_gap.preferred_gaps,
            "experience_gap": analysis.skill_gap.experience_gap,
            "education_gap": analysis.skill_gap.education_gap,
        }

    recommendations_data = None
    if analysis.recommendations:
        recommendations_data = {
            "source": analysis.recommendations[0].source if analysis.recommendations else "deterministic",
            "recommendations": [
                {
                    "skill": r.skill,
                    "priority": r.priority,
                    "reason": r.reason,
                    "action": r.action,
                }
                for r in analysis.recommendations
            ],
            "overall_advice": "",
        }

    return {
        "analysis_id": str(analysis.id),
        "resume_id": str(analysis.resume_id) if analysis.resume_id else None,
        "job_description_id": str(analysis.job_description_id) if analysis.job_description_id else None,
        "overall_score": analysis.overall_score,
        "match_result": analysis.match_data,
        "candidate_profile": candidate_profile,
        "job_profile": job_profile,
        "skill_gap": skill_gap_data,
        "recommendations": recommendations_data,
    }
