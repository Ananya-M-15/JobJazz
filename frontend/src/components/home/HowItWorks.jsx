export default function HowItWorks() {
    return (
        <section id="how-it-works" className="relative z-10 bg-white py-24 sm:py-32">
            <div className="mx-auto max-w-7xl px-6 lg:px-8">
                
                <div className="mx-auto max-w-2xl text-center">
                    <h2 className="text-3xl font-bold tracking-tight text-slate-900 sm:text-4xl">
                        How JobJazz works
                    </h2>
                </div>

                <div className="mx-auto mt-16 max-w-4xl sm:mt-20 lg:mt-24">
                    <dl className="grid grid-cols-1 gap-12 lg:grid-cols-3 lg:gap-16">
                        
                        <div className="flex flex-col">
                            <dt className="text-lg font-semibold leading-7 text-slate-900">
                                <span className="text-sm font-bold text-indigo-600 block mb-2">01 &mdash;</span>
                                Upload your resume
                            </dt>
                            <dd className="mt-2 flex flex-auto flex-col text-base leading-7 text-slate-600">
                                <p className="flex-auto">
                                    Build a structured profile from your experience, skills, education and projects.
                                </p>
                            </dd>
                        </div>
                        
                        <div className="flex flex-col">
                            <dt className="text-lg font-semibold leading-7 text-slate-900">
                                <span className="text-sm font-bold text-indigo-600 block mb-2">02 &mdash;</span>
                                Add the job description
                            </dt>
                            <dd className="mt-2 flex flex-auto flex-col text-base leading-7 text-slate-600">
                                <p className="flex-auto">
                                    Paste the job description or upload the PDF you're applying to.
                                </p>
                            </dd>
                        </div>

                        <div className="flex flex-col">
                            <dt className="text-lg font-semibold leading-7 text-slate-900">
                                <span className="text-sm font-bold text-indigo-600 block mb-2">03 &mdash;</span>
                                Understand your fit
                            </dt>
                            <dd className="mt-2 flex flex-auto flex-col text-base leading-7 text-slate-600">
                                <p className="flex-auto">
                                    See what matches, what's missing and what to focus on next.
                                </p>
                            </dd>
                        </div>

                    </dl>
                </div>

            </div>
        </section>
    )
}
