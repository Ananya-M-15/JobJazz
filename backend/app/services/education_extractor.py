import re

from app.models.resume_profile import Education


EDUCATION_KEYWORDS = [
    "education",
    "academic background",
    "qualifications",
]


EDUCATION_SECTION_END_KEYWORDS = [
    "technical skills",
    "skills",
    "experience",
    "work experience",
    "projects",
    "certifications",
]


DEGREE_PATTERN = re.compile(
    r"\b("
    r"b\.?\s*tech|"
    r"b\.?\s*e|"
    r"bachelor(?:'s)?|"
    r"m\.?\s*tech|"
    r"m\.?\s*e|"
    r"master(?:'s)?|"
    r"mba|"
    r"mca|"
    r"bca|"
    r"phd|"
    r"diploma"
    r")\b",
    re.IGNORECASE,
)


DATE_PATTERN = re.compile(
    r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)"
    r"[a-z]*\.?\s+\d{4}\b"
    r"|\b\d{4}\b",
    re.IGNORECASE,
)


def find_education_section(text: str) -> str:
    lines = text.splitlines()

    start_index = None

    for index, line in enumerate(lines):
        if line.strip().lower() in EDUCATION_KEYWORDS:
            start_index = index + 1
            break

    if start_index is None:
        return ""

    section_lines = []

    for line in lines[start_index:]:
        stripped = line.strip()

        if not stripped:
            continue

        if stripped.lower() in EDUCATION_SECTION_END_KEYWORDS:
            break

        section_lines.append(stripped)

    return "\n".join(section_lines)


def extract_education(text: str) -> list[Education]:
    section = find_education_section(text)

    if not section:
        return []

    lines = [
        line.strip()
        for line in section.splitlines()
        if line.strip()
    ]

    if not lines:
        return []

    education_entries = []

    institution = ""
    degree = ""
    field_of_study = ""
    dates = []

    for line in lines:

        # First likely line = institution
        if not institution and not DEGREE_PATTERN.search(line):
            institution = line
            continue

        # Degree line
        degree_match = DEGREE_PATTERN.search(line)

        if degree_match:
            degree = degree_match.group(0).strip()

            # Try to extract field of study
            field_match = re.search(
                r"\b(?:in|of)\s+(.+?)(?=\s+\d{4}|\s*$)",
                line,
                re.IGNORECASE,
            )

            if field_match:
                field_of_study = field_match.group(1).strip()

            dates.extend(DATE_PATTERN.findall(line))
            continue

        # Date line or additional information
        line_dates = DATE_PATTERN.findall(line)

        if line_dates:
            dates.extend(line_dates)

    # Remove duplicate dates while preserving order
    dates = list(dict.fromkeys(dates))

    start_date = dates[0] if len(dates) >= 1 else ""
    end_date = dates[1] if len(dates) >= 2 else ""

    if institution or degree or field_of_study:
        education_entries.append(
            Education(
                institution=institution,
                degree=degree,
                field_of_study=field_of_study,
                start_date=start_date,
                end_date=end_date,
            )
        )

    return education_entries