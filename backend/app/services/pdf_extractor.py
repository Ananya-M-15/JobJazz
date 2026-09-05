import re
import fitz


def clean_extracted_text(text: str) -> str:
    text = text.replace("\x00", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def extract_text_from_pdf(file_bytes: bytes) -> str:
    document = fitz.open(stream=file_bytes, filetype="pdf")

    extracted_pages = []

    try:
        for page in document:
            text = page.get_text("text")

            if text:
                extracted_pages.append(text)
    finally:
        document.close()

    raw_text = "\n".join(extracted_pages)

    return clean_extracted_text(raw_text)
    