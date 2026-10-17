from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.database.models import User, JobDescription
from app.services.job_profile_parser import parse_job_description
from app.services.document_extractor import extract_document_text
from app.services.document_classifier import classify_document

router = APIRouter(
    prefix="/job-description",
    tags=["Job Description"],
)


class JobDescriptionRequest(BaseModel):
    text: str


def _save_job_description(db: Session, text: str, profile_data: dict) -> JobDescription:
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

    job_title = profile_data.get("job_title") or "Untitled Job Description"
    job_description = JobDescription(
        user_id=user.id,
        job_title=job_title,
        raw_text=text,
        profile_data=profile_data,
    )

    db.add(job_description)
    db.commit()
    db.refresh(job_description)
    return job_description


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

    # Validation logic
    text_length = len(request.text.strip())
    if text_length < 100:
        raise HTTPException(
            status_code=422,
            detail="We couldn't read enough text from this. Try pasting a more complete job description."
        )

    classification = classify_document(request.text)
    if classification["document_type"] == "resume":
        raise HTTPException(
            status_code=422,
            detail="This document appears to be a candidate resume rather than a job description. Please paste the job description or role requirements you wish to match against.",
        )
    elif classification["document_type"] == "unrelated":
        raise HTTPException(
            status_code=422,
            detail="This doesn't look like a job description. We found text, but couldn't identify enough job-related requirements. Please paste the actual job posting.",
        )
    elif classification["document_type"] == "ambiguous":
        has_meaningful_title = profile.job_title and profile.job_title != "Untitled Job Description"
        total_skills = len(profile.required_skills) + len(profile.preferred_skills)
        if not has_meaningful_title and total_skills < 2:
            raise HTTPException(
                status_code=422,
                detail="The provided text could not be clearly verified as a job description. Please paste a standard job description with role requirements and responsibilities.",
            )

    has_meaningful_title = profile.job_title and profile.job_title != "Untitled Job Description"
    total_skills = len(profile.required_skills) + len(profile.preferred_skills)
    has_experience = bool(profile.experience_requirement)
    has_education = len(profile.education_requirements) > 0

    if not has_meaningful_title and total_skills < 2 and not has_experience and not has_education:
        raise HTTPException(
            status_code=422,
            detail="This doesn't look like a job description. We found text, but couldn't identify enough job-related requirements. Please paste the actual job posting."
        )

    job_description = _save_job_description(db, request.text, profile.model_dump())

    return {
        "job_description_id": str(job_description.id),
        "job_description": request.text,
        "profile": profile.model_dump(),
    }


@router.post("/analyze-pdf")
async def analyze_job_description_pdf(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    from app.api.routes.resume import ALLOWED_CONTENT_TYPES, MAX_FILE_SIZE, detect_file_type

    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Only PDF, PNG, and JPEG files are supported.",
        )

    file_bytes = await file.read()

    if not file_bytes:
        raise HTTPException(
            status_code=400,
            detail="The uploaded file is empty.",
        )

    if len(file_bytes) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="File size exceeds the 5 MB limit.",
        )

    file_type = detect_file_type(file_bytes)

    if not file_type:
        raise HTTPException(
            status_code=400,
            detail="The uploaded file is not a valid PDF, PNG, or JPEG file.",
        )

    expected_content_types = {
        "pdf": "application/pdf",
        "png": "image/png",
        "jpeg": "image/jpeg",
    }

    if file.content_type != expected_content_types[file_type]:
        raise HTTPException(
            status_code=400,
            detail="File content does not match its declared file type.",
        )

    try:
        extraction = extract_document_text(
            file_bytes,
            file_type,
        )
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Unable to extract text from the uploaded document.",
        )

    extracted_text = extraction["text"]

    if not extracted_text:
        raise HTTPException(
            status_code=422,
            detail="No readable text was found in the uploaded document.",
        )

    try:
        profile = parse_job_description(extracted_text)
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Unable to analyze the extracted job description content.",
        )

    # Validation logic
    text_length = len(extracted_text.strip())
    if text_length < 100:
        raise HTTPException(
            status_code=422,
            detail="We couldn't read enough text from this PDF. Try a text-based PDF or paste the job description instead."
        )

    classification = classify_document(extracted_text)
    if classification["document_type"] == "resume":
        raise HTTPException(
            status_code=422,
            detail="This document appears to be a candidate resume rather than a job description. Please upload the job description or role requirements you wish to match against.",
        )
    elif classification["document_type"] == "unrelated":
        raise HTTPException(
            status_code=422,
            detail="This doesn't look like a job description. We found text in this document, but couldn't identify enough job-related requirements. Please upload the actual job posting.",
        )
    elif classification["document_type"] == "ambiguous":
        has_meaningful_title = profile.job_title and profile.job_title != "Untitled Job Description"
        total_skills = len(profile.required_skills) + len(profile.preferred_skills)
        if not has_meaningful_title and total_skills < 2:
            raise HTTPException(
                status_code=422,
                detail="The uploaded document could not be clearly verified as a job description. Please upload a standard job description with role requirements and responsibilities.",
            )

    has_meaningful_title = profile.job_title and profile.job_title != "Untitled Job Description"
    total_skills = len(profile.required_skills) + len(profile.preferred_skills)
    has_experience = bool(profile.experience_requirement)
    has_education = len(profile.education_requirements) > 0

    if not has_meaningful_title and total_skills < 2 and not has_experience and not has_education:
        raise HTTPException(
            status_code=422,
            detail="This doesn't look like a job description. We found text in this document, but couldn't identify enough job-related requirements. Please upload the actual job posting."
        )

    job_description = _save_job_description(db, extracted_text, profile.model_dump())

    return {
        "job_description_id": str(job_description.id),
        "job_description": extracted_text,
        "profile": profile.model_dump(),
    }
