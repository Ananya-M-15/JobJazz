import CircularScore from "./CircularScore";

export default function OverviewTab({ matchResult, recommendations }) {
    const score = matchResult?.overall_score || 0;
    const advice = recommendations?.recommendations?.overall_advice || "";
    
    const matchedSkills = matchResult?.matched_skills || [];
    const missingSkills = matchResult?.missing_skills || [];
    
    const topOpportunities = recommendations?.recommendations?.top_opportunities || [];

    return (
        <div className="animate-in fade-in slide-in-from-bottom-2 duration-500">
            <div className="flex flex-col lg:flex-row gap-8 items-start">
                
                {/* Left Column: Match Summary & Strengths/Focus */}
                <div className="w-full lg:w-1/2 space-y-6">
                    {/* Main Score Box */}
                    <div className="rounded-2xl border border-slate-200 bg-white p-6 md:p-8 shadow-sm">
                        <div className="flex flex-col sm:flex-row gap-8 items-center sm:items-start">
                            <div className="flex-shrink-0">
                                <CircularScore score={score} />
                            </div>
                            <div className="flex-1 text-center sm:text-left">
                                <h2 className="text-sm font-bold uppercase tracking-widest text-indigo-600 mb-2">Your Match Summary</h2>
                                {advice ? (
                                    <p className="text-sm md:text-base leading-relaxed text-slate-700">{advice}</p>
                                ) : (
                                    <p className="text-sm text-slate-500 italic">No overall advice was generated for this match.</p>
                                )}
                            </div>
                        </div>
                    </div>
                    
                    {/* Strengths and Focus Areas */}
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                        <div className="rounded-2xl border border-slate-200 bg-emerald-50/50 p-5">
                            <p className="text-xs uppercase font-bold tracking-widest text-emerald-700 mb-3">You Already Match</p>
                            {matchedSkills.length > 0 ? (
                                <ul className="space-y-2">
                                    {matchedSkills.slice(0, 4).map((skill, idx) => (
                                        <li key={idx} className="flex items-start gap-2 text-sm text-slate-700 font-medium">
                                            <span className="mt-1 w-1.5 h-1.5 rounded-full bg-emerald-500 shrink-0"></span>
                                            {skill}
                                        </li>
                                    ))}
                                    {matchedSkills.length > 4 && (
                                        <li className="text-xs text-slate-500 italic mt-2">+ {matchedSkills.length - 4} more</li>
                                    )}
                                </ul>
                            ) : (
                                <p className="text-sm text-slate-500">No direct skill matches found.</p>
                            )}
                        </div>
                        
                        <div className="rounded-2xl border border-slate-200 bg-rose-50/50 p-5">
                            <p className="text-xs uppercase font-bold tracking-widest text-rose-700 mb-3">Focus Areas</p>
                            {missingSkills.length > 0 ? (
                                <ul className="space-y-2">
                                    {missingSkills.slice(0, 4).map((skill, idx) => (
                                        <li key={idx} className="flex items-start gap-2 text-sm text-slate-700 font-medium">
                                            <span className="mt-1 w-1.5 h-1.5 rounded-full bg-rose-500 shrink-0"></span>
                                            {skill}
                                        </li>
                                    ))}
                                    {missingSkills.length > 4 && (
                                        <li className="text-xs text-slate-500 italic mt-2">+ {missingSkills.length - 4} more</li>
                                    )}
                                </ul>
                            ) : (
                                <p className="text-sm text-slate-500">You matched all required skills!</p>
                            )}
                        </div>
                    </div>
                </div>
                
                {/* Right Column: Top Opportunities */}
                <div className="w-full lg:w-1/2 space-y-4">
                    <h3 className="text-sm font-bold uppercase tracking-widest text-slate-900 ml-1">Your Biggest Opportunities</h3>
                    
                    {topOpportunities.length > 0 ? (
                        <div className="space-y-4">
                            {topOpportunities.slice(0, 3).map((opp, idx) => (
                                <div key={idx} className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm hover:shadow-md transition-shadow">
                                    <div className="flex items-start gap-3">
                                        <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-indigo-50 text-indigo-600 shrink-0 font-bold">
                                            {idx + 1}
                                        </div>
                                        <div>
                                            <h4 className="font-semibold text-slate-900">{opp.title || opp.focus_area || "Opportunity"}</h4>
                                            <p className="mt-1 text-sm text-slate-600 leading-relaxed">{opp.description || opp.action || opp.why_it_matters}</p>
                                        </div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    ) : (
                        <div className="rounded-2xl border border-slate-200 bg-white p-8 text-center shadow-sm">
                            <p className="text-sm text-slate-500">No specific opportunities identified. Check the Action Plan for more details.</p>
                        </div>
                    )}
                </div>

            </div>
        </div>
    );
}
