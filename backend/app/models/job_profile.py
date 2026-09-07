from pydantic import BaseModel, Field


class JobProfile(BaseModel):
    job_title: str = ""

    required_skills: list[str] = Field(
        default_factory=list
    )

    preferred_skills: list[str] = Field(
        default_factory=list
    )

    experience_requirement: str = ""

    education_requirements: list[str] = Field(
        default_factory=list
    )

    keywords: list[str] = Field(
        default_factory=list
    )