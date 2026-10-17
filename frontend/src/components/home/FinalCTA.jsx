export default function FinalCTA({ onAnalyzeClick }) {
    return (
        <section className="relative z-10 w-full pt-32 pb-48 bg-[var(--jj-background)] overflow-hidden">
            {/* Architectural Geometry */}
            <div className="absolute bottom-0 left-1/2 -translate-x-1/2 w-[1200px] h-[600px] rounded-t-full bg-gradient-to-b from-[var(--jj-pale-blue)] to-white border-t border-[var(--jj-border)] flex items-end justify-center">
                <div className="w-[1000px] h-[500px] rounded-t-full border-t border-[var(--jj-border)]/50"></div>
            </div>

            <div className="mx-auto max-w-2xl text-center relative z-20">
                <h2 className="text-3xl font-bold tracking-tight text-[var(--jj-navy)] sm:text-5xl">
                    Know where you stand before you apply.
                </h2>
                <p className="mt-6 text-lg leading-8 text-slate-600">
                    Understand your strengths, gaps, and next steps before sending your application.
                </p>
                <div className="mt-10 flex flex-col sm:flex-row items-center justify-center gap-6">
                    <button onClick={onAnalyzeClick} className="jj-btn-primary">
                        Analyze my resume
                    </button>
                    <a href="#how-it-works" className="text-sm font-semibold leading-6 text-[var(--jj-navy)] hover:text-[var(--jj-primary-blue)] transition-colors">
                        See how it works <span aria-hidden="true">→</span>
                    </a>
                </div>
            </div>
        </section>
    )
}
