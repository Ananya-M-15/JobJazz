export default function SkillsTab({ skillGap }) {
    return (
        <div className="animate-in fade-in slide-in-from-bottom-2 duration-500 space-y-8">
            <div className="grid gap-6 md:grid-cols-2">
                
                {/* Strengths */}
                <div className="rounded-3xl border border-slate-200 bg-white p-6 md:p-8 shadow-sm relative overflow-hidden">
                    <div className="absolute top-0 right-0 p-8 opacity-[0.03] text-emerald-600 text-9xl leading-none select-none pointer-events-none">✓</div>
                    <div className="relative z-10">
                        <h2 className="text-xl font-bold text-slate-900 mb-6 flex items-center gap-3">
                            <span className="flex items-center justify-center w-8 h-8 rounded-full bg-emerald-100 text-emerald-600 text-sm">✓</span>
                            Your Strengths
                        </h2>
                        {skillGap?.strengths?.length > 0 ? (
                            <div className="flex flex-wrap gap-2.5">
                                {skillGap.strengths.map((skill, idx) => (
                                    <span key={idx} className="rounded-full border border-emerald-200 bg-emerald-50 px-4 py-1.5 text-sm font-medium text-emerald-800 shadow-sm">
                                        {skill}
                                    </span>
                                ))}
                            </div>
                        ) : (
                            <p className="text-slate-500 italic bg-slate-50 p-4 rounded-xl border border-slate-100">No matching skills were found in your profile.</p>
                        )}
                    </div>
                </div>

                {/* Critical Gaps */}
                <div className="rounded-3xl border border-slate-200 bg-white p-6 md:p-8 shadow-sm relative overflow-hidden">
                    <div className="absolute top-0 right-0 p-8 opacity-[0.03] text-rose-600 text-9xl leading-none select-none pointer-events-none">✕</div>
                    <div className="relative z-10">
                        <h2 className="text-xl font-bold text-slate-900 mb-6 flex items-center gap-3">
                            <span className="flex items-center justify-center w-8 h-8 rounded-full bg-rose-100 text-rose-600 text-sm">✕</span>
                            Critical Gaps
                        </h2>
                        {skillGap?.critical_gaps?.length > 0 ? (
                            <div className="flex flex-wrap gap-2.5">
                                {skillGap.critical_gaps.map((skill, idx) => (
                                    <span key={idx} className="rounded-full border border-rose-200 bg-rose-50 px-4 py-1.5 text-sm font-medium text-rose-800 shadow-sm">
                                        {skill}
                                    </span>
                                ))}
                            </div>
                        ) : (
                            <div className="flex items-center gap-3 bg-slate-50 p-4 rounded-xl border border-slate-100">
                                <span className="text-2xl">🎉</span>
                                <p className="text-slate-700 text-sm font-medium">You're a perfect fit! No critical requirements are missing.</p>
                            </div>
                        )}
                    </div>
                </div>
            </div>

            {/* Preferred Gaps */}
            <div className="rounded-3xl border border-slate-200 bg-white p-6 md:p-8 shadow-sm">
                <h2 className="text-xl font-bold text-slate-900 mb-6 flex items-center gap-3">
                    <span className="flex items-center justify-center w-8 h-8 rounded-full bg-amber-100 text-amber-600 text-sm">⚠</span>
                    Preferred Gaps (Bonus Skills)
                </h2>
                {skillGap?.preferred_gaps?.length > 0 ? (
                    <div className="flex flex-wrap gap-2.5">
                        {skillGap.preferred_gaps.map((skill, idx) => (
                            <span key={idx} className="rounded-full border border-amber-200 bg-amber-50 px-4 py-1.5 text-sm font-medium text-amber-800 shadow-sm">
                                {skill}
                            </span>
                        ))}
                    </div>
                ) : (
                    <p className="text-slate-500 italic bg-slate-50 p-4 rounded-xl border border-slate-100">You have all the preferred bonus skills!</p>
                )}
            </div>
        </div>
    );
}
