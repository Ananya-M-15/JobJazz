import { useState } from "react"
import Background from "./components/Background"
import Navbar from "./components/Navbar"
import ResumeUpload from "./components/ResumeUpload"
import CareerProfile from "./components/CareerProfile"
import JobDescriptionInput from "./components/JobDescriptionInput"
import JobDescriptionConfirmation from "./components/JobDescriptionConfirmation"
import DashboardLayout from "./components/dashboard/DashboardLayout"
import HowItWorks from "./components/home/HowItWorks"
import { analyzeMatching, analyzeSkillGap, generateRecommendations } from "./api/jobjazzApi"

function App() {
  const [showAnalysis, setShowAnalysis] = useState(false)
  const [workflowStep, setWorkflowStep] = useState("resume") // resume, career_profile, job, job_confirmation, analyzing, results
  
  const [resumeData, setResumeData] = useState(null)
  const [jobData, setJobData] = useState(null)
  
  const [matchResult, setMatchResult] = useState(null)
  const [skillGap, setSkillGap] = useState(null)
  const [recommendations, setRecommendations] = useState(null)

  const [loadingStep, setLoadingStep] = useState("")
  const [error, setError] = useState("")

  const startAnalysis = () => {
    setShowAnalysis(true)
    setWorkflowStep("resume")
    setResumeData(null)
    setJobData(null)
    setMatchResult(null)
    setSkillGap(null)
    setRecommendations(null)
  }

  const analyzeAnotherJob = () => {
    setWorkflowStep("job")
    setJobData(null)
    setMatchResult(null)
    setSkillGap(null)
    setRecommendations(null)
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

      setWorkflowStep("results")
    } catch (err) {
      setError(err instanceof Error ? err.message : "An unexpected error occurred during analysis.")
    }
  }

  // Resume analysis screen
  if (showAnalysis) {
    return (
      <main className="relative min-h-screen overflow-hidden text-white">
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
            <div className="w-full max-w-lg rounded-3xl border border-white/10 bg-white/[0.04] p-10 text-center backdrop-blur-xl">
              <p className="text-sm font-medium uppercase tracking-[0.2em] text-purple-300">
                JobJazz Analysis
              </p>
              
              {!error ? (
                <>
                    <h1 className="mt-5 text-2xl font-bold text-white sm:text-3xl">
                        {loadingStep}
                    </h1>
                    <div className="mt-10 flex justify-center">
                        <div className="h-10 w-10 animate-spin rounded-full border-4 border-white/10 border-t-purple-400"></div>
                    </div>
                </>
              ) : (
                <>
                    <h1 className="mt-5 text-2xl font-bold text-red-400 sm:text-3xl">
                        Analysis Failed
                    </h1>
                    <div className="mt-6 rounded-xl border border-red-500/20 bg-red-500/10 p-4 text-sm text-red-200">
                        {error}
                    </div>
                    <button
                        onClick={() => setWorkflowStep("job")}
                        className="mt-8 w-full rounded-xl bg-white px-5 py-3 font-semibold text-black transition hover:bg-white/90"
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
            matchResult={matchResult}
            skillGap={skillGap}
            recommendations={recommendations}
            jobProfile={jobData?.profile}
            onStartOver={analyzeAnotherJob}
          />
        )}
      </main>
    )
  }

  // Landing page
  return (
    <main className="relative min-h-screen text-slate-900 bg-slate-50 selection:bg-indigo-100 selection:text-indigo-900">
      <Navbar onAnalyzeClick={startAnalysis} />
      
      <Background />

      {/* Hero Section */}
      <section className="relative z-10 mx-auto max-w-7xl px-6 pt-32 pb-20 sm:pt-40 sm:px-12 lg:px-16">
        <div className="max-w-2xl lg:text-left">
          <h1 className="text-5xl font-bold tracking-tight text-slate-900 md:text-6xl max-w-xl">
            Make every application count.
          </h1>
          <p className="mt-6 text-lg leading-8 text-slate-600 max-w-xl">
            See how your resume matches the job before you apply. JobJazz highlights your strengths, identifies important gaps, and gives you clear next steps to improve your fit.
          </p>
          
          <div className="mt-10 flex flex-col sm:flex-row items-center justify-start gap-4">
            <button onClick={startAnalysis} className="jj-btn-primary">
              Analyze my resume
            </button>
          </div>
          
          <p className="mt-6 text-sm font-medium text-slate-500">
            Resume analysis &bull; Job matching &bull; Skill gaps &bull; Actionable insights
          </p>
        </div>
      </section>

      <HowItWorks />
      
      {/* Capabilities Section */}
      <section id="capabilities" className="relative z-10 mx-auto max-w-7xl px-6 py-24 sm:py-32 lg:px-8 border-t border-slate-200 bg-slate-50">
        <div className="mx-auto max-w-2xl text-center lg:text-left lg:mx-0">
            <h2 className="text-3xl font-bold tracking-tight text-slate-900 sm:text-4xl">
              A clearer view of your fit
            </h2>
        </div>

        <div className="mx-auto mt-16 max-w-5xl lg:mx-0 sm:mt-20">
            <dl className="grid grid-cols-1 gap-12 sm:grid-cols-2 lg:grid-cols-4 text-left">
                
                <div className="flex flex-col">
                    <dt className="text-lg font-semibold leading-7 text-slate-900">
                        Skills
                    </dt>
                    <dd className="mt-2 text-base leading-7 text-slate-600">
                        See which requirements your resume already covers.
                    </dd>
                </div>
                
                <div className="flex flex-col">
                    <dt className="text-lg font-semibold leading-7 text-slate-900">
                        Experience
                    </dt>
                    <dd className="mt-2 text-base leading-7 text-slate-600">
                        Understand how your experience aligns with the role.
                    </dd>
                </div>

                <div className="flex flex-col">
                    <dt className="text-lg font-semibold leading-7 text-slate-900">
                        Education
                    </dt>
                    <dd className="mt-2 text-base leading-7 text-slate-600">
                        Check how your academic background matches the stated requirements.
                    </dd>
                </div>

                <div className="flex flex-col">
                    <dt className="text-lg font-semibold leading-7 text-slate-900">
                        Keywords & gaps
                    </dt>
                    <dd className="mt-2 text-base leading-7 text-slate-600">
                        Identify important requirements that may need attention.
                    </dd>
                </div>

            </dl>
        </div>
      </section>

      {/* Final CTA */}
      <section className="relative z-10 mx-auto max-w-7xl px-6 py-24 sm:py-32 lg:px-8 text-center">
        <h2 className="text-3xl font-bold tracking-tight text-slate-900 sm:text-4xl">
          Know where you stand before you apply.
        </h2>
        <div className="mt-10 flex items-center justify-center">
          <button onClick={startAnalysis} className="jj-btn-primary">
            Analyze my resume
          </button>
        </div>
      </section>
    </main>
  )
}

export default App