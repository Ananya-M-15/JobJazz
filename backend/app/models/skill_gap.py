from pydantic import BaseModel, Field


class SkillGapResult(BaseModel):
    strengths: list[str] = Field(default_factory=list)
    critical_gaps: list[str] = Field(default_factory=list)
    preferred_gaps: list[str] = Field(default_factory=list)
    experience_gap: bool = False
    education_gap: bool = False