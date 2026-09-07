import re


SECTION_ALIASES = {
    "required": [
        "requirements",
        "required skills",
        "required qualifications",
        "must have",
        "must-have",
        "mandatory skills",
        "basic qualifications",
    ],
    "preferred": [
        "preferred skills",
        "preferred qualifications",
        "nice to have",
        "nice-to-have",
        "good to have",
        "desired skills",
        "preferred",
    ],
    "experience": [
        "experience",
        "work experience",
        "professional experience",
        "years of experience",
    ],
    "education": [
        "education",
        "educational qualifications",
        "academic qualifications",
        "qualification",
        "qualifications",
    ],
    "responsibilities": [
        "responsibilities",
        "job responsibilities",
        "what you'll do",
        "what you will do",
        "role responsibilities",
        "duties",
    ],
}


def normalize_line(line: str) -> str:
    line = line.strip()

    # Remove common bullet characters.
    line = re.sub(r"^[•●▪◦\-*]+\s*", "", line)

    return line.strip()


def find_section(lines: list[str], keywords: list[str]) -> str:
    start_index = None

    for index, line in enumerate(lines):
        normalized = normalize_line(line).lower()

        if normalized in keywords:
            start_index = index + 1
            break

    if start_index is None:
        return ""

    section_lines = []

    for line in lines[start_index:]:
        normalized = normalize_line(line)

        if not normalized:
            continue

        # Stop when another known section heading appears.
        lower_line = normalized.lower()

        is_another_section = any(
            lower_line in section_keywords
            for section_keywords in SECTION_ALIASES.values()
        )

        if is_another_section:
            break

        section_lines.append(normalized)

    return "\n".join(section_lines)


def extract_job_sections(text: str) -> dict[str, str]:
    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    return {
        "required": find_section(
            lines,
            SECTION_ALIASES["required"],
        ),
        "preferred": find_section(
            lines,
            SECTION_ALIASES["preferred"],
        ),
        "experience": find_section(
            lines,
            SECTION_ALIASES["experience"],
        ),
        "education": find_section(
            lines,
            SECTION_ALIASES["education"],
        ),
    }
def extract_job_title(text: str) -> str:
    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    if not lines:
        return ""

    # Usually the job title appears near the beginning
    # of the job description.
    return lines[0] 