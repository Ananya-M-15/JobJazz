import { ArrowRight, FileText, Briefcase, GitCompare, AlertCircle, Map } from "lucide-react"

export default function WorkflowFlow() {
    const stages = [
        {
            num: "01",
            title: "RESUME",
            icon: <FileText className="w-5 h-5" />,
            items: ["Skills", "Experience", "Education", "Projects"]
        },
        {
            num: "02",
            title: "JOB",
            icon: <Briefcase className="w-5 h-5" />,
            items: ["Requirements", "Skills", "Experience", "Keywords"]
        },
        {
            num: "03",
            title: "MATCH",
            icon: <GitCompare className="w-5 h-5" />,
            items: ["Strengths", "Matches", "Requirements", "Alignment"]
        },
        {
            num: "04",
            title: "GAPS",
            icon: <AlertCircle className="w-5 h-5" />,
            items: ["Critical", "Preferred", "Experience", "Missing"]
        },
        {
            num: "05",
            title: "ACTION",
            icon: <Map className="w-5 h-5" />,
            items: ["Priorities", "Reasons", "Next steps", "Focus"]
        }
    ]

    return (
        <section className="relative z-10 w-full py-24 sm:py-32 bg-white scroll-mt-20" id="workflow">
            <div className="mx-auto max-w-7xl px-6 lg:px-8">

                <div className="mx-auto max-w-2xl text-center">
                    <h2 className="text-3xl font-bold tracking-tight text-[var(--jj-navy)] sm:text-4xl">
                        From resume to decision.
                    </h2>
                    <p className="mt-4 text-lg text-slate-600">
                        JobJazz turns the information in your resume and the requirements of a job into a structured view of your fit.
                    </p>
                </div>

                <div className="mx-auto mt-16 max-w-7xl">
                    <div className="flex flex-col lg:flex-row items-center justify-between gap-4 lg:gap-2">
                        {stages.map((stage, i) => (
                            <div key={stage.title} className="flex flex-col lg:flex-row items-center w-full lg:w-auto lg:flex-1">

                                {/* Stage Card */}
                                <div className="group relative w-full bg-white border border-[var(--jj-border)] rounded-2xl p-5 xl:p-6 shadow-[0_4px_20px_-4px_rgba(0,0,0,0.05)] hover:shadow-[0_10px_40px_-10px_rgba(49,92,246,0.2)] hover:border-[var(--jj-primary-blue)] hover:-translate-y-2 transition-all duration-300 overflow-hidden">
                                    {/* Top accent line */}
                                    <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-[var(--jj-pale-blue)] to-[var(--jj-border)] group-hover:from-[var(--jj-primary-blue)] group-hover:to-[var(--jj-indigo)] transition-all duration-300"></div>

                                    <div className="flex items-center justify-between mb-5 mt-2">
                                        <span className="text-xs font-bold text-slate-300 font-mono group-hover:text-[var(--jj-primary-blue)] transition-colors">{stage.num}</span>
                                        <div className="text-slate-400 group-hover:text-[var(--jj-primary-blue)] transition-colors transform group-hover:scale-110">
                                            {stage.icon}
                                        </div>
                                    </div>
                                    <h3 className="text-[13px] xl:text-sm font-bold tracking-widest text-[var(--jj-navy)] mb-4 uppercase">{stage.title}</h3>
                                    <ul className="space-y-2.5">
                                        {stage.items.map((item, j) => (
                                            <li key={j} className="text-[13px] xl:text-sm text-slate-500 flex items-center gap-2 group-hover:text-slate-700 transition-colors">
                                                <div className="w-1.5 h-1.5 rounded-full flex-shrink-0 bg-slate-200 group-hover:bg-[var(--jj-primary-blue)] group-hover:shadow-[0_0_5px_rgba(49,92,246,0.5)] transition-all"></div>
                                                <span className="truncate">{item}</span>
                                            </li>
                                        ))}
                                    </ul>
                                </div>

                                {/* Connector */}
                                {i < stages.length - 1 && (
                                    <div className="hidden lg:flex items-center justify-center w-6 xl:w-8 h-8 text-slate-300 mx-1 xl:mx-2 flex-shrink-0">
                                        <ArrowRight className="w-4 h-4 xl:w-5 xl:h-5" />
                                    </div>
                                )}
                                {i < stages.length - 1 && (
                                    <div className="lg:hidden flex items-center justify-center h-8 w-full text-slate-300 my-2">
                                        <ArrowRight className="w-5 h-5 rotate-90" />
                                    </div>
                                )}
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </section>
    )
}
