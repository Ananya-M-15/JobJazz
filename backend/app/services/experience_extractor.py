import re

from app.models.resume_profile import Experience


EXPERIENCE_SECTION_KEYWORDS = [
    "experience",
    "work experience",
    "professional experience",
    "internship experience",
]


SECTION_END_KEYWORDS = [
    "education",
    "technical skills",
    "skills",
    "projects",
    "certifications",
]


DATE_PATTERN = re.compile(
    r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)"
    r"[a-z]*\.?\s+\d{4}\b",
    re.IGNORECASE,
)


def find_experience_section(text: str) -> str:
    lines = text.splitlines()

    start_index = None

    for index, line in enumerate(lines):
        if line.strip().lower() in EXPERIENCE_SECTION_KEYWORDS:
            start_index = index + 1
            break

    if start_index is None:
        return ""

    section_lines = []

    for line in lines[start_index:]:
        stripped = line.strip()

        if not stripped:
            continue

        if stripped.lower() in SECTION_END_KEYWORDS:
            break

        section_lines.append(stripped)

    return "\n".join(section_lines)


def extract_experience(text: str) -> list[Experience]:
    section = find_experience_section(text)

    if not section:
        return []

    lines = [
        line.strip()
        for line in section.splitlines()
        if line.strip()
    ]

    entries = []

    i = 0

    while i < len(lines):

        # We expect:
        # Role
        # Company
        # Date
        #
        # Description...

        if i + 2 >= len(lines):
            break

        role = lines[i]
        company = lines[i + 1]

        date_matches = DATE_PATTERN.findall(lines[i + 2])

        if len(date_matches) < 1:
            i += 1
            continue

        start_date = date_matches[0]
        end_date = date_matches[1] if len(date_matches) >= 2 else ""

        i += 3

        description_lines = []

        # Collect everything until the next possible
        # Role + Company + Date combination.
        while i < len(lines):

            if (
                i + 2 < len(lines)
                and len(DATE_PATTERN.findall(lines[i + 2])) >= 1
            ):
                break

            description_lines.append(lines[i])
            i += 1

        description = " ".join(description_lines)

        entries.append(
            Experience(
                company=company,
                role=role,
                start_date=start_date,
                end_date=end_date,
                description=description,
            )
        )

    return entries