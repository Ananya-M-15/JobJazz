import { CheckCircle2, AlertCircle, Sparkles, Target } from "lucide-react"

export default function GapToAction() {
    const gapCategories = [
        {
            title: "Strengths & Matches",
            badge: "4 Skills Aligned",
            badgeClass: "bg-emerald-50 text-emerald-700 border-emerald-200",
            icon: CheckCircle2,
            iconClass: "text-emerald-600 bg-emerald-50 border-emerald-200",
            desc: "Verified skills and qualifications you already possess that directly satisfy the role.",
            skills: ["Python", "PostgreSQL", "FastAPI", "B.S. in CS"],
        },
        {
            title: "Critical Gaps",
            badge: "Top Priority",
            badgeClass: "bg-rose-50 text-rose-700 border-rose-200",
            icon: AlertCircle,
            iconClass: "text-rose-600 bg-rose-50 border-rose-200",
            desc: "Non-negotiable requirements missing from your profile that will trigger interviewer hesitation.",
            skills: ["Docker Containerization"],
        },
        {
            title: "Preferred & Bonus",
            badge: "Secondary Focus",
            badgeClass: "bg-amber-50 text-amber-700 border-amber-200",
            icon: Sparkles,
            iconClass: "text-amber-600 bg-amber-50 border-amber-200",
            desc: "Valuable supplementary criteria that set you apart once critical requirements are met.",
            skills: ["AWS Cloud Deployment"],
        },
    ]

    const actionMilestones = [
        {
            step: "01",
            title: "Master Core Containerization",
            duration: "2 Weeks",
            priority: "Critical Priority",
            priorityClass: "bg-rose-50 text-rose-700 border-rose-200",
            desc: "Focus strictly on Docker fundamentals, image building, and multi-container configurations demanded by the role.",
            recommended: "Docker for Backend Engineering",
        },
        {
            step: "02",
            title: "Apply to Portfolio Repositories",
            duration: "1 Week",
            priority: "Portfolio Update",
            priorityClass: "bg-blue-50 text-[var(--jj-primary-blue)] border-blue-200",
            desc: "Containerize existing backend projects and document Docker Compose workflows clearly in your resume bullets.",
            recommended: "Tangible GitHub Proof",
        },
        {
            step: "03",
            title: "Re-Evaluate Match Alignment",
            duration: "Instant",
            priority: "Projected Outcome",
            priorityClass: "bg-emerald-50 text-emerald-700 border-emerald-200",
            desc: "Re-analyze your updated resume in JobJazz to verify your elevated match percentage before applying.",
            recommended: "+15% Projected Alignment",
        },
    ]

    return (
        <section className="relative z-10 w-full py-16 sm:py-20 lg:py-24 bg-[var(--jj-background)] border-y border-[var(--jj-border)] overflow-hidden" id="gap-to-action">
            <div className="mx-auto max-w-7xl px-6 lg:px-8 relative z-10">
                
                {/* Section Header */}
                <div className="mx-auto max-w-3xl text-center mb-14 sm:mb-16">
                    <div className="inline-flex items-center gap-2 px-3.5 py-1 rounded-full border border-[var(--jj-border)] bg-white text-xs font-semibold text-[var(--jj-primary-blue)] tracking-wide uppercase mb-4 shadow-sm">
                        <Target className="w-3.5 h-3.5" />
                        Gaps to Action Plan
                    </div>
                    <h2 className="text-3xl font-bold tracking-tight text-[var(--jj-navy)] sm:text-4xl leading-[1.2]">
                        Don't stop at the score. <br className="hidden sm:inline" />
                        <span className="text-[var(--jj-primary-blue)]">Turn gaps into your career roadmap.</span>
                    </h2>
                    <p className="mt-4 text-base sm:text-lg text-slate-600 max-w-2xl mx-auto leading-relaxed">
                        A match score only shows where you stand today. JobJazz classifies missing requirements by priority and generates a structured, step-by-step roadmap to bridge them.
                    </p>
                </div>

                {/* Unified Two-Card Layout */}
                <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 lg:gap-8 items-stretch max-w-7xl mx-auto">
                    
                    {/* Left Column: Gap Classification (Merged from GapMap) */}
                    <div className="lg:col-span-6 bg-white rounded-3xl border border-[var(--jj-border)] shadow-[0_4px_25px_-5px_rgba(15,23,42,0.05)] p-6 sm:p-8 flex flex-col justify-between">
                        <div>
                            <div className="flex items-center justify-between pb-5 border-b border-slate-100 mb-6">
                                <div>
                                    <span className="text-[11px] font-bold text-slate-400 uppercase tracking-widest block mb-0.5">Step 1: Gap Breakdown</span>
                                    <h3 className="text-lg font-bold text-[var(--jj-navy)]">Weighted Requirement Analysis</h3>
                                </div>
                                <span className="text-xs font-bold text-[var(--jj-primary-blue)] bg-blue-50 px-2.5 py-1 rounded-lg border border-blue-100">
                                    3 Tiers
                                </span>
                            </div>

                            <div className="space-y-4">
                                {gapCategories.map((cat, idx) => (
                                    <div
                                        key={idx}
                                        className="rounded-2xl border border-slate-100 bg-slate-50/60 p-4 sm:p-5 hover:bg-slate-50 transition-colors"
                                    >
                                        <div className="flex items-center justify-between gap-3 mb-2">
                                            <div className="flex items-center gap-2.5">
                                                <div className={`w-7 h-7 rounded-lg border flex items-center justify-center flex-shrink-0 ${cat.iconClass}`}>
                                                    <cat.icon className="w-4 h-4" />
                                                </div>
                                                <h4 className="text-sm font-bold text-[var(--jj-navy)]">{cat.title}</h4>
                                            </div>
                                            <span className={`text-[11px] font-semibold px-2 py-0.5 rounded-md border ${cat.badgeClass}`}>
                                                {cat.badge}
                                            </span>
                                        </div>

                                        <p className="text-xs text-slate-500 font-light leading-relaxed mb-3">
                                            {cat.desc}
                                        </p>

                                        <div className="flex flex-wrap gap-1.5">
                                            {cat.skills.map((skill, sIdx) => (
                                                <span
                                                    key={sIdx}
                                                    className="inline-flex items-center gap-1 text-[11px] font-medium px-2 py-0.5 rounded bg-white text-slate-700 border border-slate-200/80 shadow-2xs"
                                                >
                                                    <span className="w-1 h-1 rounded-full bg-slate-400"></span>
                                                    {skill}
                                                </span>
                                            ))}
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>

                        <div className="mt-6 pt-4 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500">
                            <span>Every gap is categorized before recommendation</span>
                            <span className="font-semibold text-[var(--jj-primary-blue)]">Objective Assessment</span>
                        </div>
                    </div>

                    {/* Right Column: Prioritized Action Roadmap (Merged from GapToAction) */}
                    <div className="lg:col-span-6 bg-white rounded-3xl border border-[var(--jj-border)] shadow-[0_4px_25px_-5px_rgba(15,23,42,0.05)] p-6 sm:p-8 flex flex-col justify-between">
                        <div>
                            <div className="flex items-center justify-between pb-5 border-b border-slate-100 mb-6">
                                <div>
                                    <span className="text-[11px] font-bold text-slate-400 uppercase tracking-widest block mb-0.5">Step 2: Action Roadmap</span>
                                    <h3 className="text-lg font-bold text-[var(--jj-navy)]">Prioritized Next Steps</h3>
                                </div>
                                <div className="text-right">
                                    <span className="text-[10px] uppercase font-bold text-slate-400 block tracking-wider">Target Gap</span>
                                    <span className="inline-block px-2 py-0.5 bg-rose-50 text-rose-700 rounded text-xs font-bold border border-rose-100">
                                        Docker
                                    </span>
                                </div>
                            </div>

                            <div className="space-y-4 relative">
                                {actionMilestones.map((milestone, idx) => (
                                    <div
                                        key={idx}
                                        className="rounded-2xl border border-slate-100 bg-slate-50/60 p-4 sm:p-5 hover:bg-slate-50 transition-colors relative"
                                    >
                                        <div className="flex items-start justify-between gap-3 mb-1.5">
                                            <div className="flex items-center gap-2.5">
                                                <span className="w-6 h-6 rounded-lg bg-[var(--jj-navy)] text-white text-xs font-mono font-bold flex items-center justify-center flex-shrink-0">
                                                    {milestone.step}
                                                </span>
                                                <h4 className="text-sm font-bold text-[var(--jj-navy)]">
                                                    {milestone.title}
                                                </h4>
                                            </div>
                                            <div className="flex items-center gap-2">
                                                <span className="text-[10px] font-mono font-bold text-slate-400 uppercase">
                                                    {milestone.duration}
                                                </span>
                                                <span className={`text-[10px] font-bold px-2 py-0.5 rounded border ${milestone.priorityClass}`}>
                                                    {milestone.priority}
                                                </span>
                                            </div>
                                        </div>

                                        <p className="text-xs text-slate-500 font-light leading-relaxed mb-3 pl-8.5">
                                            {milestone.desc}
                                        </p>

                                        <div className="pl-8.5">
                                            <div className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md text-[11px] font-medium bg-white text-slate-700 border border-slate-200/80 shadow-2xs">
                                                <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" />
                                                <span>{milestone.recommended}</span>
                                            </div>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>

                        <div className="mt-6 pt-4 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500">
                            <span>Tailored specifically to your resume & target role</span>
                            <span className="font-semibold text-emerald-600">Actionable Guidance</span>
                        </div>
                    </div>

                </div>

            </div>
        </section>
    )
}
