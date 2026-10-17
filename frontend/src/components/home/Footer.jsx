import logoDark from "../../assets/logo_dark.png"

export default function Footer() {
    return (
        <footer className="bg-[var(--jj-navy)] border-t border-[var(--jj-deep-blue)] py-16 text-slate-300 relative z-30">
            <div className="mx-auto max-w-7xl px-6 lg:px-8">
                <div className="grid grid-cols-1 md:grid-cols-4 gap-12">

                    <div className="col-span-1 md:col-span-2">
                        <img
                            src={logoDark}
                            alt="JobJazz - Your career, in tune."
                            className="h-9 w-auto object-contain mb-4"
                        />
                        <p className="text-slate-400 text-sm max-w-xs leading-relaxed">
                            AI-powered career intelligence and personalized skill development roadmap platform.
                        </p>
                    </div>

                    <div>
                        <h3 className="text-sm font-bold text-white tracking-widest uppercase mb-4">Platform</h3>
                        <ul className="space-y-3 text-sm text-slate-400">
                            <li><a href="#workflow" className="hover:text-[var(--jj-primary-blue)] transition-colors">Career Workflow</a></li>
                            <li><a href="#how-it-works" className="hover:text-[var(--jj-primary-blue)] transition-colors">How It Works</a></li>
                            <li><a href="#insights" className="hover:text-[var(--jj-primary-blue)] transition-colors">Holistic Insights</a></li>
                            <li><a href="#about" className="hover:text-[var(--jj-primary-blue)] transition-colors">Architecture</a></li>
                        </ul>
                    </div>

                    <div>
                        <h3 className="text-sm font-bold text-white tracking-widest uppercase mb-4">Company</h3>
                        <ul className="space-y-3 text-sm text-slate-400">
                            <li><a href="#why-jobjazz" className="hover:text-[var(--jj-primary-blue)] transition-colors">Why JobJazz</a></li>
                            <li><a href="#about" className="hover:text-[var(--jj-primary-blue)] transition-colors">About</a></li>
                        </ul>
                    </div>

                </div>

                <div className="mt-16 pt-8 border-t border-[var(--jj-deep-blue)] text-sm text-slate-500 flex flex-col sm:flex-row items-center justify-between gap-4">
                    <p>&copy; 2026 JobJazz. All rights reserved.</p>
                    <p className="text-xs text-slate-500">Your career, in tune.</p>
                </div>
            </div>
        </footer>
    )
}
