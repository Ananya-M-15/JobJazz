import CircularScore from "./CircularScore";

export default function OverviewTab({ matchResult, recommendations }) {
    const score = matchResult?.overall_score ?? 0;
    const advice = recommendations?.overall_advice || recommendations?.recommendations?.overall_advice || "";
    const scoreBreakdown = matchResult?.score_breakdown || "";

    const matchedRequired = matchResult?.matched_required_skills || [];
    const missingRequired = matchResult?.missing_required_skills || [];
    const matchedPreferred = matchResult?.matched_preferred_skills || [];
    const missingPreferred = matchResult?.missing_preferred_skills || [];

    const totalRequired = matchResult?.total_required_skills ?? (matchedRequired.length + missingRequired.length);
    const totalPreferred = matchResult?.total_preferred_skills ?? (matchedPreferred.length + missingPreferred.length);

    const allRecs = Array.isArray(recommendations?.recommendations)
        ? recommendations.recommendations
        : (recommendations?.recommendations?.recommendations || []);
    // Prioritize High priority recommendations first, then Medium/others
    const topOpportunities = [...allRecs].sort((a, b) => {
        if (a.priority === "High" && b.priority !== "High") return -1;
        if (b.priority === "High" && a.priority !== "High") return 1;
        return 0;
    }).slice(0, 3);

    return (
        <div className="animate-in fade-in slide-in-from-bottom-2 duration-500 space-y-8">

            {/* Main Score & Assessment Card */}
            <div className="rounded-3xl border border-slate-200 bg-white p-6 sm:p-8 shadow-sm">
                <div className="flex flex-col sm:flex-row gap-6 sm:gap-8 items-center sm:items-start">
                    <div className="flex-shrink-0">
                        <CircularScore score={score} />
                    </div>
                    <div className="flex-1 text-center sm:text-left min-w-0">
                        <div className="flex flex-wrap items-center justify-center sm:justify-start gap-2 mb-2">
                            <span className="text-xs font-bold uppercase tracking-widest text-indigo-600">
                                Overall Assessment
                            </span>
                        </div>

                        {scoreBreakdown && (
                            <p className="text-xs font-semibold text-slate-500 mb-2">
                                {scoreBreakdown}
                            </p>
                        )}

                        {advice ? (
                            <p className="text-sm sm:text-base leading-relaxed text-slate-700 max-w-2xl">
                                {advice}
                            </p>
                        ) : (
                            <p className="text-sm text-slate-500 italic">
                                Assessment details generated based on matching requirements.
                            </p>
                        )}

                        {/* Metric Badges */}
                        <div className="mt-5 flex flex-wrap justify-center sm:justify-start gap-2 pt-4 border-t border-slate-100">
                            <span className="inline-flex items-center gap-1.5 rounded-lg bg-slate-50 border border-slate-200 px-3 py-1 text-xs font-semibold text-slate-700">
                                <span className="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>
                                Required Skills: {totalRequired > 0 ? `${matchedRequired.length} of ${totalRequired}` : "None Detected"}
                            </span>
                            {totalPreferred > 0 && (
                                <span className="inline-flex items-center gap-1.5 rounded-lg bg-slate-50 border border-slate-200 px-3 py-1 text-xs font-semibold text-slate-700">
                                    <span className="w-1.5 h-1.5 rounded-full bg-indigo-500"></span>
                                    Preferred Skills: {matchedPreferred.length} of {totalPreferred}
                                </span>
                            )}
                            <span className={`inline-flex items-center gap-1.5 rounded-lg border px-3 py-1 text-xs font-semibold ${
                                matchResult?.experience_status === 'met'
                                    ? 'bg-emerald-50 border-emerald-200 text-emerald-700'
                                    : matchResult?.experience_status === 'gap'
                                    ? 'bg-rose-50 border-rose-200 text-rose-700'
                                    : 'bg-slate-50 border-slate-200 text-slate-600'
                            }`}>
                                Experience: {matchResult?.experience_status === 'met' ? 'Satisfied' : matchResult?.experience_status === 'gap' ? 'Gap' : 'Not Specified'}
                            </span>
                        </div>
                    </div>
                </div>
            </div>

            {/* Two-Column Grid: Strengths/Focus Areas & Highest-Impact Opportunities */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 items-start">

                {/* Left Column: Strengths & Focus Areas */}
                <div className="space-y-6">
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                        {/* Matched Required Skills */}
                        <div className="rounded-2xl border border-slate-200 bg-emerald-50/40 p-5">
                            <div className="flex items-center justify-between mb-3">
                                <p className="text-xs uppercase font-bold tracking-widest text-emerald-800">
                                    Matched Skills
                                </p>
                                <span className="text-xs font-bold px-2 py-0.5 rounded-full bg-emerald-100 text-emerald-800">
                                    {totalRequired > 0 ? `${matchedRequired.length} of ${totalRequired}` : matchedRequired.length}
                                </span>
                            </div>
                            {matchedRequired.length > 0 ? (
                                <ul className="space-y-2">
                                    {matchedRequired.slice(0, 5).map((skill, idx) => (
                                        <li key={idx} className="flex items-start gap-2 text-sm text-slate-800 font-medium">
                                            <span className="mt-1 w-1.5 h-1.5 rounded-full bg-emerald-500 shrink-0"></span>
                                            <span className="truncate">{skill}</span>
                                        </li>
                                    ))}
                                    {matchedRequired.length > 5 && (
                                        <li className="text-xs text-slate-500 italic mt-2">
                                            + {matchedRequired.length - 5} more in Skills tab
                                        </li>
                                    )}
                                </ul>
                            ) : (
                                <p className="text-sm text-slate-500 italic">
                                    {totalRequired > 0
                                        ? "No direct required skill matches found."
                                        : "No explicit required skills detected in posting."}
                                </p>
                            )}
                        </div>

                        {/* Critical Missing Requirements */}
                        <div className="rounded-2xl border border-slate-200 bg-rose-50/40 p-5">
                            <div className="flex items-center justify-between mb-3">
                                <p className="text-xs uppercase font-bold tracking-widest text-rose-800">
                                    Critical Gaps
                                </p>
                                <span className="text-xs font-bold px-2 py-0.5 rounded-full bg-rose-100 text-rose-800">
                                    {missingRequired.length}
                                </span>
                            </div>
                            {missingRequired.length > 0 ? (
                                <ul className="space-y-2">
                                    {missingRequired.slice(0, 5).map((skill, idx) => (
                                        <li key={idx} className="flex items-start gap-2 text-sm text-slate-800 font-medium">
                                            <span className="mt-1 w-1.5 h-1.5 rounded-full bg-rose-500 shrink-0"></span>
                                            <span className="truncate">{skill}</span>
                                        </li>
                                    ))}
                                    {missingRequired.length > 5 && (
                                        <li className="text-xs text-slate-500 italic mt-2">
                                            + {missingRequired.length - 5} more in Skills tab
                                        </li>
                                    )}
                                </ul>
                            ) : totalRequired > 0 ? (
                                <p className="text-sm text-slate-600 font-medium">
                                    ✓ You match all stated required skills!
                                </p>
                            ) : (
                                <p className="text-sm text-slate-500 italic">
                                    No explicit required skills detected in posting.
                                </p>
                            )}
                        </div>
                    </div>

                    {/* Preferred Skills Summary Card */}
                    {(matchedPreferred.length > 0 || missingPreferred.length > 0) && (
                        <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
                            <h3 className="text-xs uppercase font-bold tracking-widest text-indigo-700 mb-3">
                                Preferred & Bonus Skills
                            </h3>
                            <div className="flex flex-wrap gap-2">
                                {matchedPreferred.map((skill, idx) => (
                                    <span key={idx} className="inline-flex items-center gap-1 rounded-full bg-emerald-50 border border-emerald-200 px-3 py-1 text-xs font-medium text-emerald-800">
                                        ✓ {skill}
                                    </span>
                                ))}
                                {missingPreferred.map((skill, idx) => (
                                    <span key={idx} className="inline-flex items-center gap-1 rounded-full bg-amber-50 border border-amber-200 px-3 py-1 text-xs font-medium text-amber-800">
                                        + {skill}
                                    </span>
                                ))}
                            </div>
                        </div>
                    )}
                </div>

                {/* Right Column: Top Actionable Opportunities */}
                <div className="space-y-4">
                    <div className="flex items-center justify-between">
                        <h3 className="text-sm font-bold uppercase tracking-widest text-slate-900 ml-1">
                            Your Highest-Impact Opportunities
                        </h3>
                        {topOpportunities.length > 0 && (
                            <span className="text-xs font-semibold text-indigo-600">
                                Top {topOpportunities.length} Priorities
                            </span>
                        )}
                    </div>

                    {topOpportunities.length > 0 ? (
                        <div className="space-y-3">
                            {topOpportunities.map((opp, idx) => {
                                const isHigh = opp.priority === "High";
                                return (
                                    <div key={idx} className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm hover:shadow-md transition-shadow">
                                        <div className="flex items-start gap-3.5">
                                            <div className="flex h-8 w-8 items-center justify-center rounded-xl bg-indigo-50 text-indigo-700 shrink-0 font-bold text-sm">
                                                {idx + 1}
                                            </div>
                                            <div className="min-w-0 flex-1">
                                                <div className="flex items-center justify-between gap-2">
                                                    <h4 className="font-bold text-slate-900 truncate">
                                                        {opp.skill || opp.title || "Target Area"}
                                                    </h4>
                                                    <span className={`text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-full border shrink-0 ${
                                                        isHigh
                                                            ? 'bg-rose-50 text-rose-700 border-rose-200'
                                                            : 'bg-amber-50 text-amber-700 border-amber-200'
                                                    }`}>
                                                        {opp.priority} Priority
                                                    </span>
                                                </div>
                                                <p className="mt-1 text-sm text-slate-700 font-medium leading-relaxed">
                                                    {opp.action}
                                                </p>
                                                {opp.reason && (
                                                    <p className="mt-1 text-xs text-slate-500 leading-normal">
                                                        {opp.reason}
                                                    </p>
                                                )}
                                            </div>
                                        </div>
                                    </div>
                                );
                            })}
                        </div>
                    ) : totalRequired > 0 && matchedRequired.length > 0 ? (
                        <div className="rounded-2xl border border-slate-200 bg-white p-8 text-center shadow-sm">
                            <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-emerald-50 text-emerald-600 text-xl mb-3">
                                ✓
                            </div>
                            <h4 className="font-bold text-slate-900 mb-1">
                                No Critical Skill Gaps Identified
                            </h4>
                            <p className="text-sm text-slate-600 max-w-sm mx-auto">
                                Your profile directly matches the key skills analyzed for this position.
                            </p>
                        </div>
                    ) : (
                        <div className="rounded-2xl border border-slate-200 bg-white p-8 text-center shadow-sm">
                            <h4 className="font-bold text-slate-900 mb-1">
                                No Priority Action Items
                            </h4>
                            <p className="text-sm text-slate-500 max-w-sm mx-auto">
                                {totalRequired === 0
                                    ? "JobJazz could not detect enough explicit requirements in this posting to generate targeted skill recommendations."
                                    : "No high-priority skill recommendations were generated for this comparison."}
                            </p>
                        </div>
                    )}
                </div>

            </div>
        </div>
    );
}
