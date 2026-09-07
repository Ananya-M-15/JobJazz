import re


SUMMARY_HEADINGS = [
    "introduction",
    "summary",
    "profile",
    "objective",
]


SUMMARY_END_HEADINGS = [
    "education",
    "technical skills",
    "skills",
    "experience",
    "projects",
    "certifications",
    "achievements",
    "publications",
]


def extract_summary(text: str) -> str:
    if not text:
        return ""

    lines = [line.strip() for line in text.splitlines()]

    start_index = None

    # Find the beginning of the summary section.
    for index, line in enumerate(lines):
        normalized_line = re.sub(r"[^a-zA-Z ]", "", line).strip().lower()

        # Handle normal headings and common OCR variation:
        # Introduction -> Introducti
        if normalized_line in SUMMARY_HEADINGS:
            start_index = index
            break

        if normalized_line == "introducti":
            start_index = index
            break

    if start_index is None:
        return ""

    summary_lines = []

    # Collect everything after the heading
    # until the next major resume section.
    for line in lines[start_index + 1:]:
        if not line:
            continue

        normalized_line = re.sub(
            r"[^a-zA-Z ]",
            "",
            line,
        ).strip().lower()

        if normalized_line in SUMMARY_END_HEADINGS:
            break

        summary_lines.append(line)

    summary = " ".join(summary_lines)

    # Fix accidental whitespace caused by extraction.
    summary = re.sub(r"\s+", " ", summary)

    return summary.strip()