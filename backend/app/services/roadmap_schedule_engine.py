"""
Deterministic schedule and timetable engine for JobJazz personalized roadmaps.
Calculates weekly allocations, dependency ordering, feasibility against target dates,
and categorized effort distribution (learning vs practising vs building).
"""
from datetime import date, datetime, timedelta, UTC
from app.schemas.roadmap import (
    RoadmapStep,
    RoadmapModule,
    RoadmapSchedule,
    WeeklyScheduleAllocation,
    RoadmapStage,
)


def calculate_schedule(
    modules: list[RoadmapModule],
    hours_per_week: int,
    target_date_str: str | None = None,
    start_date: date | None = None,
) -> RoadmapSchedule:
    """
    Calculate an ordered, capacity-constrained weekly schedule based on step effort,
    dependencies, and student availability.
    """
    if hours_per_week <= 0:
        hours_per_week = 10

    if start_date is None:
        start_date = date.today()

    # Collect all steps in topological dependency order
    all_steps: list[RoadmapStep] = []
    for module in modules:
        all_steps.extend(module.steps)

    # Sort steps respecting dependencies
    ordered_steps = _order_steps_by_dependencies(all_steps)

    total_hours = sum(step.estimated_hours for step in ordered_steps)
    learning_hours = sum(
        step.estimated_hours for step in ordered_steps
        if step.stage == RoadmapStage.LEARN
    )
    practising_hours = sum(
        step.estimated_hours for step in ordered_steps
        if step.stage == RoadmapStage.PRACTISE
    )
    building_hours = sum(
        step.estimated_hours for step in ordered_steps
        if step.stage in (RoadmapStage.BUILD, RoadmapStage.SHOWCASE, RoadmapStage.REASSESS)
    )

    weekly_allocations: list[WeeklyScheduleAllocation] = []

    current_week_num = 1
    current_week_start = start_date
    current_week_end = current_week_start + timedelta(days=6)
    
    current_allocated = 0.0
    current_learn = 0.0
    current_practise = 0.0
    current_build = 0.0
    current_step_ids = []
    current_step_titles = []
    current_milestone = None

    for step in ordered_steps:
        step_hours_remaining = step.estimated_hours

        while step_hours_remaining > 0:
            available_this_week = hours_per_week - current_allocated

            if available_this_week <= 0:
                # Close current week and advance to next
                weekly_allocations.append(
                    WeeklyScheduleAllocation(
                        week_number=current_week_num,
                        start_date=current_week_start.isoformat(),
                        end_date=current_week_end.isoformat(),
                        allocated_hours=round(current_allocated, 1),
                        learning_hours=round(current_learn, 1),
                        practising_hours=round(current_practise, 1),
                        building_hours=round(current_build, 1),
                        step_ids=list(current_step_ids),
                        step_titles=list(current_step_titles),
                        milestone=current_milestone,
                    )
                )
                current_week_num += 1
                current_week_start = current_week_end + timedelta(days=1)
                current_week_end = current_week_start + timedelta(days=6)
                current_allocated = 0.0
                current_learn = 0.0
                current_practise = 0.0
                current_build = 0.0
                current_step_ids = []
                current_step_titles = []
                current_milestone = None
                available_this_week = float(hours_per_week)

            chunk = min(step_hours_remaining, available_this_week)
            current_allocated += chunk
            step_hours_remaining -= chunk

            if step.id not in current_step_ids:
                current_step_ids.append(step.id)
                current_step_titles.append(f"{step.stage.value}: {step.title}")

            # Categorize hours
            if step.stage == RoadmapStage.LEARN:
                current_learn += chunk
            elif step.stage == RoadmapStage.PRACTISE:
                current_practise += chunk
            else:
                current_build += chunk

            if step.stage in (RoadmapStage.BUILD, RoadmapStage.SHOWCASE) and not current_milestone:
                current_milestone = f"Milestone: {step.title}"

    # Flush final week
    if current_allocated > 0 or not weekly_allocations:
        weekly_allocations.append(
            WeeklyScheduleAllocation(
                week_number=current_week_num,
                start_date=current_week_start.isoformat(),
                end_date=current_week_end.isoformat(),
                allocated_hours=round(current_allocated, 1),
                learning_hours=round(current_learn, 1),
                practising_hours=round(current_practise, 1),
                building_hours=round(current_build, 1),
                step_ids=list(current_step_ids),
                step_titles=list(current_step_titles),
                milestone=current_milestone or (ordered_steps[-1].title if ordered_steps else "Roadmap Complete"),
            )
        )

    total_weeks = len(weekly_allocations)
    projected_end_date = weekly_allocations[-1].end_date if weekly_allocations else start_date.isoformat()

    # Target Date Feasibility Analysis
    is_feasible = True
    feasibility_notes = ""
    assumptions = [
        f"Based on consistent study of {hours_per_week} hours per week.",
        "Step durations are reasonable realistic estimates and vary with prior background.",
        "Dependencies are strictly sequenced to avoid premature project development before fundamental learning.",
    ]

    if target_date_str:
        try:
            target_dt = datetime.fromisoformat(target_date_str.split("T")[0]).date()
            projected_dt = date.fromisoformat(projected_end_date)
            
            days_available = (target_dt - start_date).days
            if days_available <= 0:
                is_feasible = False
                feasibility_notes = (
                    f"Selected target date ({target_date_str}) is in the past or today. "
                    f"Estimated completion date is {projected_end_date} ({total_weeks} weeks at {hours_per_week} hrs/week)."
                )
            elif target_dt < projected_dt:
                is_feasible = False
                available_weeks = max(round(days_available / 7, 1), 0.5)
                needed_hours_per_week = round(total_hours / available_weeks, 1) if available_weeks > 0 else 0
                feasibility_notes = (
                    f"Target date of {target_date_str} allows ~{available_weeks} weeks. "
                    f"At your current pace of {hours_per_week} hrs/week, this roadmap requires {total_weeks} weeks (finishing ~{projected_end_date}). "
                    f"To finish by {target_date_str}, you would need approximately {needed_hours_per_week} hours/week."
                )
            else:
                is_feasible = True
                slack_days = (target_dt - projected_dt).days
                feasibility_notes = (
                    f"Target date {target_date_str} is feasible. "
                    f"Projected completion is ~{projected_end_date}, leaving a healthy ~{slack_days} days of buffer."
                )
        except Exception:
            is_feasible = True
            feasibility_notes = "Target date format was not standard ISO date (YYYY-MM-DD); schedule projected normally."

    return RoadmapSchedule(
        total_hours=round(total_hours, 1),
        hours_per_week=float(hours_per_week),
        total_weeks=total_weeks,
        learning_hours=round(learning_hours, 1),
        practising_hours=round(practising_hours, 1),
        building_hours=round(building_hours, 1),
        start_date=start_date.isoformat(),
        projected_completion_date=projected_end_date,
        target_date=target_date_str,
        is_feasible=is_feasible,
        feasibility_notes=feasibility_notes,
        weekly_schedule=weekly_allocations,
        assumptions=assumptions,
    )


def _order_steps_by_dependencies(steps: list[RoadmapStep]) -> list[RoadmapStep]:
    """Topological ordering of steps respecting dependencies."""
    step_dict = {s.id: s for s in steps}
    visited = set()
    ordered = []

    def visit(step_id: str):
        if step_id in visited:
            return
        step = step_dict.get(step_id)
        if not step:
            return
        for dep in step.dependencies:
            if dep in step_dict:
                visit(dep)
        visited.add(step_id)
        ordered.append(step)

    for step in steps:
        visit(step.id)

    return ordered
