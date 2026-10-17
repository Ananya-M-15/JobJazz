import { CheckCircle2, Briefcase, GraduationCap, Search } from "lucide-react"

export default function CapabilitiesAsymmetric() {
    const capabilities = [
        {
            num: "01",
            title: "Skills",
            desc: "See which requirements your resume already covers.",
            icon: CheckCircle2,
        },
        {
            num: "02",
            title: "Experience",
            desc: "Understand how your experience aligns with the role.",
            icon: Briefcase,
        },
        {
            num: "03",
            title: "Education",
            desc: "Check how your academic background matches the stated requirements.",
            icon: GraduationCap,
        },
        {
            num: "04",
            title: "Keywords & Gaps",
            desc: "Identify important requirements that need attention.",
            icon: Search,
        },
    ]

    return (
        <section className="relative z-10 w-full py-16 sm:py-20 lg:py-24 bg-[var(--jj-background)] overflow-hidden scroll-mt-20" id="insights">
            <div className="mx-auto max-w-7xl px-6 lg:px-8">

                <div className="mx-auto max-w-2xl text-center mb-12 sm:mb-16">
                    <h2 className="text-3xl font-bold tracking-tight text-[var(--jj-navy)] sm:text-4xl">
                        A resume is more than a list of skills.
                    </h2>
                    <p className="mt-4 text-base sm:text-lg text-slate-600">
                        JobJazz considers multiple dimensions of the candidate profile, ensuring a holistic understanding of how your background aligns with the job requirements.
                    </p>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 max-w-7xl mx-auto">
                    {capabilities.map((cap) => (
                        <div
                            key={cap.num}
                            className="group relative bg-white border border-[var(--jj-border)] rounded-2xl p-6 shadow-[0_4px_20px_-4px_rgba(0,0,0,0.05)] hover:shadow-[0_10px_40px_-10px_rgba(49,92,246,0.15)] hover:border-[var(--jj-primary-blue)]/50 transition-all duration-300 hover:-translate-y-1.5 overflow-hidden z-10 flex flex-col justify-between"
                        >
                            {/* Top subtle accent line on hover */}
                            <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-transparent to-transparent group-hover:from-[var(--jj-primary-blue)] group-hover:to-[var(--jj-indigo)] transition-all duration-300"></div>

                            {/* Glow accent */}
                            <div className="absolute top-0 right-0 w-28 h-28 bg-[var(--jj-pale-blue)] rounded-full blur-3xl opacity-0 group-hover:opacity-100 transition-opacity duration-500 -z-10"></div>

                            <div>
                                <div className="flex justify-between items-start mb-5">
                                    <div className="w-11 h-11 rounded-xl bg-[var(--jj-background)] flex items-center justify-center group-hover:bg-gradient-to-br group-hover:from-[var(--jj-primary-blue)] group-hover:to-[var(--jj-indigo)] group-hover:shadow-[0_4px_15px_rgba(49,92,246,0.4)] transition-all duration-300">
                                        <cap.icon className="w-5 h-5 text-[var(--jj-primary-blue)] group-hover:text-white transition-colors" />
                                    </div>
                                    <span className="text-xs font-bold text-slate-300 font-mono group-hover:text-[var(--jj-primary-blue)] transition-colors">
                                        {cap.num}
                                    </span>
                                </div>
                                <h3 className="text-lg font-bold text-[var(--jj-navy)] mb-2 group-hover:text-[var(--jj-primary-blue)] transition-colors">
                                    {cap.title}
                                </h3>
                                <p className="text-sm text-slate-600 font-light leading-relaxed">
                                    {cap.desc}
                                </p>
                            </div>
                        </div>
                    ))}
                </div>

            </div>
        </section>
    )
}
