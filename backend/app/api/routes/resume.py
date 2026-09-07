from fastapi import APIRouter, UploadFile, File, HTTPException

from app.services.document_extractor import extract_document_text
from app.services.resume_parser import parse_resume_text

router = APIRouter(
    prefix="/resume",
    tags=["Resume"],
)

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB

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
async def extract_resume(file: UploadFile = File(...)):
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

    if not extracted_text:
        raise HTTPException(
            status_code=422,
            detail="No readable text was found in the uploaded document.",
        )

    # --------------------------------------------------
    # 7. Parse resume information
    # --------------------------------------------------

    try:
        resume_profile = parse_resume_text(extracted_text)
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Unable to analyze the extracted resume content.",
        )

    # --------------------------------------------------
    # 8. Return extraction + parsed profile
    # --------------------------------------------------

    return {
        "filename": file.filename,
        "extraction": {
            "method": extraction["method"],
            "ocr_used": extraction["ocr_used"],
            "ocr_pages": extraction["ocr_pages"],
            "quality": extraction["quality"],
        },
        "text": extracted_text,
        "profile": resume_profile.model_dump(),
    }