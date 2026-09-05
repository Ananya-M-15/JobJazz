from fastapi import APIRouter, UploadFile, File, HTTPException

from app.services.pdf_extractor import extract_text_from_pdf


router = APIRouter(
    prefix="/resume",
    tags=["Resume"],
)


MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB


@router.post("/extract")
async def extract_resume(file: UploadFile = File(...)):
    # 1. Check file type
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported.",
        )

    # 2. Read the uploaded file
    file_bytes = await file.read()

    # 3. Check if the file is empty
    if not file_bytes:
        raise HTTPException(
            status_code=400,
            detail="The uploaded file is empty.",
        )

    # 4. Check file size
    if len(file_bytes) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="File size exceeds the 5 MB limit.",
        )

    # 5. Check that the file is actually a PDF
    if not file_bytes.startswith(b"%PDF"):
        raise HTTPException(
            status_code=400,
            detail="The uploaded file is not a valid PDF.",
        )

    # 6. Extract text
    try:
        extracted_text = extract_text_from_pdf(file_bytes)

    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Unable to read the PDF file.",
        )

    # 7. Check whether readable text was found
    if not extracted_text:
        raise HTTPException(
            status_code=422,
            detail="No readable text was found in the PDF.",
        )

    # 8. Return extracted content
    return {
        "filename": file.filename,
        "text": extracted_text,
    }