import { useState } from "react"
import { CheckCircle2, AlertCircle, Minus, Sparkles, ShieldCheck } from "lucide-react"

export default function MatchingMatrix() {
    const [activeFilter, setActiveFilter] = useState("all")

    const requirements = [
        {
            id: 1,
            label: "Python & FastAPI",
            category: "Core Skill",
            status: "matched",
            statusText: "Direct Match",
            evidence: "5+ years backend API development in resume",
            type: "matched",
        },
        {
            id: 2,
            label: "PostgreSQL & Database Design",
            category: "Core Skill",
            status: "matched",
            statusText: "Direct Match",
            evidence: "Schema optimization and complex queries verified",
            type: "matched",
        },
        {
            id: 3,
            label: "Machine Learning Pipelines",
            category: "Preferred",
            status: "matched",
            statusText: "Direct Match",
            evidence: "PyTorch and feature engineering demonstrated",
            type: "matched",
        },
        {
            id: 4,
            label: "Docker & Containerization",
            category: "Required Skill",
            status: "gap",
            statusText: "Critical Gap",
            evidence: "Mandatory requirement missing in work history",
            type: "gap",
        },
        {
            id: 5,
            label: "AWS Cloud Infrastructure",
            category: "Preferred",
            status: "partial",
            statusText: "Partial Match",
            evidence: "Cloud concepts mentioned without AWS specifics",
            type: "gap",
        },
        {
            id: 6,
            label: "B.S. in Computer Science",
            category: "Education",
            status: "matched",
            statusText: "Verified",
            evidence: "Academic degree directly matches requirements",
            type: "matched",
        },
    ]

    const filtered = requirements.filter((item) => {
        if (activeFilter === "matched") return item.type === "matched"
        if (activeFilter === "gaps") return item.type === "gap"
        return true
    })

    return (
        <section className="relative z-10 w-full py-16 sm:py-20 lg:py-24 bg-white border-y border-[var(--jj-border)] overflow-hidden">
            <div className="mx-auto max-w-7xl px-6 lg:px-8 relative z-10">
                <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 lg:gap-16 items-center">
                    
                    {/* Left Column: Context & Value */}
                    <div className="lg:col-span-5 text-left">
                        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-[var(--jj-border)] bg-[var(--jj-pale-blue)]/60 text-xs font-semibold text-[var(--jj-primary-blue)] tracking-wide uppercase mb-6 shadow-sm">
                            <Sparkles className="w-3.5 h-3.5" />
                            Precision Requirement Matching
                        </div>

                        <h2 className="text-3xl font-bold tracking-tight text-[var(--jj-navy)] sm:text-4xl leading-[1.2]">
                            Know what matches. <br />
                            <span className="text-[var(--jj-primary-blue)]">Know what's missing.</span>
                        </h2>

                        <p className="mt-4 text-base sm:text-lg text-slate-600 leading-relaxed mb-8">
                            JobJazz compares your profile with the requirements of the role across skills, keywords, experience, and education — highlighting direct matches, partial overlaps, and critical gaps.
                        </p>

                        <div className="space-y-4 pt-2">
                            <div className="flex items-start gap-3">
                                <div className="mt-0.5 flex h-6 w-6 items-center justify-center rounded-lg bg-emerald-50 text-emerald-600 border border-emerald-100 flex-shrink-0">
                                    <CheckCircle2 className="w-4 h-4" />
                                </div>
                                <div>
                                    <p className="text-sm font-semibold text-[var(--jj-navy)]">Direct Match Verification</p>
                                    <p className="text-xs text-slate-500">Validates required skills directly backed by your work history.</p>
                                </div>
                            </div>

                            <div className="flex items-start gap-3">
                                <div className="mt-0.5 flex h-6 w-6 items-center justify-center rounded-lg bg-rose-50 text-rose-600 border border-rose-100 flex-shrink-0">
                                    <AlertCircle className="w-4 h-4" />
                                </div>
                                <div>
                                    <p className="text-sm font-semibold text-[var(--jj-navy)]">Weighted Gap Detection</p>
                                    <p className="text-xs text-slate-500">Separates critical dealbreaker gaps from preferred bonus skills.</p>
                                </div>
                            </div>

                            <div className="flex items-start gap-3">
                                <div className="mt-0.5 flex h-6 w-6 items-center justify-center rounded-lg bg-blue-50 text-[var(--jj-primary-blue)] border border-blue-100 flex-shrink-0">
                                    <ShieldCheck className="w-4 h-4" />
                                </div>
                                <div>
                                    <p className="text-sm font-semibold text-[var(--jj-navy)]">Evidence-Based Insights</p>
                                    <p className="text-xs text-slate-500">Traces every match back to tangible resume achievements.</p>
                                </div>
                            </div>
                        </div>
                    </div>

                    {/* Right Column: Authentic Interactive Match Inspector Card */}
                    <div className="lg:col-span-7 relative w-full max-w-xl mx-auto lg:mx-0 lg:ml-auto">
                        
                        {/* Ambient glow accents */}
                        <div className="absolute -top-6 -right-6 w-56 h-56 bg-[var(--jj-pale-blue)] rounded-full blur-3xl opacity-70 -z-10 pointer-events-none"></div>
                        <div className="absolute -bottom-6 -left-6 w-56 h-56 bg-indigo-50/80 rounded-full blur-3xl opacity-60 -z-10 pointer-events-none"></div>

                        {/* Inspector Container */}
                        <div className="bg-white rounded-3xl border border-[var(--jj-border)] shadow-[0_20px_50px_-12px_rgba(15,23,42,0.08)] p-6 sm:p-7 relative transition-all duration-300">
                            
                            {/* Card Header */}
                            <div className="flex flex-wrap items-center justify-between gap-3 pb-5 border-b border-slate-100">
                                <div>
                                    <div className="flex items-center gap-2 mb-1">
                                        <span className="w-2 h-2 rounded-full bg-emerald-500"></span>
                                        <span className="text-[11px] font-bold text-slate-400 uppercase tracking-widest">Match Analysis</span>
                                    </div>
                                    <h3 className="text-base sm:text-lg font-bold text-[var(--jj-navy)]">Senior Backend Engineer</h3>
                                </div>
                                <div>
                                    <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold bg-emerald-50 text-emerald-700 border border-emerald-200 shadow-sm">
                                        <span className="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>
                                        83% Match
                                    </span>
                                </div>
                            </div>

                            {/* Filter Bar */}
                            <div className="flex items-center justify-between gap-2 pt-4 pb-3">
                                <div className="flex items-center gap-1.5 bg-slate-50 p-1 rounded-xl border border-slate-100">
                                    <button
                                        type="button"
                                        onClick={() => setActiveFilter("all")}
                                        className={`px-3 py-1 rounded-lg text-xs font-semibold transition-all duration-200 ${
                                            activeFilter === "all"
                                                ? "bg-white text-[var(--jj-navy)] shadow-sm border border-slate-200/60"
                                                : "text-slate-500 hover:text-slate-800"
                                        }`}
                                    >
                                        All ({requirements.length})
                                    </button>
                                    <button
                                        type="button"
                                        onClick={() => setActiveFilter("matched")}
                                        className={`px-3 py-1 rounded-lg text-xs font-semibold transition-all duration-200 ${
                                            activeFilter === "matched"
                                                ? "bg-white text-emerald-700 shadow-sm border border-emerald-200/60"
                                                : "text-slate-500 hover:text-emerald-700"
                                        }`}
                                    >
                                        Matched (4)
                                    </button>
                                    <button
                                        type="button"
                                        onClick={() => setActiveFilter("gaps")}
                                        className={`px-3 py-1 rounded-lg text-xs font-semibold transition-all duration-200 ${
                                            activeFilter === "gaps"
                                                ? "bg-white text-rose-700 shadow-sm border border-rose-200/60"
                                                : "text-slate-500 hover:text-rose-700"
                                        }`}
                                    >
                                        Gaps (2)
                                    </button>
                                </div>

                                <span className="text-[11px] text-slate-400 font-medium hidden sm:inline-block">
                                    Interactive Preview
                                </span>
                            </div>

                            {/* Requirements List */}
                            <div className="divide-y divide-slate-100 min-h-[300px]">
                                {filtered.map((item) => (
                                    <div
                                        key={item.id}
                                        className="py-3 px-2 flex items-center justify-between gap-3 group rounded-xl hover:bg-slate-50/70 transition-colors"
                                    >
                                        <div className="flex-1 min-w-0">
                                            <div className="flex items-center gap-2 mb-0.5">
                                                <h4 className="text-sm font-semibold text-[var(--jj-navy)] truncate">
                                                    {item.label}
                                                </h4>
                                                <span className="text-[10px] font-medium px-2 py-0.5 rounded bg-slate-100 text-slate-500 border border-slate-200/60">
                                                    {item.category}
                                                </span>
                                            </div>
                                            <p className="text-xs text-slate-500 font-light truncate">
                                                {item.evidence}
                                            </p>
                                        </div>

                                        <div className="flex-shrink-0">
                                            {item.status === "matched" && (
                                                <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-md text-xs font-semibold bg-emerald-50 text-emerald-700 border border-emerald-200">
                                                    <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" />
                                                    {item.statusText}
                                                </span>
                                            )}
                                            {item.status === "gap" && (
                                                <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-md text-xs font-semibold bg-rose-50 text-rose-700 border border-rose-200">
                                                    <AlertCircle className="w-3.5 h-3.5 text-rose-600" />
                                                    {item.statusText}
                                                </span>
                                            )}
                                            {item.status === "partial" && (
                                                <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-md text-xs font-semibold bg-amber-50 text-amber-700 border border-amber-200">
                                                    <Minus className="w-3.5 h-3.5 text-amber-600" />
                                                    {item.statusText}
                                                </span>
                                            )}
                                        </div>
                                    </div>
                                ))}
                            </div>

                            {/* Card Footer Summary */}
                            <div className="mt-4 pt-3.5 border-t border-slate-100 flex flex-wrap items-center justify-between gap-2 text-xs">
                                <div className="flex items-center gap-3">
                                    <span className="flex items-center gap-1.5 font-medium text-emerald-700">
                                        <span className="w-2 h-2 rounded-full bg-emerald-500"></span> 4 Matched
                                    </span>
                                    <span className="flex items-center gap-1.5 font-medium text-amber-700">
                                        <span className="w-2 h-2 rounded-full bg-amber-500"></span> 1 Partial
                                    </span>
                                    <span className="flex items-center gap-1.5 font-medium text-rose-700">
                                        <span className="w-2 h-2 rounded-full bg-rose-500"></span> 1 Critical Gap
                                    </span>
                                </div>
                                <span className="text-[11px] text-slate-400 font-mono">
                                    JobJazz Analysis Engine
                                </span>
                            </div>

                        </div>
                    </div>

                </div>
            </div>
        </section>
    )
}
