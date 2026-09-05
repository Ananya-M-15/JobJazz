import re


SKILL_ALIASES = {
    "python": "Python",
    "java": "Java",
    "c++": "C++",
    "javascript": "JavaScript",
    "typescript": "TypeScript",
    "sql": "SQL",
    "html": "HTML",
    "css": "CSS",
    "react": "React",
    "reactjs": "React",
    "node.js": "Node.js",
    "nodejs": "Node.js",
    "django": "Django",
    "flask": "Flask",
    "fastapi": "FastAPI",
    "mongodb": "MongoDB",
    "mysql": "MySQL",
    "postgresql": "PostgreSQL",
    "git": "Git",
    "github": "GitHub",
    "docker": "Docker",
    "kubernetes": "Kubernetes",
    "machine learning": "Machine Learning",
    "deep learning": "Deep Learning",
    "artificial intelligence": "Artificial Intelligence",
    "generative ai": "Generative AI",
    "nlp": "NLP",
    "natural language processing": "Natural Language Processing",
    "computer vision": "Computer Vision",
    "pandas": "Pandas",
    "numpy": "NumPy",
    "scikit-learn": "Scikit-learn",
    "tensorflow": "TensorFlow",
    "pytorch": "PyTorch",
    "tableau": "Tableau",
    "power bi": "Power BI",
    "excel": "Excel",
    "rest api": "REST APIs",
    "api integration": "API Integration",
}


def extract_skills(text: str) -> list[str]:
    text_lower = text.lower()
    found_skills = []

    for skill, display_name in SKILL_ALIASES.items():
        pattern = r"(?<![a-z0-9])" + re.escape(skill) + r"(?![a-z0-9])"

        if re.search(pattern, text_lower):
            if display_name not in found_skills:
                found_skills.append(display_name)

    return found_skills