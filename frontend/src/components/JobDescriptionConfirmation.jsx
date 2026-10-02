export default function JobDescriptionConfirmation({ profile, onConfirm, onCancel }) {
    const { job_title, required_skills, preferred_skills, experience_requirement, education_requirements } = profile;

    return (
        <section className="relative z-10 mx-auto flex min-h-screen max-w-3xl flex-col justify-center px-6 py-28 sm:px-10">
            <div className="rounded-3xl border border-slate-200 bg-white p-8 shadow-xl shadow-slate-200/50 sm:p-10 text-center md:text-left">
                <p className="text-sm font-semibold uppercase tracking-widest text-indigo-600 mb-2">
                    Job Description Recognized
                </p>
                <h1 className="text-2xl font-bold text-slate-900 sm:text-3xl mb-8">
                    {job_title || "Untitled Role"}
                </h1>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6 text-left mb-10">
                    <div className="rounded-xl border border-slate-100 bg-slate-50 p-5">
                        <p className="text-sm font-medium text-slate-500 mb-1">Required Skills</p>
                        <p className="text-2xl font-bold text-slate-900">{required_skills?.length || 0}</p>
                    </div>
                    <div className="rounded-xl border border-slate-100 bg-slate-50 p-5">
                        <p className="text-sm font-medium text-slate-500 mb-1">Preferred Skills</p>
                        <p className="text-2xl font-bold text-slate-900">{preferred_skills?.length || 0}</p>
                    </div>
                    <div className="rounded-xl border border-slate-100 bg-slate-50 p-5 md:col-span-2 flex flex-col md:flex-row md:gap-10">
                        <div className="mb-4 md:mb-0">
                            <p className="text-sm font-medium text-slate-500 mb-1">Experience</p>
                            <p className="text-base font-semibold text-slate-900">
                                {experience_requirement || "Not explicitly stated"}
                            </p>
                        </div>
                        <div>
                            <p className="text-sm font-medium text-slate-500 mb-1">Education</p>
                            <p className="text-base font-semibold text-slate-900">
                                {education_requirements?.length > 0 ? education_requirements[0] : "Not explicitly stated"}
                            </p>
                        </div>
                    </div>
                </div>

                <div className="flex flex-col sm:flex-row items-center justify-end gap-4">
                    <button
                        onClick={onCancel}
                        className="w-full sm:w-auto jj-btn-secondary"
                    >
                        Try a different job
                    </button>
                    <button
                        onClick={onConfirm}
                        className="w-full sm:w-auto jj-btn-primary"
                    >
                        Continue to Match My Resume
                    </button>
                </div>
            </div>
        </section>
    );
}
