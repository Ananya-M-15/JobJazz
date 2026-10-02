export default function ActionPlanTab({ recommendations }) {
    const recs = recommendations?.recommendations?.recommendations || [];

    if (!recs || recs.length === 0) {
        return (
            <div className="animate-in fade-in slide-in-from-bottom-2 duration-500 rounded-3xl border border-slate-200 bg-white p-12 text-center shadow-sm">
                <div className="mx-auto w-16 h-16 rounded-full bg-emerald-50 border border-emerald-100 flex items-center justify-center mb-4">
                    <span className="text-2xl">🎉</span>
                </div>
                <h2 className="text-2xl font-bold text-slate-900 mb-2">You're fully prepared!</h2>
                <p className="text-slate-600">We don't have any specific skill development recommendations for this role.</p>
            </div>
        );
    }

    return (
        <div className="animate-in fade-in slide-in-from-bottom-2 duration-500 relative">
            {/* Timeline line */}
            <div className="absolute left-8 top-8 bottom-8 w-px bg-slate-200 hidden md:block"></div>
            
            <div className="space-y-6 relative z-10">
                {recs.map((rec, idx) => {
                    const isHigh = rec.priority === 'High';
                    const isMed = rec.priority === 'Medium';
                    const badgeClass = isHigh 
                        ? 'bg-rose-50 text-rose-700 border-rose-200' 
                        : isMed 
                        ? 'bg-amber-50 text-amber-700 border-amber-200' 
                        : 'bg-indigo-50 text-indigo-700 border-indigo-200';
                    const stepNumberClass = isHigh ? 'bg-rose-100 text-rose-700 border-white' : 'bg-slate-100 text-slate-600 border-white';

                    return (
                        <div key={idx} className="relative flex flex-col md:flex-row gap-6 group">
                            {/* Step Indicator */}
                            <div className="hidden md:flex items-center justify-center w-16 flex-shrink-0">
                                <div className={`w-10 h-10 rounded-full border-4 flex items-center justify-center font-bold text-sm shadow-sm z-10 transition-colors duration-300 group-hover:border-indigo-100 group-hover:text-indigo-600 group-hover:bg-white ${stepNumberClass}`}>
                                    {idx + 1}
                                </div>
                            </div>
                            
                            {/* Content Card */}
                            <div className="flex-1 rounded-3xl border border-slate-200 bg-white hover:shadow-md p-6 md:p-8 transition duration-300 shadow-sm">
                                <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-4 mb-5">
                                    <div>
                                        <div className="flex items-center gap-3 mb-2 md:hidden">
                                            <div className="w-6 h-6 rounded-full bg-slate-100 flex items-center justify-center text-xs font-bold text-slate-600">
                                                {idx + 1}
                                            </div>
                                            <span className="text-sm font-semibold uppercase tracking-widest text-slate-500">Step</span>
                                        </div>
                                        <h3 className="text-xl md:text-2xl font-bold text-slate-900 leading-tight">{rec.skill}</h3>
                                    </div>
                                    <span className={`self-start rounded-full px-4 py-1.5 text-xs font-bold uppercase tracking-[0.15em] border shadow-sm ${badgeClass}`}>
                                        {rec.priority} Priority
                                    </span>
                                </div>
                                
                                <div className="space-y-4">
                                    <div className="bg-slate-50 rounded-2xl p-5 border border-slate-100">
                                        <h4 className="text-xs font-bold uppercase tracking-widest text-slate-500 mb-2 flex items-center gap-2">
                                            <svg className="w-4 h-4 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                                            Why it matters
                                        </h4>
                                        <p className="text-sm md:text-base text-slate-700 leading-relaxed">{rec.reason}</p>
                                    </div>
                                    
                                    <div className="bg-indigo-50/50 rounded-2xl p-5 border border-indigo-100 relative overflow-hidden">
                                        <div className="absolute left-0 top-0 bottom-0 w-1 bg-indigo-500 rounded-l-2xl"></div>
                                        <h4 className="text-xs font-bold uppercase tracking-widest text-indigo-700 mb-2 flex items-center gap-2 pl-3">
                                            <svg className="w-4 h-4 text-indigo-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" /></svg>
                                            Action
                                        </h4>
                                        <p className="text-sm md:text-base text-slate-900 font-medium leading-relaxed pl-3">{rec.action}</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    );
                })}
            </div>
        </div>
    );
}
