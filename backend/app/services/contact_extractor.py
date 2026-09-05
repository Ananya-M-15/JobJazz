import re


EMAIL_PATTERN = re.compile(
    r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
)

PHONE_PATTERN = re.compile(
    r"(?<!\d)(?:\+?\d{1,3}[\s.-]?)?(?:\(?\d{3,5}\)?[\s.-]?)?\d{5,10}(?!\d)"
)


def extract_email(text: str) -> str:
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
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    location_keywords = [
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

    for line in lines[:10]:
        line_lower = line.lower()

        for keyword in location_keywords:
            if keyword in line_lower:
                return line

    return ""


def extract_contact_information(text: str) -> dict:
    return {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "location": extract_location(text),
    }