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
        "match_result": result.model_dump(),
    }