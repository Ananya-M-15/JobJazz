import re
from typing import Dict, Any, List


RESUME_SECTION_PATTERNS = [
    r"\b(education|academic\s+background|academic\s+qualifications|educational\s+history)\b",
    r"\b(work\s+experience|professional\s+experience|employment\s+history|career\s+history|experience)\b",
    r"\b(projects|personal\s+projects|academic\s+projects|key\s+projects)\b",
    r"(?<!required\s)(?<!preferred\s)(?<!desired\s)\b(skills|technical\s+skills|core\s+competencies|programming\s+languages|technologies)\b",
    r"\b(certifications|licenses|achievements|honors|publications)\b",
]

CONTACT_PATTERNS = [
    r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",  # email
    r"(\+?\d{1,3}[-.\s]?)?(\(?\d{3}\)?[-.\s]?)?\d{3}[-.\s]?\d{4}\b",  # phone
    r"(linkedin\.com/in/|github\.com/)",  # profile links
]

TIMELINE_PATTERNS = [
    r"\b(20\d{2}|19\d{2})\s*[-–—to]+\s*(20\d{2}|present|current)\b",
    r"\b(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s+\d{4}\b",
]

JD_SECTION_PATTERNS = [
    r"\b(job\s+description|about\s+the\s+role|about\s+the\s+job|role\s+overview|position\s+overview|position\s+summary|job\s+summary)\b",
    r"\b(responsibilities|key\s+responsibilities|what\s+you('ll|\s+will)\s+do|duties|job\s+duties|core\s+responsibilities)\b",
    r"\b(requirements|minimum\s+qualifications|basic\s+qualifications|required\s+qualifications|what\s+we('re|\s+are)\s+looking\s+for|what\s+you\s+bring)\b",
    r"\b(required\s+skills|preferred\s+skills|desired\s+skills|core\s+requirements|key\s+requirements|job\s+requirements|role\s+requirements)\b",
    r"\b(preferred\s+qualifications|nice\s+to\s+have|bonus\s+qualifications|bonus\s+points)\b",
    r"\b(about\s+us|about\s+the\s+company|who\s+we\s+are|company\s+overview|our\s+team)\b",
    r"\b(benefits|what\s+we\s+offer|compensation|perks)\b",
    r"\b(equal\s+opportunity\s+employer|affirmative\s+action)\b",
]

JD_IMPERATIVE_PATTERNS = [
    r"\b(you\s+will|you\s+must|we\s+are\s+looking\s+for|join\s+our\s+team|ideal\s+candidate|the\s+successful\s+candidate)\b",
    r"\b(apply\s+now|submit\s+your\s+application|job\s+type:\s*(full-time|part-time|contract))\b",
    r"\b(reporting\s+to|reports\s+to)\b",
    r"\b\d+\+?\s*years(\s+of)?\s+experience\b",
]


def classify_document(text: str) -> Dict[str, Any]:
    """
    Classify a document's purpose based on structural, content-based, and semantic markers.
    Returns:
        {
            "document_type": "resume" | "job_description" | "unrelated" | "ambiguous",
            "resume_score": int,
            "jd_score": int,
            "reasons": list[str]
        }
    """
    cleaned = text.strip()
    if len(cleaned) < 40:
        return {
            "document_type": "unrelated",
            "resume_score": 0,
            "jd_score": 0,
            "reasons": ["Text length is insufficient for career document analysis."],
        }

    lower_text = cleaned.lower()

    # 1. Evaluate Resume Signals
    resume_score = 0
    resume_reasons = []

    # Explicit self-identification
    if re.search(r"\b(resume|curriculum\s+vitae)\b", lower_text) and not any(
        term in lower_text for term in ["job description", "job posting", "apply now", "benefits:"]
    ):
        resume_score += 4
        resume_reasons.append("Document explicitly indicates resume/CV")

    # Contact markers
    contact_matches = 0
    for pat in CONTACT_PATTERNS:
        if re.search(pat, cleaned, re.IGNORECASE):
            contact_matches += 1
    if contact_matches > 0:
        resume_score += contact_matches * 2
        resume_reasons.append(f"Found {contact_matches} contact/identity marker(s)")

    # Resume section markers
    section_matches = 0
    for pat in RESUME_SECTION_PATTERNS:
        if re.search(pat, lower_text):
            section_matches += 1
    if section_matches > 0:
        resume_score += section_matches * 2
        resume_reasons.append(f"Found {section_matches} candidate resume section(s)")

    # Timeline/employment date ranges
    timeline_matches = len(re.findall(TIMELINE_PATTERNS[0], lower_text)) + len(re.findall(TIMELINE_PATTERNS[1], lower_text))
    if timeline_matches > 0:
        resume_score += min(3, timeline_matches)
        resume_reasons.append("Found chronological employment or education date markers")

    # 2. Evaluate Job Description Signals
    jd_score = 0
    jd_reasons = []

    # Explicit JD identification
    if re.search(r"\b(job\s+description|job\s+posting|we\s+are\s+hiring|open\s+position)\b", lower_text):
        jd_score += 4
        jd_reasons.append("Document explicitly indicates a job posting/description")

    # JD section markers
    jd_sections = 0
    for pat in JD_SECTION_PATTERNS:
        if re.search(pat, lower_text):
            jd_sections += 1
    if jd_sections > 0:
        jd_score += jd_sections * 3
        jd_reasons.append(f"Found {jd_sections} employer/job-posting section(s)")

    # Imperative/hiring markers
    jd_imperatives = 0
    for pat in JD_IMPERATIVE_PATTERNS:
        if re.search(pat, lower_text):
            jd_imperatives += 1
    if jd_imperatives > 0:
        jd_score += jd_imperatives * 2
        jd_reasons.append("Found hiring/employer directive language")

    # 3. Determine Document Type
    # If it strongly matches a Job Description
    if jd_score >= 3 and jd_score > resume_score:
        return {
            "document_type": "job_description",
            "resume_score": resume_score,
            "jd_score": jd_score,
            "reasons": jd_reasons,
        }

    # If it strongly matches a Resume
    if resume_score >= 3 and resume_score > jd_score:
        return {
            "document_type": "resume",
            "resume_score": resume_score,
            "jd_score": jd_score,
            "reasons": resume_reasons,
        }

    # If both scores are negligible, it's an unrelated document (e.g. recipe, invoice, essay)
    if resume_score < 2 and jd_score < 2:
        return {
            "document_type": "unrelated",
            "resume_score": resume_score,
            "jd_score": jd_score,
            "reasons": ["Lacks standard candidate resume or job description structural sections."],
        }

    # Ambiguous document (both scores >= 2, but neither clearly dominates)
    return {
        "document_type": "ambiguous",
        "resume_score": resume_score,
        "jd_score": jd_score,
        "reasons": ["Document contains overlapping or unclear markers between candidate credentials and job posting requirements."],
    }
