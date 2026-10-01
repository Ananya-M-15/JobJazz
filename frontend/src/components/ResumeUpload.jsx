import React, { useState } from "react";
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
            <div className="rounded-2xl border border-white/10 bg-white/[0.04] p-8 backdrop-blur-xl">
                <div className="mb-8">
                    <p className="text-sm font-medium uppercase tracking-[0.2em] text-purple-300">
                        JobJazz Analysis
                    </p>

                    <h2 className="mt-3 text-3xl font-bold text-white sm:text-4xl">
                        Upload your resume
                    </h2>

                    <p className="mt-3 max-w-2xl text-white/60">
                        Upload your PDF resume and JobJazz will extract your
                        professional profile for the next stages of analysis.
                    </p>
                </div>

                <label
                    htmlFor="resume-upload"
                    className="flex cursor-pointer flex-col items-center justify-center rounded-xl border border-dashed border-white/20 bg-black/20 px-6 py-14 text-center transition hover:border-white/40 hover:bg-white/[0.04]"
                >
                    <div className="text-4xl">↑</div>

                    <p className="mt-4 text-lg font-medium text-white">
                        {file ? file.name : "Choose your resume"}
                    </p>

                    <p className="mt-2 text-sm text-white/50">
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
                    <div className="mt-4 rounded-lg border border-red-400/20 bg-red-400/10 px-4 py-3 text-sm text-red-300">
                        {error}
                    </div>
                )}

                <button
                    type="button"
                    onClick={handleUpload}
                    disabled={!file || loading}
                    className="mt-6 w-full rounded-xl bg-white px-5 py-3 font-semibold text-black transition hover:bg-white/90 disabled:cursor-not-allowed disabled:opacity-40"
                >
                    {loading ? "Analyzing resume..." : "Analyze Resume"}
                </button>
            </div>
        </section>
    );
}

export default ResumeUpload;