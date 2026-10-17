"""
Personalized learning roadmap generator for JobJazz.
Integrates Gemini for intelligent module generation and resource discovery,
with deterministic gap classification, resource validation, and timetable calculation.
"""
import json
import logging
import time
from datetime import datetime, UTC
from typing import Any

from google.genai import types

from app.models.resume_profile import ResumeProfile
from app.models.job_profile import JobProfile
from app.models.match_result import MatchResult
from app.models.skill_gap import SkillGapResult
from app.models.recommendation import RecommendationResult
from app.schemas.roadmap import (
    RoadmapPreferences,
    RoadmapResult,
    RoadmapModule,
    RoadmapStep,
    RoadmapSummary,
    RoadmapStage,
    StepStatus,
    GapType,
    ProficiencyLevel,
)
from app.services.gemini_service import get_gemini_client
from app.services.roadmap_vetted_resources import (
    get_vetted_resources_for_skill,
    VETTED_PROJECT_TEMPLATES,
    validate_and_sanitize_resource,
)
from app.services.roadmap_schedule_engine import calculate_schedule

logger = logging.getLogger(__name__)


def classify_skill_gap(
    skill: str,
    resume: ResumeProfile,
) -> GapType:
    """
    Classify a skill into one of the 4 strict categories:
    1. genuinely_missing
    2. partially_demonstrated
    3. demonstrated_unpolished
    4. indeterminate
    """
    skill_lower = skill.lower()
    resume_skills_lower = [s.lower() for s in resume.skills]

    if skill_lower in resume_skills_lower:
        return GapType.DEMONSTRATED_UNPOLISHED

    # Check resume experience, projects, or summary for partial mentions
    resume_text_corpus = []
    if resume.summary:
        resume_text_corpus.append(resume.summary.lower())
    for exp in resume.experience:
        if exp.description:
            resume_text_corpus.append(exp.description.lower())
        if exp.role:
            resume_text_corpus.append(exp.role.lower())
    for proj in resume.projects:
        if proj.description:
            resume_text_corpus.append(proj.description.lower())
        if proj.technologies:
            resume_text_corpus.extend([t.lower() for t in proj.technologies])

    full_corpus = " ".join(resume_text_corpus)
    if skill_lower in full_corpus:
        return GapType.PARTIALLY_DEMONSTRATED

    return GapType.GENUINELY_MISSING


def generate_deterministic_roadmap(
    resume: ResumeProfile,
    job: JobProfile,
    match_result: MatchResult,
    skill_gap: SkillGapResult,
    recommendations: RecommendationResult | None,
    preferences: RoadmapPreferences,
) -> RoadmapResult:
    """
    Construct a personalized, multi-stage skill development roadmap deterministically
    using verified resources and realistic project exercises.
    """
    critical_skills = list(skill_gap.critical_gaps)
    preferred_skills = list(skill_gap.preferred_gaps)

    # If no gaps at all, select 1-2 key requirements to polish and showcase
    if not critical_skills and not preferred_skills:
        target_skills = job.required_skills[:2] if job.required_skills else ["Software Engineering Principles"]
        is_polishing_plan = True
    else:
        target_skills = critical_skills + preferred_skills
        is_polishing_plan = False

    modules: list[RoadmapModule] = []
    step_counter = 1

    # Group skills into cohesive modules
    grouped_modules = _group_skills_into_modules(target_skills)

    # Effort multiplier based on proficiency
    hours_factor = 1.2 if preferences.proficiency == ProficiencyLevel.BEGINNER else (
        0.8 if preferences.proficiency == ProficiencyLevel.ADVANCED else 1.0
    )

    for mod_title, mod_skills in grouped_modules.items():
        mod_id = f"mod-{len(modules) + 1}"
        priority = "High" if any(s in critical_skills for s in mod_skills) else "Medium"
        primary_skill = mod_skills[0]
        gap_type = classify_skill_gap(primary_skill, resume)

        steps: list[RoadmapStep] = []

        # Stage 1: Learn
        step_1_id = f"step-{step_counter}"
        step_counter += 1
        resources_1 = get_vetted_resources_for_skill(
            primary_skill,
            format_pref=preferences.resource_format,
            budget_pref=preferences.budget,
        )
        learn_hours = round(max(4.0 * hours_factor, 2.0), 1)

        steps.append(
            RoadmapStep(
                id=step_1_id,
                module_id=mod_id,
                title=f"Master {primary_skill} Core Fundamentals",
                skill=primary_skill,
                gap_type=gap_type,
                stage=RoadmapStage.LEARN,
                why_it_matters=f"{primary_skill} is a key requirement for {job.job_title}. Building a solid conceptual foundation is critical.",
                activities=[
                    f"Study the official {primary_skill} documentation and complete initial quickstart modules.",
                    f"Understand core design patterns, configuration, and syntax conventions for {primary_skill}.",
                    f"Note architectural trade-offs relevant to {job.job_title}.",
                ],
                resources=resources_1,
                estimated_hours=learn_hours,
                dependencies=[],
                measurable_outcome=f"Completed introductory exercises and created a personal cheat-sheet of {primary_skill} core concepts.",
            )
        )

        # Stage 2: Practise
        step_2_id = f"step-{step_counter}"
        step_counter += 1
        practise_hours = round(max(5.0 * hours_factor, 3.0), 1)

        steps.append(
            RoadmapStep(
                id=step_2_id,
                module_id=mod_id,
                title=f"Hands-On Problem Sets in {primary_skill}",
                skill=primary_skill,
                gap_type=gap_type,
                stage=RoadmapStage.PRACTISE,
                why_it_matters=f"Passive learning does not translate to job readiness. Targeted practice builds muscle memory and debugging skills.",
                activities=[
                    f"Implement 3 progressive coding exercises focusing on real-world {primary_skill} scenarios.",
                    "Practice error handling, edge cases, and unit testing.",
                    "Refactor solution code for readability, performance, and best practices.",
                ],
                resources=resources_1[:1],
                estimated_hours=practise_hours,
                dependencies=[step_1_id],
                measurable_outcome=f"3 tested code exercises pushed to a dedicated practice repository.",
            )
        )

        # Stage 3: Build
        step_3_id = f"step-{step_counter}"
        step_counter += 1
        build_hours = round(max(8.0 * hours_factor, 5.0), 1)
        project_template = VETTED_PROJECT_TEMPLATES.get(
            primary_skill,
            {
                "title": f"Practical {primary_skill} Application",
                "description": f"Build a practical working module using {primary_skill} tailored to {job.job_title}.",
                "deliverable": f"A working, tested repository demonstrating {primary_skill} in action.",
            },
        )

        steps.append(
            RoadmapStep(
                id=step_3_id,
                module_id=mod_id,
                title=project_template["title"],
                skill=primary_skill,
                gap_type=gap_type,
                stage=RoadmapStage.BUILD,
                why_it_matters=f"Employers evaluate evidence of applied capability. Building a concrete project demonstrates practical problem-solving.",
                activities=[
                    project_template["description"],
                    "Implement clean modular code with automated testing.",
                    "Integrate configuration management and environment variables.",
                ],
                resources=[],
                estimated_hours=build_hours,
                dependencies=[step_2_id],
                measurable_outcome=project_template["deliverable"],
            )
        )

        # Stage 4: Showcase & Reassess (for primary module)
        if len(modules) == 0:
            step_4_id = f"step-{step_counter}"
            step_counter += 1
            showcase_hours = 3.0

            steps.append(
                RoadmapStep(
                    id=step_4_id,
                    module_id=mod_id,
                    title="Document Project & Reassess Career Fit",
                    skill="Portfolio & Resume Polish",
                    gap_type=GapType.DEMONSTRATED_UNPOLISHED,
                    stage=RoadmapStage.SHOWCASE,
                    why_it_matters="A completed project only helps if recruiters and engineering leads can understand what you built, why you built it, and how it worked.",
                    activities=[
                        "Write a comprehensive README with architecture diagram, setup steps, and API/CLI examples.",
                        "Add quantified bullet points highlighting this deliverable to your JobJazz resume profile.",
                        f"Re-run JobJazz analysis against '{job.job_title}' to observe your updated match fit.",
                    ],
                    resources=[],
                    estimated_hours=showcase_hours,
                    dependencies=[step_3_id],
                    measurable_outcome="Published GitHub project with professional documentation and updated resume draft ready for review.",
                )
            )

        module_hours = sum(s.estimated_hours for s in steps)
        modules.append(
            RoadmapModule(
                id=mod_id,
                title=mod_title,
                skills=mod_skills,
                priority=priority,
                why_it_matters=f"Addresses key competencies required for the {job.job_title} role.",
                estimated_hours=round(module_hours, 1),
                steps=steps,
            )
        )

    # Calculate deterministic schedule
    schedule = calculate_schedule(
        modules=modules,
        hours_per_week=preferences.hours_per_week,
        target_date_str=preferences.target_date,
    )

    total_steps = sum(len(m.steps) for m in modules)
    total_hours = schedule.total_hours

    if is_polishing_plan:
        overall_strategy = (
            f"You already demonstrate strong alignment with the key technical requirements for {job.job_title}. "
            "This focused plan deepens your architectural knowledge and helps you build concrete showcase evidence."
        )
    else:
        overall_strategy = (
            f"Targeted learning path to bridge {len(critical_skills)} critical skill gap{'' if len(critical_skills) == 1 else 's'} "
            f"and strengthen your alignment for {job.job_title} through hands-on practice and portfolio projects."
        )

    summary = RoadmapSummary(
        target_role=job.job_title or "Target Position",
        overall_strategy=overall_strategy,
        key_focus_areas=list(grouped_modules.keys())[:4],
        total_modules=len(modules),
        total_steps=total_steps,
        total_hours=total_hours,
        estimated_weeks=schedule.total_weeks,
        completed_steps=0,
        progress_percentage=0.0,
    )

    now_iso = datetime.now(UTC).isoformat()
    return RoadmapResult(
        analysis_id="",
        preferences=preferences,
        summary=summary,
        modules=modules,
        schedule=schedule,
        source="deterministic",
        created_at=now_iso,
        updated_at=now_iso,
    )


def _group_skills_into_modules(skills: list[str]) -> dict[str, list[str]]:
    """Group individual technical skills into sensible thematic modules."""
    if not skills:
        return {"Core Engineering Foundations": ["Python"]}

    groups: dict[str, list[str]] = {}
    backend_skills = {"python", "fastapi", "django", "flask", "sql", "postgresql", "mysql", "mongodb", "rest apis"}
    cloud_devops = {"docker", "kubernetes", "aws", "microsoft azure", "google cloud", "git", "github", "mlops"}
    frontend = {"react", "javascript", "typescript", "html", "css"}
    ml_ai = {"machine learning", "deep learning", "nlp", "computer vision", "tensorflow", "pytorch", "scikit-learn", "pandas", "numpy"}

    unassigned = list(skills)

    # Check thematic clusters
    mod_backend = [s for s in unassigned if s.lower() in backend_skills]
    if mod_backend:
        groups["Backend Architecture & API Systems"] = mod_backend
        unassigned = [s for s in unassigned if s not in mod_backend]

    mod_cloud = [s for s in unassigned if s.lower() in cloud_devops]
    if mod_cloud:
        groups["Cloud Infrastructure & DevOps"] = mod_cloud
        unassigned = [s for s in unassigned if s not in mod_cloud]

    mod_frontend = [s for s in unassigned if s.lower() in frontend]
    if mod_frontend:
        groups["Modern Frontend Development"] = mod_frontend
        unassigned = [s for s in unassigned if s not in mod_frontend]

    mod_ml = [s for s in unassigned if s.lower() in ml_ai]
    if mod_ml:
        groups["Machine Learning & Data Intelligence"] = mod_ml
        unassigned = [s for s in unassigned if s not in mod_ml]

    for leftover in unassigned:
        groups[f"Applied {leftover} Competency"] = [leftover]

    return groups


def generate_personalized_roadmap(
    resume: ResumeProfile,
    job: JobProfile,
    match_result: MatchResult,
    skill_gap: SkillGapResult,
    recommendations: RecommendationResult | None,
    preferences: RoadmapPreferences,
) -> RoadmapResult:
    """
    Generate an intelligent, personalized roadmap attempting Gemini structured generation
    with search grounding first, falling back reliably to deterministic vetted generation.
    """
    start_time = time.perf_counter()

    try:
        client = get_gemini_client()
        prompt = _build_gemini_roadmap_prompt(
            resume,
            job,
            match_result,
            skill_gap,
            preferences,
        )

        response = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.2,
            ),
        )

        raw_data = json.loads(response.text)
        roadmap = _parse_and_validate_gemini_roadmap(
            raw_data,
            resume,
            job,
            preferences,
        )
        duration = time.perf_counter() - start_time
        logger.info("AI Roadmap generated in %.2fs", duration)
        return roadmap

    except Exception as exc:
        duration = time.perf_counter() - start_time
        logger.warning(
            "AI Roadmap generation failed after %.2fs (%s). Using deterministic vetted engine.",
            duration,
            type(exc).__name__,
        )
        return generate_deterministic_roadmap(
            resume=resume,
            job=job,
            match_result=match_result,
            skill_gap=skill_gap,
            recommendations=recommendations,
            preferences=preferences,
        )


def _build_gemini_roadmap_prompt(
    resume: ResumeProfile,
    job: JobProfile,
    match_result: MatchResult,
    skill_gap: SkillGapResult,
    preferences: RoadmapPreferences,
) -> str:
    return f"""
You are JobJazz, an AI career development advisor.
Construct a realistic, highly personalized skill roadmap for a student aiming for the target job below.

CANDIDATE PROFILE:
- Extracted Skills: {resume.skills}
- Experience: {[e.role + " at " + e.company for e in resume.experience]}
- Student Proficiency Level: {preferences.proficiency.value}
- Weekly Availability: {preferences.hours_per_week} hours/week
- Target Completion Date: {preferences.target_date or "Flexible"}
- Format Preference: {preferences.resource_format.value}
- Budget: {preferences.budget.value} only

TARGET ROLE:
- Title: {job.job_title}
- Required Skills: {job.required_skills}
- Preferred Skills: {job.preferred_skills}

GAP ANALYSIS:
- Matched Required: {match_result.matched_required_skills}
- Missing Required (Critical): {skill_gap.critical_gaps}
- Missing Preferred (Bonus): {skill_gap.preferred_gaps}

ROADMAP RULES:
1. Group related gaps into 1 to 4 thematic modules.
2. For each module, generate structured sequential steps:
   - Stages allowed: Learn, Practise, Build, Showcase, Reassess.
   - For every step, provide realistic estimated hours (between 2 and 20 hours).
   - Provide concrete, non-generic activities and a measurable outcome.
   - For resources: provide ONLY real, valid URLs (official docs, reputable free platforms like freeCodeCamp, MDN, PostgreSQL docs, etc.). Do not hallucinate fake links.
3. Distinguish gap types: "genuinely_missing", "partially_demonstrated", or "demonstrated_unpolished".
4. Do NOT promise that completing this guarantees a job.

Return valid JSON adhering to this structure:
{{
  "overall_strategy": "string",
  "modules": [
    {{
      "title": "string",
      "skills": ["string"],
      "priority": "High",
      "why_it_matters": "string",
      "steps": [
        {{
          "title": "string",
          "skill": "string",
          "stage": "Learn",
          "gap_type": "genuinely_missing",
          "why_it_matters": "string",
          "activities": ["string"],
          "resources": [
            {{
              "title": "string",
              "provider": "string",
              "url": "https://...",
              "resource_type": "documentation",
              "pricing": "free",
              "difficulty": "intermediate",
              "why_relevant": "string"
            }}
          ],
          "estimated_hours": 6.0,
          "measurable_outcome": "string"
        }}
      ]
    }}
  ]
}}
"""


def _parse_and_validate_gemini_roadmap(
    raw: dict,
    resume: ResumeProfile,
    job: JobProfile,
    preferences: RoadmapPreferences,
) -> RoadmapResult:
    """Parse Gemini JSON, enforce resource validation, and deterministically compute schedule."""
    raw_modules = raw.get("modules", [])
    if not raw_modules:
        raise ValueError("AI response did not contain any modules.")

    modules: list[RoadmapModule] = []
    step_counter = 1

    for mod_idx, rm in enumerate(raw_modules):
        mod_id = f"mod-{mod_idx + 1}"
        mod_title = rm.get("title", f"Module {mod_idx + 1}")
        skills = rm.get("skills", ["General"])
        priority = rm.get("priority", "High")
        if priority not in ("High", "Medium", "Low"):
            priority = "High"

        steps: list[RoadmapStep] = []
        for rs in rm.get("steps", []):
            step_id = f"step-{step_counter}"
            step_counter += 1

            skill = rs.get("skill", skills[0] if skills else "Technical Skill")
            stage_str = rs.get("stage", "Learn").capitalize()
            if stage_str not in ("Learn", "Practise", "Build", "Showcase", "Reassess"):
                stage_str = "Learn"
            stage = RoadmapStage(stage_str)

            # Validate resources: filter out hallucinated/broken links & attach vetted fallbacks
            valid_resources = []
            for res_data in rs.get("resources", []):
                sanitized = validate_and_sanitize_resource(res_data)
                if sanitized:
                    valid_resources.append(sanitized)

            # If no valid resource survived, pull from vetted catalogue
            if not valid_resources and stage == RoadmapStage.LEARN:
                valid_resources = get_vetted_resources_for_skill(
                    skill,
                    format_pref=preferences.resource_format,
                    budget_pref=preferences.budget,
                )

            # Safe effort bounds
            try:
                hrs = float(rs.get("estimated_hours", 6.0))
                hrs = max(min(hrs, 30.0), 1.0)
            except Exception:
                hrs = 6.0

            gap_type_str = rs.get("gap_type", "genuinely_missing")
            gap_type = GapType(gap_type_str) if gap_type_str in [g.value for g in GapType] else classify_skill_gap(skill, resume)

            dependencies = []
            if steps:
                dependencies.append(steps[-1].id)

            steps.append(
                RoadmapStep(
                    id=step_id,
                    module_id=mod_id,
                    title=rs.get("title", f"Study {skill}"),
                    skill=skill,
                    gap_type=gap_type,
                    stage=stage,
                    why_it_matters=rs.get("why_it_matters", f"Essential competency for {job.job_title}."),
                    activities=rs.get("activities", [f"Work through {skill} exercises."]),
                    resources=valid_resources,
                    estimated_hours=round(hrs, 1),
                    dependencies=dependencies,
                    measurable_outcome=rs.get("measurable_outcome", f"Working deliverable demonstrating {skill}."),
                )
            )

        module_hours = sum(s.estimated_hours for s in steps)
        modules.append(
            RoadmapModule(
                id=mod_id,
                title=mod_title,
                skills=skills,
                priority=priority,
                why_it_matters=rm.get("why_it_matters", f"Relevant to {job.job_title}."),
                estimated_hours=round(module_hours, 1),
                steps=steps,
            )
        )

    # Calculate schedule deterministically
    schedule = calculate_schedule(
        modules=modules,
        hours_per_week=preferences.hours_per_week,
        target_date_str=preferences.target_date,
    )

    total_steps = sum(len(m.steps) for m in modules)
    summary = RoadmapSummary(
        target_role=job.job_title or "Target Position",
        overall_strategy=raw.get("overall_strategy", f"Tailored development roadmap for {job.job_title}."),
        key_focus_areas=[m.title for m in modules][:4],
        total_modules=len(modules),
        total_steps=total_steps,
        total_hours=schedule.total_hours,
        estimated_weeks=schedule.total_weeks,
        completed_steps=0,
        progress_percentage=0.0,
    )

    now_iso = datetime.now(UTC).isoformat()
    return RoadmapResult(
        analysis_id="",
        preferences=preferences,
        summary=summary,
        modules=modules,
        schedule=schedule,
        source="ai",
        created_at=now_iso,
        updated_at=now_iso,
    )


def merge_roadmap_progress(
    new_roadmap: RoadmapResult,
    existing_modules_data: list[dict] | None,
) -> RoadmapResult:
    """
    Preserve completed status, completed_at timestamps, and user notes
    for steps that are demonstrably equivalent across roadmap regenerations.
    """
    if not existing_modules_data or not new_roadmap.modules:
        return new_roadmap

    # Collect existing steps with their completion metadata
    existing_steps: list[dict] = []
    for mod in existing_modules_data:
        for s in mod.get("steps", []):
            if isinstance(s, dict):
                existing_steps.append(s)

    if not existing_steps:
        return new_roadmap

    # Track which old steps have been matched to avoid duplicated preservation
    matched_old_indices: set[int] = set()

    for new_mod in new_roadmap.modules:
        for new_step in new_mod.steps:
            new_skill = (new_step.skill or "").strip().lower()
            new_stage = (
                new_step.stage.value.lower()
                if hasattr(new_step.stage, "value")
                else str(new_step.stage).lower()
            )
            new_title = (new_step.title or "").strip().lower()

            best_match_idx = None
            best_score = -1

            for idx, old_step in enumerate(existing_steps):
                if idx in matched_old_indices:
                    continue

                old_skill = str(old_step.get("skill", "")).strip().lower()
                old_stage = str(old_step.get("stage", "")).strip().lower()
                old_title = str(old_step.get("title", "")).strip().lower()

                # Primary equivalence requirement: same target skill and pedagogical stage
                if old_skill == new_skill and old_stage == new_stage:
                    score = 10
                    # Title alignment boosts confidence
                    if old_title == new_title:
                        score += 5
                    elif any(word in old_title for word in new_title.split() if len(word) > 3):
                        score += 2

                    if score > best_score:
                        best_score = score
                        best_match_idx = idx

            if best_match_idx is not None and best_score >= 10:
                old_match = existing_steps[best_match_idx]
                matched_old_indices.add(best_match_idx)

                old_status = old_match.get("status")
                if old_status == StepStatus.COMPLETED.value or old_match.get("completed") is True:
                    new_step.status = StepStatus.COMPLETED
                    new_step.completed_at = old_match.get("completed_at") or datetime.now(UTC).isoformat()
                elif old_status == StepStatus.IN_PROGRESS.value:
                    new_step.status = StepStatus.IN_PROGRESS
                    new_step.completed_at = None

                if old_match.get("user_notes"):
                    new_step.user_notes = old_match.get("user_notes")

    # Recalculate summary metrics from updated steps
    total_steps = sum(len(m.steps) for m in new_roadmap.modules)
    completed_steps = sum(
        1 for m in new_roadmap.modules
        for s in m.steps
        if s.status == StepStatus.COMPLETED
    )
    progress_pct = round((completed_steps / total_steps * 100), 1) if total_steps > 0 else 0.0

    new_roadmap.summary.total_steps = total_steps
    new_roadmap.summary.completed_steps = completed_steps
    new_roadmap.summary.progress_percentage = progress_pct

    return new_roadmap
