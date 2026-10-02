function CareerProfile({ resumeData, onContinue }) {
    const profile = resumeData?.profile || {}

    const skills = profile.skills || []
    const education = profile.education || []
    const experience = profile.experience || []
    const projects = profile.projects || []
    const certifications = profile.certifications || []

    return (
        <section className="relative z-10 mx-auto min-h-screen max-w-5xl px-6 py-28 sm:px-10 lg:px-12">
            <div className="rounded-3xl border border-slate-200 bg-white p-8 shadow-xl shadow-slate-200/50 sm:p-10 text-center md:text-left">

                {/* Header */}
                <div>
                    <p className="text-sm font-medium uppercase tracking-[0.2em] text-indigo-600">
                        JobJazz Analysis
                    </p>

                    <h1 className="mt-3 text-3xl font-bold tracking-tight text-slate-900 sm:text-5xl">
                        Your career profile is ready
                    </h1>

                    <p className="mt-4 max-w-2xl text-base leading-7 text-slate-600 sm:text-lg mx-auto md:mx-0">
                        We've understood your resume. Now let's see which opportunities
                        fit your profile.
                    </p>
                </div>

                {/* Profile Identity */}
                <div className="mt-10 rounded-2xl border border-slate-100 bg-slate-50 p-6 shadow-sm">
                    <div className="flex flex-col gap-5 sm:flex-row sm:items-center sm:justify-between text-left">

                        <div>
                            <p className="text-xs font-semibold uppercase tracking-[0.15em] text-slate-500">
                                Candidate
                            </p>

                            <h2 className="mt-2 text-2xl font-bold text-slate-900">
                                {profile.name || "Your Profile"}
                            </h2>

                            {profile.location && (
                                <p className="mt-1 text-sm font-medium text-slate-600">
                                    {profile.location}
                                </p>
                            )}
                        </div>

                        <div className="rounded-full border border-emerald-200 bg-emerald-50 px-4 py-2 text-sm font-semibold text-emerald-700 shadow-sm self-start sm:self-auto">
                            ✓ Resume analyzed
                        </div>

                    </div>
                </div>

                {/* Skills */}
                <div className="mt-6 rounded-2xl border border-slate-100 bg-slate-50 p-6 shadow-sm text-left">
                    <div className="flex items-center justify-between">
                        <h2 className="text-lg font-bold text-slate-900">
                            Skills
                        </h2>

                        <span className="text-sm font-semibold text-slate-500">
                            {skills.length} detected
                        </span>
                    </div>

                    {skills.length > 0 ? (
                        <div className="mt-5 flex flex-wrap gap-2">
                            {skills.slice(0, 15).map((skill, index) => (
                                <span
                                    key={`${skill}-${index}`}
                                    className="rounded-full border border-slate-200 bg-white px-3 py-1.5 text-sm font-medium text-slate-700 shadow-sm"
                                >
                                    {skill}
                                </span>
                            ))}
                        </div>
                    ) : (
                        <p className="mt-4 text-sm text-slate-500 italic">
                            No skills were detected.
                        </p>
                    )}
                </div>

                {/* Profile Overview */}
                <div className="mt-6 grid gap-4 sm:grid-cols-3 text-left">

                    <div className="rounded-2xl border border-slate-100 bg-slate-50 p-6 shadow-sm">
                        <p className="text-sm font-semibold text-slate-500">
                            Experience
                        </p>

                        <p className="mt-2 text-3xl font-bold text-slate-900">
                            {experience.length}
                        </p>

                        <p className="mt-1 text-sm font-medium text-slate-500">
                            positions detected
                        </p>
                    </div>

                    <div className="rounded-2xl border border-slate-100 bg-slate-50 p-6 shadow-sm">
                        <p className="text-sm font-semibold text-slate-500">
                            Projects
                        </p>

                        <p className="mt-2 text-3xl font-bold text-slate-900">
                            {projects.length}
                        </p>

                        <p className="mt-1 text-sm font-medium text-slate-500">
                            projects detected
                        </p>
                    </div>

                    <div className="rounded-2xl border border-slate-100 bg-slate-50 p-6 shadow-sm">
                        <p className="text-sm font-semibold text-slate-500">
                            Education
                        </p>

                        <p className="mt-2 text-3xl font-bold text-slate-900">
                            {education.length}
                        </p>

                        <p className="mt-1 text-sm font-medium text-slate-500">
                            qualifications detected
                        </p>
                    </div>

                </div>

                {/* Certifications */}
                {certifications.length > 0 && (
                    <div className="mt-6 rounded-2xl border border-slate-100 bg-slate-50 p-6 shadow-sm text-left">
                        <div className="flex items-center justify-between">
                            <h2 className="text-lg font-bold text-slate-900">
                                Certifications
                            </h2>

                            <span className="text-sm font-semibold text-slate-500">
                                {certifications.length} detected
                            </span>
                        </div>
                    </div>
                )}

                {/* Continue */}
                <div className="mt-8 flex justify-end">
                    <button
                        type="button"
                        onClick={onContinue}
                        className="jj-btn-primary"
                    >
                        Continue →
                    </button>
                </div>

            </div>
        </section>
    )
}

export default CareerProfile