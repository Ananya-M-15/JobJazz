import re


SECTION_ALIASES = {
    "required": [
        "requirements",
        "required skills",
        "required qualifications",
        "must have",
        "must-have",
        "must haves",
        "must-haves",
        "mandatory skills",
        "basic qualifications",
        "minimum qualifications",
        "technical skills",
        "skills",
        "key skills",
        "core skills",
        "core competencies",
        "core competency",
        "key competencies",
        "technical requirements",
        "minimum requirements",
        "basic requirements",
        "role requirements",
        "job requirements",
        "candidate requirements",
        "key requirements",
        "what you'll need",
        "what you will need",
        "what you need",
        "what you bring",
        "what you'll bring",
        "what you will bring",
        "what we're looking for",
        "what we are looking for",
        "skills & qualifications",
        "skills and qualifications",
        "skills & requirements",
        "skills and requirements",
        "required experience & skills",
        "required skills & experience",
        "who you are",
        "qualifications",
    ],
    "preferred": [
        "preferred skills",
        "preferred qualifications",
        "nice to have",
        "nice-to-have",
        "nice to haves",
        "nice-to-haves",
        "good to have",
        "good-to-have",
        "good to haves",
        "good-to-haves",
        "desired skills",
        "desired qualifications",
        "preferred",
        "bonus",
        "bonus points",
        "bonus skills",
        "plus",
        "pluses",
        "additional skills",
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
        "academic background",
        "education requirements",
    ],
    "responsibilities": [
        "responsibilities",
        "job responsibilities",
        "what you'll do",
        "what you will do",
        "role responsibilities",
        "duties",
        "key responsibilities",
    ],
    "contextual": [
        "about the role",
        "about the job",
        "about the position",
        "about the team",
        "team overview",
        "about the company",
        "about us",
        "who we are",
        "company overview",
        "benefits",
        "what we offer",
        "perks",
        "compensation",
        "benefits & perks",
        "how to apply",
        "application process",
    ],
}


def normalize_line(line: str) -> str:
    if not line:
        return ""

    line = line.strip()

    # Normalize common Unicode bullet characters.
    line = re.sub(r"^[•●▪◦\-*]+\s*", "", line)

    # Remove common mojibake bullet artifacts.
    line = re.sub(r"^(?:â€¢|â—¦|â–ª|â—¦)+\s*", "", line)

    return line.strip()


def normalize_heading(line: str) -> str:
    line = normalize_line(line)

    # Strip markdown heading characters (e.g., ## or ###)
    line = re.sub(r"^#+\s*", "", line)

    # Strip markdown bold/italic decorators (e.g., **Requirements:**)
    line = re.sub(r"^[*_]+|[*_]+$", "", line)

    # Remove trailing punctuation commonly found in JD headings.
    line = re.sub(r"[:\-–—]+$", "", line)

    # Strip again in case markdown decorators were outside punctuation
    line = re.sub(r"^[*_]+|[*_]+$", "", line)

    # Collapse whitespace.
    line = re.sub(r"\s+", " ", line)

    return line.strip().lower()


def is_known_section_heading(line: str) -> bool:
    normalized = normalize_heading(line)

    return any(
        normalized in aliases
        for aliases in SECTION_ALIASES.values()
    )


def find_section(lines: list[str], keywords: list[str]) -> str:
    normalized_keywords = {
        normalize_heading(keyword)
        for keyword in keywords
    }

    start_index = None

    for index, line in enumerate(lines):
        normalized = normalize_heading(line)

        if normalized in normalized_keywords:
            start_index = index + 1
            break

    if start_index is None:
        return ""

    section_lines = []

    for line in lines[start_index:]:
        normalized = normalize_line(line)

        if not normalized:
            continue

        if is_known_section_heading(normalized):
            break

        section_lines.append(normalized)

    return "\n".join(section_lines)


def extract_job_sections(text: str) -> dict[str, str]:
    if not text:
        return {
            "required": "",
            "preferred": "",
            "experience": "",
            "education": "",
            "responsibilities": "",
        }

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
        "responsibilities": find_section(
            lines,
            SECTION_ALIASES["responsibilities"],
        ),
    }


def extract_job_title(text: str) -> str:
    lines = [
        normalize_line(line)
        for line in text.splitlines()
        if normalize_line(line)
    ]

    if not lines:
        return ""

    # Ignore generic document labels.
    ignored_titles = {
        "job description",
        "job posting",
        "position",
        "role",
        "about the role",
    }

    for line in lines[:8]:
        normalized = normalize_heading(line)

        if normalized in ignored_titles:
            continue

        if is_known_section_heading(line):
            continue

        # Avoid selecting very long descriptive sentences.
        if len(line.split()) <= 12:
            return line

    return lines[0]