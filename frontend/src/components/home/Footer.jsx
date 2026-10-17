import { Sparkles } from "lucide-react"

export default function Footer() {
    return (
        <footer className="bg-[var(--jj-navy)] border-t border-[var(--jj-deep-blue)] py-16 text-slate-300 relative z-30">
            <div className="mx-auto max-w-7xl px-6 lg:px-8">
                <div className="grid grid-cols-1 md:grid-cols-4 gap-12">
                    
                    <div className="col-span-1 md:col-span-2">
                        <span className="text-xl font-bold tracking-tight text-white flex items-center gap-2 mb-4">
                            <Sparkles size={20} className="text-[var(--jj-primary-blue)]" />
                            JobJazz
                        </span>
                        <p className="text-slate-400 text-sm max-w-xs">
                            Your career, in tune.
                        </p>
                    </div>
                    
                    <div>
                        <h3 className="text-sm font-bold text-white tracking-widest uppercase mb-4">Product</h3>
                        <ul className="space-y-3 text-sm text-slate-400">
                            <li><a href="#" className="hover:text-[var(--jj-primary-blue)] transition-colors">Resume analysis</a></li>
                            <li><a href="#" className="hover:text-[var(--jj-primary-blue)] transition-colors">Job matching</a></li>
                            <li><a href="#" className="hover:text-[var(--jj-primary-blue)] transition-colors">Skill gaps</a></li>
                            <li><a href="#" className="hover:text-[var(--jj-primary-blue)] transition-colors">Action plan</a></li>
                        </ul>
                    </div>

                    <div>
                        <h3 className="text-sm font-bold text-white tracking-widest uppercase mb-4">Company</h3>
                        <ul className="space-y-3 text-sm text-slate-400">
                            <li><a href="#how-it-works" className="hover:text-[var(--jj-primary-blue)] transition-colors">How it works</a></li>
                            <li><a href="#why-jobjazz" className="hover:text-[var(--jj-primary-blue)] transition-colors">Why JobJazz</a></li>
                            <li><a href="#about" className="hover:text-[var(--jj-primary-blue)] transition-colors">About</a></li>
                        </ul>
                    </div>

                </div>
                
                <div className="mt-16 pt-8 border-t border-[var(--jj-deep-blue)] text-sm text-slate-500">
                    <p>&copy; 2026 JobJazz</p>
                </div>
            </div>
        </footer>
    )
}
