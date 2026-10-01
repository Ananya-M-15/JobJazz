import React from "react"

function CareerProfile({ resumeData, onContinue }) {
    const profile = resumeData?.profile || {}

    const skills = profile.skills || []
    const education = profile.education || []
    const experience = profile.experience || []
    const projects = profile.projects || []
    const certifications = profile.certifications || []

    return (
        <section className="relative z-10 mx-auto min-h-screen max-w-5xl px-6 py-28 sm:px-10 lg:px-12">
            <div className="rounded-3xl border border-white/10 bg-white/[0.04] p-8 backdrop-blur-xl sm:p-10">

                {/* Header */}
                <div>
                    <p className="text-sm font-medium uppercase tracking-[0.2em] text-purple-300">
                        JobJazz Analysis
                    </p>

                    <h1 className="mt-3 text-4xl font-bold tracking-tight text-white sm:text-5xl">
                        Your career profile is ready
                    </h1>

                    <p className="mt-4 max-w-2xl text-base leading-7 text-white/55 sm:text-lg">
                        We've understood your resume. Now let's see which opportunities
                        fit your profile.
                    </p>
                </div>

                {/* Profile Identity */}
                <div className="mt-10 rounded-2xl border border-white/10 bg-black/20 p-6">
                    <div className="flex flex-col gap-5 sm:flex-row sm:items-center sm:justify-between">

                        <div>
                            <p className="text-xs uppercase tracking-[0.15em] text-white/35">
                                Candidate
                            </p>

                            <h2 className="mt-2 text-2xl font-semibold text-white">
                                {profile.name || "Your Profile"}
                            </h2>

                            {profile.location && (
                                <p className="mt-1 text-sm text-white/45">
                                    {profile.location}
                                </p>
                            )}
                        </div>

                        <div className="rounded-full border border-emerald-400/20 bg-emerald-400/10 px-4 py-2 text-sm text-emerald-300">
                            ✓ Resume analyzed
                        </div>

                    </div>
                </div>

                {/* Skills */}
                <div className="mt-6 rounded-2xl border border-white/10 bg-black/20 p-6">
                    <div className="flex items-center justify-between">
                        <h2 className="text-lg font-semibold text-white">
                            Skills
                        </h2>

                        <span className="text-sm text-white/35">
                            {skills.length} detected
                        </span>
                    </div>

                    {skills.length > 0 ? (
                        <div className="mt-5 flex flex-wrap gap-2">
                            {skills.slice(0, 15).map((skill, index) => (
                                <span
                                    key={`${skill}-${index}`}
                                    className="rounded-full border border-white/10 bg-white/[0.05] px-3 py-1.5 text-sm text-white/70"
                                >
                                    {skill}
                                </span>
                            ))}
                        </div>
                    ) : (
                        <p className="mt-4 text-sm text-white/40">
                            No skills were detected.
                        </p>
                    )}
                </div>

                {/* Profile Overview */}
                <div className="mt-6 grid gap-4 sm:grid-cols-3">

                    <div className="rounded-2xl border border-white/10 bg-black/20 p-6">
                        <p className="text-sm text-white/40">
                            Experience
                        </p>

                        <p className="mt-2 text-3xl font-semibold text-white">
                            {experience.length}
                        </p>

                        <p className="mt-1 text-sm text-white/35">
                            positions detected
                        </p>
                    </div>

                    <div className="rounded-2xl border border-white/10 bg-black/20 p-6">
                        <p className="text-sm text-white/40">
                            Projects
                        </p>

                        <p className="mt-2 text-3xl font-semibold text-white">
                            {projects.length}
                        </p>

                        <p className="mt-1 text-sm text-white/35">
                            projects detected
                        </p>
                    </div>

                    <div className="rounded-2xl border border-white/10 bg-black/20 p-6">
                        <p className="text-sm text-white/40">
                            Education
                        </p>

                        <p className="mt-2 text-3xl font-semibold text-white">
                            {education.length}
                        </p>

                        <p className="mt-1 text-sm text-white/35">
                            qualifications detected
                        </p>
                    </div>

                </div>

                {/* Certifications */}
                {certifications.length > 0 && (
                    <div className="mt-6 rounded-2xl border border-white/10 bg-black/20 p-6">
                        <div className="flex items-center justify-between">
                            <h2 className="text-lg font-semibold text-white">
                                Certifications
                            </h2>

                            <span className="text-sm text-white/35">
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