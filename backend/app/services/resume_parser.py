from app.models.resume_profile import ResumeProfile
from app.services.certification_extractor import extract_certifications
from app.services.contact_extractor import extract_contact_information
from app.services.education_extractor import extract_education
from app.services.experience_extractor import extract_experience
from app.services.project_extractor import extract_projects
from app.services.skills_extractor import extract_skills
from app.services.summary_extractor import extract_summary

def parse_resume_text(text: str) -> ResumeProfile:
    contact_info = extract_contact_information(text)
    summary = extract_summary(text)
    skills = extract_skills(text)
    education = extract_education(text)
    experience = extract_experience(text)
    projects = extract_projects(text)
    certifications = extract_certifications(text)

    return ResumeProfile(
        name=contact_info["name"],
        email=contact_info["email"],
        phone=contact_info["phone"],
        location=contact_info["location"],
        summary=summary,
        skills=skills,
        education=education,
        experience=experience,
        projects=projects,
        certifications=certifications,
    )