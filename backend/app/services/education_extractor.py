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
    "achievements",
    "publications",
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

DATE_RANGE_PATTERN = re.compile(
    r"("
    r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)"
    r"[a-z]*\.?\s+\d{4}"
    r"\s*[-–—]\s*"
    r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)"
    r"[a-z]*\.?\s+\d{4}"
    r"|"
    r"\d{4}\s*[-–—]\s*\d{4}"
    r")",
    re.IGNORECASE,
)

EDUCATION_DESCRIPTOR_PATTERN = re.compile(
    r"\b("
    r"senior secondary|"
    r"secondary education|"
    r"higher secondary|"
    r"high school|"
    r"school education|"
    r"class\s+[ivx]+"
    r")\b",
    re.IGNORECASE,
)


def find_education_section(text: str) -> str:
    lines = text.splitlines()

    start_index = None

    for index, line in enumerate(lines):
        normalized = re.sub(
            r"[^a-zA-Z ]",
            "",
            line,
        ).strip().lower()

        if normalized in EDUCATION_KEYWORDS:
            start_index = index + 1
            break

    if start_index is None:
        return ""

    section_lines = []

    for line in lines[start_index:]:
        stripped = line.strip()

        if not stripped:
            continue

        normalized = re.sub(
            r"[^a-zA-Z ]",
            "",
            stripped,
        ).strip().lower()

        if normalized in EDUCATION_SECTION_END_KEYWORDS:
            break

        section_lines.append(stripped)

    return "\n".join(section_lines)


def extract_dates(text: str) -> tuple[str, str]:
    range_match = DATE_RANGE_PATTERN.search(text)

    if range_match:
        date_range = range_match.group(1)

        parts = re.split(
            r"\s*[-–—]\s*",
            date_range,
        )

        if len(parts) == 2:
            return parts[0].strip(), parts[1].strip()

    dates = DATE_PATTERN.findall(text)

    if len(dates) >= 2:
        return dates[0].strip(), dates[1].strip()

    if len(dates) == 1:
        return dates[0].strip(), ""

    return "", ""


def remove_dates(text: str) -> str:
    text = DATE_RANGE_PATTERN.sub("", text)
    text = DATE_PATTERN.sub("", text)

    text = re.sub(r"\s+", " ", text)

    return text.strip(" -–—|")


def extract_degree_and_field(line: str) -> tuple[str, str]:
    degree_match = DEGREE_PATTERN.search(line)

    if not degree_match:
        return "", ""

    degree = degree_match.group(0).strip()

    field_of_study = ""

    field_match = re.search(
        r"\b(?:in|of)\s+(.+?)(?=\s*$)",
        line,
        re.IGNORECASE,
    )

    if field_match:
        field_of_study = field_match.group(1).strip()

    return degree, field_of_study


def is_date_line(line: str) -> bool:
    return bool(DATE_RANGE_PATTERN.search(line))


def is_institution_line(line: str) -> bool:
    if not line:
        return False

    if DEGREE_PATTERN.search(line):
        return False

    if line.lower().startswith("coursework"):
        return False

    if EDUCATION_DESCRIPTOR_PATTERN.search(line):
        return False

    return True


def extract_education(text: str) -> list[Education]:
    section = find_education_section(text)

    if not section:
        return []

    lines = [
        line.strip()
        for line in section.splitlines()
        if line.strip()
    ]

    education_entries = []

    current_institution = ""
    current_degree = ""
    current_field = ""
    current_start = ""
    current_end = ""

    pending_start = ""
    pending_end = ""

    def save_current_entry():
        nonlocal current_institution
        nonlocal current_degree
        nonlocal current_field
        nonlocal current_start
        nonlocal current_end

        if not (
            current_institution
            or current_degree
            or current_field
        ):
            return

        education_entries.append(
            Education(
                institution=current_institution,
                degree=current_degree,
                field_of_study=current_field,
                start_date=current_start,
                end_date=current_end,
            )
        )

        current_institution = ""
        current_degree = ""
        current_field = ""
        current_start = ""
        current_end = ""

    index = 0

    while index < len(lines):
        line = lines[index]

        # --------------------------------------------------
        # Date appearing BEFORE institution
        # Example:
        # Aug 2023 - July 2027
        # Manipal University Jaipur
        # --------------------------------------------------
        if is_date_line(line):
            pending_start, pending_end = extract_dates(line)

            # If an institution follows this date,
            # attach the dates to that institution.
            if index + 1 < len(lines):
                next_line = lines[index + 1]

                if (
                    not DEGREE_PATTERN.search(next_line)
                    and not EDUCATION_DESCRIPTOR_PATTERN.search(next_line)
                    and not next_line.lower().startswith("coursework")
                ):
                    # Save previous education record first.
                    if (
                        current_institution
                        or current_degree
                        or current_field
                    ):
                        save_current_entry()

                    current_start = pending_start
                    current_end = pending_end

                    current_institution = next_line

                    index += 2
                    continue

            index += 1
            continue

        # --------------------------------------------------
        # Degree + field
        # --------------------------------------------------
        degree, field = extract_degree_and_field(line)

        if degree:
            current_degree = degree
            current_field = field

            start, end = extract_dates(line)

            if start:
                current_start = start

            if end:
                current_end = end

            index += 1
            continue

        # --------------------------------------------------
        # School-level education
        # --------------------------------------------------
        if EDUCATION_DESCRIPTOR_PATTERN.search(line):
            current_degree = line

            index += 1
            continue

        # --------------------------------------------------
        # Coursework should not become part of education
        # --------------------------------------------------
        if line.lower().startswith("coursework"):
            index += 1
            continue

        # --------------------------------------------------
        # Institution without a preceding date
        # --------------------------------------------------
        if not current_institution:
            current_institution = line

        index += 1

    save_current_entry()

    return education_entries