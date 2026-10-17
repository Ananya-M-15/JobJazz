from datetime import datetime, UTC
from typing import Dict, Any, List
import pymupdf as fitz


class RoadmapPdfBuilder:
    def __init__(self, roadmap_data: Dict[str, Any]):
        self.data = roadmap_data
        self.summary = roadmap_data.get("summary", {})
        self.schedule = roadmap_data.get("schedule", {})
        self.preferences = roadmap_data.get("preferences", {})
        self.modules = roadmap_data.get("modules", [])
        
        self.doc = fitz.open()
        self.page_width = 595.32
        self.page_height = 841.92
        self.margin_left = 45.0
        self.margin_right = 550.0
        self.content_width = self.margin_right - self.margin_left
        self.y = 50.0
        self.current_page = None
        self.page_count = 0

    def new_page(self):
        self.current_page = self.doc.new_page(width=self.page_width, height=self.page_height)
        self.page_count += 1
        self.y = 45.0

        # Running header on pages > 1
        if self.page_count > 1:
            target_role = self.summary.get("target_role", "Career Roadmap")
            self.current_page.insert_text(
                (self.margin_left, self.y),
                f"JobJazz — Learning Roadmap: {target_role}",
                fontsize=8,
                color=(0.4, 0.45, 0.55),
            )
            # Subtle divider
            self.current_page.draw_line(
                (self.margin_left, self.y + 4),
                (self.margin_right, self.y + 4),
                color=(0.85, 0.88, 0.92),
                width=0.5,
            )
            self.y += 24.0

    def check_page_break(self, needed_height: float):
        if self.y + needed_height > 780.0:
            self.new_page()

    def draw_header_banner(self):
        target_role = self.summary.get("target_role", "Target Role")
        now_str = datetime.now(UTC).strftime("%B %d, %Y")

        # Top decorative bar
        self.current_page.draw_rect(
            fitz.Rect(self.margin_left, self.y, self.margin_right, self.y + 4),
            color=None,
            fill=(0.23, 0.51, 0.96),  # #3B82F6 blue
        )
        self.y += 14.0

        # Title
        self.current_page.insert_text(
            (self.margin_left, self.y + 12),
            "JobJazz",
            fontsize=20,
            color=(0.04, 0.06, 0.15),  # deep navy
        )
        self.current_page.insert_text(
            (self.margin_left + 85, self.y + 12),
            "— Personalized Career Learning Roadmap",
            fontsize=13,
            color=(0.3, 0.35, 0.45),
        )
        self.y += 22.0

        # Subtitle / Target role
        self.current_page.insert_text(
            (self.margin_left, self.y + 10),
            f"Target Position: {target_role}",
            fontsize=12,
            color=(0.12, 0.16, 0.25),
        )
        self.current_page.insert_text(
            (self.margin_right - 130, self.y + 10),
            f"Generated: {now_str}",
            fontsize=9,
            color=(0.5, 0.55, 0.65),
        )
        self.y += 20.0

        self.current_page.draw_line(
            (self.margin_left, self.y),
            (self.margin_right, self.y),
            color=(0.85, 0.88, 0.92),
            width=0.75,
        )
        self.y += 12.0

    def draw_summary_card(self):
        self.check_page_break(110.0)
        box_y_start = self.y
        box_height = 95.0

        # Card background
        self.current_page.draw_rect(
            fitz.Rect(self.margin_left, box_y_start, self.margin_right, box_y_start + box_height),
            color=(0.85, 0.88, 0.95),
            fill=(0.96, 0.97, 1.0),
            width=0.75,
        )

        progress_pct = self.summary.get("progress_percentage", 0.0)
        completed_steps = self.summary.get("completed_steps", 0)
        total_steps = self.summary.get("total_steps", 0)
        total_hours = self.summary.get("total_hours", 0.0)
        est_weeks = self.summary.get("estimated_weeks", 0)
        hours_per_week = self.schedule.get("hours_per_week", 10)
        is_feasible = self.schedule.get("is_feasible", True)

        # Metrics columns
        col1_x = self.margin_left + 16
        col2_x = self.margin_left + 140
        col3_x = self.margin_left + 265
        col4_x = self.margin_left + 390

        # Metric 1: Progress
        self.current_page.insert_text((col1_x, box_y_start + 18), "PROGRESS", fontsize=8, color=(0.4, 0.45, 0.55))
        self.current_page.insert_text((col1_x, box_y_start + 36), f"{progress_pct}%", fontsize=16, color=(0.14, 0.45, 0.9))
        self.current_page.insert_text((col1_x, box_y_start + 48), f"{completed_steps} of {total_steps} steps", fontsize=8, color=(0.45, 0.5, 0.6))

        # Metric 2: Estimated Effort
        self.current_page.insert_text((col2_x, box_y_start + 18), "TOTAL EFFORT", fontsize=8, color=(0.4, 0.45, 0.55))
        self.current_page.insert_text((col2_x, box_y_start + 36), f"{total_hours} hrs", fontsize=16, color=(0.1, 0.15, 0.25))
        self.current_page.insert_text((col2_x, box_y_start + 48), f"{len(self.modules)} modules", fontsize=8, color=(0.45, 0.5, 0.6))

        # Metric 3: Pace & Timeline
        self.current_page.insert_text((col3_x, box_y_start + 18), "TIMELINE PACE", fontsize=8, color=(0.4, 0.45, 0.55))
        self.current_page.insert_text((col3_x, box_y_start + 36), f"{est_weeks} weeks", fontsize=16, color=(0.1, 0.15, 0.25))
        self.current_page.insert_text((col3_x, box_y_start + 48), f"at {hours_per_week} hrs/wk", fontsize=8, color=(0.45, 0.5, 0.6))

        # Metric 4: Feasibility
        feas_label = "Feasible" if is_feasible else "Intensive"
        feas_color = (0.08, 0.55, 0.3) if is_feasible else (0.85, 0.45, 0.05)
        self.current_page.insert_text((col4_x, box_y_start + 18), "FEASIBILITY", fontsize=8, color=(0.4, 0.45, 0.55))
        self.current_page.insert_text((col4_x, box_y_start + 36), feas_label, fontsize=16, color=feas_color)
        proj_date = self.schedule.get("projected_completion_date", "TBD")
        self.current_page.insert_text((col4_x, box_y_start + 48), f"Target: {proj_date}", fontsize=8, color=(0.45, 0.5, 0.6))

        # Strategy text across bottom of card
        strategy = self.summary.get("overall_strategy", "")
        if strategy:
            clean_strat = strategy[:170] + ("..." if len(strategy) > 170 else "")
            self.current_page.insert_text((col1_x, box_y_start + 72), "Strategy:", fontsize=8, color=(0.2, 0.25, 0.35))
            self.current_page.insert_text((col1_x + 45, box_y_start + 72), clean_strat, fontsize=8, color=(0.35, 0.4, 0.5))

        self.y = box_y_start + box_height + 15.0

    def draw_modules(self):
        for mod_idx, mod in enumerate(self.modules, 1):
            self.check_page_break(65.0)

            title = mod.get("title", f"Module {mod_idx}")
            priority = mod.get("priority", "High")
            skills = mod.get("skills", [])
            steps = mod.get("steps", [])

            # Priority color
            prio_color = (0.75, 0.15, 0.15) if priority == "High" else (0.15, 0.45, 0.75)

            # Module Title Bar
            self.current_page.draw_rect(
                fitz.Rect(self.margin_left, self.y, self.margin_right, self.y + 22),
                color=(0.88, 0.9, 0.94),
                fill=(0.94, 0.95, 0.98),
                width=0.5,
            )
            self.current_page.insert_text(
                (self.margin_left + 8, self.y + 15),
                f"Module {mod_idx}: {title}",
                fontsize=11,
                color=(0.08, 0.1, 0.2),
            )
            self.current_page.insert_text(
                (self.margin_right - 65, self.y + 15),
                f"[{priority} Priority]",
                fontsize=9,
                color=prio_color,
            )
            self.y += 28.0

            # Module skills summary if available
            if skills:
                skills_str = ", ".join(skills[:6])
                self.current_page.insert_text(
                    (self.margin_left + 6, self.y),
                    f"Core Competencies: {skills_str}",
                    fontsize=8.5,
                    color=(0.4, 0.45, 0.55),
                )
                self.y += 12.0

            # Steps
            for step_idx, step in enumerate(steps, 1):
                self.check_page_break(50.0)

                step_title = step.get("title", f"Step {step_idx}")
                status = step.get("status", "not_started")
                stage = step.get("stage", "Learn")
                hours = step.get("estimated_hours", 0.0)
                outcome = step.get("measurable_outcome", "")
                resources = step.get("resources", [])

                # Status checkbox
                is_done = status == "completed"
                check_symbol = "[X]" if is_done else "[ ]"
                check_color = (0.1, 0.55, 0.25) if is_done else (0.5, 0.55, 0.65)

                self.current_page.insert_text(
                    (self.margin_left + 8, self.y + 9),
                    check_symbol,
                    fontsize=9,
                    color=check_color,
                )
                self.current_page.insert_text(
                    (self.margin_left + 26, self.y + 9),
                    f"{step_title}",
                    fontsize=9.5,
                    color=(0.1, 0.12, 0.2),
                )
                self.current_page.insert_text(
                    (self.margin_right - 100, self.y + 9),
                    f"{stage} • {hours} hrs",
                    fontsize=8.5,
                    color=(0.4, 0.45, 0.55),
                )
                self.y += 15.0

                # Deliverable / Measurable outcome
                if outcome:
                    clean_outcome = outcome[:120] + ("..." if len(outcome) > 120 else "")
                    self.current_page.insert_text(
                        (self.margin_left + 26, self.y + 8),
                        f"Deliverable: {clean_outcome}",
                        fontsize=8,
                        color=(0.35, 0.4, 0.5),
                    )
                    self.y += 13.0

                # Resources links (formatted cleanly without overflow)
                if resources:
                    res_items = []
                    for r in resources[:2]:
                        r_provider = r.get("provider", "Resource")
                        r_title = r.get("title", "")
                        r_url = r.get("url", "")
                        # Shorten URL display
                        short_url = r_url.split("?")[0][:45]
                        res_items.append(f"{r_provider}: {r_title[:30]} ({short_url})")

                    for res_str in res_items:
                        self.check_page_break(14.0)
                        self.current_page.insert_text(
                            (self.margin_left + 26, self.y + 8),
                            f"Resource: {res_str}",
                            fontsize=7.5,
                            color=(0.2, 0.4, 0.7),
                        )
                        self.y += 12.0

                self.y += 4.0

            self.y += 10.0

    def draw_schedule_summary(self):
        weekly = self.schedule.get("weekly_schedule", [])
        if not weekly:
            return

        self.check_page_break(70.0)

        # Schedule section heading
        self.current_page.draw_rect(
            fitz.Rect(self.margin_left, self.y, self.margin_right, self.y + 18),
            color=(0.88, 0.9, 0.94),
            fill=(0.94, 0.95, 0.98),
            width=0.5,
        )
        self.current_page.insert_text(
            (self.margin_left + 8, self.y + 13),
            "Timeline & Weekly Milestone Schedule",
            fontsize=10,
            color=(0.08, 0.1, 0.2),
        )
        self.y += 24.0

        for w in weekly:
            self.check_page_break(24.0)
            week_num = w.get("week_number", 1)
            alloc_hours = w.get("allocated_hours", 0.0)
            start_d = w.get("start_date", "")
            end_d = w.get("end_date", "")
            milestone = w.get("milestone", "")
            steps = w.get("step_titles", [])

            self.current_page.insert_text(
                (self.margin_left + 8, self.y + 8),
                f"Week {week_num} ({start_d} – {end_d}):",
                fontsize=8.5,
                color=(0.15, 0.2, 0.3),
            )
            self.current_page.insert_text(
                (self.margin_left + 175, self.y + 8),
                f"{alloc_hours} hrs",
                fontsize=8.5,
                color=(0.35, 0.4, 0.5),
            )

            desc = milestone if milestone else (", ".join(steps[:2]) if steps else "Skills advancement")
            clean_desc = desc[:70] + ("..." if len(desc) > 70 else "")
            self.current_page.insert_text(
                (self.margin_left + 230, self.y + 8),
                clean_desc,
                fontsize=8,
                color=(0.25, 0.3, 0.4),
            )
            self.y += 14.0

        self.y += 10.0

    def add_page_numbers_and_footers(self):
        total = len(self.doc)
        for idx in range(total):
            page = self.doc[idx]
            # Bottom divider line
            page.draw_line(
                (self.margin_left, 810),
                (self.margin_right, 810),
                color=(0.85, 0.88, 0.92),
                width=0.5,
            )
            # Left footer
            page.insert_text(
                (self.margin_left, 822),
                "JobJazz — Your career, in tune.",
                fontsize=7.5,
                color=(0.5, 0.55, 0.65),
            )
            # Right footer
            page.insert_text(
                (self.margin_right - 65, 822),
                f"Page {idx + 1} of {total}",
                fontsize=7.5,
                color=(0.5, 0.55, 0.65),
            )

    def build_pdf(self) -> bytes:
        self.new_page()
        self.draw_header_banner()
        self.draw_summary_card()
        self.draw_modules()
        self.draw_schedule_summary()
        self.add_page_numbers_and_footers()
        
        pdf_bytes = self.doc.tobytes(garbage=3, deflate=True)
        self.doc.close()
        return pdf_bytes


def generate_roadmap_pdf(roadmap_data: Dict[str, Any]) -> bytes:
    builder = RoadmapPdfBuilder(roadmap_data)
    return builder.build_pdf()
