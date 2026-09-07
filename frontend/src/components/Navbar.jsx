import { BarChart3, Sparkles } from "lucide-react"

function Navbar() {
    return (
        <nav className="fixed left-1/2 top-5 z-50 w-[calc(100%-2rem)] max-w-6xl -translate-x-1/2">

            <div className="jj-glass flex items-center justify-between rounded-2xl px-5 py-3 shadow-2xl shadow-black/20">

                {/* Logo */}
                <div className="flex items-center gap-3">

                    <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-gradient-to-br from-cyan-300 via-violet-400 to-fuchsia-400 shadow-lg shadow-violet-500/20">
                        <Sparkles size={18} className="text-white" />
                    </div>

                    <span className="jj-display text-lg font-semibold tracking-tight">
                        JobJazz
                    </span>

                </div>


                {/* Navigation */}
                <div className="hidden items-center gap-8 md:flex">

                    <a
                        href="#analyze"
                        className="text-sm text-slate-400 transition-colors duration-200 hover:text-white"
                    >
                        Analyze
                    </a>

                    <a
                        href="#market"
                        className="text-sm text-slate-400 transition-colors duration-200 hover:text-white"
                    >
                        Job Market
                    </a>

                    <a
                        href="#how-it-works"
                        className="text-sm text-slate-400 transition-colors duration-200 hover:text-white"
                    >
                        How it works
                    </a>

                </div>


                {/* CTA */}
                <button className="hidden items-center gap-2 rounded-xl bg-white px-4 py-2 text-sm font-semibold text-slate-950 transition duration-300 hover:-translate-y-0.5 hover:bg-slate-100 md:flex">

                    <BarChart3 size={16} />

                    Analyze Resume

                </button>

            </div>

        </nav>
    )
}

export default Navbar