import io

import pymupdf
import pytesseract
from PIL import Image


def extract_text_from_image(image_bytes: bytes) -> str:
    """
    Extract text from an image using Tesseract OCR.

    Supports JPG, JPEG, PNG, BMP, TIFF, and WEBP.
    """

    if not image_bytes:
        raise ValueError("Image data is empty.")

    try:
        image = Image.open(io.BytesIO(image_bytes))
        image = image.convert("RGB")

        text = pytesseract.image_to_string(
            image,
            lang="eng",
        )

        return text.strip()

    except Exception as exc:
        raise RuntimeError(
            "Unable to extract text from the image."
        ) from exc


def extract_text_from_scanned_pdf(
    file_bytes: bytes,
    dpi: int = 200,
) -> str:
    """
    Extract text from a scanned/image-based PDF using OCR.

    Each PDF page is rendered as an image and passed to
    Tesseract OCR.
    """

    if not file_bytes:
        raise ValueError("PDF data is empty.")

    document = pymupdf.open(
        stream=file_bytes,
        filetype="pdf",
    )

    extracted_pages = []

    try:
        scale = dpi / 72

        matrix = pymupdf.Matrix(
            scale,
            scale,
        )

        for page in document:

            pixmap = page.get_pixmap(
                matrix=matrix,
                alpha=False,
            )

            image_bytes = pixmap.tobytes(
                "png",
            )

            page_text = extract_text_from_image(
                image_bytes,
            )

            if page_text:
                extracted_pages.append(
                    page_text,
                )

    finally:
        document.close()

    return "\n\n".join(
        extracted_pages,
    ).strip()
def extract_text_from_pdf_page(
    page,
    dpi: int = 200,
) -> str:
    """
    Render a single PDF page and extract its text using OCR.
    """

    scale = dpi / 72

    matrix = pymupdf.Matrix(
        scale,
        scale,
    )

    pixmap = page.get_pixmap(
        matrix=matrix,
        alpha=False,
    )

    image_bytes = pixmap.tobytes(
        "png",
    )

    return extract_text_from_image(
        image_bytes
    )