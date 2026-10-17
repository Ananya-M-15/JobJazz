import { useState, useEffect } from "react"
import Background from "./components/Background"
import Navbar from "./components/Navbar"
import ResumeUpload from "./components/ResumeUpload"
import CareerProfile from "./components/CareerProfile"
import JobDescriptionInput from "./components/JobDescriptionInput"
import JobDescriptionConfirmation from "./components/JobDescriptionConfirmation"
import DashboardLayout from "./components/dashboard/DashboardLayout"
import Hero from "./components/home/Hero"
import WorkflowFlow from "./components/home/WorkflowFlow"
import CapabilitiesAsymmetric from "./components/home/CapabilitiesAsymmetric"
import MatchingMatrix from "./components/home/MatchingMatrix"
import ArchitectureDiagram from "./components/home/ArchitectureDiagram"
import HowItWorksTimeline from "./components/home/HowItWorksTimeline"
import WhyJobJazz from "./components/home/WhyJobJazz"
import FinalCTA from "./components/home/FinalCTA"
import Footer from "./components/home/Footer"
import { analyzeMatching, analyzeSkillGap, generateRecommendations, getAnalysis } from "./api/jobjazzApi"

function App() {
  const [showAnalysis, setShowAnalysis] = useState(false)
  const [workflowStep, setWorkflowStep] = useState("resume") // resume, career_profile, job, job_confirmation, analyzing, results

  const [resumeData, setResumeData] = useState(null)
  const [jobData, setJobData] = useState(null)

  const [matchResult, setMatchResult] = useState(null)
  const [skillGap, setSkillGap] = useState(null)
  const [recommendations, setRecommendations] = useState(null)
  const [analysisId, setAnalysisId] = useState(null)

  const [loadingStep, setLoadingStep] = useState("")
  const [error, setError] = useState("")
  const [recoveryMessage, setRecoveryMessage] = useState("")
  const [isRestoringSession, setIsRestoringSession] = useState(() => {
    return Boolean(typeof window !== "undefined" && window.sessionStorage?.getItem("jobjazz_active_analysis_id"))
  })

  // Restore active analysis session on page refresh if available
  useEffect(() => {
    const savedAnalysisId = sessionStorage.getItem("jobjazz_active_analysis_id")
    if (!savedAnalysisId) return

    let isMounted = true

    async function restoreAnalysisSession() {
      try {
        const data = await getAnalysis(savedAnalysisId)
        if (!isMounted || !data) return

        setAnalysisId(data.analysis_id)
        setMatchResult(data.match_result)
        setSkillGap(data.skill_gap)
        setRecommendations(data.recommendations)

        if (data.candidate_profile) {
          setResumeData({
            resume_id: data.resume_id,
            profile: data.candidate_profile,
          })
        }

        if (data.job_profile) {
          setJobData({
            job_description_id: data.job_description_id,
            profile: data.job_profile,
          })
        }

        setShowAnalysis(true)
        setWorkflowStep("results")
      } catch (err) {
        console.warn("Could not restore previous analysis session:", err)
        sessionStorage.removeItem("jobjazz_active_analysis_id")
        setRecoveryMessage("Your previous analysis session could not be restored or has expired. You can start a fresh analysis below.")
      } finally {
        if (isMounted) {
          setIsRestoringSession(false)
        }
      }
    }

    restoreAnalysisSession()

    return () => {
      isMounted = false
    }
  }, [])

  const startAnalysis = () => {
    sessionStorage.removeItem("jobjazz_active_analysis_id")
    setRecoveryMessage("")
    setShowAnalysis(true)
    setWorkflowStep("resume")
    setResumeData(null)
    setJobData(null)
    setMatchResult(null)
    setSkillGap(null)
    setRecommendations(null)
    setAnalysisId(null)
  }

  const analyzeAnotherJob = () => {
    sessionStorage.removeItem("jobjazz_active_analysis_id")
    setRecoveryMessage("")
    setWorkflowStep("job")
    setJobData(null)
    setMatchResult(null)
    setSkillGap(null)
    setRecommendations(null)
    setAnalysisId(null)
  }

  const handleResumeAnalyzed = (data) => {
    setResumeData(data)
    setWorkflowStep("career_profile")
  }

  const handleCareerProfileContinue = () => {
    setWorkflowStep("job")
  }

  const handleJobAnalyzed = (currentJobData) => {
    setJobData(currentJobData)
    setWorkflowStep("job_confirmation")
    setError("")
  }

  const handleJobConfirmed = async () => {
    setWorkflowStep("analyzing")
    setError("")
    setMatchResult(null)
    setSkillGap(null)
    setRecommendations(null)

    try {
      setLoadingStep("Comparing your profile to the job...")
      const matchPayload = {
        resume_id: resumeData.resume_id,
        job_description_id: jobData.job_description_id,
        resume: resumeData.profile,
        job: jobData.profile
      }
      const matchRes = await analyzeMatching(matchPayload)
      setMatchResult(matchRes.match_result)
      setAnalysisId(matchRes.analysis_id)

      setLoadingStep("Identifying skill gaps...")
      const gapPayload = {
        analysis_id: matchRes.analysis_id,
        match_result: matchRes.match_result
      }
      const gapRes = await analyzeSkillGap(gapPayload)
      setSkillGap(gapRes.skill_gap)

      setLoadingStep("Generating recommendations...")
      const recPayload = {
        analysis_id: matchRes.analysis_id,
        match_result: matchRes.match_result,
        skill_gap: gapRes.skill_gap
      }
      const recRes = await generateRecommendations(recPayload)
      setRecommendations(recRes)

      // Persist active analysis ID for session recovery across page reloads
      sessionStorage.setItem("jobjazz_active_analysis_id", matchRes.analysis_id)

      setWorkflowStep("results")
    } catch (err) {
      setError(err instanceof Error ? err.message : "An unexpected error occurred during analysis.")
    }
  }

  // Session restoring screen
  if (isRestoringSession) {
    return (
      <main className="relative min-h-screen flex items-center justify-center bg-slate-50 text-slate-900 px-6">
        <Background />
        <div className="relative z-10 w-full max-w-md rounded-3xl border border-slate-200 bg-white p-10 text-center shadow-xl shadow-slate-200/50">
          <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-2xl bg-indigo-50 text-indigo-600 mb-4 font-bold text-2xl shadow-sm border border-indigo-100">
            ✨
          </div>
          <h2 className="text-xl font-bold text-slate-900">Restoring Your Analysis</h2>
          <p className="mt-2 text-sm text-slate-500">
            Recovering your match results, skill gaps, and learning roadmap...
          </p>
          <div className="mt-6 flex justify-center">
            <div className="h-8 w-8 animate-spin rounded-full border-3 border-slate-100 border-t-indigo-600"></div>
          </div>
        </div>
      </main>
    )
  }

  // Resume analysis screen
  if (showAnalysis) {
    return (
      <main className="relative min-h-screen overflow-hidden text-slate-900">
        <Navbar onAnalyzeClick={startAnalysis} />
        <Background />

        {workflowStep === "resume" && (
          <ResumeUpload onResumeAnalyzed={handleResumeAnalyzed} />
        )}

        {workflowStep === "career_profile" && (
          <CareerProfile resumeData={resumeData} onContinue={handleCareerProfileContinue} />
        )}

        {workflowStep === "job" && (
          <JobDescriptionInput onJobAnalyzed={handleJobAnalyzed} />
        )}

        {workflowStep === "job_confirmation" && jobData && (
          <JobDescriptionConfirmation
            profile={jobData.profile}
            onConfirm={handleJobConfirmed}
            onCancel={() => setWorkflowStep("job")}
          />
        )}

        {workflowStep === "analyzing" && (
          <div className="relative z-10 flex min-h-screen items-center justify-center px-6">
            <div className="w-full max-w-lg rounded-3xl border border-slate-200 bg-white p-10 text-center shadow-xl shadow-slate-200/50">
              <p className="text-xs font-semibold uppercase tracking-[0.2em] text-indigo-600">
                JobJazz Analysis
              </p>

              {!error ? (
                <>
                    <h1 className="mt-4 text-2xl font-bold text-slate-900 sm:text-3xl">
                        {loadingStep}
                    </h1>
                    <p className="mt-2 text-sm text-slate-500">
                        Analyzing your experience and career alignment
                    </p>
                    <div className="mt-8 flex justify-center">
                        <div className="h-10 w-10 animate-spin rounded-full border-4 border-slate-100 border-t-indigo-600"></div>
                    </div>
                </>
              ) : (
                <>
                    <h1 className="mt-4 text-2xl font-bold text-rose-600 sm:text-3xl">
                        Analysis Could Not Complete
                    </h1>
                    <div className="mt-5 rounded-2xl border border-rose-200 bg-rose-50 p-4 text-sm font-medium text-rose-700 text-left">
                        {error}
                    </div>
                    <button
                        onClick={() => { setError(""); setWorkflowStep("job"); }}
                        className="mt-6 w-full jj-btn-primary"
                    >
                        Try Again
                    </button>
                </>
              )}
            </div>
          </div>
        )}

        {workflowStep === "results" && (
          <DashboardLayout
            analysisId={analysisId}
            matchResult={matchResult}
            skillGap={skillGap}
            recommendations={recommendations}
            jobProfile={jobData?.profile}
            candidateProfile={resumeData?.profile}
            onStartOver={analyzeAnotherJob}
          />
        )}
      </main>
    )
  }

  // Landing page
  return (
    <main className="relative min-h-screen text-slate-900 bg-white selection:bg-[var(--jj-primary-blue)] selection:text-white flex flex-col">
      <Navbar onAnalyzeClick={startAnalysis} />

      {recoveryMessage && (
        <div className="mx-auto w-full max-w-4xl px-6 pt-20 -mb-16 relative z-30">
          <div className="flex items-center justify-between gap-3 rounded-2xl border border-amber-200 bg-amber-50/95 p-4 text-sm font-medium text-amber-800 shadow-sm backdrop-blur-sm">
            <div className="flex items-center gap-2.5">
              <span className="text-lg">ℹ️</span>
              <span>{recoveryMessage}</span>
            </div>
            <button
              onClick={() => setRecoveryMessage("")}
              className="text-xs font-bold text-amber-700 hover:text-amber-900 px-2 py-1 rounded-lg hover:bg-amber-100 transition-colors"
            >
              Dismiss
            </button>
          </div>
        </div>
      )}

      <Hero onAnalyzeClick={startAnalysis} />
      <WorkflowFlow />
      <CapabilitiesAsymmetric />
      <MatchingMatrix />
      <ArchitectureDiagram />
      <HowItWorksTimeline />
      <WhyJobJazz />
      <FinalCTA onAnalyzeClick={startAnalysis} />
      <Footer />

    </main>
  )
}

export default App
