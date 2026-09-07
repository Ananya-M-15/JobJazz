from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.job_profile_parser import parse_job_description


router = APIRouter(
    prefix="/job-description",
    tags=["Job Description"],
)


class JobDescriptionRequest(BaseModel):
    text: str


@router.post("/analyze")
async def analyze_job_description(
    request: JobDescriptionRequest,
):
    if not request.text.strip():
        raise HTTPException(
            status_code=400,
            detail="Job description cannot be empty.",
        )

    profile = parse_job_description(request.text)

    return {
        "job_description": request.text,
        "profile": profile.model_dump(),
    }