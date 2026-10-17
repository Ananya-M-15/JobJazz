import { ArrowRight, PlayCircle, FileText, Target, GitMerge, CheckSquare, Sparkles } from "lucide-react"

export default function Hero({ onAnalyzeClick }) {
    return (
        <section className="relative w-full overflow-hidden bg-[#030712] pt-40 pb-24 sm:pt-48 lg:pb-32 border-b border-slate-800/50 flex flex-col items-center text-center">
            {/* Ambient deep space glow and textured 3D rings */}
            <div className="absolute inset-0 overflow-hidden pointer-events-none z-0">
                {/* Center glow */}
                <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[1000px] h-[1000px] bg-blue-900/10 blur-[150px] rounded-full"></div>

                {/* Left massive textured ring */}
                <div className="absolute top-[-20%] left-[-20%] w-[1200px] h-[1200px] rounded-full border-[100px] border-[#08132e]/80 shadow-[inset_0_0_150px_rgba(37,99,235,0.1),0_0_150px_rgba(30,58,138,0.2)] transform rotate-[15deg]"></div>

                {/* Right huge textured sweep */}
                <div className="absolute top-[10%] right-[-30%] w-[1500px] h-[1500px] rounded-full border-[150px] border-[#0b1b42]/60 shadow-[inset_40px_0_200px_rgba(59,130,246,0.15),-40px_0_150px_rgba(37,99,235,0.1)] transform -rotate-[25deg] mix-blend-lighten"></div>
            </div>

            <div className="relative z-10 w-full max-w-5xl px-6 lg:px-8 flex flex-col items-center">

                {/* Pill Badge */}
                <div className="inline-flex items-center justify-center gap-2 px-4 py-1.5 rounded-full border border-blue-500/30 bg-blue-500/10 text-[11px] font-bold text-blue-400 tracking-[0.25em] uppercase mb-8 shadow-[0_0_20px_rgba(59,130,246,0.1)]">
                    <Sparkles className="w-3 h-3" />
                    Your career, in tune
                </div>

                {/* Headline (Constrained max-width to guarantee exactly 2 lines on desktop) */}
                <h1 className="text-5xl font-extrabold tracking-tight text-white sm:text-6xl lg:text-[4.5rem] max-w-[900px] leading-[1.1] mb-8">
                    Make every application <span className="bg-gradient-to-r from-blue-400 via-blue-500 to-indigo-500 bg-clip-text text-transparent drop-shadow-[0_0_25px_rgba(59,130,246,0.4)]">count.</span>
                </h1>

                {/* Subtitle */}
                <p className="text-lg leading-8 text-slate-400 max-w-3xl font-light mb-12">
                    Understand how your resume aligns with the job before you apply. <br></br>
                    JobJazz highlights your strengths, identifies important gaps,
                    and gives you clear next steps.
                </p>

                {/* Buttons */}
                <div className="flex flex-col sm:flex-row items-center justify-center gap-5 w-full">
                    <button onClick={onAnalyzeClick} className="w-full sm:w-auto px-8 py-3.5 rounded-xl bg-blue-600 text-white font-semibold flex items-center justify-center hover:bg-blue-500 transition-colors shadow-[0_10px_30px_-10px_rgba(59,130,246,0.8)] group">
                        Analyze my resume
                        <ArrowRight className="ml-2 w-4 h-4 transition-transform group-hover:translate-x-1" />
                    </button>
                    <a href="#how-it-works" className="w-full sm:w-auto px-8 py-3.5 rounded-full border border-slate-700 bg-slate-900/50 backdrop-blur-sm text-slate-300 font-medium flex items-center justify-center hover:bg-slate-800 hover:text-white transition-colors group">
                        <PlayCircle className="w-5 h-5 mr-2 text-blue-500 group-hover:text-blue-400 transition-colors" />
                        See how it works
                    </a>
                </div>

                {/* Capability Strip (Forced to one line) */}
                <div className="mt-20 w-full flex justify-center border-t border-slate-800/80 pt-10">
                    <div className="flex items-center justify-center flex-wrap gap-x-8 gap-y-4 max-w-4xl">
                        {[
                            { icon: FileText, label: 'Resume analysis' },
                            { icon: GitMerge, label: 'Job matching' },
                            { icon: Target, label: 'Skill gaps' },
                            { icon: CheckSquare, label: 'Action plan' }
                        ].map((item) => (
                            <div key={item.label} className="flex items-center gap-2 whitespace-nowrap text-[15px] font-semibold text-slate-400 hover:text-slate-200 transition-colors">
                                <item.icon className="w-5 h-5 text-blue-500" />
                                <span>{item.label}</span>
                            </div>
                        ))}
                    </div>
                </div>

            </div>
        </section>
    )
}
