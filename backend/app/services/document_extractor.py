import pymupdf

from app.services.extraction_quality import (
    calculate_text_quality,
)
from app.services.ocr_extractor import (
    extract_text_from_image,
    extract_text_from_pdf_page,
)
from app.services.pdf_extractor import (
    extract_pdf_pages_text,
)
from app.services.resume_text_normalizer import normalize_resume_text

def extract_document_text(
    file_bytes: bytes,
    file_type: str,
) -> dict:
    """
    Unified document extraction.

    PDF:
        PyMuPDF is used first on every page.
        OCR is used only for pages with poor extraction.

    Image:
        Tesseract OCR is used directly.
    """

    if not file_bytes:
        raise ValueError("Document is empty.")

    file_type = file_type.lower().strip()

    # ---------------------------------------------------------
    # PDF
    # ---------------------------------------------------------

    if file_type == "pdf":

        pages_text = extract_pdf_pages_text(
            file_bytes
        )

        document = pymupdf.open(
            stream=file_bytes,
            filetype="pdf",
        )

        final_pages = []
        ocr_pages = []

        try:
            for index, page_text in enumerate(
                pages_text
            ):

                quality = calculate_text_quality(
                    page_text
                )

                if quality["quality"] != "poor":
                    final_pages.append(
                        page_text
                    )
                    continue

                # -------------------------------------------------
                # Poor page → OCR only this page
                # -------------------------------------------------

                page = document[index]

                ocr_text = extract_text_from_pdf_page(
                    page
                )

                final_pages.append(
                    ocr_text
                )

                ocr_pages.append(
                    index + 1
                )

        finally:
            document.close()

        combined_text = "\n\n".join(page for page in final_pages if page)
        combined_text = normalize_resume_text(combined_text)
        quality = calculate_text_quality(combined_text)

        return {
            "text": combined_text,
            "method": (
                "hybrid"
                if ocr_pages
                else "pymupdf"
            ),
            "ocr_used": bool(ocr_pages),
            "ocr_pages": ocr_pages,
            "quality": quality,
        }

    # ---------------------------------------------------------
    # Images
    # ---------------------------------------------------------

    if file_type in {"jpg", "jpeg", "png"}:
        text = extract_text_from_image(file_bytes)
        text = normalize_resume_text(text)
        quality = calculate_text_quality(text)

        return {
            "text": text,
            "method": "ocr",
            "ocr_used": True,
            "ocr_pages": [],
            "quality": quality,
        }

    raise ValueError(
        f"Unsupported document type: {file_type}"
    )