import re


def clean_extracted_text(text: str) -> str:
    """
    Clean text extracted from PDFs or OCR.

    The cleaning is intentionally conservative so that
    actual resume content is not accidentally changed.
    """

    if not text:
        return ""

    # Remove null characters.
    text = text.replace("\x00", " ")

    # Normalize common bullet characters.
    text = re.sub(
        r"[•●▪◦©®]",
        " ",
        text,
    )

    # Remove common OCR artifacts at the beginning of lines.
    text = re.sub(
        r"(?m)^[ \t]*(?:eo|o)[ \t]+",
        "",
        text,
        flags=re.IGNORECASE,
    )

    # Normalize Unicode dashes.
    text = text.replace("–", "-")
    text = text.replace("—", "-")

    # Repair words broken by a line-ending hyphen.
    #
    # Example:
    # result-
    # driven
    #
    # becomes:
    # result-driven
    text = re.sub(
        r"(\w+)-\s*\n\s*(\w+)",
        r"\1-\2",
        text,
    )

    # Repair hyphenated words where PDF/OCR extraction
    # inserted spaces after the hyphen.
    #
    # Example:
    # result- driven
    #
    # becomes:
    # result-driven
    text = re.sub(
        r"(\w+)-\s+(\w+)",
        r"\1-\2",
        text,
    )

    # Normalize repeated spaces and tabs.
    text = re.sub(
        r"[ \t]+",
        " ",
        text,
    )

    # Remove trailing whitespace from lines.
    text = re.sub(
        r"[ \t]+\n",
        "\n",
        text,
    )

    # Collapse excessive blank lines.
    text = re.sub(
        r"\n{3,}",
        "\n\n",
        text,
    )

    return text.strip()