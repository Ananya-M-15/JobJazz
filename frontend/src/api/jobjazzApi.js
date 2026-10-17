const rawApiUrl = (import.meta.env.VITE_API_BASE_URL || import.meta.env.VITE_API_URL || "http://127.0.0.1:8000").trim();
const API_BASE_URL = rawApiUrl.replace(/\/+$/, "");

/**
 * Upload a resume PDF and extract its profile.
 */
export async function extractResume(file) {
    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch(`${API_BASE_URL}/resume/extract`, {
        method: "POST",
        body: formData,
    });

    if (!response.ok) {
        let message = "Failed to extract resume.";

        try {
            const errorData = await response.json();
            message = errorData.detail || message;
        } catch {
            // Keep the default message.
        }

        throw new Error(message);
    }

    return response.json();
}


/**
 * Analyze a job description.
 */
export async function analyzeJobDescription(text) {
    const response = await fetch(`${API_BASE_URL}/job-description/analyze`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ text }),
    });

    if (!response.ok) {
        let message = "Failed to analyze job description.";

        try {
            const errorData = await response.json();
            message = errorData.detail || message;
        } catch {
            // Keep the default message.
        }

        throw new Error(message);
    }

    return response.json();
}


/**
 * Analyze a job description from a PDF file.
 */
export async function analyzeJobDescriptionPdf(file) {
    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch(`${API_BASE_URL}/job-description/analyze-pdf`, {
        method: "POST",
        body: formData,
    });

    if (!response.ok) {
        let message = "Failed to analyze job description PDF.";

        try {
            const errorData = await response.json();
            message = errorData.detail || message;
        } catch {
            // Keep the default message.
        }

        throw new Error(message);
    }

    return response.json();
}


/**
 * Match a resume profile against a job profile.
 */
export async function analyzeMatching(data) {
    const response = await fetch(`${API_BASE_URL}/matching/analyze`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
    });

    if (!response.ok) {
        let message = "Failed to analyze resume-job match.";

        try {
            const errorData = await response.json();
            message = errorData.detail || message;
        } catch {
            // Keep the default message.
        }

        throw new Error(message);
    }

    return response.json();
}


/**
 * Analyze skill gaps from a matching result.
 */
export async function analyzeSkillGap(data) {
    const response = await fetch(`${API_BASE_URL}/skill-gap/analyze`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
    });

    if (!response.ok) {
        let message = "Failed to analyze skill gaps.";

        try {
            const errorData = await response.json();
            message = errorData.detail || message;
        } catch {
            // Keep the default message.
        }

        throw new Error(message);
    }

    return response.json();
}


/**
 * Normalizes recommendation responses to a single canonical contract:
 * { source: string, recommendations: Array, overall_advice: string }
 */
export function normalizeRecommendationsResponse(raw) {
    if (!raw) return { source: "deterministic", recommendations: [], overall_advice: "" };

    let recList = [];
    let advice = raw.overall_advice || "";
    const source = raw.source || "deterministic";

    if (Array.isArray(raw.recommendations)) {
        recList = raw.recommendations;
    } else if (raw.recommendations && Array.isArray(raw.recommendations.recommendations)) {
        recList = raw.recommendations.recommendations;
        advice = advice || raw.recommendations.overall_advice || "";
    }

    return {
        source,
        recommendations: recList,
        overall_advice: advice,
    };
}


/**
 * Generate AI/fallback recommendations.
 */
export async function generateRecommendations(data) {
    const response = await fetch(`${API_BASE_URL}/recommendations/generate`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
    });

    if (!response.ok) {
        let message = "Failed to generate recommendations.";

        try {
            const errorData = await response.json();
            message = errorData.detail || message;
        } catch {
            // Keep the default message.
        }

        throw new Error(message);
    }

    const json = await response.json();
    return normalizeRecommendationsResponse(json);
}


/**
 * Generate or regenerate a learning roadmap for an analysis.
 */
export async function generateRoadmap(data) {
    const response = await fetch(`${API_BASE_URL}/roadmap/generate`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
    });

    if (!response.ok) {
        let message = "Failed to generate learning roadmap.";

        try {
            const errorData = await response.json();
            message = errorData.detail || message;
        } catch {
            // Keep default message
        }

        throw new Error(message);
    }

    return response.json();
}


/**
 * Retrieve an existing learning roadmap by analysis ID.
 */
export async function getRoadmap(analysisId) {
    const response = await fetch(`${API_BASE_URL}/roadmap/${analysisId}`);

    if (!response.ok) {
        let message = "Failed to fetch roadmap.";

        try {
            const errorData = await response.json();
            message = errorData.detail || message;
        } catch {
            // Keep default message
        }

        throw new Error(message);
    }

    return response.json();
}


/**
 * Update completion status and/or user notes for a roadmap step.
 */
export async function updateRoadmapStep(analysisId, stepId, completed, userNotes = null) {
    const payload = {};
    if (completed !== undefined && completed !== null) {
        payload.status = completed ? "completed" : "not_started";
    }
    if (userNotes !== null) {
        payload.user_notes = userNotes;
    }

    const response = await fetch(`${API_BASE_URL}/roadmap/${analysisId}/step/${stepId}`, {
        method: "PATCH",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
    });

    if (!response.ok) {
        let message = "Failed to update roadmap step.";

        try {
            const errorData = await response.json();
            message = errorData.detail || message;
        } catch {
            // Keep default message
        }

        throw new Error(message);
    }

    return response.json();
}


/**
 * Retrieve roadmap progress metrics by analysis ID.
 */
export async function getRoadmapProgress(analysisId) {
    const response = await fetch(`${API_BASE_URL}/roadmap/${analysisId}/progress`);

    if (!response.ok) {
        let message = "Failed to fetch roadmap progress.";

        try {
            const errorData = await response.json();
            message = errorData.detail || message;
        } catch {
            // Keep default message
        }

        throw new Error(message);
    }

    return response.json();
}


/**
 * Retrieve a persisted analysis session by ID to restore dashboard state.
 */
export async function getAnalysis(analysisId) {
    const response = await fetch(`${API_BASE_URL}/matching/analysis/${analysisId}`);

    if (!response.ok) {
        let message = "Failed to fetch analysis session.";

        try {
            const errorData = await response.json();
            message = errorData.detail || message;
        } catch {
            // Keep default message
        }

        throw new Error(message);
    }

    const data = await response.json();
    if (data.recommendations) {
        data.recommendations = normalizeRecommendationsResponse(data.recommendations);
    }
    return data;
}

/**
 * Download the personalized roadmap as a PDF document.
 */
export async function downloadRoadmapPdf(analysisId) {
    const response = await fetch(`${API_BASE_URL}/roadmap/${analysisId}/pdf`);

    if (!response.ok) {
        let message = "Failed to download roadmap PDF.";

        try {
            const errorData = await response.json();
            message = errorData.detail || message;
        } catch {
            // Keep default message
        }

        throw new Error(message);
    }

    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;

    const disposition = response.headers.get("Content-Disposition");
    let filename = `JobJazz_Roadmap_${analysisId.slice(0, 8)}.pdf`;
    if (disposition && disposition.includes("filename=")) {
        const match = disposition.match(/filename="?([^"]+)"?/);
        if (match && match[1]) {
            filename = match[1];
        }
    }

    a.download = filename;
    document.body.appendChild(a);
    a.click();
    a.remove();
    window.URL.revokeObjectURL(url);
}
