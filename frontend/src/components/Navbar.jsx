import { useState } from "react"
import { Menu, X } from "lucide-react"
import logoLight from "../assets/logo_light.png"

export default function Navbar() {
    const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

    const navLinks = [
        { label: "Workflow", href: "#workflow" },
        { label: "How it works", href: "#how-it-works" },
        { label: "Insights", href: "#insights" },
        { label: "Why JobJazz", href: "#why-jobjazz" },
        { label: "About", href: "#about" },
    ]

    return (
        <nav className="fixed top-0 left-0 w-full z-50 bg-white/95 backdrop-blur-md border-b border-slate-200 transition-all shadow-sm">
            <div className="mx-auto flex w-full max-w-7xl items-center justify-between px-6 py-2.5 lg:px-8">

                {/* Official Brand Logo */}
                <div className="flex items-center gap-3">
                    <button
                        type="button"
                        className="flex items-center gap-2 cursor-pointer focus:outline-none"
                        onClick={() => {
                            window.scrollTo({ top: 0, behavior: "smooth" })
                            setMobileMenuOpen(false)
                        }}
                        aria-label="JobJazz Home"
                    >
                        <img
                            src={logoLight}
                            alt="JobJazz - Your career, in tune."
                            className="h-8 md:h-9 w-auto object-contain"
                        />
                    </button>
                </div>

                {/* Navigation Desktop */}
                <div className="hidden lg:flex items-center gap-8">
                    {navLinks.map((link) => (
                        <a
                            key={link.label}
                            href={link.href}
                            className="text-[13px] font-semibold text-slate-700 hover:text-blue-600 relative group transition-colors py-2"
                        >
                            {link.label}
                            <span className="absolute bottom-0 left-0 w-0 h-[2px] bg-blue-600 transition-all duration-300 group-hover:w-full rounded-full"></span>
                        </a>
                    ))}
                </div>

                {/* Mobile Menu Toggle */}
                <div className="flex items-center lg:hidden">
                    <button
                        onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
                        className="text-slate-700 p-2 rounded-lg hover:bg-slate-100 transition-colors"
                        aria-label={mobileMenuOpen ? "Close menu" : "Open menu"}
                    >
                        {mobileMenuOpen ? <X size={22} /> : <Menu size={22} />}
                    </button>
                </div>

            </div>

            {/* Mobile Navigation Drawer */}
            {mobileMenuOpen && (
                <div className="lg:hidden border-t border-slate-200 bg-white/98 px-6 py-4 space-y-3 shadow-lg animate-in slide-in-from-top-2 duration-200">
                    {navLinks.map((link) => (
                        <a
                            key={link.label}
                            href={link.href}
                            onClick={() => setMobileMenuOpen(false)}
                            className="block text-sm font-semibold text-slate-700 hover:text-blue-600 py-1.5"
                        >
                            {link.label}
                        </a>
                    ))}
                </div>
            )}
        </nav>
    )
}
