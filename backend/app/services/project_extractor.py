import re

from app.models.resume_profile import Project


PROJECT_SECTION_KEYWORDS = [
    "projects",
    "academic projects",
    "personal projects",
    "projects & work",
]


SECTION_END_KEYWORDS = [
    "experience",
    "work experience",
    "education",
    "technical skills",
    "skills",
    "certifications",
]


IGNORED_PROJECT_LINES = {
    "github repository",
    "github repo",
    "in progress",
}


TECHNOLOGY_ALIASES = {
    "python": "Python",
    "javascript": "JavaScript",
    "typescript": "TypeScript",
    "react": "React",
    "django": "Django",
    "flask": "Flask",
    "fastapi": "FastAPI",
    "mongodb": "MongoDB",
    "mysql": "MySQL",
    "sql": "SQL",
    "html": "HTML",
    "css": "CSS",
    "machine learning": "Machine Learning",
    "deep learning": "Deep Learning",
    "tensorflow": "TensorFlow",
    "pytorch": "PyTorch",
    "pandas": "Pandas",
    "numpy": "NumPy",
    "scikit-learn": "Scikit-learn",
    "docker": "Docker",
    "git": "Git",
}


DESCRIPTION_START_WORDS = [
    "built",
    "developed",
    "created",
    "designed",
    "implemented",
    "developing",
    "worked",
    "working",
    "used",
    "using",
    "integrated",
    "integrating",
    "contributed",
    "collaborated",
    "deployed",
]


def find_projects_section(text: str) -> str:
    lines = text.splitlines()

    start_index = None

    for index, line in enumerate(lines):
        if line.strip().lower() in PROJECT_SECTION_KEYWORDS:
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


def extract_technologies(text: str) -> list[str]:
    text_lower = text.lower()

    technologies = []

    for technology, display_name in TECHNOLOGY_ALIASES.items():
        pattern = (
            r"(?<![a-z0-9])"
            + re.escape(technology)
            + r"(?![a-z0-9])"
        )

        if re.search(pattern, text_lower):
            if display_name not in technologies:
                technologies.append(display_name)

    return technologies


def looks_like_project_title(line: str) -> bool:
    stripped = line.strip()

    if not stripped:
        return False

    if stripped.lower() in IGNORED_PROJECT_LINES:
        return False

    if stripped.startswith(("-", "•", "*")):
        return False

    if len(stripped) > 60:
        return False

    if stripped.endswith((".", ":", ";")):
        return False

    first_word = stripped.split()[0].lower()

    if first_word in DESCRIPTION_START_WORDS:
        return False

    # "In Progress" is metadata, not a project title.
    if stripped.lower() == "in progress":
        return False

    words = stripped.split()

    return 1 <= len(words) <= 8


def clean_description(lines: list[str]) -> str:
    cleaned_lines = []

    for line in lines:
        line = line.strip()

        if line.lower() in IGNORED_PROJECT_LINES:
            continue

        if line.lower() == "in progress":
            continue

        line = re.sub(r"^[-•*]\s*", "", line)

        if line:
            cleaned_lines.append(line)

    return " ".join(cleaned_lines)


def save_project(
    projects: list[Project],
    name: str,
    description_lines: list[str],
) -> None:
    if not name:
        return

    description = clean_description(description_lines)

    projects.append(
        Project(
            name=name,
            description=description,
            technologies=extract_technologies(
                name + " " + description
            ),
        )
    )


def extract_projects(text: str) -> list[Project]:
    section = find_projects_section(text)

    if not section:
        return []

    lines = [
        line.strip()
        for line in section.splitlines()
        if line.strip()
    ]

    projects = []
    current_name = ""
    description_lines = []

    for line in lines:

        # Ignore project metadata.
        if line.lower() in IGNORED_PROJECT_LINES:
            continue

        if line.lower() == "in progress":
            continue

        # A new title starts a new project.
        if looks_like_project_title(line):

            if current_name:
                save_project(
                    projects,
                    current_name,
                    description_lines,
                )

            current_name = line
            description_lines = []

        else:
            description_lines.append(line)

    # Save final project.
    if current_name:
        save_project(
            projects,
            current_name,
            description_lines,
        )

    return projects