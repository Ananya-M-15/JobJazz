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


KNOWN_ISSUERS = {
    "nptel": "NPTEL",
    "python": "Python",
    "microsoft azure": "Microsoft Azure",
    "red hat": "Red Hat",
    "cisco": "Cisco",
}


def normalize_line(line: str) -> str:
    """Remove common OCR artifacts from certification lines."""

    line = line.strip()

    # Remove common OCR bullets.
    line = re.sub(
        r"^(?:o|eo)\s+",
        "",
        line,
        flags=re.IGNORECASE,
    )

    # Normalize spaces before colons.
    line = re.sub(r"\s+:", ":", line)

    return line.strip()


def find_certification_section(text: str) -> str:
    lines = text.splitlines()

    start_index = None

    for index, line in enumerate(lines):
        normalized = re.sub(
            r"[^a-zA-Z &]",
            "",
            line,
        ).strip().lower()

        if normalized in CERTIFICATION_SECTION_KEYWORDS:
            start_index = index + 1
            break

    if start_index is None:
        return ""

    section_lines = []

    for line in lines[start_index:]:
        stripped = normalize_line(line)

        if not stripped:
            continue

        normalized = re.sub(
            r"[^a-zA-Z &]",
            "",
            stripped,
        ).strip().lower()

        if normalized in SECTION_END_KEYWORDS:
            break

        section_lines.append(stripped)

    return "\n".join(section_lines)


def get_known_issuer(value: str) -> str:
    """Return canonical issuer name if recognized."""

    return KNOWN_ISSUERS.get(
        value.strip().lower(),
        "",
    )


def extract_certifications(text: str) -> list[Certification]:
    section = find_certification_section(text)

    if not section:
        return []

    lines = [
        normalize_line(line)
        for line in section.splitlines()
        if normalize_line(line)
    ]

    certifications = []

    current_issuer = ""

    for line in lines:

        # ---------------------------------------------
        # Case 1:
        #
        # Cisco:
        # Computer Networks
        # ---------------------------------------------

        if line.endswith(":"):
            issuer_text = line.rstrip(":").strip()

            issuer = get_known_issuer(issuer_text)

            if issuer:
                current_issuer = issuer

            continue

        # ---------------------------------------------
        # Case 2:
        #
        # NPTEL: Data Structures & Algorithms, ...
        # ---------------------------------------------

        if ":" in line:
            issuer_text, certification_text = line.split(
                ":",
                1,
            )

            issuer = get_known_issuer(issuer_text)

            if issuer:
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

                current_issuer = ""

                continue

        # ---------------------------------------------
        # Case 3:
        #
        # Line following:
        #
        # Cisco:
        # Computer Networks
        # ---------------------------------------------

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

        # ---------------------------------------------
        # Case 4:
        #
        # Fallback certification without issuer.
        # ---------------------------------------------

        certifications.append(
            Certification(
                name=line,
                issuer="",
                date="",
            )
        )

    return certifications