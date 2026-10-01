import { useState, useRef } from "react"
import { analyzeJobDescription, analyzeJobDescriptionPdf } from "../api/jobjazzApi"

function JobDescriptionInput({ onJobAnalyzed }) {
    const [mode, setMode] = useState("text") // "text" | "pdf"
    const [jobDescription, setJobDescription] = useState("")
    const [pdfFile, setPdfFile] = useState(null)
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState("")

    const fileInputRef = useRef(null)

    const handleAnalyzeText = async () => {
        if (!jobDescription.trim()) {
            setError("Please paste a job description first.")
            return
        }

        setLoading(true)
        setError("")

        try {
            const result = await analyzeJobDescription(jobDescription)
            console.log("Job description analysis received:", result)
            onJobAnalyzed(result)
        } catch (err) {
            setError(
                err instanceof Error
                    ? err.message
                    : "Something went wrong while analyzing the job description."
            )
        } finally {
            setLoading(false)
        }
    }

    const handleAnalyzePdf = async () => {
        if (!pdfFile) {
            setError("Please select a PDF file first.")
            return
        }

        setLoading(true)
        setError("")

        try {
            const result = await analyzeJobDescriptionPdf(pdfFile)
            console.log("Job description PDF analysis received:", result)
            onJobAnalyzed(result)
        } catch (err) {
            setError(
                err instanceof Error
                    ? err.message
                    : "Something went wrong while analyzing the job description PDF."
            )
        } finally {
            setLoading(false)
        }
    }

    const handleAnalyze = () => {
        if (mode === "text") {
            handleAnalyzeText()
        } else {
            handleAnalyzePdf()
        }
    }

    const handleFileChange = (e) => {
        const file = e.target.files?.[0]
        if (!file) return

        if (file.type !== "application/pdf") {
            setError("Only PDF files are supported.")
            setPdfFile(null)
            return
        }

        setError("")
        setPdfFile(file)
    }

    return (
        <section className="relative z-10 mx-auto flex min-h-screen max-w-5xl flex-col justify-center px-6 py-28 sm:px-10 lg:px-12">
            <div className="rounded-3xl border border-white/10 bg-white/[0.04] p-8 backdrop-blur-xl sm:p-10">

                {/* Header */}
                <div>
                    <p className="text-sm font-medium uppercase tracking-[0.2em] text-purple-300">
                        JobJazz Analysis
                    </p>

                    <h1 className="mt-3 text-4xl font-bold tracking-tight text-white sm:text-5xl">
                        Analyze your fit for a job
                    </h1>

                    <p className="mt-4 max-w-2xl text-base leading-7 text-white/55 sm:text-lg">
                        Provide a job description and JobJazz will understand the role,
                        required skills, experience, education, and important keywords.
                    </p>
                </div>

                {/* Mode Toggle */}
                <div className="mt-8 flex gap-4">
                    <button
                        type="button"
                        onClick={() => { setMode("text"); setError(""); }}
                        className={`rounded-xl px-5 py-2 text-sm font-medium transition ${
                            mode === "text"
                                ? "bg-purple-500/20 text-purple-200 border border-purple-500/30"
                                : "text-white/60 hover:bg-white/5 hover:text-white"
                        }`}
                    >
                        Paste Text
                    </button>
                    <button
                        type="button"
                        onClick={() => { setMode("pdf"); setError(""); }}
                        className={`rounded-xl px-5 py-2 text-sm font-medium transition ${
                            mode === "pdf"
                                ? "bg-purple-500/20 text-purple-200 border border-purple-500/30"
                                : "text-white/60 hover:bg-white/5 hover:text-white"
                        }`}
                    >
                        Upload PDF
                    </button>
                </div>

                {/* Job Description Input */}
                <div className="mt-6">
                    {mode === "text" ? (
                        <>
                            <label
                                htmlFor="job-description"
                                className="mb-3 block text-sm font-medium text-white/70"
                            >
                                Job description text
                            </label>

                            <textarea
                                id="job-description"
                                value={jobDescription}
                                onChange={(event) => {
                                    setJobDescription(event.target.value)
                                    if (error) setError("")
                                }}
                                placeholder="Paste the complete job description here..."
                                rows={14}
                                className="w-full resize-y rounded-2xl border border-white/10 bg-black/20 px-5 py-4 text-sm leading-7 text-white outline-none placeholder:text-white/25 transition focus:border-purple-400/40 focus:bg-black/30"
                            />

                            {/* Character count */}
                            <div className="mt-2 flex justify-end">
                                <span className="text-xs text-white/30">
                                    {jobDescription.length} characters
                                </span>
                            </div>
                        </>
                    ) : (
                        <div className="rounded-2xl border border-white/10 bg-black/20 p-8 text-center transition hover:border-purple-400/40">
                            <input
                                type="file"
                                accept=".pdf"
                                className="hidden"
                                ref={fileInputRef}
                                onChange={handleFileChange}
                            />
                            {pdfFile ? (
                                <div className="flex flex-col items-center gap-4">
                                    <div className="flex h-16 w-16 items-center justify-center rounded-full bg-purple-500/20">
                                        <svg
                                            className="h-8 w-8 text-purple-300"
                                            fill="none"
                                            viewBox="0 0 24 24"
                                            stroke="currentColor"
                                        >
                                            <path
                                                strokeLinecap="round"
                                                strokeLinejoin="round"
                                                strokeWidth={2}
                                                d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                                            />
                                        </svg>
                                    </div>
                                    <div>
                                        <p className="text-sm font-medium text-white">{pdfFile.name}</p>
                                        <p className="text-xs text-white/50">{(pdfFile.size / 1024 / 1024).toFixed(2)} MB</p>
                                    </div>
                                    <button
                                        type="button"
                                        onClick={() => fileInputRef.current?.click()}
                                        className="mt-2 text-sm text-purple-300 hover:text-purple-200"
                                    >
                                        Select a different file
                                    </button>
                                </div>
                            ) : (
                                <div className="flex flex-col items-center gap-4">
                                    <button
                                        type="button"
                                        onClick={() => fileInputRef.current?.click()}
                                        className="rounded-full bg-white/10 p-4 transition hover:bg-white/20"
                                    >
                                        <svg
                                            className="h-8 w-8 text-white/70"
                                            fill="none"
                                            viewBox="0 0 24 24"
                                            stroke="currentColor"
                                        >
                                            <path
                                                strokeLinecap="round"
                                                strokeLinejoin="round"
                                                strokeWidth={2}
                                                d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12"
                                            />
                                        </svg>
                                    </button>
                                    <div>
                                        <p className="text-sm font-medium text-white">Upload Job Description PDF</p>
                                        <p className="mt-1 text-xs text-white/50">Only PDF files are supported</p>
                                    </div>
                                </div>
                            )}
                        </div>
                    )}
                </div>

                {/* Error */}
                {error && (
                    <div className="mt-4 rounded-xl border border-red-400/20 bg-red-400/10 px-4 py-3 text-sm text-red-300">
                        {error}
                    </div>
                )}

                {/* Analyze Button */}
                <div className="mt-6 flex justify-end">
                    <button
                        type="button"
                        onClick={handleAnalyze}
                        disabled={loading}
                        className="jj-btn-primary disabled:cursor-not-allowed disabled:opacity-50"
                    >
                        {loading ? "Analyzing job..." : "Analyze Job →"}
                    </button>
                </div>

            </div>
        </section>
    )
}

export default JobDescriptionInput