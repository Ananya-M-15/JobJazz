import { useState } from "react"
import { ArrowDown, Info } from "lucide-react"

export default function ArchitectureDiagram() {
    const [activeIndex, setActiveIndex] = useState(0)

    const nodes = [
        {
            title: "RESUME PDF",
            description: "The pipeline begins by securely ingesting your uploaded resume in PDF format for high-fidelity processing."
        },
        {
            title: "DOCUMENT EXTRACTION",
            description: "Advanced text parsers and OCR technology extract raw content, preserving context and timeline information."
        },
        {
            title: "STRUCTURED PROFILE",
            description: "The raw text is transformed into a standardized career profile, categorizing your specific skills, experience, and education."
        },
        {
            title: "JOB DESCRIPTION ANALYSIS",
            description: "The target job description is deeply analyzed to identify core requirements, preferred skills, and underlying keywords."
        },
        {
            title: "MATCHING ENGINE",
            description: "Our core engine compares your structured profile against the job requirements to determine a precise alignment score."
        },
        {
            title: "SKILL GAP ENGINE",
            description: "Automatically identifies critical missing skills or experience gaps between your current profile and the target role."
        },
        {
            title: "RECOMMENDATIONS",
            description: "Generates personalized, actionable steps and learning paths to bridge identified gaps and improve your chances."
        },
        {
            title: "DASHBOARD",
            description: "Presents the final comprehensive analysis in an interactive, easy-to-understand dashboard for rapid decision making."
        }
    ]

    return (
        <section className="relative z-10 w-full py-24 sm:py-32 bg-white border-y border-[var(--jj-border)] overflow-hidden scroll-mt-20" id="about">
            {/* Subtle grid background */}
            <div className="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjAiIGhlaWdodD0iNjAiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxwYXRoIGQ9Ik02MCAwaC0xdjYwaDFWMHptLTYwIDYwaDYwdi0xSDB2MXoiIGZpbGw9IiNlMmU4ZjAiIGZpbGwtcnVsZT0iZXZlbm9kZCIgZmlsbC1vcGFjaXR5PSIuNSIvPgo8L3N2Zz4=')] opacity-[0.3]"></div>

            <div className="mx-auto max-w-7xl px-6 lg:px-8 relative z-10">
                <div className="mx-auto max-w-2xl text-center mb-16">
                    <h2 className="text-3xl font-bold tracking-tight text-[var(--jj-navy)] sm:text-4xl">
                        From documents to useful decisions.
                    </h2>
                    <p className="mt-4 text-lg text-slate-600">
                        The structured product architecture behind every analysis.
                    </p>
                </div>

                {/* DESKTOP: Split Layout */}
                <div className="hidden lg:grid grid-cols-2 gap-12 items-center mx-auto max-w-6xl">

                    {/* Left: Circular Flowchart (Smaller) */}
                    <div className="relative w-full max-w-[500px] h-[500px] mx-auto">

                        {/* SVG Background Ring */}
                        <svg className="absolute inset-0 w-full h-full" viewBox="0 0 500 500" fill="none">
                            <circle cx="250" cy="250" r="180" stroke="var(--jj-primary-blue)" strokeWidth="1.5" className="opacity-20" />
                        </svg>

                        {/* Circular Nodes */}
                        {nodes.map((node, i) => {
                            const angle = (i * 45 - 90) * (Math.PI / 180)
                            const left = `${50 + 36 * Math.cos(angle)}%`
                            const top = `${50 + 36 * Math.sin(angle)}%`
                            const isActive = activeIndex === i

                            return (
                                <div
                                    key={node.title}
                                    className="absolute -translate-x-1/2 -translate-y-1/2 w-[130px] flex justify-center group cursor-pointer"
                                    style={{ left, top }}
                                    onClick={() => setActiveIndex(i)}
                                >
                                    <div className={`relative bg-white border ${isActive ? 'border-[var(--jj-primary-blue)] shadow-lg scale-105' : 'border-[var(--jj-border)] shadow-sm hover:border-[var(--jj-primary-blue)] hover:shadow-md'} rounded-xl py-2.5 px-3 text-center transition-all duration-300 z-10 overflow-hidden w-full`}>
                                        <div className={`absolute left-0 top-0 bottom-0 w-1 ${isActive ? 'bg-[var(--jj-primary-blue)]' : 'bg-[var(--jj-pale-blue)] group-hover:bg-[var(--jj-primary-blue)]'} transition-colors duration-300`}></div>
                                        <span className={`text-[9px] font-bold tracking-wider leading-tight block ${isActive ? 'text-[var(--jj-primary-blue)]' : 'text-[var(--jj-navy)]'} transition-colors`}>{node.title}</span>
                                    </div>
                                </div>
                            )
                        })}
                    </div>

                    {/* Right: Description Panel */}
                    <div className="flex flex-col justify-center max-w-md mx-auto lg:mx-0 lg:pl-10">
                        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-[var(--jj-pale-blue)] bg-slate-50 text-xs font-semibold text-[var(--jj-primary-blue)] tracking-wide uppercase mb-6 shadow-sm w-max">
                            <Info className="w-3.5 h-3.5" />
                            Step {activeIndex + 1} of 8
                        </div>
                        <h3 className="text-3xl font-extrabold text-[var(--jj-navy)] mb-4 leading-tight">
                            {nodes[activeIndex].title}
                        </h3>
                        <p className="text-lg text-slate-600 leading-relaxed">
                            {nodes[activeIndex].description}
                        </p>

                        {/* Progress Indicators */}
                        <div className="mt-10 flex items-center gap-2">
                            {nodes.map((_, i) => (
                                <button
                                    key={i}
                                    onClick={() => setActiveIndex(i)}
                                    className={`h-1.5 rounded-full transition-all duration-300 ${activeIndex === i ? 'w-8 bg-[var(--jj-primary-blue)]' : 'w-2 bg-slate-200 hover:bg-slate-300'}`}
                                    aria-label={`Go to step ${i + 1}`}
                                />
                            ))}
                        </div>
                    </div>
                </div>

                {/* MOBILE/TABLET: Vertical Flowchart */}
                <div className="lg:hidden mx-auto max-w-md flex flex-col items-center mt-12 gap-3">
                    {nodes.map((node, i) => (
                        <div key={node.title} className="flex flex-col items-center w-full group cursor-pointer" onClick={() => setActiveIndex(i)}>
                            <div className={`relative w-full bg-white border ${activeIndex === i ? 'border-[var(--jj-primary-blue)] shadow-md' : 'border-[var(--jj-border)] shadow-sm'} rounded-xl p-5 text-center transition-all overflow-hidden`}>
                                <div className={`absolute left-0 top-0 bottom-0 w-1.5 ${activeIndex === i ? 'bg-[var(--jj-primary-blue)]' : 'bg-[var(--jj-pale-blue)]'} transition-colors duration-300`}></div>
                                <span className={`text-sm font-bold tracking-widest ${activeIndex === i ? 'text-[var(--jj-primary-blue)]' : 'text-[var(--jj-navy)]'}`}>{node.title}</span>

                                {activeIndex === i && (
                                    <p className="mt-3 text-sm text-slate-600 leading-relaxed text-left border-t border-slate-100 pt-3">
                                        {node.description}
                                    </p>
                                )}
                            </div>

                            {i < nodes.length - 1 && (
                                <div className="flex flex-col items-center my-1 text-[var(--jj-border)]">
                                    <ArrowDown className="w-5 h-5 text-[var(--jj-primary-blue)] opacity-50" />
                                </div>
                            )}
                        </div>
                    ))}
                </div>
            </div>
        </section>
    )
}
