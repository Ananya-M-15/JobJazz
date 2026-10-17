from datetime import datetime, UTC
from enum import Enum
from typing import Literal
from pydantic import BaseModel, Field, HttpUrl, field_validator


class ResourceFormat(str, Enum):
    COURSES = "courses"
    DOCS = "docs"
    VIDEOS = "videos"
    PROJECTS = "projects"
    MIX = "mix"


class BudgetPreference(str, Enum):
    FREE = "free"
    ALL = "all"


class ProficiencyLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class RoadmapStage(str, Enum):
    LEARN = "Learn"
    PRACTISE = "Practise"
    BUILD = "Build"
    SHOWCASE = "Showcase"
    REASSESS = "Reassess"


class StepStatus(str, Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class GapType(str, Enum):
    GENUINELY_MISSING = "genuinely_missing"
    PARTIALLY_DEMONSTRATED = "partially_demonstrated"
    DEMONSTRATED_UNPOLISHED = "demonstrated_unpolished"
    INDETERMINATE = "indeterminate"


class RoadmapPreferences(BaseModel):
    proficiency: ProficiencyLevel = ProficiencyLevel.INTERMEDIATE
    hours_per_week: int = Field(default=10, ge=1, le=60)
    target_date: str | None = None
    resource_format: ResourceFormat = ResourceFormat.MIX
    budget: BudgetPreference = BudgetPreference.FREE


class LearningResource(BaseModel):
    id: str = Field(default_factory=lambda: "res-" + datetime.now(UTC).strftime("%H%M%S%f")[:10])
    title: str
    provider: str
    url: str
    resource_type: str = "tutorial"  # documentation, course, tutorial, project_guide, video
    skill: str
    why_relevant: str
    pricing: Literal["free", "paid", "unknown"] = "free"
    difficulty: Literal["beginner", "intermediate", "advanced"] = "intermediate"
    estimated_duration: str = "Self-paced"
    is_verified: bool = False
    source: str = "vetted_catalogue"  # gemini_grounded, vetted_catalogue, or fallback

    @field_validator("url")
    @classmethod
    def validate_url(cls, v: str) -> str:
        v = v.strip()
        if not (v.startswith("http://") or v.startswith("https://")):
            raise ValueError("URL must start with http:// or https://")
        return v


class RoadmapStep(BaseModel):
    id: str
    module_id: str
    title: str
    skill: str
    gap_type: GapType = GapType.GENUINELY_MISSING
    stage: RoadmapStage = RoadmapStage.LEARN
    why_it_matters: str
    activities: list[str] = Field(default_factory=list)
    resources: list[LearningResource] = Field(default_factory=list)
    estimated_hours: float = Field(ge=0.5, le=100.0)
    dependencies: list[str] = Field(default_factory=list)
    measurable_outcome: str
    status: StepStatus = StepStatus.NOT_STARTED
    completed_at: str | None = None
    user_notes: str | None = None


class RoadmapModule(BaseModel):
    id: str
    title: str
    skills: list[str]
    priority: Literal["High", "Medium", "Low"] = "High"
    why_it_matters: str
    estimated_hours: float = 0.0
    steps: list[RoadmapStep] = Field(default_factory=list)


class WeeklyScheduleAllocation(BaseModel):
    week_number: int
    start_date: str
    end_date: str
    allocated_hours: float
    learning_hours: float = 0.0
    practising_hours: float = 0.0
    building_hours: float = 0.0
    step_ids: list[str] = Field(default_factory=list)
    step_titles: list[str] = Field(default_factory=list)
    milestone: str | None = None


class RoadmapSchedule(BaseModel):
    total_hours: float = 0.0
    hours_per_week: float = 10.0
    total_weeks: int = 1
    learning_hours: float = 0.0
    practising_hours: float = 0.0
    building_hours: float = 0.0
    start_date: str
    projected_completion_date: str
    target_date: str | None = None
    is_feasible: bool = True
    feasibility_notes: str = ""
    weekly_schedule: list[WeeklyScheduleAllocation] = Field(default_factory=list)
    assumptions: list[str] = Field(default_factory=list)


class RoadmapSummary(BaseModel):
    target_role: str
    overall_strategy: str
    key_focus_areas: list[str] = Field(default_factory=list)
    total_modules: int = 0
    total_steps: int = 0
    total_hours: float = 0.0
    estimated_weeks: int = 0
    completed_steps: int = 0
    progress_percentage: float = 0.0


class RoadmapResult(BaseModel):
    id: str | None = None
    analysis_id: str
    preferences: RoadmapPreferences = Field(default_factory=RoadmapPreferences)
    summary: RoadmapSummary
    modules: list[RoadmapModule] = Field(default_factory=list)
    schedule: RoadmapSchedule
    source: str = "ai"
    created_at: str | None = None
    updated_at: str | None = None


class RoadmapGenerateRequest(BaseModel):
    analysis_id: str
    preferences: RoadmapPreferences = Field(default_factory=RoadmapPreferences)


class StepUpdateRequest(BaseModel):
    status: StepStatus
    user_notes: str | None = None
