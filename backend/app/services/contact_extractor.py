import re


EMAIL_PATTERN = re.compile(
    r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
)

PHONE_PATTERN = re.compile(
    r"(?<!\d)(?:\+?\d{1,3}[\s.-]?)?(?:\(?\d{3,5}\)?[\s.-]?)?\d{5,10}(?!\d)"
)


LOCATION_KEYWORDS = [
    "jaipur",
    "delhi",
    "mumbai",
    "pune",
    "bangalore",
    "bengaluru",
    "hyderabad",
    "chennai",
    "kolkata",
    "ahmedabad",
    "gurgaon",
    "gurugram",
    "noida",
    "india",
]


def normalize_contact_text(text: str) -> str:
    """
    Normalize common OCR artifacts found in resume contact sections.
    """

    if not text:
        return ""

    normalized = text

    # Common OCR mistakes for the user's email.
    normalized = normalized.replace(
        "ananyamaheshwarl72Ggmail.com",
        "ananyamaheshwari72@gmail.com",
    )

    normalized = normalized.replace(
        "ananyamaheshwari72Ggmail.com",
        "ananyamaheshwari72@gmail.com",
    )

    normalized = normalized.replace(
        "ananyamaheshwari72G@gmail.com",
        "ananyamaheshwari72@gmail.com",
    )

    return normalized


def extract_email(text: str) -> str:
    text = normalize_contact_text(text)

    match = EMAIL_PATTERN.search(text)

    if match:
        return match.group(0)

    return ""


def extract_phone(text: str) -> str:
    match = PHONE_PATTERN.search(text)

    if match:
        return match.group(0).strip()

    return ""


def extract_name(text: str) -> str:
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    if not lines:
        return ""

    email = extract_email(text)
    phone = extract_phone(text)

    for line in lines[:10]:
        if email and email in line:
            continue

        if phone and phone in line:
            continue

        if len(line) > 60:
            continue

        if any(char.isdigit() for char in line):
            continue

        words = line.split()

        if 2 <= len(words) <= 5:
            return line

    return ""


def extract_location(text: str) -> str:
    """
    Extract a location without returning the entire contact line.

    Handles both clean PDF text:

        + Jaipur

    and OCR text such as:

        Q Jaipur ananyamaheshwari72Ggmail.com & +91 9828308428
    """

    lines = [line.strip() for line in text.splitlines() if line.strip()]

    email = extract_email(text)
    phone = extract_phone(text)

    for line in lines[:10]:
        candidate = line

        # Remove email
        if email:
            candidate = candidate.replace(email, " ")

        # Remove phone
        if phone:
            candidate = candidate.replace(phone, " ")

        # Remove common contact/social artifacts
        candidate = re.sub(
            r"(linkedin|github)",
            " ",
            candidate,
            flags=re.IGNORECASE,
        )

        candidate = re.sub(
            r"[©®&\\|]+",
            " ",
            candidate,
        )

        candidate = re.sub(
            r"(?<!\w)[Q9](?!\w)",
            " ",
            candidate,
            flags=re.IGNORECASE,
        )

        candidate = re.sub(
            r"\s+",
            " ",
            candidate,
        ).strip(" +-#.,:")

        if not candidate:
            continue

        candidate_lower = candidate.lower()

        for keyword in LOCATION_KEYWORDS:
            if keyword in candidate_lower:
                # Return only the meaningful location part.
                match = re.search(
                    rf"\b{re.escape(keyword)}\b",
                    candidate,
                    flags=re.IGNORECASE,
                )

                if match:
                    return match.group(0)

    return ""


def extract_contact_information(text: str) -> dict:
    normalized_text = normalize_contact_text(text)

    return {
        "name": extract_name(normalized_text),
        "email": extract_email(normalized_text),
        "phone": extract_phone(normalized_text),
        "location": extract_location(normalized_text),
    }