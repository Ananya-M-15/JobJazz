export default function ExperienceEducationTab({ matchResult }) {
    const expStatus = matchResult?.experience_status || (matchResult?.experience_match ? "met" : "gap");
    const eduStatus = matchResult?.education_status || (matchResult?.education_match ? "met" : "gap");

    const getStatusConfig = (status) => {
        if (status === "met") {
            return {
                title: "Requirement Satisfied",
                badgeClass: "bg-emerald-50 border-emerald-200 text-emerald-700",
                iconClass: "bg-emerald-50 border-emerald-200 text-emerald-600",
                icon: "✓",
            };
        }
        if (status === "gap") {
            return {
                title: "Gap Identified",
                badgeClass: "bg-rose-50 border-rose-200 text-rose-700",
                iconClass: "bg-rose-50 border-rose-200 text-rose-600",
                icon: "✕",
            };
        }
        return {
            title: "Not Explicitly Required",
            badgeClass: "bg-slate-50 border-slate-200 text-slate-600",
            iconClass: "bg-slate-50 border-slate-200 text-slate-500",
            icon: "–",
        };
    };

    const expConfig = getStatusConfig(expStatus);
    const eduConfig = getStatusConfig(eduStatus);

    const expNotes = matchResult?.experience_notes || (
        expStatus === "met" 
            ? "Your documented career history satisfies the role's tenure requirements."
            : expStatus === "gap"
            ? "Your documented experience appears shorter than the target role's stated requirement."
            : "The job posting does not specify a mandatory minimum number of years of experience."
    );

    const eduNotes = matchResult?.education_notes || (
        eduStatus === "met"
            ? "Your education qualifications satisfy the academic requirements specified for this role."
            : eduStatus === "gap"
            ? "Your profile does not clearly document the specific degree or field requested by this job."
            : "No specific academic degree requirements were identified in this job posting."
    );

    return (
        <div className="animate-in fade-in slide-in-from-bottom-2 duration-500 space-y-6">
            
            {/* Experience Alignment Card */}
            <div className="rounded-3xl border border-slate-200 bg-white p-6 md:p-8 shadow-sm">
                <div className="flex flex-col sm:flex-row sm:items-start gap-5">
                    <div className="flex-shrink-0">
                        <div className={`flex items-center justify-center w-12 h-12 rounded-2xl border text-lg font-bold shadow-sm ${expConfig.iconClass}`}>
                            {expConfig.icon}
                        </div>
                    </div>
                    <div className="flex-1 min-w-0">
                        <div className="flex flex-wrap items-center justify-between gap-3 mb-2">
                            <h2 className="text-xs font-bold uppercase tracking-widest text-slate-500">
                                Work Experience Alignment
                            </h2>
                            <span className={`rounded-full px-3 py-1 text-xs font-bold uppercase tracking-wider border shadow-sm ${expConfig.badgeClass}`}>
                                {expConfig.title}
                            </span>
                        </div>
                        <h3 className="text-xl font-bold text-slate-900 mb-3">
                            {expStatus === "met" ? "Experience Criteria Met" : expStatus === "gap" ? "Experience Gap Detected" : "Experience Level Open / Unspecified"}
                        </h3>
                        <div className="bg-slate-50 rounded-2xl p-5 border border-slate-100">
                            <p className="text-slate-800 leading-relaxed text-sm md:text-base font-medium">
                                {expNotes}
                            </p>
                        </div>
                    </div>
                </div>
            </div>

            {/* Education Alignment Card */}
            <div className="rounded-3xl border border-slate-200 bg-white p-6 md:p-8 shadow-sm">
                <div className="flex flex-col sm:flex-row sm:items-start gap-5">
                    <div className="flex-shrink-0">
                        <div className={`flex items-center justify-center w-12 h-12 rounded-2xl border text-lg font-bold shadow-sm ${eduConfig.iconClass}`}>
                            {eduConfig.icon}
                        </div>
                    </div>
                    <div className="flex-1 min-w-0">
                        <div className="flex flex-wrap items-center justify-between gap-3 mb-2">
                            <h2 className="text-xs font-bold uppercase tracking-widest text-slate-500">
                                Academic & Education Alignment
                            </h2>
                            <span className={`rounded-full px-3 py-1 text-xs font-bold uppercase tracking-wider border shadow-sm ${eduConfig.badgeClass}`}>
                                {eduConfig.title}
                            </span>
                        </div>
                        <h3 className="text-xl font-bold text-slate-900 mb-3">
                            {eduStatus === "met" ? "Education Criteria Met" : eduStatus === "gap" ? "Education Gap Detected" : "Education Open / Unstated"}
                        </h3>
                        <div className="bg-slate-50 rounded-2xl p-5 border border-slate-100">
                            <p className="text-slate-800 leading-relaxed text-sm md:text-base font-medium">
                                {eduNotes}
                            </p>
                        </div>
                    </div>
                </div>
            </div>

        </div>
    );
}
