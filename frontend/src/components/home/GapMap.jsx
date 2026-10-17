export default function GapMap() {
    return (
        <section className="relative z-10 w-full py-24 sm:py-32 bg-white">
            <div className="mx-auto max-w-7xl px-6 lg:px-8">

                <div className="mx-auto max-w-2xl text-center mb-16">
                    <h2 className="text-3xl font-bold tracking-tight text-[var(--jj-navy)] sm:text-4xl">
                        Don't stop at the score.
                    </h2>
                    <p className="mt-4 text-lg text-slate-600">
                        A match score alone does not explain what a candidate should do next. We break it down into actionable categories.
                    </p>
                </div>

                {/* Gap Map Diagram */}
                <div className="mx-auto max-w-4xl relative">

                    {/* Top Node */}
                    <div className="flex justify-center mb-12">
                        <div className="px-6 py-3 rounded-full bg-[var(--jj-navy)] text-white font-semibold text-sm shadow-md z-20 relative">
                            YOUR PROFILE
                        </div>
                    </div>

                    {/* Connector lines (Desktop) */}
                    <div className="hidden md:block absolute top-[23px] left-[16.6%] right-[16.6%] h-px bg-gradient-to-r from-transparent via-[var(--jj-primary-blue)] to-transparent opacity-40"></div>
                    <div className="hidden md:block absolute top-[23px] left-1/2 w-px h-[40px] bg-[var(--jj-primary-blue)] opacity-40 -translate-x-1/2"></div>
                    <div className="hidden md:block absolute top-[23px] left-[16.6%] w-px h-[40px] bg-gradient-to-b from-[var(--jj-primary-blue)] to-transparent opacity-40"></div>
                    <div className="hidden md:block absolute top-[23px] right-[16.6%] w-px h-[40px] bg-gradient-to-b from-[var(--jj-primary-blue)] to-transparent opacity-40"></div>

                    {/* Three Columns */}
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-6 lg:gap-8 mb-12 relative z-10 mt-10">
                        {/* Column 1 */}
                        <div className="flex flex-col items-center mt-6 md:mt-0">
                            <div className="w-full bg-white border border-[var(--jj-border)] rounded-2xl p-8 shadow-[0_4px_20px_-4px_rgba(0,0,0,0.05)] hover:shadow-[0_10px_40px_-10px_rgba(49,92,246,0.15)] hover:border-[var(--jj-primary-blue)]/50 transition-all duration-300 hover:-translate-y-1 relative overflow-hidden group">
                                <div className="absolute top-0 left-0 w-full h-1 bg-[var(--jj-pale-blue)] group-hover:bg-green-400 transition-colors"></div>
                                <h3 className="text-xs font-bold tracking-[0.2em] text-slate-400 mb-3 uppercase text-center group-hover:text-green-500 transition-colors">Matches</h3>
                                <h4 className="text-xl font-bold text-[var(--jj-navy)] mb-2 text-center">Strengths</h4>
                                <p className="text-sm text-slate-500 text-center font-light">What already aligns.</p>
                            </div>
                        </div>

                        {/* Column 2 */}
                        <div className="flex flex-col items-center gap-6 mt-6 md:mt-0 relative">
                            <div className="w-full bg-white border border-[var(--jj-primary-blue)]/30 rounded-2xl p-8 shadow-[0_4px_20px_-4px_rgba(49,92,246,0.1)] hover:shadow-[0_10px_40px_-10px_rgba(49,92,246,0.25)] hover:border-[var(--jj-primary-blue)] transition-all duration-300 hover:-translate-y-1 relative overflow-hidden group z-10">
                                <div className="absolute top-0 left-0 w-full h-1 bg-[var(--jj-primary-blue)]"></div>
                                <h3 className="text-xs font-bold tracking-[0.2em] text-[var(--jj-primary-blue)] mb-3 uppercase text-center">Gaps</h3>
                                <h4 className="text-xl font-bold text-[var(--jj-navy)] mb-2 text-center">Critical Gaps</h4>
                                <p className="text-sm text-slate-500 text-center font-light">Important requirements that are missing.</p>
                            </div>

                            {/* Vertical connector between gaps */}
                            <div className="hidden md:block absolute top-[120px] left-1/2 w-px h-[40px] bg-gradient-to-b from-[var(--jj-primary-blue)] to-transparent opacity-30 -translate-x-1/2"></div>

                            <div className="w-full bg-white border border-[var(--jj-border)] rounded-2xl p-8 shadow-[0_4px_20px_-4px_rgba(0,0,0,0.05)] hover:shadow-[0_10px_40px_-10px_rgba(49,92,246,0.15)] hover:border-[var(--jj-primary-blue)]/50 transition-all duration-300 hover:-translate-y-1 relative overflow-hidden group">
                                <div className="absolute top-0 left-0 w-full h-1 bg-[var(--jj-pale-blue)] group-hover:bg-[var(--jj-mid-blue)] transition-colors"></div>
                                <h4 className="text-lg font-bold text-[var(--jj-navy)] mb-2 text-center mt-2">Preferred Gaps</h4>
                                <p className="text-sm text-slate-500 text-center font-light">Useful requirements not currently covered.</p>
                            </div>
                        </div>

                        {/* Column 3 */}
                        <div className="flex flex-col items-center mt-6 md:mt-0">
                            <div className="w-full bg-white border border-[var(--jj-border)] rounded-2xl p-8 shadow-[0_4px_20px_-4px_rgba(0,0,0,0.05)] hover:shadow-[0_10px_40px_-10px_rgba(49,92,246,0.15)] hover:border-[var(--jj-primary-blue)]/50 transition-all duration-300 hover:-translate-y-1 relative overflow-hidden group">
                                <div className="absolute top-0 left-0 w-full h-1 bg-[var(--jj-pale-blue)] group-hover:bg-slate-400 transition-colors"></div>
                                <h3 className="text-xs font-bold tracking-[0.2em] text-slate-400 mb-3 uppercase text-center group-hover:text-slate-600 transition-colors">Requirements</h3>
                                <h4 className="text-xl font-bold text-[var(--jj-navy)] mb-2 text-center">Experience & Education </h4>
                                <p className="text-sm text-slate-500 text-center font-light">Additional constraints affecting alignment.</p>
                            </div>
                        </div>
                    </div>

                    {/* Bottom Node */}
                    <div className="hidden md:block absolute bottom-[80px] left-1/2 w-[2px] h-[30px] bg-[var(--jj-primary-blue)] opacity-20 -translate-x-1/2"></div>
                    <div className="flex justify-center mt-12 relative z-20">
                        <div className="px-6 py-3 rounded-full bg-[var(--jj-primary-blue)] text-white font-semibold text-sm shadow-md">
                            PRIORITIES
                        </div>
                    </div>
                </div>

            </div>
        </section>
    )
}
