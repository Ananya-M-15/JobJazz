import { Sparkles } from "lucide-react"

export default function Navbar({ onAnalyzeClick }) {
    return (
        <nav className="fixed top-0 w-full z-50 bg-white/80 backdrop-blur-md border-b border-slate-200">
            <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4 lg:px-8">
                
                {/* Logo */}
                <div className="flex items-center gap-3">
                    <span className="text-xl font-bold tracking-tight text-slate-900 flex items-center gap-2">
                        <Sparkles size={20} className="text-indigo-600" />
                        JobJazz
                    </span>
                </div>

                {/* Navigation */}
                <div className="hidden items-center gap-8 md:flex">
                    <a href="#how-it-works" className="text-sm font-medium text-slate-500 hover:text-slate-900 transition-colors">
                        How it works
                    </a>
                    <a href="#about" className="text-sm font-medium text-slate-500 hover:text-slate-900 transition-colors">
                        About
                    </a>
                </div>

                {/* CTA */}
                <div className="flex items-center gap-4">
                    <button 
                        onClick={onAnalyzeClick}
                        className="hidden items-center gap-2 rounded-lg bg-indigo-50 px-4 py-2 text-sm font-semibold text-indigo-700 transition hover:bg-indigo-100 md:flex"
                    >
                        Analyze my resume
                    </button>
                </div>

            </div>
        </nav>
    )
}