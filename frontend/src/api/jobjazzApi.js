const API_BASE_URL = "http://127.0.0.1:8000";

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

    return response.json();
}