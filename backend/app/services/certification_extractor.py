import re

from app.models.resume_profile import Certification


CERTIFICATION_SECTION_KEYWORDS = [
    "certifications",
    "certificates",
    "licenses & certifications",
]


SECTION_END_KEYWORDS = [
    "education",
    "technical skills",
    "skills",
    "experience",
    "work experience",
    "projects",
]


KNOWN_ISSUERS = [
    "NPTEL",
    "Python",
    "Microsoft Azure",
    "Red Hat",
    "Cisco",
]


def find_certification_section(text: str) -> str:
    lines = text.splitlines()

    start_index = None

    for index, line in enumerate(lines):
        if line.strip().lower() in CERTIFICATION_SECTION_KEYWORDS:
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


def extract_certifications(text: str) -> list[Certification]:
    section = find_certification_section(text)

    if not section:
        return []

    lines = [
        line.strip()
        for line in section.splitlines()
        if line.strip()
    ]

    certifications = []

    current_issuer = ""

    for line in lines:

        # Case 1:
        # "Cisco:"
        # "Computer Networks"
        #
        # Remember the issuer and use the next line
        # as the certification name.
        if line.endswith(":"):
            current_issuer = line.rstrip(":").strip()
            continue

        # Case 2:
        # "NPTEL: Data Structures & Algorithms, Design & Analysis..."
        #
        # Split the issuer from the certification names.
        if ":" in line:
            issuer, certification_text = line.split(":", 1)

            issuer = issuer.strip()
            certification_text = certification_text.strip()

            if issuer in KNOWN_ISSUERS:
                current_issuer = issuer

                certification_names = [
                    item.strip()
                    for item in certification_text.split(",")
                    if item.strip()
                ]

                for name in certification_names:
                    certifications.append(
                        Certification(
                            name=name,
                            issuer=current_issuer,
                            date="",
                        )
                    )

                continue

        # Case 3:
        # A line following something like:
        # "Cisco:"
        if current_issuer:
            certifications.append(
                Certification(
                    name=line,
                    issuer=current_issuer,
                    date="",
                )
            )

            current_issuer = ""

            continue

        # Fallback
        certifications.append(
            Certification(
                name=line,
                issuer="",
                date="",
            )
        )

    return certifications