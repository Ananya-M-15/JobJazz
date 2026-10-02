import { useState } from "react";
import { extractResume } from "../api/jobjazzApi";

function ResumeUpload({ onResumeAnalyzed }) {
    const [file, setFile] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    const handleFileChange = (event) => {
        const selectedFile = event.target.files?.[0];

        setError("");

        if (!selectedFile) {
            setFile(null);
            return;
        }

        if (selectedFile.type !== "application/pdf") {
            setFile(null);
            setError("Please upload a PDF resume.");
            return;
        }

        setFile(selectedFile);
    };

    const handleUpload = async () => {
        if (!file) {
            setError("Please select a PDF resume first.");
            return;
        }

        setLoading(true);
        setError("");

        try {
            const result = await extractResume(file);

            onResumeAnalyzed(result);
        } catch (err) {
            setError(
                err instanceof Error
                    ? err.message
                    : "Something went wrong while analyzing the resume."
            );
        } finally {
            setLoading(false);
        }
    };

    return (
        <section className="relative z-10 mx-auto flex min-h-screen max-w-4xl flex-col justify-center px-6 py-24">
            <div className="rounded-3xl border border-slate-200 bg-white p-8 shadow-xl shadow-slate-200/50 sm:p-10 text-center md:text-left">
                <div className="mb-8">
                    <p className="text-sm font-medium uppercase tracking-[0.2em] text-indigo-600">
                        JobJazz Analysis
                    </p>

                    <h2 className="mt-3 text-3xl font-bold text-slate-900 sm:text-4xl">
                        Upload your resume
                    </h2>

                    <p className="mt-3 max-w-2xl text-slate-600 mx-auto md:mx-0">
                        Upload your PDF resume and JobJazz will extract your
                        professional profile for the next stages of analysis.
                    </p>
                </div>

                <label
                    htmlFor="resume-upload"
                    className="flex cursor-pointer flex-col items-center justify-center rounded-2xl border-2 border-dashed border-slate-200 bg-slate-50 px-6 py-14 text-center transition hover:border-indigo-300 hover:bg-slate-100"
                >
                    <div className="flex h-16 w-16 items-center justify-center rounded-full bg-white shadow-sm border border-slate-100 text-indigo-600 mb-4">
                        <svg className="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
                        </svg>
                    </div>

                    <p className="text-lg font-semibold text-slate-900">
                        {file ? file.name : "Choose your resume"}
                    </p>

                    <p className="mt-2 text-sm font-medium text-slate-500">
                        PDF files only
                    </p>

                    <input
                        id="resume-upload"
                        type="file"
                        accept=".pdf,application/pdf"
                        onChange={handleFileChange}
                        className="hidden"
                    />
                </label>

                {error && (
                    <div className="mt-4 rounded-xl border border-rose-200 bg-rose-50 px-4 py-3 text-sm font-medium text-rose-700">
                        {error}
                    </div>
                )}

                <div className="mt-8 flex justify-end">
                    <button
                        type="button"
                        onClick={handleUpload}
                        disabled={!file || loading}
                        className="w-full sm:w-auto jj-btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                        {loading ? "Analyzing resume..." : "Analyze Resume →"}
                    </button>
                </div>
            </div>
        </section>
    );
}

export default ResumeUpload;