from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.models.resume_profile import ResumeProfile
from app.models.job_profile import JobProfile
from app.services.matching_engine import calculate_match


router = APIRouter(
    prefix="/matching",
    tags=["Matching"],
)


class MatchingRequest(BaseModel):
    resume: ResumeProfile
    job: JobProfile


@router.post("/analyze")
async def analyze_match(request: MatchingRequest):
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

    return {
        "match_result": result.model_dump(),
    }