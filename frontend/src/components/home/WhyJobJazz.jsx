export default function WhyJobJazz() {
    return (
        <section className="relative z-10 w-full py-24 sm:py-32 bg-[var(--jj-deep-blue)] text-white overflow-hidden scroll-mt-20" id="why-jobjazz">
            <div className="absolute top-0 left-0 w-[600px] h-[600px] rounded-full border-[80px] border-[var(--jj-navy)] opacity-50 -translate-x-1/2 -translate-y-1/2 blur-2xl"></div>

            <div className="mx-auto max-w-7xl px-6 lg:px-8 relative z-10">
                <div className="mx-auto max-w-2xl text-center mb-16">
                    <h2 className="text-3xl font-bold tracking-tight text-white sm:text-4xl">
                        Built to explain your fit, not just score it.
                    </h2>
                </div>

                <div className="mx-auto max-w-5xl">
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-12 border-t border-[var(--jj-primary-blue)]/30 pt-16">

                        <div>
                            <h3 className="text-xl font-bold text-white mb-4">TRANSPARENT</h3>
                            <p className="text-slate-300">
                                See exactly what matched and what didn't. No hidden algorithms, just a clear comparison against the requirements.
                            </p>
                        </div>

                        <div>
                            <h3 className="text-xl font-bold text-white mb-4">PRACTICAL</h3>
                            <p className="text-slate-300">
                                Turn gaps into concrete next steps. Understand what's critical and what you should focus on improving.
                            </p>
                        </div>

                        <div>
                            <h3 className="text-xl font-bold text-white mb-4">GROUNDED</h3>
                            <p className="text-slate-300">
                                Recommendations are based entirely on the reality of the resume and job requirements provided, nothing more.
                            </p>
                        </div>

                    </div>
                </div>
            </div>
        </section>
    )
}
