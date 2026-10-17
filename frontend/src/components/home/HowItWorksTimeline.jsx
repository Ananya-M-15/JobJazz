export default function HowItWorksTimeline() {
    return (
        <section className="relative w-full py-24 sm:py-32 bg-[var(--jj-background)] scroll-mt-20" id="how-it-works">
            <div className="mx-auto max-w-7xl px-6 lg:px-8">

                <div className="mx-auto max-w-2xl text-center mb-20">
                    <h2 className="text-3xl font-bold tracking-tight text-[var(--jj-navy)] sm:text-4xl">
                        Three steps between you and a clearer application.
                    </h2>
                </div>

                <div className="relative mx-auto max-w-6xl">
                    {/* Desktop horizontal connector */}
                    <div className="hidden lg:block absolute top-8 left-[10%] right-[10%] h-[2px] bg-gradient-to-r from-transparent via-[var(--jj-primary-blue)] to-transparent opacity-20"></div>
                    <div className="hidden lg:block absolute top-8 left-1/2 w-[60%] h-[2px] bg-[var(--jj-primary-blue)] opacity-50 blur-sm -translate-x-1/2"></div>

                    <div className="grid grid-cols-1 lg:grid-cols-3 gap-12 relative z-10">
                        {/* Step 1 */}
                        <div className="group relative bg-white/80 backdrop-blur-md border border-[var(--jj-border)] rounded-2xl p-8 shadow-[0_4px_20px_-4px_rgba(0,0,0,0.05)] hover:border-[var(--jj-primary-blue)]/50 hover:shadow-[0_10px_40px_-10px_rgba(49,92,246,0.15)] transition-all duration-300 hover:-translate-y-2 overflow-hidden">
                            <div className="absolute top-0 right-0 w-32 h-32 bg-[var(--jj-pale-blue)] rounded-full blur-3xl opacity-0 group-hover:opacity-100 transition-opacity duration-500 -z-10"></div>
                            <div className="w-16 h-16 rounded-2xl bg-[var(--jj-background)] flex items-center justify-center mx-auto mb-8 relative z-10 group-hover:bg-gradient-to-br group-hover:from-[var(--jj-primary-blue)] group-hover:to-[var(--jj-indigo)] group-hover:shadow-[0_4px_15px_rgba(49,92,246,0.4)] transition-all duration-300">
                                <span className="text-xl font-bold font-mono text-[var(--jj-primary-blue)] group-hover:text-white transition-colors">01</span>
                            </div>
                            <h3 className="text-xl font-bold text-center text-[var(--jj-navy)] mb-4 group-hover:text-[var(--jj-primary-blue)] transition-colors">Upload your resume</h3>
                            <p className="text-slate-600 text-center font-light">
                                Build a structured profile from your experience, skills, education and projects.
                            </p>
                        </div>

                        {/* Step 2 */}
                        <div className="group relative bg-white/80 backdrop-blur-md border border-[var(--jj-border)] rounded-2xl p-8 shadow-[0_4px_20px_-4px_rgba(0,0,0,0.05)] hover:border-[var(--jj-primary-blue)]/50 hover:shadow-[0_10px_40px_-10px_rgba(49,92,246,0.15)] transition-all duration-300 hover:-translate-y-2 overflow-hidden">
                            <div className="absolute top-0 right-0 w-32 h-32 bg-[var(--jj-pale-blue)] rounded-full blur-3xl opacity-0 group-hover:opacity-100 transition-opacity duration-500 -z-10"></div>
                            <div className="w-16 h-16 rounded-2xl bg-[var(--jj-background)] flex items-center justify-center mx-auto mb-8 relative z-10 group-hover:bg-gradient-to-br group-hover:from-[var(--jj-primary-blue)] group-hover:to-[var(--jj-indigo)] group-hover:shadow-[0_4px_15px_rgba(49,92,246,0.4)] transition-all duration-300">
                                <span className="text-xl font-bold font-mono text-[var(--jj-primary-blue)] group-hover:text-white transition-colors">02</span>
                            </div>
                            <h3 className="text-xl font-bold text-center text-[var(--jj-navy)] mb-4 group-hover:text-[var(--jj-primary-blue)] transition-colors">Add the job description</h3>
                            <p className="text-slate-600 text-center font-light">
                                Paste the job description or upload the PDF you're applying to.
                            </p>
                        </div>

                        {/* Step 3 */}
                        <div className="group relative bg-white/80 backdrop-blur-md border border-[var(--jj-border)] rounded-2xl p-8 shadow-[0_4px_20px_-4px_rgba(0,0,0,0.05)] hover:border-[var(--jj-primary-blue)]/50 hover:shadow-[0_10px_40px_-10px_rgba(49,92,246,0.15)] transition-all duration-300 hover:-translate-y-2 overflow-hidden">
                            <div className="absolute top-0 right-0 w-32 h-32 bg-[var(--jj-pale-blue)] rounded-full blur-3xl opacity-0 group-hover:opacity-100 transition-opacity duration-500 -z-10"></div>
                            <div className="w-16 h-16 rounded-2xl bg-[var(--jj-background)] flex items-center justify-center mx-auto mb-8 relative z-10 group-hover:bg-gradient-to-br group-hover:from-[var(--jj-primary-blue)] group-hover:to-[var(--jj-indigo)] group-hover:shadow-[0_4px_15px_rgba(49,92,246,0.4)] transition-all duration-300">
                                <span className="text-xl font-bold font-mono text-[var(--jj-primary-blue)] group-hover:text-white transition-colors">03</span>
                            </div>
                            <h3 className="text-xl font-bold text-center text-[var(--jj-navy)] mb-4 group-hover:text-[var(--jj-primary-blue)] transition-colors">Understand your fit</h3>
                            <p className="text-slate-600 text-center font-light">
                                See what matches, what's missing, and what to focus on next.
                            </p>
                        </div>
                    </div>
                </div>

            </div>
        </section>
    )
}
