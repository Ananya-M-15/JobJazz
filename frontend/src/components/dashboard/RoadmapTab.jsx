import { useState, useEffect, useMemo } from "react";
import {
    CheckCircle2,
    Circle,
    Clock,
    Calendar,
    BookOpen,
    Code2,
    Hammer,
    Award,
    RefreshCw,
    ExternalLink,
    Sliders,
    AlertCircle,
    Sparkles,
    ShieldCheck,
    Layers,
    Check,
    Info,
    ChevronRight,
    TrendingUp,
    FileText,
    Download,
} from "lucide-react";
import { generateRoadmap, getRoadmap, updateRoadmapStep, downloadRoadmapPdf } from "../../api/jobjazzApi";

export default function RoadmapTab({
    analysisId,
    jobProfile,
}) {
    const [roadmap, setRoadmap] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [updatingStepId, setUpdatingStepId] = useState(null);
    const [viewMode, setViewMode] = useState("curriculum"); // "curriculum" | "schedule"
    const [showConfig, setShowConfig] = useState(false);
    const [stepFeedback, setStepFeedback] = useState(null);
    const [editingNotesStepId, setEditingNotesStepId] = useState(null);
    const [noteDraft, setNoteDraft] = useState("");
    const [savingNoteStepId, setSavingNoteStepId] = useState(null);
    const [exportingPdf, setExportingPdf] = useState(false);
    const [exportError, setExportError] = useState(null);

    const handleDownloadPdf = async () => {
        if (!analysisId) return;
        setExportingPdf(true);
        setExportError(null);
        try {
            await downloadRoadmapPdf(analysisId);
        } catch (err) {
            setExportError(err instanceof Error ? err.message : "Failed to export roadmap PDF.");
        } finally {
            setExportingPdf(false);
        }
    };

    // Roadmap Generation Preferences
    const [preferences, setPreferences] = useState({
        proficiency: "intermediate",
        hours_per_week: 10,
        target_date: "",
        resource_format: "mix",
        budget: "free",
    });

    // Load initial roadmap on mount if analysisId is present
    useEffect(() => {
        let isMounted = true;

        async function fetchInitialRoadmap() {
            if (!analysisId) return;
            setLoading(true);
            setError(null);
            try {
                const data = await getRoadmap(analysisId);
                if (isMounted && data) {
                    setRoadmap(data);
                    if (data.preferences) {
                        setPreferences((prev) => ({
                            ...prev,
                            ...data.preferences,
                            target_date: data.preferences.target_date || data.preferences.target_completion_date || "",
                            resource_format: data.preferences.resource_format || data.preferences.preferred_format || "mix",
                            budget: data.preferences.budget === "all" || data.preferences.budget_preference === "free_and_paid" ? "all" : "free",
                        }));
                    }
                }
            } catch {
                // If 404 or not found, it's expected for new analyses that haven't generated a roadmap yet
                if (isMounted) {
                    setRoadmap(null);
                }
            } finally {
                if (isMounted) setLoading(false);
            }
        }

        fetchInitialRoadmap();

        return () => {
            isMounted = false;
        };
    }, [analysisId]);

    // Handle Generation or Regeneration
    const handleGenerate = async (e) => {
        if (e) e.preventDefault();
        if (!analysisId) {
            setError("Analysis ID missing. Please re-run the job matching first.");
            return;
        }

        setLoading(true);
        setError(null);

        try {
            const payload = {
                analysis_id: analysisId,
                preferences: {
                    proficiency: preferences.proficiency,
                    hours_per_week: Number(preferences.hours_per_week) || 10,
                    target_date: preferences.target_date || null,
                    resource_format: preferences.resource_format,
                    budget: preferences.budget,
                },
            };

            const result = await generateRoadmap(payload);
            setRoadmap(result);
            setShowConfig(false);
        } catch (err) {
            setError(err instanceof Error ? err.message : "Failed to generate roadmap.");
        } finally {
            setLoading(false);
        }
    };

    // Helper to test if a step is completed
    const isStepDone = (step) => step.status === "completed" || step.completed === true;

    // Toggle step completion status
    const handleToggleStep = async (stepId, step) => {
        if (!analysisId || updatingStepId) return;

        const currentCompleted = isStepDone(step);
        setUpdatingStepId(stepId);
        try {
            setStepFeedback(null);
            const updatedRoadmap = await updateRoadmapStep(analysisId, stepId, !currentCompleted);
            setRoadmap(updatedRoadmap);
            setStepFeedback({
                type: "success",
                message: !currentCompleted ? "Step marked complete!" : "Step marked incomplete.",
                stepId,
            });
            setTimeout(() => setStepFeedback(null), 3000);
        } catch (err) {
            console.error("Failed to update step:", err);
            setStepFeedback({
                type: "error",
                message: err instanceof Error ? err.message : "Failed to update step progress.",
                stepId,
            });
            setTimeout(() => setStepFeedback(null), 5000);
        } finally {
            setUpdatingStepId(null);
        }
    };

    // Notes editing handlers
    const handleStartEditNote = (step) => {
        setEditingNotesStepId(step.id);
        setNoteDraft(step.user_notes || "");
    };

    const handleSaveNote = async (step) => {
        if (!analysisId || savingNoteStepId) return;
        setSavingNoteStepId(step.id);
        try {
            const updatedRoadmap = await updateRoadmapStep(
                analysisId,
                step.id,
                isStepDone(step),
                noteDraft.trim()
            );
            setRoadmap(updatedRoadmap);
            setEditingNotesStepId(null);
            setStepFeedback({
                type: "success",
                message: "Note saved successfully!",
                stepId: step.id,
            });
            setTimeout(() => setStepFeedback(null), 3000);
        } catch (err) {
            console.error("Failed to save note:", err);
            setStepFeedback({
                type: "error",
                message: err instanceof Error ? err.message : "Failed to save note.",
                stepId: step.id,
            });
            setTimeout(() => setStepFeedback(null), 5000);
        } finally {
            setSavingNoteStepId(null);
        }
    };

    // Compute progress stats
    const progressStats = useMemo(() => {
        if (!roadmap?.modules) {
            return { total: 0, completed: 0, percent: 0, remainingHours: 0 };
        }
        let total = 0;
        let completed = 0;
        let remainingHours = 0;

        roadmap.modules.forEach((mod) => {
            mod.steps.forEach((step) => {
                total += 1;
                if (isStepDone(step)) {
                    completed += 1;
                } else {
                    remainingHours += step.estimated_hours || 0;
                }
            });
        });

        const percent = total > 0 ? Math.round((completed / total) * 100) : 0;
        return { total, completed, percent, remainingHours };
    }, [roadmap]);

    // Stage configuration for colors & icons
    const getStageBadge = (stage) => {
        switch (stage?.toLowerCase()) {
            case "learn":
                return {
                    label: "Learn",
                    icon: BookOpen,
                    bg: "bg-blue-50 text-blue-700 border-blue-200",
                    border: "border-blue-400",
                };
            case "practise":
            case "practice":
                return {
                    label: "Practise",
                    icon: Code2,
                    bg: "bg-purple-50 text-purple-700 border-purple-200",
                    border: "border-purple-400",
                };
            case "build":
                return {
                    label: "Build",
                    icon: Hammer,
                    bg: "bg-emerald-50 text-emerald-700 border-emerald-200",
                    border: "border-emerald-400",
                };
            case "showcase":
                return {
                    label: "Showcase",
                    icon: Award,
                    bg: "bg-amber-50 text-amber-700 border-amber-200",
                    border: "border-amber-400",
                };
            case "reassess":
                return {
                    label: "Reassess",
                    icon: RefreshCw,
                    bg: "bg-indigo-50 text-indigo-700 border-indigo-200",
                    border: "border-indigo-400",
                };
            default:
                return {
                    label: stage || "Stage",
                    icon: Layers,
                    bg: "bg-slate-50 text-slate-700 border-slate-200",
                    border: "border-slate-400",
                };
        }
    };

    // Format badge styling
    const getGapTypeBadge = (gapType) => {
        switch (gapType) {
            case "genuinely_missing":
                return { label: "Core Gap", bg: "bg-rose-50 text-rose-700 border-rose-200" };
            case "partially_demonstrated":
                return { label: "Needs Practice", bg: "bg-amber-50 text-amber-700 border-amber-200" };
            case "demonstrated_unpolished":
                return { label: "Resume Polish", bg: "bg-blue-50 text-blue-700 border-blue-200" };
            default:
                return { label: "Skill Growth", bg: "bg-slate-50 text-slate-700 border-slate-200" };
        }
    };

    // Loading State
    if (loading && !roadmap) {
        return (
            <div className="animate-in fade-in duration-500 rounded-3xl border border-slate-200 bg-white p-12 text-center shadow-sm">
                <div className="mx-auto w-16 h-16 rounded-full bg-indigo-50 border border-indigo-100 flex items-center justify-center mb-6">
                    <div className="h-8 w-8 animate-spin rounded-full border-3 border-indigo-200 border-t-indigo-600" />
                </div>
                <h2 className="text-2xl font-bold text-slate-900 mb-2">Building Your Personalized Roadmap</h2>
                <p className="text-sm text-slate-600 max-w-md mx-auto leading-relaxed">
                    Analyzing skill gaps against {jobProfile?.job_title || "the target role"}, discovering verified learning resources, and calculating a realistic weekly timetable...
                </p>
                <div className="mt-6 flex flex-wrap items-center justify-center gap-3 text-xs text-slate-500">
                    <span className="flex items-center gap-1.5"><ShieldCheck className="w-4 h-4 text-emerald-500" /> Vetted Resources</span>
                    <span>•</span>
                    <span className="flex items-center gap-1.5"><Clock className="w-4 h-4 text-indigo-500" /> Weekly Capacity Bounds</span>
                    <span>•</span>
                    <span className="flex items-center gap-1.5"><Sparkles className="w-4 h-4 text-purple-500" /> Actionable Milestones</span>
                </div>
            </div>
        );
    }

    // Empty / Setup state: If roadmap has not been generated yet
    if (!roadmap) {
        return (
            <div className="animate-in fade-in duration-500 space-y-6">
                <div className="rounded-3xl border border-slate-200 bg-white p-8 md:p-10 shadow-sm relative overflow-hidden">
                    <div className="max-w-2xl">
                        <div className="inline-flex items-center gap-2 rounded-full bg-indigo-50 px-3 py-1 text-xs font-semibold text-indigo-700 border border-indigo-100 mb-4">
                            <Sparkles className="w-3.5 h-3.5" />
                            Personalized Skill Development Plan
                        </div>
                        <h2 className="text-3xl font-bold tracking-tight text-slate-900 mb-3">
                            Turn Skill Gaps into Step-by-Step Mastery
                        </h2>
                        <p className="text-slate-600 text-base leading-relaxed mb-8">
                            JobJazz analyzes the exact missing and unpolished skills identified between your resume and <span className="font-semibold text-slate-900">{jobProfile?.job_title || "this role"}</span>. Configure your learning preferences below to generate an actionable, week-by-week roadmap with verified resources, hands-on practice, and project deliverables.
                        </p>
                    </div>

                    {error && (
                        <div className="mb-6 rounded-2xl border border-rose-200 bg-rose-50 p-4 text-sm text-rose-700 flex items-start gap-3">
                            <AlertCircle className="w-5 h-5 flex-shrink-0 mt-0.5" />
                            <span>{error}</span>
                        </div>
                    )}

                    {/* Preferences Form */}
                    <form onSubmit={handleGenerate} className="space-y-6 max-w-3xl pt-4 border-t border-slate-100">
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                            {/* Current Proficiency */}
                            <div>
                                <label className="block text-xs font-bold uppercase tracking-wider text-slate-600 mb-2">
                                    Current Proficiency
                                </label>
                                <select
                                    value={preferences.proficiency}
                                    onChange={(e) => setPreferences({ ...preferences, proficiency: e.target.value })}
                                    className="w-full rounded-xl border border-slate-200 bg-slate-50 px-4 py-2.5 text-sm text-slate-900 focus:bg-white focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-100 transition-all font-medium"
                                >
                                    <option value="beginner">Beginner (Foundations first)</option>
                                    <option value="intermediate">Intermediate (Standard depth)</option>
                                    <option value="advanced">Advanced (Fast-track to architecture & projects)</option>
                                </select>
                            </div>

                            {/* Available Study Hours / Week */}
                            <div>
                                <label className="block text-xs font-bold uppercase tracking-wider text-slate-600 mb-2">
                                    Weekly Study Commitment: <span className="text-indigo-600 font-bold">{preferences.hours_per_week} hrs/week</span>
                                </label>
                                <div className="flex items-center gap-4">
                                    <input
                                        type="range"
                                        min="2"
                                        max="40"
                                        step="1"
                                        value={preferences.hours_per_week}
                                        onChange={(e) => setPreferences({ ...preferences, hours_per_week: Number(e.target.value) })}
                                        className="w-full accent-indigo-600 cursor-pointer"
                                    />
                                    <span className="text-sm font-semibold text-slate-700 min-w-12 text-right">
                                        {preferences.hours_per_week}h
                                    </span>
                                </div>
                            </div>

                            {/* Resource Format */}
                            <div>
                                <label className="block text-xs font-bold uppercase tracking-wider text-slate-600 mb-2">
                                    Preferred Resource Style
                                </label>
                                <select
                                    value={preferences.resource_format}
                                    onChange={(e) => setPreferences({ ...preferences, resource_format: e.target.value })}
                                    className="w-full rounded-xl border border-slate-200 bg-slate-50 px-4 py-2.5 text-sm text-slate-900 focus:bg-white focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-100 transition-all font-medium"
                                >
                                    <option value="mix">Balanced Mix (Docs, Practice & Projects)</option>
                                    <option value="docs">Official Documentation & Specs</option>
                                    <option value="projects">Project-First & Hands-on Labs</option>
                                    <option value="courses">Structured Courses & Tutorials</option>
                                    <option value="videos">Video Guides & Walkthroughs</option>
                                </select>
                            </div>

                            {/* Budget Preference */}
                            <div>
                                <label className="block text-xs font-bold uppercase tracking-wider text-slate-600 mb-2">
                                    Budget Preference
                                </label>
                                <select
                                    value={preferences.budget}
                                    onChange={(e) => setPreferences({ ...preferences, budget: e.target.value })}
                                    className="w-full rounded-xl border border-slate-200 bg-slate-50 px-4 py-2.5 text-sm text-slate-900 focus:bg-white focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-100 transition-all font-medium"
                                >
                                    <option value="free">100% Free Resources Only</option>
                                    <option value="all">Free and Paid (All Verified Providers)</option>
                                </select>
                            </div>

                            {/* Optional Target Completion Date */}
                            <div className="md:col-span-2">
                                <label className="block text-xs font-bold uppercase tracking-wider text-slate-600 mb-2">
                                    Target Completion Date <span className="text-slate-400 font-normal lowercase">(optional — we calculate schedule feasibility)</span>
                                </label>
                                <input
                                    type="date"
                                    value={preferences.target_date}
                                    min={new Date().toISOString().split("T")[0]}
                                    onChange={(e) => setPreferences({ ...preferences, target_date: e.target.value })}
                                    className="w-full max-w-sm rounded-xl border border-slate-200 bg-slate-50 px-4 py-2.5 text-sm text-slate-900 focus:bg-white focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-100 transition-all font-medium"
                                />
                            </div>
                        </div>

                        <div className="pt-4 flex flex-col sm:flex-row items-center gap-4">
                            <button
                                type="submit"
                                disabled={loading}
                                className="w-full sm:w-auto inline-flex items-center justify-center gap-2 rounded-xl bg-indigo-600 px-6 py-3 text-sm font-semibold text-white shadow-sm hover:bg-indigo-700 transition-all disabled:opacity-50"
                            >
                                <Sparkles className="w-4 h-4" />
                                Generate My Learning Roadmap
                            </button>
                            <span className="text-xs text-slate-500">
                                Grounded with verified curricula & hands-on exercises
                            </span>
                        </div>
                    </form>
                </div>
            </div>
        );
    }

    const { summary, modules, schedule } = roadmap;

    return (
        <div className="animate-in fade-in slide-in-from-bottom-2 duration-500 space-y-8">
            {/* Top Overview & Metrics Card */}
            <div className="rounded-3xl border border-slate-200 bg-white p-6 md:p-8 shadow-sm">
                <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-6 pb-6 border-b border-slate-100">
                    <div>
                        <div className="flex flex-wrap items-center gap-2.5 mb-2">
                            <span className="inline-flex items-center gap-1.5 rounded-full bg-indigo-50 px-3 py-0.5 text-xs font-bold text-indigo-700 border border-indigo-100">
                                <Sparkles className="w-3.5 h-3.5" />
                                Personalized Roadmap
                            </span>
                            <span className="rounded-full bg-slate-100 px-2.5 py-0.5 text-xs font-semibold text-slate-600 border border-slate-200">
                                {roadmap.source === "ai" ? "AI Grounded Curriculum" : "Vetted Deterministic Curriculum"}
                            </span>
                            <span className="rounded-full bg-emerald-50 px-2.5 py-0.5 text-xs font-semibold text-emerald-700 border border-emerald-200">
                                {roadmap.preferences?.budget === "all" ? "Free & Paid Resources" : "100% Free Resources"}
                            </span>
                        </div>
                        <h2 className="text-2xl md:text-3xl font-bold tracking-tight text-slate-900">
                            Roadmap for {summary?.target_role || jobProfile?.job_title || "Target Role"}
                        </h2>
                        <p className="mt-1.5 text-sm text-slate-600 max-w-2xl leading-relaxed">
                            {summary?.overall_strategy || summary?.overview || "An adaptive, step-by-step curriculum to close skill gaps and build demonstrable portfolio projects."}
                        </p>
                    </div>

                    {/* Action Controls */}
                    <div className="flex items-center gap-3 self-start lg:self-center">
                        <button
                            type="button"
                            onClick={handleDownloadPdf}
                            disabled={exportingPdf}
                            className="inline-flex items-center gap-2 rounded-xl border border-indigo-200 bg-indigo-50/70 px-4 py-2.5 text-xs font-semibold text-indigo-700 hover:bg-indigo-100 transition-colors shadow-xs disabled:opacity-50"
                        >
                            <Download className="w-3.5 h-3.5 text-indigo-600" />
                            {exportingPdf ? "Exporting PDF..." : "Download Roadmap PDF"}
                        </button>
                        <button
                            type="button"
                            onClick={() => setShowConfig(!showConfig)}
                            className="inline-flex items-center gap-2 rounded-xl border border-slate-200 bg-white px-4 py-2.5 text-xs font-semibold text-slate-700 hover:bg-slate-50 hover:text-slate-900 transition-colors shadow-xs"
                        >
                            <Sliders className="w-3.5 h-3.5 text-slate-500" />
                            {showConfig ? "Hide Settings" : "Adjust Preferences"}
                        </button>
                    </div>
                </div>

                {exportError && (
                    <div className="mt-3 rounded-xl border border-rose-200 bg-rose-50 px-4 py-2 text-xs font-medium text-rose-700">
                        {exportError}
                    </div>
                )}

                {/* Collapsible Preferences Panel */}
                {showConfig && (
                    <div className="py-6 border-b border-slate-100 animate-in fade-in duration-300">
                        <h3 className="text-xs font-bold uppercase tracking-widest text-slate-500 mb-4 flex items-center gap-2">
                            <Sliders className="w-4 h-4 text-indigo-500" />
                            Adjust Roadmap Parameters
                        </h3>
                        <form onSubmit={handleGenerate} className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                            <div>
                                <label className="block text-xs font-semibold text-slate-600 mb-1.5">Proficiency</label>
                                <select
                                    value={preferences.proficiency}
                                    onChange={(e) => setPreferences({ ...preferences, proficiency: e.target.value })}
                                    className="w-full rounded-xl border border-slate-200 bg-slate-50 px-3 py-2 text-xs text-slate-800 font-medium"
                                >
                                    <option value="beginner">Beginner</option>
                                    <option value="intermediate">Intermediate</option>
                                    <option value="advanced">Advanced</option>
                                </select>
                            </div>
                            <div>
                                <label className="block text-xs font-semibold text-slate-600 mb-1.5">Study Hours / Week</label>
                                <input
                                    type="number"
                                    min="2"
                                    max="50"
                                    value={preferences.hours_per_week}
                                    onChange={(e) => setPreferences({ ...preferences, hours_per_week: Number(e.target.value) })}
                                    className="w-full rounded-xl border border-slate-200 bg-slate-50 px-3 py-2 text-xs text-slate-800 font-medium"
                                />
                            </div>
                            <div>
                                <label className="block text-xs font-semibold text-slate-600 mb-1.5">Resource Format</label>
                                <select
                                    value={preferences.resource_format}
                                    onChange={(e) => setPreferences({ ...preferences, resource_format: e.target.value })}
                                    className="w-full rounded-xl border border-slate-200 bg-slate-50 px-3 py-2 text-xs text-slate-800 font-medium"
                                >
                                    <option value="mix">Balanced Mix</option>
                                    <option value="docs">Official Documentation</option>
                                    <option value="projects">Hands-on Projects</option>
                                    <option value="courses">Courses</option>
                                </select>
                            </div>
                            <div className="flex items-end">
                                <button
                                    type="submit"
                                    disabled={loading}
                                    className="w-full inline-flex items-center justify-center gap-2 rounded-xl bg-indigo-600 px-4 py-2 text-xs font-semibold text-white hover:bg-indigo-700 transition-colors disabled:opacity-50"
                                >
                                    <RefreshCw className={`w-3.5 h-3.5 ${loading ? "animate-spin" : ""}`} />
                                    Regenerate Roadmap
                                </button>
                            </div>
                        </form>
                    </div>
                )}

                {/* Key Metrics Dashboard Tiles */}
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 pt-6">
                    {/* Overall Progress */}
                    <div className="rounded-2xl border border-slate-100 bg-slate-50/70 p-4">
                        <div className="flex items-center justify-between text-xs font-bold uppercase tracking-wider text-slate-500 mb-1">
                            <span>Progress</span>
                            <span className="text-indigo-600 font-bold">
                                {summary?.progress_percentage !== undefined ? summary.progress_percentage : progressStats.percent}%
                            </span>
                        </div>
                        <div className="text-2xl font-bold text-slate-900 mb-2">
                            {summary?.completed_steps !== undefined ? summary.completed_steps : progressStats.completed} <span className="text-xs font-semibold text-slate-500">/ {summary?.total_steps || progressStats.total} steps</span>
                        </div>
                        <div className="w-full bg-slate-200 h-2 rounded-full overflow-hidden">
                            <div
                                className="bg-indigo-600 h-full rounded-full transition-all duration-500"
                                style={{ width: `${summary?.progress_percentage !== undefined ? summary.progress_percentage : progressStats.percent}%` }}
                            />
                        </div>
                    </div>

                    {/* Estimated Total Effort */}
                    <div className="rounded-2xl border border-slate-100 bg-slate-50/70 p-4">
                        <div className="text-xs font-bold uppercase tracking-wider text-slate-500 mb-1 flex items-center gap-1.5">
                            <Clock className="w-3.5 h-3.5 text-slate-400" />
                            Total Effort
                        </div>
                        <div className="text-2xl font-bold text-slate-900">
                            {summary?.total_hours || schedule?.total_hours || summary?.total_estimated_hours || 0} <span className="text-xs font-semibold text-slate-500">hrs</span>
                        </div>
                        <p className="text-xs text-slate-500 mt-1">
                            ~{summary?.estimated_weeks || schedule?.total_weeks || Math.ceil((summary?.total_hours || 10) / (preferences.hours_per_week || 10))} weeks at {preferences.hours_per_week || schedule?.hours_per_week || 10}h/wk
                        </p>
                    </div>

                    {/* Hands-on Ratio */}
                    <div className="rounded-2xl border border-slate-100 bg-slate-50/70 p-4">
                        <div className="text-xs font-bold uppercase tracking-wider text-slate-500 mb-1 flex items-center gap-1.5">
                            <TrendingUp className="w-3.5 h-3.5 text-emerald-500" />
                            Hands-On Ratio
                        </div>
                        <div className="text-2xl font-bold text-slate-900">
                            {schedule ? (
                                <>
                                    {Math.round((((schedule.practising_hours || 0) + (schedule.building_hours || 0)) / Math.max(schedule.total_hours || 1, 1)) * 100)}%
                                    <span className="text-xs font-semibold text-slate-500 ml-1.5">applied</span>
                                </>
                            ) : (
                                "65% applied"
                            )}
                        </div>
                        <p className="text-xs text-slate-500 mt-1">
                            {schedule?.learning_hours || 0}h theory • {((schedule?.practising_hours || 0) + (schedule?.building_hours || 0))}h build
                        </p>
                    </div>

                    {/* Target Completion Feasibility */}
                    <div className="rounded-2xl border border-slate-100 bg-slate-50/70 p-4">
                        <div className="text-xs font-bold uppercase tracking-wider text-slate-500 mb-1 flex items-center gap-1.5">
                            <Calendar className="w-3.5 h-3.5 text-purple-400" />
                            Timeline Feasibility
                        </div>
                        <div className="flex items-center gap-2">
                            {schedule?.is_feasible === false ? (
                                <span className="inline-flex items-center gap-1 rounded-full bg-amber-50 px-2.5 py-0.5 text-xs font-bold text-amber-700 border border-amber-200">
                                    <AlertCircle className="w-3 h-3" /> Aggressive Date
                                </span>
                            ) : (
                                <span className="inline-flex items-center gap-1 rounded-full bg-emerald-50 px-2.5 py-0.5 text-xs font-bold text-emerald-700 border border-emerald-200">
                                    <ShieldCheck className="w-3 h-3" /> Realistic
                                </span>
                            )}
                        </div>
                        <p className="text-xs text-slate-500 mt-1.5 truncate" title={schedule?.feasibility_notes || schedule?.projected_completion_date}>
                            {schedule?.is_feasible === false
                                ? schedule?.feasibility_notes || "Suggested: extend target date"
                                : `Target: ${schedule?.projected_completion_date || "On track"}`}
                        </p>
                    </div>
                </div>

                {/* Skill Priorities Strip */}
                {((summary?.key_focus_areas && summary.key_focus_areas.length > 0) || (summary?.key_skill_priorities && summary.key_skill_priorities.length > 0)) && (
                    <div className="mt-6 pt-5 border-t border-slate-100">
                        <div className="flex flex-wrap items-center gap-2">
                            <span className="text-xs font-bold uppercase tracking-wider text-slate-400 mr-1">
                                Priority Competencies Addressed:
                            </span>
                            {(summary.key_focus_areas || summary.key_skill_priorities).map((skill, sIdx) => (
                                <span
                                    key={sIdx}
                                    className="inline-flex items-center rounded-lg bg-indigo-50/60 border border-indigo-100/80 px-2.5 py-1 text-xs font-medium text-indigo-900"
                                >
                                    {skill}
                                </span>
                            ))}
                        </div>
                    </div>
                )}
            </div>

            {/* View Switcher Tabs (Curriculum Modules vs Weekly Timetable) */}
            <div className="flex items-center justify-between gap-4 border-b border-slate-200 pb-3">
                <div className="flex items-center space-x-2">
                    <button
                        onClick={() => setViewMode("curriculum")}
                        className={`px-4 py-2 rounded-xl text-xs font-bold transition-all ${
                            viewMode === "curriculum"
                                ? "bg-indigo-600 text-white shadow-xs"
                                : "bg-white text-slate-600 border border-slate-200 hover:bg-slate-50 hover:text-slate-900"
                        }`}
                    >
                        Module Curriculum ({modules?.length || 0})
                    </button>
                    <button
                        onClick={() => setViewMode("schedule")}
                        className={`px-4 py-2 rounded-xl text-xs font-bold transition-all ${
                            viewMode === "schedule"
                                ? "bg-indigo-600 text-white shadow-xs"
                                : "bg-white text-slate-600 border border-slate-200 hover:bg-slate-50 hover:text-slate-900"
                        }`}
                    >
                        Weekly Timetable ({schedule?.weekly_schedule?.length || schedule?.total_weeks || 0} Weeks)
                    </button>
                </div>

                <div className="hidden sm:flex items-center gap-2 text-xs text-slate-500 font-medium">
                    <Info className="w-3.5 h-3.5 text-slate-400" />
                    <span>Check off steps to record progress</span>
                </div>
            </div>

            {/* View 1: Module Curriculum View */}
            {viewMode === "curriculum" && (
                <div className="space-y-10">
                    {stepFeedback && (
                        <div className={`p-3.5 rounded-2xl border text-xs font-semibold flex items-center justify-between transition-all ${
                            stepFeedback.type === "error"
                                ? "bg-rose-50 border-rose-200 text-rose-800"
                                : "bg-emerald-50 border-emerald-200 text-emerald-800"
                        }`}>
                            <div className="flex items-center gap-2">
                                <span>{stepFeedback.type === "error" ? "⚠️" : "✓"}</span>
                                <span>{stepFeedback.message}</span>
                            </div>
                            <button
                                type="button"
                                onClick={() => setStepFeedback(null)}
                                className="text-slate-400 hover:text-slate-600 text-xs font-bold px-1"
                            >
                                ✕
                            </button>
                        </div>
                    )}
                    {modules?.map((mod, modIdx) => {
                        const modCompleted = mod.steps.filter(isStepDone).length;
                        const modTotal = mod.steps.length;
                        const modPercent = modTotal > 0 ? Math.round((modCompleted / modTotal) * 100) : 0;
                        const gapBadge = getGapTypeBadge(mod.gap_type);

                        return (
                            <div key={mod.id || modIdx} className="rounded-3xl border border-slate-200 bg-white p-6 md:p-8 shadow-sm">
                                {/* Module Header */}
                                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-6 border-b border-slate-100">
                                    <div>
                                        <div className="flex flex-wrap items-center gap-2 mb-2">
                                            <span className="text-xs font-bold uppercase tracking-widest text-indigo-600">
                                                Module {modIdx + 1}
                                            </span>
                                            <span className={`rounded-full px-2.5 py-0.5 text-xs font-semibold border ${gapBadge.bg}`}>
                                                {gapBadge.label}
                                            </span>
                                            {(mod.skills || mod.target_skills || []).map((ts, i) => (
                                                <span key={i} className="rounded-md bg-slate-100 px-2 py-0.5 text-xs font-medium text-slate-700">
                                                    {ts}
                                                </span>
                                            ))}
                                        </div>
                                        <h3 className="text-xl md:text-2xl font-bold text-slate-900">
                                            {mod.title}
                                        </h3>
                                        <p className="mt-1 text-sm text-slate-600 leading-relaxed">
                                            {mod.why_it_matters || mod.description}
                                        </p>
                                    </div>

                                    {/* Module Progress */}
                                    <div className="sm:text-right flex sm:flex-col items-center sm:items-end justify-between gap-2 flex-shrink-0">
                                        <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">
                                            {modCompleted}/{modTotal} Steps
                                        </span>
                                        <div className="w-24 sm:w-28 bg-slate-100 h-2 rounded-full overflow-hidden">
                                            <div
                                                className="bg-indigo-600 h-full rounded-full transition-all duration-300"
                                                style={{ width: `${modPercent}%` }}
                                            />
                                        </div>
                                        <span className="text-xs font-medium text-slate-400">
                                            ~{mod.estimated_hours} hours total
                                        </span>
                                    </div>
                                </div>

                                {/* Step Cards */}
                                <div className="mt-6 space-y-6">
                                    {mod.steps?.map((step, sIdx) => {
                                        const stage = getStageBadge(step.stage);
                                        const StageIcon = stage.icon;
                                        const isUpdating = updatingStepId === step.id;
                                        const completed = isStepDone(step);

                                        return (
                                            <div
                                                key={step.id || sIdx}
                                                className={`rounded-2xl border transition-all duration-200 p-5 md:p-6 ${
                                                    completed
                                                        ? "border-emerald-200 bg-emerald-50/20"
                                                        : "border-slate-200 bg-white hover:border-indigo-200 hover:shadow-xs"
                                                }`}
                                            >
                                                <div className="flex items-start gap-4">
                                                    {/* Checkbox */}
                                                    <button
                                                        type="button"
                                                        onClick={() => handleToggleStep(step.id, step)}
                                                        disabled={isUpdating}
                                                        className={`mt-1 flex-shrink-0 transition-transform active:scale-90 ${
                                                            isUpdating ? "opacity-50" : ""
                                                        }`}
                                                        aria-label={completed ? "Mark as incomplete" : "Mark as complete"}
                                                    >
                                                        {completed ? (
                                                            <CheckCircle2 className="w-6 h-6 text-emerald-600 fill-emerald-50" />
                                                        ) : (
                                                            <Circle className="w-6 h-6 text-slate-300 hover:text-indigo-600" />
                                                        )}
                                                    </button>

                                                    {/* Step Body */}
                                                    <div className="flex-1 min-w-0">
                                                        <div className="flex flex-wrap items-center gap-2 mb-2">
                                                            {/* Stage Pill */}
                                                            <span className={`inline-flex items-center gap-1 rounded-full px-2.5 py-0.5 text-xs font-bold border ${stage.bg}`}>
                                                                <StageIcon className="w-3 h-3" />
                                                                {stage.label}
                                                            </span>

                                                            {/* Competency Pill */}
                                                            <span className="rounded-md bg-slate-100 px-2 py-0.5 text-xs font-medium text-slate-700">
                                                                {step.skill}
                                                            </span>

                                                            {/* Estimated Hours */}
                                                            <span className="text-xs font-semibold text-slate-500 ml-auto flex items-center gap-1">
                                                                <Clock className="w-3.5 h-3.5 text-slate-400" />
                                                                {step.estimated_hours}h
                                                            </span>
                                                        </div>

                                                        {/* Step Title */}
                                                        <h4 className={`text-base md:text-lg font-bold text-slate-900 ${completed ? "line-through text-slate-500" : ""}`}>
                                                            {step.title}
                                                        </h4>

                                                        {/* Why It Matters */}
                                                        <div className="mt-2 text-xs md:text-sm text-slate-600 leading-relaxed bg-slate-50 rounded-xl p-3 border border-slate-100">
                                                            <span className="font-semibold text-slate-800">Why it matters: </span>
                                                            {step.why_it_matters}
                                                        </div>

                                                        {/* Concrete Activities */}
                                                        {step.activities && step.activities.length > 0 && (
                                                            <div className="mt-3">
                                                                <div className="text-xs font-bold uppercase tracking-wider text-slate-500 mb-1.5">
                                                                    Activities & Completion Criteria:
                                                                </div>
                                                                <ul className="space-y-1">
                                                                    {step.activities.map((act, aIdx) => (
                                                                        <li key={aIdx} className="text-xs md:text-sm text-slate-700 flex items-start gap-2">
                                                                            <ChevronRight className="w-3.5 h-3.5 text-indigo-500 flex-shrink-0 mt-0.5" />
                                                                            <span>{act}</span>
                                                                        </li>
                                                                    ))}
                                                                </ul>
                                                            </div>
                                                        )}

                                                        {/* Measurable Outcome */}
                                                        {step.measurable_outcome && (
                                                            <div className="mt-3 inline-flex items-center gap-1.5 text-xs font-medium text-emerald-800 bg-emerald-50 rounded-lg px-3 py-1.5 border border-emerald-100">
                                                                <Check className="w-3.5 h-3.5 text-emerald-600" />
                                                                <span><strong className="font-semibold">Deliverable:</strong> {step.measurable_outcome}</span>
                                                            </div>
                                                        )}

                                                        {/* Verified Resources Cards */}
                                                        {step.resources && step.resources.length > 0 && (
                                                            <div className="mt-4 pt-3 border-t border-slate-100">
                                                                <div className="text-xs font-bold uppercase tracking-wider text-slate-500 mb-2">
                                                                    Recommended Resources:
                                                                </div>
                                                                <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
                                                                    {step.resources.map((res, rIdx) => (
                                                                        <a
                                                                            key={rIdx}
                                                                            href={res.url}
                                                                            target="_blank"
                                                                            rel="noopener noreferrer"
                                                                            className="group/res flex items-center justify-between p-2.5 rounded-xl border border-slate-200 bg-white hover:border-indigo-300 hover:bg-indigo-50/30 transition-all text-left shadow-2xs"
                                                                        >
                                                                            <div className="min-w-0 pr-2">
                                                                                <div className="flex items-center gap-1.5">
                                                                                    <span className="text-xs font-semibold text-slate-900 truncate group-hover/res:text-indigo-700">
                                                                                        {res.title}
                                                                                    </span>
                                                                                </div>
                                                                                <div className="flex items-center gap-2 mt-0.5 text-2xs text-slate-500">
                                                                                    <span>{res.provider}</span>
                                                                                    <span>•</span>
                                                                                    <span className={res.pricing === "free" ? "text-emerald-600 font-semibold" : "text-slate-600"}>
                                                                                        {res.pricing === "free" ? "Free" : "Paid"}
                                                                                    </span>
                                                                                    {res.verified && (
                                                                                        <span className="inline-flex items-center text-indigo-600">
                                                                                            <ShieldCheck className="w-3 h-3 mr-0.5" /> Vetted
                                                                                        </span>
                                                                                    )}
                                                                                </div>
                                                                            </div>
                                                                            <ExternalLink className="w-3.5 h-3.5 text-slate-400 group-hover/res:text-indigo-600 flex-shrink-0" />
                                                                        </a>
                                                                    ))}
                                                                </div>
                                                            </div>
                                                        )}

                                                        {/* Personal Study Notes */}
                                                        <div className="mt-3 pt-2.5 border-t border-slate-100">
                                                            <div className="flex items-center justify-between">
                                                                <span className="text-xs font-bold uppercase tracking-wider text-slate-500 flex items-center gap-1.5">
                                                                    <FileText className="w-3.5 h-3.5 text-slate-400" />
                                                                    Study Notes
                                                                </span>
                                                                {editingNotesStepId !== step.id && (
                                                                    <button
                                                                        type="button"
                                                                        onClick={() => handleStartEditNote(step)}
                                                                        className="text-2xs font-semibold text-indigo-600 hover:text-indigo-800 transition-colors"
                                                                        aria-label={step.user_notes ? "Edit note" : "Add note"}
                                                                    >
                                                                        {step.user_notes ? "Edit Note" : "+ Add Note"}
                                                                    </button>
                                                                )}
                                                            </div>

                                                            {editingNotesStepId === step.id ? (
                                                                <div className="mt-2 space-y-2">
                                                                    <textarea
                                                                        value={noteDraft}
                                                                        onChange={(e) => setNoteDraft(e.target.value)}
                                                                        placeholder="Write your notes, key takeaways, code repositories, or reflections..."
                                                                        rows={2}
                                                                        className="w-full text-xs rounded-xl border border-slate-300 p-2.5 focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 outline-none"
                                                                    />
                                                                    <div className="flex items-center justify-end gap-2">
                                                                        <button
                                                                            type="button"
                                                                            onClick={() => setEditingNotesStepId(null)}
                                                                            className="text-2xs px-2.5 py-1 rounded-lg border border-slate-200 text-slate-600 hover:bg-slate-50 font-medium"
                                                                        >
                                                                            Cancel
                                                                        </button>
                                                                        <button
                                                                            type="button"
                                                                            disabled={savingNoteStepId === step.id}
                                                                            onClick={() => handleSaveNote(step)}
                                                                            className="text-2xs px-3 py-1 rounded-lg bg-indigo-600 text-white hover:bg-indigo-700 font-semibold disabled:opacity-50"
                                                                        >
                                                                            {savingNoteStepId === step.id ? "Saving..." : "Save Note"}
                                                                        </button>
                                                                    </div>
                                                                </div>
                                                            ) : step.user_notes ? (
                                                                <div className="mt-1.5 p-2.5 rounded-xl bg-slate-50 border border-slate-200 text-xs text-slate-700">
                                                                    <span className="font-medium text-slate-800">Note: </span>{step.user_notes}
                                                                </div>
                                                            ) : null}
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        );
                                    })}
                                </div>
                            </div>
                        );
                    })}
                </div>
            )}

            {/* View 2: Weekly Schedule Timetable View */}
            {viewMode === "schedule" && (
                <div className="space-y-6">
                    <div className="rounded-3xl border border-slate-200 bg-white p-6 md:p-8 shadow-sm">
                        <div className="max-w-2xl mb-6">
                            <h3 className="text-xl font-bold text-slate-900">
                                Week-by-Week Capacity Schedule
                            </h3>
                            <p className="text-xs md:text-sm text-slate-600 mt-1">
                                Calculated with a strict cap of {preferences.hours_per_week} hours/week to prevent burnout and ensure steady practical project progress.
                            </p>
                        </div>

                        {((schedule?.weekly_schedule && schedule.weekly_schedule.length > 0) || (schedule?.weeks && schedule.weeks.length > 0)) ? (
                            <div className="space-y-4">
                                {(schedule.weekly_schedule || schedule.weeks).map((week, wIdx) => {
                                    const percentAllocated = Math.min(100, Math.round((week.allocated_hours / (preferences.hours_per_week || 10)) * 100));

                                    return (
                                        <div
                                            key={week.week_number || wIdx}
                                            className="rounded-2xl border border-slate-200 bg-slate-50/40 p-5 md:p-6"
                                        >
                                            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-4">
                                                <div>
                                                    <div className="flex items-center gap-2">
                                                        <span className="rounded-full bg-indigo-600 text-white text-xs font-bold px-2.5 py-0.5">
                                                            Week {week.week_number}
                                                        </span>
                                                        <h4 className="text-base font-bold text-slate-900">
                                                            {week.milestone || week.theme || `Phase Focus Week ${week.week_number}`}
                                                        </h4>
                                                    </div>
                                                    <div className="flex flex-wrap items-center gap-3 text-xs text-slate-500 mt-1.5">
                                                        <span>{week.start_date} → {week.end_date}</span>
                                                        {week.learning_hours > 0 && (
                                                            <span>• {week.learning_hours}h Theory</span>
                                                        )}
                                                        {((week.practising_hours || 0) + (week.building_hours || 0)) > 0 && (
                                                            <span>• {(week.practising_hours || 0) + (week.building_hours || 0)}h Build/Practice</span>
                                                        )}
                                                    </div>
                                                </div>

                                                <div className="text-right sm:self-auto self-start">
                                                    <span className="text-xs font-bold text-slate-700">
                                                        {week.allocated_hours} / {preferences.hours_per_week} hrs
                                                    </span>
                                                    <div className="w-24 bg-slate-200 h-1.5 rounded-full overflow-hidden mt-1">
                                                        <div
                                                            className="bg-indigo-600 h-full rounded-full"
                                                            style={{ width: `${percentAllocated}%` }}
                                                        />
                                                    </div>
                                                </div>
                                            </div>

                                            {/* Step Breakdown in Week */}
                                            {((week.step_titles && week.step_titles.length > 0) || (week.scheduled_steps && week.scheduled_steps.length > 0)) && (
                                                <div className="space-y-2 mt-3 pt-3 border-t border-slate-200/60">
                                                    {(week.step_titles || week.scheduled_steps).map((st, i) => (
                                                        <div
                                                            key={i}
                                                            className="flex items-center justify-between text-xs py-2 px-3 rounded-xl bg-white border border-slate-200/80"
                                                        >
                                                            <div className="flex items-center gap-2 truncate">
                                                                <span className="w-1.5 h-1.5 rounded-full bg-indigo-500 flex-shrink-0" />
                                                                <span className="font-semibold text-slate-800 truncate">
                                                                    {typeof st === "string" ? st : st.title}
                                                                </span>
                                                                {typeof st !== "string" && st.stage && (
                                                                    <span className="text-2xs uppercase tracking-wider font-bold px-1.5 py-0.5 rounded bg-slate-100 text-slate-600">
                                                                        {st.stage}
                                                                    </span>
                                                                )}
                                                            </div>
                                                            {typeof st !== "string" && st.hours_allocated && (
                                                                <span className="font-medium text-slate-500 flex-shrink-0 ml-2">
                                                                    {st.hours_allocated}h
                                                                </span>
                                                            )}
                                                        </div>
                                                    ))}
                                                </div>
                                            )}
                                        </div>
                                    );
                                })}
                            </div>
                        ) : (
                            <p className="text-sm text-slate-500">No weekly schedule data available.</p>
                        )}
                    </div>
                </div>
            )}

            {/* Academic & Career Integrity Callout */}
            <div className="rounded-2xl border border-indigo-100 bg-indigo-50/50 p-5 text-xs text-indigo-950 flex items-start gap-3.5">
                <ShieldCheck className="w-5 h-5 text-indigo-600 flex-shrink-0 mt-0.5" />
                <div className="space-y-1">
                    <p className="font-bold text-indigo-900 text-sm">
                        JobJazz Career Integrity & Reassessment Note
                    </p>
                    <p className="text-slate-600 leading-relaxed">
                        Completing roadmap steps helps you stay accountable, but it does <strong className="font-semibold text-slate-900">not</strong> automatically inflate your match score or guarantee role readiness. To reflect new proficiency, apply your learning in real projects, document them in your resume, and re-run your JobJazz match analysis.
                    </p>
                </div>
            </div>
        </div>
    );
}
