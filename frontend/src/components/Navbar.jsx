import { Sparkles, ChevronDown, Menu } from "lucide-react"

export default function Navbar({ onAnalyzeClick }) {
    return (
        <nav className="fixed top-0 left-0 w-full z-50 bg-white/95 backdrop-blur-md border-b border-slate-200 transition-all shadow-sm">
            <div className="mx-auto flex w-full max-w-7xl items-center justify-between px-6 py-2.5 lg:px-8">
                
                {/* Logo */}
                <div className="flex items-center gap-3">
                    <span className="text-xl font-bold tracking-tight text-slate-900 flex items-center gap-2 cursor-pointer" onClick={() => window.scrollTo(0,0)}>
                        <Sparkles size={20} className="text-blue-600" />
                        JobJazz
                    </span>
                </div>

                {/* Navigation Desktop */}
                <div className="hidden lg:flex items-center gap-8">
                    <div className="relative group cursor-pointer">
                        <span className="flex items-center gap-1 text-[13px] font-semibold text-slate-700 group-hover:text-blue-600 transition-colors py-2">
                            Product <ChevronDown size={14} className="opacity-60" />
                        </span>
                        <div className="absolute top-full left-0 mt-0 w-48 rounded-xl bg-white border border-slate-200 shadow-lg opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 p-2 translate-y-2 group-hover:translate-y-0">
                            {['Resume analysis', 'Job matching', 'Skill gaps', 'Action plan'].map(item => (
                                <a key={item} href="#how-it-works" className="block px-4 py-2 text-sm text-slate-700 hover:text-blue-600 hover:bg-slate-50 rounded-lg transition-colors">
                                    {item}
                                </a>
                            ))}
                        </div>
                    </div>
                    
                    <a href="#how-it-works" className="text-[13px] font-semibold text-slate-700 hover:text-blue-600 relative group transition-colors py-2">
                        How it works
                        <span className="absolute bottom-0 left-0 w-0 h-[2px] bg-blue-600 transition-all duration-300 group-hover:w-full rounded-full"></span>
                    </a>
                    <a href="#why-jobjazz" className="text-[13px] font-semibold text-slate-700 hover:text-blue-600 relative group transition-colors py-2">
                        Why JobJazz
                        <span className="absolute bottom-0 left-0 w-0 h-[2px] bg-blue-600 transition-all duration-300 group-hover:w-full rounded-full"></span>
                    </a>
                    <a href="#about" className="text-[13px] font-semibold text-slate-700 hover:text-blue-600 relative group transition-colors py-2">
                        About
                        <span className="absolute bottom-0 left-0 w-0 h-[2px] bg-blue-600 transition-all duration-300 group-hover:w-full rounded-full"></span>
                    </a>
                </div>

                {/* CTA & Mobile Toggle */}
                <div className="flex items-center gap-4">
                    <button 
                        onClick={onAnalyzeClick}
                        className="hidden md:flex bg-blue-600 text-white hover:bg-blue-700 py-1.5 px-5 rounded-lg text-sm font-semibold shadow-sm transition-colors"
                    >
                        Analyze my resume
                    </button>
                    
                    {/* Mobile Menu Toggle */}
                    <button className="lg:hidden text-slate-700 p-2">
                        <Menu size={24} />
                    </button>
                </div>

            </div>
        </nav>
    )
}