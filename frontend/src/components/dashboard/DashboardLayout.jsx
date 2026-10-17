import { useState } from "react";
import OverviewTab from "./OverviewTab";
import SkillsTab from "./SkillsTab";
import ExperienceEducationTab from "./ExperienceEducationTab";
import ActionPlanTab from "./ActionPlanTab";
import RoadmapTab from "./RoadmapTab";

export default function DashboardLayout({ analysisId, matchResult, skillGap, recommendations, jobProfile, candidateProfile, onStartOver }) {
    const [activeTab, setActiveTab] = useState("overview");

    const tabs = [
        { id: "overview", label: "Overview" },
        { id: "skills", label: "Skills & Gaps" },
        { id: "experience", label: "Experience & Ed" },
        { id: "action", label: "Action Plan" },
        { id: "roadmap", label: "Learning Roadmap" },
    ];

    const score = matchResult?.overall_score || 0;
    const matchTier = score >= 75 ? "Strong Fit" : score >= 50 ? "Moderate Fit" : "Development Needed";
    const badgeColor = score >= 75 ? "bg-emerald-50 text-emerald-700 border-emerald-200" : score >= 50 ? "bg-amber-50 text-amber-700 border-amber-200" : "bg-rose-50 text-rose-700 border-rose-200";

    return (
        <section className="relative z-10 mx-auto min-h-screen max-w-6xl px-4 py-24 md:py-32 sm:px-6 lg:px-8">
            
            {/* Contextual Workflow Indicator */}
            <div className="mb-6 flex items-center gap-2 text-xs font-medium text-slate-500 overflow-x-auto whitespace-nowrap pb-2 no-scrollbar">
                <span className="text-emerald-600 flex items-center gap-1 font-semibold">
                    Resume <svg className="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" /></svg>
                </span>
                <span className="text-slate-300">&rarr;</span>
                <span className="text-emerald-600 flex items-center gap-1 font-semibold">
                    Job Description <svg className="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" /></svg>
                </span>
                <span className="text-slate-300">&rarr;</span>
                <span className="text-indigo-600 flex items-center gap-1 font-semibold">
                    Career Fit Analysis <span className="w-1.5 h-1.5 rounded-full bg-indigo-600"></span>
                </span>
            </div>

            <div className="mb-8 flex flex-col sm:flex-row sm:items-end justify-between gap-6 pb-6 border-b border-slate-200">
                <div>
                    <div className="flex flex-wrap items-center gap-3 mb-2">
                        <p className="text-xs font-semibold uppercase tracking-[0.2em] text-indigo-600">
                            Match Analysis
                        </p>
                        {candidateProfile?.name && (
                            <span className="text-xs font-medium text-slate-500">
                                for {candidateProfile.name}
                            </span>
                        )}
                        <span className={`rounded-full px-2.5 py-0.5 text-xs font-bold uppercase tracking-wider border ${badgeColor}`}>
                            {matchTier}
                        </span>
                    </div>
                    <h1 className="text-3xl font-bold tracking-tight text-slate-900 sm:text-4xl">
                        {jobProfile?.job_title || "Job Description Match"}
                    </h1>
                </div>
                <button
                    onClick={onStartOver}
                    className="jj-btn-secondary self-start sm:self-auto"
                >
                    Analyze Another Job
                </button>
            </div>

            <div className="flex flex-col lg:flex-row gap-8">
                {/* Mobile / Tablet Tabs (Horizontal Scroll) */}
                <nav className="lg:hidden flex overflow-x-auto pb-2 -mx-4 px-4 sm:mx-0 sm:px-0 space-x-2 no-scrollbar" aria-label="Dashboard Navigation">
                    {tabs.map((tab) => (
                        <button
                            key={tab.id}
                            onClick={() => setActiveTab(tab.id)}
                            className={`whitespace-nowrap px-5 py-2.5 rounded-full text-sm font-semibold transition-colors ${
                                activeTab === tab.id 
                                    ? "bg-indigo-600 text-white shadow-sm" 
                                    : "bg-white text-slate-600 border border-slate-200 hover:bg-slate-50 hover:text-slate-900"
                            }`}
                            aria-current={activeTab === tab.id ? "page" : undefined}
                        >
                            {tab.label}
                        </button>
                    ))}
                </nav>

                {/* Desktop Sidebar (Vertical) */}
                <nav className="hidden lg:flex flex-col w-56 flex-shrink-0 space-y-1" aria-label="Dashboard Sidebar">
                    {tabs.map((tab) => (
                        <button
                            key={tab.id}
                            onClick={() => setActiveTab(tab.id)}
                            className={`text-left px-4 py-3 rounded-xl text-sm font-semibold transition-all duration-200 ${
                                activeTab === tab.id 
                                    ? "bg-indigo-50 text-indigo-700" 
                                    : "bg-transparent text-slate-600 hover:bg-slate-100 hover:text-slate-900"
                            }`}
                            aria-current={activeTab === tab.id ? "page" : undefined}
                        >
                            {tab.label}
                        </button>
                    ))}
                </nav>

                {/* Main Content Area */}
                <div className="flex-1 min-w-0">
                    {activeTab === "overview" && (
                        <OverviewTab 
                            matchResult={matchResult} 
                            recommendations={recommendations} 
                            jobProfile={jobProfile}
                            candidateProfile={candidateProfile}
                        />
                    )}
                    {activeTab === "skills" && (
                        <SkillsTab 
                            skillGap={skillGap} 
                            matchResult={matchResult} 
                            jobProfile={jobProfile}
                            candidateProfile={candidateProfile}
                        />
                    )}
                    {activeTab === "experience" && <ExperienceEducationTab matchResult={matchResult} skillGap={skillGap} />}
                    {activeTab === "action" && <ActionPlanTab recommendations={recommendations} />}
                    {activeTab === "roadmap" && (
                        <RoadmapTab 
                            analysisId={analysisId}
                            matchResult={matchResult}
                            skillGap={skillGap}
                            recommendations={recommendations}
                            jobProfile={jobProfile}
                            candidateProfile={candidateProfile}
                        />
                    )}
                </div>
            </div>
        </section>
    );
}
