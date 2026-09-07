import re

from app.models.resume_profile import Experience


EXPERIENCE_KEYWORDS = [
    "experience",
    "work experience",
    "professional experience",
    "employment",
]

EXPERIENCE_SECTION_END_KEYWORDS = [
    "projects",
    "certifications",
    "education",
    "technical skills",
    "skills",
    "achievements",
    "publications",
]

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


def find_experience_section(text: str) -> str:
    lines = text.splitlines()

    start_index = None

    for index, line in enumerate(lines):
        normalized = re.sub(
            r"[^a-zA-Z ]",
            "",
            line,
        ).strip().lower()

        if normalized in EXPERIENCE_KEYWORDS:
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

        if normalized in EXPERIENCE_SECTION_END_KEYWORDS:
            break

        section_lines.append(stripped)

    return "\n".join(section_lines)


def extract_dates(text: str) -> tuple[str, str]:
    match = DATE_RANGE_PATTERN.search(text)

    if not match:
        return "", ""

    date_range = match.group(1)

    parts = re.split(
        r"\s*[-–—]\s*",
        date_range,
    )

    if len(parts) == 2:
        return parts[0].strip(), parts[1].strip()

    return "", ""


def is_date_line(line: str) -> bool:
    return bool(DATE_RANGE_PATTERN.search(line))


def clean_description(lines: list[str]) -> str:
    cleaned = []

    for line in lines:
        line = line.strip()

        if not line:
            continue

        # Remove common OCR bullet artifacts.
        line = re.sub(
            r"^(?:o|eo|•|●|▪|◦)\s+",
            "",
            line,
            flags=re.IGNORECASE,
        )

        cleaned.append(line)

    return " ".join(cleaned)


def looks_like_role(line: str) -> bool:
    role_keywords = [
        "intern",
        "engineer",
        "developer",
        "coordinator",
        "manager",
        "analyst",
        "designer",
        "consultant",
        "associate",
        "lead",
        "specialist",
        "trainee",
        "executive",
        "administrator",
        "assistant",
    ]

    lowered = line.lower()

    return any(keyword in lowered for keyword in role_keywords)


def looks_like_company(line: str) -> bool:
    if not line:
        return False

    if looks_like_role(line):
        return False

    if len(line.split()) > 8:
        return False

    return True


def extract_experience(text: str) -> list[Experience]:
    section = find_experience_section(text)

    if not section:
        return []

    lines = [
        line.strip()
        for line in section.splitlines()
        if line.strip()
    ]

    experiences = []

    index = 0

    while index < len(lines):

        # --------------------------------------------------
        # Expected structure:
        #
        # DATE
        # ROLE
        # COMPANY
        # DESCRIPTION
        # --------------------------------------------------

        if not is_date_line(lines[index]):
            index += 1
            continue

        start_date, end_date = extract_dates(lines[index])

        index += 1

        if index >= len(lines):
            break

        # The next line is normally the role.
        role = lines[index]

        index += 1

        if index >= len(lines):
            break

        # The following line is normally the company.
        company = lines[index]

        index += 1

        description_lines = []

        # Everything until the next date is description.
        while index < len(lines):

            if is_date_line(lines[index]):
                break

            description_lines.append(lines[index])
            index += 1

        description = clean_description(description_lines)

        experiences.append(
            Experience(
                company=company,
                role=role,
                start_date=start_date,
                end_date=end_date,
                description=description,
            )
        )

    return experiences