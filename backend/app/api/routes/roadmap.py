from datetime import datetime, UTC
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.database.models import Analysis, Roadmap, SkillGap, Recommendation
from app.models.resume_profile import ResumeProfile
from app.models.job_profile import JobProfile
from app.models.match_result import MatchResult
from app.models.skill_gap import SkillGapResult
from app.models.recommendation import RecommendationResult, SkillRecommendation
from app.schemas.roadmap import (
    RoadmapGenerateRequest,
    RoadmapResult,
    StepUpdateRequest,
    StepStatus,
)
from app.services.roadmap_generator import (
    generate_personalized_roadmap,
    merge_roadmap_progress,
)
from app.services.roadmap_pdf_service import generate_roadmap_pdf

router = APIRouter(
    prefix="/roadmap",
    tags=["Roadmap"],
)


@router.post("/generate", response_model=RoadmapResult)
async def generate_roadmap_endpoint(
    request: RoadmapGenerateRequest,
    db: Session = Depends(get_db),
):
    analysis = db.query(Analysis).filter(
        Analysis.id == request.analysis_id
    ).first()

    if not analysis:
        raise HTTPException(
            status_code=404,
            detail="Analysis not found.",
        )

    # Load authoritative data from stored analysis
    resume = analysis.resume
    job_description = analysis.job_description

    if not resume or not job_description:
        raise HTTPException(
            status_code=400,
            detail="Analysis record is missing resume or job description association.",
        )

    # Reconstruct authoritative Pydantic profiles
    resume_profile = ResumeProfile.model_validate(resume.profile_data)
    job_profile = JobProfile.model_validate(job_description.profile_data)
    match_result = MatchResult.model_validate(analysis.match_data)

    db_skill_gap = db.query(SkillGap).filter(
        SkillGap.analysis_id == analysis.id
    ).first()

    if db_skill_gap:
        skill_gap_result = SkillGapResult(
            strengths=db_skill_gap.strengths,
            critical_gaps=db_skill_gap.critical_gaps,
            preferred_gaps=db_skill_gap.preferred_gaps,
            experience_gap=db_skill_gap.experience_gap,
            education_gap=db_skill_gap.education_gap,
        )
    else:
        # Fallback to match_result gaps
        skill_gap_result = SkillGapResult(
            strengths=match_result.matched_required_skills + match_result.matched_preferred_skills,
            critical_gaps=match_result.missing_required_skills,
            preferred_gaps=match_result.missing_preferred_skills,
            experience_gap=not match_result.experience_match,
            education_gap=not match_result.education_match,
        )

    db_recs = db.query(Recommendation).filter(
        Recommendation.analysis_id == analysis.id
    ).all()

    recs_result = None
    if db_recs:
        recs_result = RecommendationResult(
            recommendations=[
                SkillRecommendation(
                    skill=r.skill,
                    priority=r.priority,
                    reason=r.reason,
                    action=r.action,
                )
                for r in db_recs
            ]
        )

    # Generate personalized roadmap
    roadmap_result = generate_personalized_roadmap(
        resume=resume_profile,
        job=job_profile,
        match_result=match_result,
        skill_gap=skill_gap_result,
        recommendations=recs_result,
        preferences=request.preferences,
    )
    roadmap_result.analysis_id = str(analysis.id)

    # Check existing roadmap
    db_roadmap = db.query(Roadmap).filter(
        Roadmap.analysis_id == analysis.id
    ).first()

    now_utc = datetime.now(UTC)

    if db_roadmap:
        # Preserve completed status, timestamps, and user notes for demonstrably equivalent steps
        if db_roadmap.modules:
            roadmap_result = merge_roadmap_progress(roadmap_result, db_roadmap.modules)

        db_roadmap.preferences = roadmap_result.preferences.model_dump()
        db_roadmap.summary = roadmap_result.summary.model_dump()
        db_roadmap.modules = [m.model_dump() for m in roadmap_result.modules]
        db_roadmap.schedule = roadmap_result.schedule.model_dump()
        db_roadmap.source = roadmap_result.source
        db_roadmap.updated_at = now_utc
    else:
        db_roadmap = Roadmap(
            analysis_id=analysis.id,
            preferences=roadmap_result.preferences.model_dump(),
            summary=roadmap_result.summary.model_dump(),
            modules=[m.model_dump() for m in roadmap_result.modules],
            schedule=roadmap_result.schedule.model_dump(),
            source=roadmap_result.source,
            created_at=now_utc,
            updated_at=now_utc,
        )
        db.add(db_roadmap)

    db.commit()
    db.refresh(db_roadmap)

    roadmap_result.id = str(db_roadmap.id)
    roadmap_result.created_at = db_roadmap.created_at.isoformat()
    roadmap_result.updated_at = db_roadmap.updated_at.isoformat()

    return roadmap_result


@router.get("/{analysis_id}", response_model=RoadmapResult)
async def get_roadmap_endpoint(
    analysis_id: str,
    db: Session = Depends(get_db),
):
    db_roadmap = db.query(Roadmap).filter(
        Roadmap.analysis_id == analysis_id
    ).first()

    if not db_roadmap:
        raise HTTPException(
            status_code=404,
            detail="Roadmap not found for this analysis.",
        )

    return RoadmapResult(
        id=str(db_roadmap.id),
        analysis_id=str(db_roadmap.analysis_id),
        preferences=db_roadmap.preferences,
        summary=db_roadmap.summary,
        modules=db_roadmap.modules,
        schedule=db_roadmap.schedule,
        source=db_roadmap.source,
        created_at=db_roadmap.created_at.isoformat(),
        updated_at=db_roadmap.updated_at.isoformat(),
    )


@router.patch("/{analysis_id}/step/{step_id}", response_model=RoadmapResult)
async def update_step_status_endpoint(
    analysis_id: str,
    step_id: str,
    update_data: StepUpdateRequest,
    db: Session = Depends(get_db),
):
    db_roadmap = db.query(Roadmap).filter(
        Roadmap.analysis_id == analysis_id
    ).first()

    if not db_roadmap:
        raise HTTPException(
            status_code=404,
            detail="Roadmap not found.",
        )

    import copy
    from sqlalchemy.orm.attributes import flag_modified

    modules_data = copy.deepcopy(db_roadmap.modules)
    step_found = False
    now_iso = datetime.now(UTC).isoformat()

    for module in modules_data:
        for step in module.get("steps", []):
            if step.get("id") == step_id:
                step["status"] = update_data.status.value
                if update_data.status == StepStatus.COMPLETED:
                    step["completed_at"] = now_iso
                else:
                    step["completed_at"] = None

                if update_data.user_notes is not None:
                    step["user_notes"] = update_data.user_notes
                step_found = True
                break
        if step_found:
            break

    if not step_found:
        raise HTTPException(
            status_code=404,
            detail=f"Step '{step_id}' not found in roadmap.",
        )

    # Recalculate summary metrics
    total_steps = sum(len(m.get("steps", [])) for m in modules_data)
    completed_steps = sum(
        1 for m in modules_data
        for s in m.get("steps", [])
        if s.get("status") == StepStatus.COMPLETED.value
    )
    progress_pct = round((completed_steps / total_steps * 100), 1) if total_steps > 0 else 0.0

    summary_data = copy.deepcopy(db_roadmap.summary)
    summary_data["completed_steps"] = completed_steps
    summary_data["progress_percentage"] = progress_pct

    db_roadmap.modules = modules_data
    db_roadmap.summary = summary_data
    db_roadmap.updated_at = datetime.now(UTC)

    flag_modified(db_roadmap, "modules")
    flag_modified(db_roadmap, "summary")

    db.commit()
    db.refresh(db_roadmap)

    return RoadmapResult(
        id=str(db_roadmap.id),
        analysis_id=str(db_roadmap.analysis_id),
        preferences=db_roadmap.preferences,
        summary=db_roadmap.summary,
        modules=db_roadmap.modules,
        schedule=db_roadmap.schedule,
        source=db_roadmap.source,
        created_at=db_roadmap.created_at.isoformat(),
        updated_at=db_roadmap.updated_at.isoformat(),
    )


@router.get("/{analysis_id}/progress")
async def get_roadmap_progress_endpoint(
    analysis_id: str,
    db: Session = Depends(get_db),
):
    db_roadmap = db.query(Roadmap).filter(
        Roadmap.analysis_id == analysis_id
    ).first()

    if not db_roadmap:
        raise HTTPException(
            status_code=404,
            detail="Roadmap not found.",
        )

    modules_data = db_roadmap.modules or []
    completed_skills = set()
    total_steps = 0
    completed_steps = 0

    for module in modules_data:
        for step in module.get("steps", []):
            total_steps += 1
            if step.get("status") == StepStatus.COMPLETED.value:
                completed_steps += 1
                completed_skills.add(step.get("skill"))

    progress_pct = round((completed_steps / total_steps * 100), 1) if total_steps > 0 else 0.0

    return {
        "analysis_id": str(db_roadmap.analysis_id),
        "total_steps": total_steps,
        "completed_steps": completed_steps,
        "progress_percentage": progress_pct,
        "completed_skills": list(completed_skills),
    }


@router.get("/{analysis_id}/pdf")
async def download_roadmap_pdf_endpoint(
    analysis_id: str,
    db: Session = Depends(get_db),
):
    db_roadmap = db.query(Roadmap).filter(
        Roadmap.analysis_id == analysis_id
    ).first()

    if not db_roadmap:
        raise HTTPException(
            status_code=404,
            detail="Roadmap not found for this analysis.",
        )

    roadmap_dict = {
        "analysis_id": str(db_roadmap.analysis_id),
        "preferences": db_roadmap.preferences or {},
        "summary": db_roadmap.summary or {},
        "modules": db_roadmap.modules or [],
        "schedule": db_roadmap.schedule or {},
    }

    try:
        pdf_bytes = generate_roadmap_pdf(roadmap_dict)
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Unable to generate roadmap PDF: {str(exc)}",
        )

    target_role = (db_roadmap.summary or {}).get("target_role", "Roadmap")
    safe_role = "".join(c for c in target_role if c.isalnum() or c in ("-", "_")).strip() or "Career"
    filename = f"JobJazz_{safe_role}_Roadmap.pdf"

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"',
            "Cache-Control": "no-cache",
        },
    )
