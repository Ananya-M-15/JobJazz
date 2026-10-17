export default function SkillsTab({ skillGap, matchResult, candidateProfile }) {
    const matchedRequired = matchResult?.matched_required_skills || skillGap?.strengths || [];
    const criticalGaps = matchResult?.missing_required_skills || skillGap?.critical_gaps || [];
    const matchedPreferred = matchResult?.matched_preferred_skills || [];
    const preferredGaps = matchResult?.missing_preferred_skills || skillGap?.preferred_gaps || [];
    
    const keywordMatches = matchResult?.keyword_matches || [];
    const keywordGaps = matchResult?.keyword_gaps || [];

    const totalRequired = matchResult?.total_required_skills ?? (matchedRequired.length + criticalGaps.length);
    const totalPreferred = matchResult?.total_preferred_skills ?? (matchedPreferred.length + preferredGaps.length);

    const candidateSkillCount = matchResult?.candidate_skills_detected ?? (candidateProfile?.skills?.length ?? 0);
    const isResumeSkillsEmpty = candidateSkillCount === 0;

    return (
        <div className="animate-in fade-in slide-in-from-bottom-2 duration-500 space-y-8">
            
            {/* Case E Banner: Resume skills insufficient */}
            {isResumeSkillsEmpty && (
                <div className="rounded-2xl border border-amber-200 bg-amber-50/70 p-5">
                    <div className="flex items-start gap-3.5">
                        <span className="text-2xl shrink-0">⚠️</span>
                        <div>
                            <h4 className="text-sm font-bold text-amber-900">
                                Resume Skill Data Insufficient
                            </h4>
                            <p className="mt-1 text-xs text-amber-800 leading-relaxed">
                                No technical skills were extracted from your resume profile. This does not necessarily mean you lack these skills, but JobJazz cannot reliably calculate skill matches without documented skill entries in your resume.
                            </p>
                        </div>
                    </div>
                </div>
            )}

            {/* Required Skills Section Header */}
            <div>
                <p className="text-xs font-bold uppercase tracking-widest text-indigo-600 mb-1">
                    Core Qualifications
                </p>
                <h2 className="text-2xl font-bold text-slate-900">
                    Required Skills Breakdown
                </h2>
                <p className="text-sm text-slate-500 mt-1">
                    Skills explicitly demanded as minimum qualifications for this position.
                </p>
            </div>

            {/* Case D: No required skills detected in JD */}
            {totalRequired === 0 ? (
                <div className="rounded-3xl border border-slate-200 bg-white p-6 md:p-8 shadow-sm">
                    <div className="flex items-start gap-4">
                        <div className="w-10 h-10 rounded-2xl bg-amber-50 text-amber-600 flex items-center justify-center font-bold text-lg shrink-0 border border-amber-200">
                            ℹ️
                        </div>
                        <div className="flex-1 min-w-0">
                            <h3 className="text-base font-bold text-slate-900">
                                No Explicit Required Skills Identified
                            </h3>
                            <p className="mt-1 text-sm text-slate-600 leading-relaxed">
                                JobJazz could not identify enough explicitly stated required skills in this job description to evaluate core technical qualification matches reliably.
                            </p>
                            {totalPreferred > 0 && (
                                <p className="mt-3 text-xs font-semibold text-indigo-700 bg-indigo-50 px-3 py-2 rounded-xl border border-indigo-100 inline-block">
                                    Note: {totalPreferred} preferred / bonus skill{totalPreferred > 1 ? "s were" : " was"} identified below and factored into your score.
                                </p>
                            )}
                        </div>
                    </div>
                </div>
            ) : (
                /* Cases A, B, C: Required skills detected */
                <div className="grid gap-6 md:grid-cols-2">
                    
                    {/* Matched Required Skills */}
                    <div className="rounded-3xl border border-slate-200 bg-white p-6 md:p-8 shadow-sm relative overflow-hidden">
                        <div className="relative z-10">
                            <div className="flex items-center justify-between mb-6">
                                <h3 className="text-lg font-bold text-slate-900 flex items-center gap-3">
                                    <span className="flex items-center justify-center w-7 h-7 rounded-full bg-emerald-100 text-emerald-700 text-sm font-bold">
                                        ✓
                                    </span>
                                    Matched Required Skills
                                </h3>
                                <span className="text-xs font-bold px-2.5 py-1 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200">
                                    {matchedRequired.length} of {totalRequired} matched
                                </span>
                            </div>

                            {matchedRequired.length > 0 ? (
                                <div className="flex flex-wrap gap-2.5">
                                    {matchedRequired.map((skill, idx) => (
                                        <span key={idx} className="rounded-xl border border-emerald-200 bg-emerald-50/70 px-3.5 py-1.5 text-sm font-semibold text-emerald-800 shadow-sm flex items-center gap-1.5">
                                            <span className="w-1.5 h-1.5 rounded-full bg-emerald-600"></span>
                                            {skill}
                                        </span>
                                    ))}
                                </div>
                            ) : (
                                <p className="text-slate-500 text-sm italic bg-slate-50 p-4 rounded-xl border border-slate-100">
                                    No direct required skill matches identified between your resume and this job posting.
                                </p>
                            )}
                        </div>
                    </div>

                    {/* Missing Required Skills */}
                    <div className="rounded-3xl border border-slate-200 bg-white p-6 md:p-8 shadow-sm relative overflow-hidden">
                        <div className="relative z-10">
                            <div className="flex items-center justify-between mb-6">
                                <h3 className="text-lg font-bold text-slate-900 flex items-center gap-3">
                                    <span className="flex items-center justify-center w-7 h-7 rounded-full bg-rose-100 text-rose-700 text-sm font-bold">
                                        ✕
                                    </span>
                                    Missing Required Skills
                                </h3>
                                <span className="text-xs font-bold px-2.5 py-1 rounded-full bg-rose-50 text-rose-700 border border-rose-200">
                                    {criticalGaps.length} missing
                                </span>
                            </div>

                            {criticalGaps.length > 0 ? (
                                <div className="flex flex-wrap gap-2.5">
                                    {criticalGaps.map((skill, idx) => (
                                        <span key={idx} className="rounded-xl border border-rose-200 bg-rose-50/70 px-3.5 py-1.5 text-sm font-semibold text-rose-800 shadow-sm flex items-center gap-1.5">
                                            <span className="w-1.5 h-1.5 rounded-full bg-rose-600"></span>
                                            {skill}
                                        </span>
                                    ))}
                                </div>
                            ) : (
                                /* Case A: Celebration only when totalRequired > 0 AND criticalGaps === 0 */
                                <div className="flex items-center gap-3 bg-emerald-50/70 p-4 rounded-xl border border-emerald-200">
                                    <span className="text-xl">🎉</span>
                                    <p className="text-emerald-900 text-sm font-semibold">
                                        Full required skill match! All {totalRequired} core requirements matched.
                                    </p>
                                </div>
                            )}
                        </div>
                    </div>

                </div>
            )}

            {/* Preferred / Bonus Skills Section */}
            {totalPreferred > 0 && (
                <div className="rounded-3xl border border-slate-200 bg-white p-6 md:p-8 shadow-sm">
                    <div className="mb-6">
                        <p className="text-xs font-bold uppercase tracking-widest text-indigo-600 mb-1">
                            Differentiators
                        </p>
                        <h3 className="text-xl font-bold text-slate-900">
                            Preferred & Bonus Skills
                        </h3>
                        <p className="text-sm text-slate-500 mt-1">
                            Skills listed as "nice to have" or preferred qualifications that give candidates an edge.
                        </p>
                    </div>

                    <div className="grid gap-6 sm:grid-cols-2">
                        {/* Matched Preferred */}
                        <div className="rounded-2xl border border-slate-100 bg-slate-50 p-5">
                            <h4 className="text-xs font-bold uppercase tracking-widest text-emerald-700 mb-3 flex items-center gap-2">
                                <span className="w-2 h-2 rounded-full bg-emerald-500"></span>
                                Preferred Skills You Have ({matchedPreferred.length} of {totalPreferred})
                            </h4>
                            {matchedPreferred.length > 0 ? (
                                <div className="flex flex-wrap gap-2">
                                    {matchedPreferred.map((skill, idx) => (
                                        <span key={idx} className="rounded-lg border border-emerald-200 bg-white px-3 py-1 text-xs font-semibold text-emerald-800 shadow-sm">
                                            ✓ {skill}
                                        </span>
                                    ))}
                                </div>
                            ) : (
                                <p className="text-xs text-slate-500 italic">No bonus skills directly matched.</p>
                            )}
                        </div>

                        {/* Preferred Gaps */}
                        <div className="rounded-2xl border border-slate-100 bg-slate-50 p-5">
                            <h4 className="text-xs font-bold uppercase tracking-widest text-amber-700 mb-3 flex items-center gap-2">
                                <span className="w-2 h-2 rounded-full bg-amber-500"></span>
                                Bonus Skills to Consider ({preferredGaps.length})
                            </h4>
                            {preferredGaps.length > 0 ? (
                                <div className="flex flex-wrap gap-2">
                                    {preferredGaps.map((skill, idx) => (
                                        <span key={idx} className="rounded-lg border border-amber-200 bg-white px-3 py-1 text-xs font-semibold text-amber-800 shadow-sm">
                                            + {skill}
                                        </span>
                                    ))}
                                </div>
                            ) : (
                                <p className="text-xs text-slate-500 italic">You possess all stated preferred skills!</p>
                            )}
                        </div>
                    </div>
                </div>
            )}

            {/* Keyword Relevance Section */}
            {(keywordMatches.length > 0 || keywordGaps.length > 0) && (
                <div className="rounded-3xl border border-slate-200 bg-white p-6 md:p-8 shadow-sm">
                    <h3 className="text-lg font-bold text-slate-900 mb-2">
                        Job Posting Keywords
                    </h3>
                    <p className="text-sm text-slate-500 mb-5">
                        Technical terms recognized throughout the entire text of the job description.
                    </p>

                    <div className="flex flex-wrap gap-2">
                        {keywordMatches.map((kw, idx) => (
                            <span key={`match-${idx}`} className="rounded-lg border border-slate-200 bg-slate-50 px-3 py-1 text-xs font-semibold text-slate-800">
                                ✓ {kw}
                            </span>
                        ))}
                        {keywordGaps.map((kw, idx) => (
                            <span key={`gap-${idx}`} className="rounded-lg border border-slate-200 bg-white px-3 py-1 text-xs font-medium text-slate-500">
                                {kw}
                            </span>
                        ))}
                    </div>
                </div>
            )}

        </div>
    );
}
