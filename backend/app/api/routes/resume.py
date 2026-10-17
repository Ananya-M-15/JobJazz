from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.database.models import User, Resume

from app.services.document_extractor import extract_document_text
from app.services.resume_parser import parse_resume_text
from app.services.document_classifier import classify_document

router = APIRouter(
    prefix="/resume",
    tags=["Resume"],
)

MAX_FILE_SIZE = 5 * 1024 * 1024

ALLOWED_CONTENT_TYPES = {
    "application/pdf",
    "image/png",
    "image/jpeg",
}


def detect_file_type(file_bytes: bytes) -> str:
    """Detect supported file type using file signatures."""

    if file_bytes.startswith(b"%PDF"):
        return "pdf"

    if file_bytes.startswith(b"\x89PNG\r\n\x1a\n"):
        return "png"

    if file_bytes.startswith(b"\xff\xd8\xff"):
        return "jpeg"

    return ""


@router.post("/extract")
async def extract_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    # --------------------------------------------------
    # 1. Validate content type
    # --------------------------------------------------

    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Only PDF, PNG, and JPEG files are supported.",
        )

    # --------------------------------------------------
    # 2. Read uploaded file
    # --------------------------------------------------

    file_bytes = await file.read()

    if not file_bytes:
        raise HTTPException(
            status_code=400,
            detail="The uploaded file is empty.",
        )

    # --------------------------------------------------
    # 3. Validate file size
    # --------------------------------------------------

    if len(file_bytes) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="File size exceeds the 5 MB limit.",
        )

    # --------------------------------------------------
    # 4. Validate actual file signature
    # --------------------------------------------------

    file_type = detect_file_type(file_bytes)

    if not file_type:
        raise HTTPException(
            status_code=400,
            detail="The uploaded file is not a valid PDF, PNG, or JPEG file.",
        )

    # --------------------------------------------------
    # 5. Make sure MIME type matches detected file type
    # --------------------------------------------------

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

    # --------------------------------------------------
    # 6. Extract text
    # --------------------------------------------------

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

    if not extracted_text or len(extracted_text.strip()) < 40:
        raise HTTPException(
            status_code=422,
            detail="No readable text was found in the uploaded document. Please upload a clear resume file.",
        )

    # --------------------------------------------------
    # 7. Validate document purpose (ensure it is a resume, not JD or unrelated)
    # --------------------------------------------------
    classification = classify_document(extracted_text)
    if classification["document_type"] == "job_description":
        raise HTTPException(
            status_code=422,
            detail="This document appears to be a Job Description rather than a candidate resume. Please upload your personal resume or CV in this step.",
        )
    elif classification["document_type"] == "unrelated":
        raise HTTPException(
            status_code=422,
            detail="The uploaded file does not appear to be a candidate resume or career document. Please upload a standard resume containing your experience, skills, and education.",
        )
    elif classification["document_type"] == "ambiguous":
        raise HTTPException(
            status_code=422,
            detail="The uploaded document could not be clearly verified as a candidate resume. Please upload a clear resume with your contact details, work history, and skills.",
        )

    # --------------------------------------------------
    # 8. Parse resume information
    # --------------------------------------------------

    try:
        resume_profile = parse_resume_text(extracted_text)
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Unable to analyze the extracted resume content.",
        )

        # --------------------------------------------------
    # 8. Save resume to database
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

    resume = Resume(
        user_id=user.id,
        filename=file.filename or "uploaded_resume",
        raw_text=extracted_text,
        profile_data=resume_profile.model_dump(),
    )

    db.add(resume)
    db.commit()
    db.refresh(resume)

    # --------------------------------------------------
    # 9. Return extraction + parsed profile
    # --------------------------------------------------

    return {
        "filename": file.filename,
        "extraction": {
            "method": extraction["method"],
            "ocr_used": extraction["ocr_used"],
            "ocr_pages": extraction["ocr_pages"],
            "quality": extraction["quality"],
        },
        "resume_id": str(resume.id),
        "text": extracted_text,
        "profile": resume_profile.model_dump(),
    }
