

function AnalysisResults({ matchResult, skillGap, recommendations, onStartOver }) {
    const score = matchResult?.overall_score || 0
    const recs = recommendations?.recommendations?.recommendations || []
    const advice = recommendations?.recommendations?.overall_advice || ""

    return (
        <section className="relative z-10 mx-auto min-h-screen max-w-5xl px-6 py-28 sm:px-10 lg:px-12">
            <div className="rounded-3xl border border-white/10 bg-white/[0.04] p-8 backdrop-blur-xl sm:p-10">
                {/* Header */}
                <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-6">
                    <div>
                        <p className="text-sm font-medium uppercase tracking-[0.2em] text-purple-300">
                            JobJazz Analysis
                        </p>
                        <h1 className="mt-3 text-4xl font-bold tracking-tight text-white sm:text-5xl">
                            Your Match Results
                        </h1>
                    </div>
                    <div className="rounded-2xl border border-white/10 bg-black/40 p-4 text-center sm:min-w-[140px]">
                        <p className="text-xs uppercase tracking-widest text-white/40">Overall Score</p>
                        <p className={`mt-2 text-4xl font-bold ${score >= 75 ? 'text-emerald-400' : score >= 50 ? 'text-yellow-400' : 'text-red-400'}`}>
                            {score}%
                        </p>
                    </div>
                </div>

                {/* Overall Advice */}
                {advice && (
                    <div className="mt-8 rounded-2xl border border-purple-500/20 bg-purple-500/10 p-6">
                        <p className="text-[1.0625rem] leading-relaxed text-purple-100">{advice}</p>
                    </div>
                )}

                {/* Grid for Skills */}
                <div className="mt-8 grid gap-6 md:grid-cols-2">
                    {/* Strengths */}
                    <div className="rounded-2xl border border-white/10 bg-black/20 p-6">
                        <h2 className="text-lg font-semibold text-emerald-400 flex items-center gap-2">
                            <span>✓</span> Your Strengths
                        </h2>
                        {skillGap?.strengths?.length > 0 ? (
                            <div className="mt-4 flex flex-wrap gap-2">
                                {skillGap.strengths.map((skill, idx) => (
                                    <span key={idx} className="rounded-full border border-emerald-400/20 bg-emerald-400/10 px-3 py-1 text-sm text-emerald-300">
                                        {skill}
                                    </span>
                                ))}
                            </div>
                        ) : (
                            <p className="mt-4 text-sm text-white/40">No matching skills found.</p>
                        )}
                    </div>

                    {/* Critical Gaps */}
                    <div className="rounded-2xl border border-white/10 bg-black/20 p-6">
                        <h2 className="text-lg font-semibold text-red-400 flex items-center gap-2">
                            <span>✕</span> Missing Critical Skills
                        </h2>
                        {skillGap?.critical_gaps?.length > 0 ? (
                            <div className="mt-4 flex flex-wrap gap-2">
                                {skillGap.critical_gaps.map((skill, idx) => (
                                    <span key={idx} className="rounded-full border border-red-400/20 bg-red-400/10 px-3 py-1 text-sm text-red-300">
                                        {skill}
                                    </span>
                                ))}
                            </div>
                        ) : (
                            <p className="mt-4 text-sm text-white/40">You have all the critical skills!</p>
                        )}
                    </div>
                </div>

                {/* Preferred Gaps */}
                {skillGap?.preferred_gaps?.length > 0 && (
                    <div className="mt-6 rounded-2xl border border-white/10 bg-black/20 p-6">
                        <h2 className="text-lg font-semibold text-yellow-400 flex items-center gap-2">
                            <span>⚠</span> Missing Preferred Skills
                        </h2>
                        <div className="mt-4 flex flex-wrap gap-2">
                            {skillGap.preferred_gaps.map((skill, idx) => (
                                <span key={idx} className="rounded-full border border-yellow-400/20 bg-yellow-400/10 px-3 py-1 text-sm text-yellow-300">
                                    {skill}
                                </span>
                            ))}
                        </div>
                    </div>
                )}

                {/* Experience & Education */}
                <div className="mt-6 grid gap-6 md:grid-cols-2">
                    <div className="rounded-2xl border border-white/10 bg-black/20 p-6">
                        <h2 className="text-sm uppercase tracking-widest text-white/40 mb-3">Experience Match</h2>
                        <div className="flex items-start gap-3">
                            <span className={`mt-0.5 ${matchResult?.experience_match ? 'text-emerald-400' : 'text-red-400'}`}>
                                {matchResult?.experience_match ? '✓' : '✕'}
                            </span>
                            <p className="text-white/80 leading-relaxed text-sm">{skillGap?.experience_gap || matchResult?.experience_notes}</p>
                        </div>
                    </div>
                    <div className="rounded-2xl border border-white/10 bg-black/20 p-6">
                        <h2 className="text-sm uppercase tracking-widest text-white/40 mb-3">Education Match</h2>
                        <div className="flex items-start gap-3">
                            <span className={`mt-0.5 ${matchResult?.education_match ? 'text-emerald-400' : 'text-red-400'}`}>
                                {matchResult?.education_match ? '✓' : '✕'}
                            </span>
                            <p className="text-white/80 leading-relaxed text-sm">{skillGap?.education_gap || matchResult?.education_notes}</p>
                        </div>
                    </div>
                </div>

                {/* Recommendations */}
                {recs.length > 0 && (
                    <div className="mt-10">
                        <h2 className="text-2xl font-bold text-white mb-5">Action Plan</h2>
                        <div className="space-y-4">
                            {recs.map((rec, idx) => (
                                <div key={idx} className="rounded-2xl border border-white/10 bg-white/[0.02] p-5 transition hover:bg-white/[0.04]">
                                    <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                                        <h3 className="text-lg font-medium text-white">{rec.skill}</h3>
                                        <span className={`self-start sm:self-auto rounded-full px-3 py-1 text-[0.65rem] font-bold uppercase tracking-[0.1em] ${
                                            rec.priority === 'High' ? 'bg-red-500/20 text-red-300 border border-red-500/20' :
                                            rec.priority === 'Medium' ? 'bg-yellow-500/20 text-yellow-300 border border-yellow-500/20' :
                                            'bg-blue-500/20 text-blue-300 border border-blue-500/20'
                                        }`}>
                                            {rec.priority} Priority
                                        </span>
                                    </div>
                                    <p className="mt-3 text-sm text-white/70"><strong className="text-white/90">Why:</strong> {rec.reason}</p>
                                    <p className="mt-2 text-sm text-white/70"><strong className="text-white/90">Action:</strong> {rec.action}</p>
                                </div>
                            ))}
                        </div>
                    </div>
                )}

                {/* Start Over */}
                <div className="mt-10 flex justify-center">
                    <button
                        onClick={onStartOver}
                        className="rounded-xl border border-white/20 bg-transparent px-8 py-3.5 text-sm font-semibold tracking-wide text-white transition hover:bg-white/5 hover:border-white/40"
                    >
                        Analyze Another Job
                    </button>
                </div>
            </div>
        </section>
    )
}

export default AnalysisResults
