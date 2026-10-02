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
            // Check if error is an object with detail (from backend 422)
            if (err.detail) {
                setError(err.detail)
            } else {
                setError(
                    err instanceof Error
                        ? err.message
                        : "Something went wrong while analyzing the job description."
                )
            }
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
            if (err.detail) {
                setError(err.detail)
            } else {
                setError(
                    err instanceof Error
                        ? err.message
                        : "Something went wrong while analyzing the job description PDF."
                )
            }
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
            <div className="rounded-3xl border border-slate-200 bg-white p-8 shadow-xl shadow-slate-200/50 sm:p-10 text-center md:text-left">

                {/* Header */}
                <div>
                    <p className="text-sm font-medium uppercase tracking-[0.2em] text-indigo-600">
                        JobJazz Analysis
                    </p>

                    <h1 className="mt-3 text-3xl font-bold tracking-tight text-slate-900 sm:text-5xl">
                        Analyze your fit for a job
                    </h1>

                    <p className="mt-4 max-w-2xl text-base leading-7 text-slate-600 sm:text-lg mx-auto md:mx-0">
                        Provide a job description and JobJazz will understand the role,
                        required skills, experience, education, and important keywords.
                    </p>
                </div>

                {/* Mode Toggle */}
                <div className="mt-8 flex justify-center md:justify-start gap-4">
                    <button
                        type="button"
                        onClick={() => { setMode("text"); setError(""); }}
                        className={`rounded-xl px-5 py-2 text-sm font-semibold transition shadow-sm ${
                            mode === "text"
                                ? "bg-indigo-50 text-indigo-700 border border-indigo-200"
                                : "bg-white text-slate-600 border border-slate-200 hover:bg-slate-50"
                        }`}
                    >
                        Paste Text
                    </button>
                    <button
                        type="button"
                        onClick={() => { setMode("pdf"); setError(""); }}
                        className={`rounded-xl px-5 py-2 text-sm font-semibold transition shadow-sm ${
                            mode === "pdf"
                                ? "bg-indigo-50 text-indigo-700 border border-indigo-200"
                                : "bg-white text-slate-600 border border-slate-200 hover:bg-slate-50"
                        }`}
                    >
                        Upload PDF
                    </button>
                </div>

                {/* Job Description Input */}
                <div className="mt-6 text-left">
                    {mode === "text" ? (
                        <>
                            <label
                                htmlFor="job-description"
                                className="mb-3 block text-sm font-medium text-slate-700"
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
                                rows={12}
                                className="w-full resize-y rounded-2xl border border-slate-200 bg-slate-50 px-5 py-4 text-sm leading-7 text-slate-900 outline-none placeholder:text-slate-400 transition focus:border-indigo-400 focus:bg-white focus:ring-4 focus:ring-indigo-50"
                            />

                            {/* Character count */}
                            <div className="mt-2 flex justify-end">
                                <span className="text-xs font-medium text-slate-500">
                                    {jobDescription.length} characters
                                </span>
                            </div>
                        </>
                    ) : (
                        <div className="rounded-2xl border-2 border-dashed border-slate-200 bg-slate-50 p-8 text-center transition hover:border-indigo-300 hover:bg-slate-100 cursor-pointer"
                             onClick={() => fileInputRef.current?.click()}>
                            <input
                                type="file"
                                accept=".pdf"
                                className="hidden"
                                ref={fileInputRef}
                                onChange={handleFileChange}
                            />
                            {pdfFile ? (
                                <div className="flex flex-col items-center gap-4">
                                    <div className="flex h-16 w-16 items-center justify-center rounded-full bg-indigo-50 text-indigo-600">
                                        <svg
                                            className="h-8 w-8"
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
                                        <p className="text-sm font-semibold text-slate-900">{pdfFile.name}</p>
                                        <p className="text-xs font-medium text-slate-500">{(pdfFile.size / 1024 / 1024).toFixed(2)} MB</p>
                                    </div>
                                    <button
                                        type="button"
                                        onClick={(e) => { e.stopPropagation(); fileInputRef.current?.click(); }}
                                        className="mt-2 text-sm font-semibold text-indigo-600 hover:text-indigo-700"
                                    >
                                        Select a different file
                                    </button>
                                </div>
                            ) : (
                                <div className="flex flex-col items-center gap-4">
                                    <div className="rounded-full bg-white p-4 shadow-sm border border-slate-100 text-slate-400">
                                        <svg
                                            className="h-8 w-8"
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
                                    </div>
                                    <div>
                                        <p className="text-sm font-semibold text-slate-900">Upload Job Description PDF</p>
                                        <p className="mt-1 text-xs font-medium text-slate-500">Only PDF files are supported</p>
                                    </div>
                                </div>
                            )}
                        </div>
                    )}
                </div>

                {/* Error */}
                {error && (
                    <div className="mt-4 rounded-xl border border-rose-200 bg-rose-50 px-4 py-3 text-sm font-medium text-rose-700">
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