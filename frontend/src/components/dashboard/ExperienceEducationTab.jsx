export default function ExperienceEducationTab({ matchResult, skillGap }) {
    return (
        <div className="animate-in fade-in slide-in-from-bottom-2 duration-500 space-y-6">
            <div className="rounded-3xl border border-slate-200 bg-white p-6 md:p-10 shadow-sm">
                <div className="flex flex-col md:flex-row md:items-start gap-6">
                    <div className="flex-shrink-0 mt-1">
                        <div className={`flex items-center justify-center w-12 h-12 rounded-2xl border shadow-sm ${matchResult?.experience_match ? 'bg-emerald-50 border-emerald-200 text-emerald-600' : 'bg-rose-50 border-rose-200 text-rose-600'}`}>
                            <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                            </svg>
                        </div>
                    </div>
                    <div>
                        <h2 className="text-sm font-semibold uppercase tracking-widest text-slate-500 mb-2">Experience Alignment</h2>
                        <h3 className={`text-xl font-bold mb-4 ${matchResult?.experience_match ? 'text-slate-900' : 'text-rose-600'}`}>
                            {matchResult?.experience_match ? 'Experience Requirements Met' : 'Experience Gap Detected'}
                        </h3>
                        <div className="bg-slate-50 rounded-xl p-5 border border-slate-100">
                            <p className="text-slate-700 leading-relaxed text-base md:text-lg">
                                {skillGap?.experience_gap || matchResult?.experience_notes || "No notes provided."}
                            </p>
                        </div>
                    </div>
                </div>
            </div>

            <div className="rounded-3xl border border-slate-200 bg-white p-6 md:p-10 shadow-sm">
                <div className="flex flex-col md:flex-row md:items-start gap-6">
                    <div className="flex-shrink-0 mt-1">
                        <div className={`flex items-center justify-center w-12 h-12 rounded-2xl border shadow-sm ${matchResult?.education_match ? 'bg-emerald-50 border-emerald-200 text-emerald-600' : 'bg-rose-50 border-rose-200 text-rose-600'}`}>
                            <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path d="M12 14l9-5-9-5-9 5 9 5z" />
                                <path d="M12 14l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14z" />
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 14l9-5-9-5-9 5 9 5zm0 0l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14zm-4 6v-7.5l4-2.222" />
                            </svg>
                        </div>
                    </div>
                    <div>
                        <h2 className="text-sm font-semibold uppercase tracking-widest text-slate-500 mb-2">Education Alignment</h2>
                        <h3 className={`text-xl font-bold mb-4 ${matchResult?.education_match ? 'text-slate-900' : 'text-rose-600'}`}>
                            {matchResult?.education_match ? 'Education Requirements Met' : 'Education Gap Detected'}
                        </h3>
                        <div className="bg-slate-50 rounded-xl p-5 border border-slate-100">
                            <p className="text-slate-700 leading-relaxed text-base md:text-lg">
                                {skillGap?.education_gap || matchResult?.education_notes || "No notes provided."}
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
