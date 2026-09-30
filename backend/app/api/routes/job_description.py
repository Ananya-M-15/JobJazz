from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.database.models import User, JobDescription
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
    db: Session = Depends(get_db),
):
    if not request.text.strip():
        raise HTTPException(
            status_code=400,
            detail="Job description cannot be empty.",
        )

    profile = parse_job_description(request.text)
    # --------------------------------------------------
    # Save job description to database
    # --------------------------------------------------

    user = db.query(User).filter(
        User.email == "development@jobjazz.local"
    ).first()

    if not user:
        user = User(
            email="development@jobjazz.local",
            name="Development User",
        )
        db.add(user)
        db.flush()

    job_description = JobDescription(
        user_id=user.id,
        job_title=profile.job_title or "Untitled Job Description",
        raw_text=request.text,
        profile_data=profile.model_dump(),
    )

    db.add(job_description)
    db.commit()
    db.refresh(job_description)
    return {
        "job_description": request.text,
        "profile": profile.model_dump(),
    }