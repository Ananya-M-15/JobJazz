from pydantic import BaseModel, Field


class SkillRecommendation(BaseModel):
    skill: str
    priority: str
    reason: str
    action: str


class RecommendationResult(BaseModel):
    recommendations: list[SkillRecommendation] = Field(
        default_factory=list
    )
    overall_advice: str = ""