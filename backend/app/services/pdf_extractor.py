import re
import pymupdf


def clean_extracted_text(text: str) -> str:
    """
    Clean common PDF extraction artifacts while preserving
    useful resume structure.
    """

    # Remove null characters.
    text = text.replace("\x00", " ")

    # Normalize common PDF bullet characters.
    text = re.sub(r"[•●▪◦]", " ", text)

    # Normalize different dash characters.
    text = text.replace("–", "-").replace("—", "-")

    # Collapse excessive spaces/tabs.
    text = re.sub(r"[ \t]+", " ", text)

    # Remove spaces at the beginning/end of each line.
    lines = [
        line.strip()
        for line in text.splitlines()
    ]

    # Remove completely empty lines at the beginning/end,
    # but preserve useful separation between sections.
    cleaned_lines = []

    previous_blank = False

    for line in lines:
        if not line:
            if not previous_blank:
                cleaned_lines.append("")
            previous_blank = True
        else:
            cleaned_lines.append(line)
            previous_blank = False

    text = "\n".join(cleaned_lines)

    # Avoid excessive blank lines.
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """
    Extract text from a PDF using layout-aware block extraction.

    Blocks are sorted by their position on the page to improve
    reading order for resumes with structured layouts.
    """

    document = pymupdf.open(
        stream=file_bytes,
        filetype="pdf",
    )

    extracted_pages = []

    try:
        for page in document:

            # Extract text blocks with positional information.
            blocks = page.get_text(
                "blocks",
                sort=True,
            )

            page_lines = []

            for block in blocks:
                if not block:
                    continue

                block_text = block[4]

                if not block_text:
                    continue

                block_text = block_text.strip()

                if block_text:
                    page_lines.append(block_text)

            if page_lines:
                extracted_pages.append(
                    "\n".join(page_lines)
                )

    finally:
        document.close()

    raw_text = "\n\n".join(extracted_pages)

    return clean_extracted_text(raw_text)

def extract_pdf_pages_text(file_bytes: bytes) -> list[str]:
    """
    Extract text from each PDF page separately.

    This allows the document extractor to determine which
    individual pages may require OCR.
    """

    document = pymupdf.open(
        stream=file_bytes,
        filetype="pdf",
    )

    pages_text = []

    try:
        for page in document:

            blocks = page.get_text(
                "blocks",
                sort=True,
            )

            page_lines = []

            for block in blocks:
                if not block:
                    continue

                block_text = block[4]

                if not block_text:
                    continue

                block_text = block_text.strip()

                if block_text:
                    page_lines.append(block_text)

            page_text = "\n".join(page_lines)

            pages_text.append(
                clean_extracted_text(page_text)
            )

    finally:
        document.close()

    return pages_text