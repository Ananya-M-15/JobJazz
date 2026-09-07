from app.models.match_result import MatchResult
from app.models.skill_gap import SkillGapResult
from app.models.recommendation import (
    RecommendationResult,
    SkillRecommendation,
)


SKILL_ACTIONS = {
    "AWS": "Learn core AWS services and deploy a small machine learning project.",
    "Docker": "Practice containerizing an application and deploying it with Docker.",
    "Kubernetes": "Learn Kubernetes fundamentals and deploy a containerized application.",
    "TensorFlow": "Build a small neural-network project using TensorFlow.",
    "PyTorch": "Build a deep-learning project using PyTorch.",
    "Machine Learning": "Build an end-to-end machine learning project with data preprocessing, training, and evaluation.",
    "Scikit-learn": "Build a machine learning project using Scikit-learn pipelines and model evaluation.",
    "Pandas": "Practice data cleaning, transformation, and analysis using Pandas.",
    "NumPy": "Practice numerical operations and array-based data processing with NumPy.",
    "SQL": "Practice joins, subqueries, aggregations, and analytical SQL queries.",
    "Python": "Strengthen Python through practical automation, data, or backend projects.",
    "Git": "Practice branching, pull requests, merging, and collaborative Git workflows.",
    "GitHub": "Build and maintain projects on GitHub with clear documentation and version history.",
    "FastAPI": "Build a REST API with FastAPI and connect it to a database.",
    "REST APIs": "Build and consume REST APIs and practice authentication and error handling.",
    "React": "Build an interactive frontend project using React components and API integration.",
    "MongoDB": "Practice designing collections and performing CRUD operations with MongoDB.",
    "MySQL": "Practice relational database design, joins, indexing, and SQL queries.",
    "Tableau": "Create an interactive dashboard using a real-world dataset.",
    "Power BI": "Build a business analytics dashboard using Power BI.",
    "Excel": "Practice pivot tables, lookup functions, charts, and data analysis in Excel.",
    "MLOps": "Build an ML pipeline covering training, experiment tracking, deployment, and monitoring.",
}


def get_action(skill: str) -> str:
    return SKILL_ACTIONS.get(
        skill,
        f"Learn {skill} through a practical project related to the target role.",
    )


def generate_skill_recommendations(
    skill_gap: SkillGapResult,
) -> list[SkillRecommendation]:

    recommendations = []

    for skill in skill_gap.critical_gaps:
        recommendations.append(
            SkillRecommendation(
                skill=skill,
                priority="High",
                reason=f"{skill} is a missing required skill for the target role.",
                action=get_action(skill),
            )
        )

    for skill in skill_gap.preferred_gaps:
        recommendations.append(
            SkillRecommendation(
                skill=skill,
                priority="Medium",
                reason=f"{skill} is a preferred skill that could strengthen your application.",
                action=get_action(skill),
            )
        )

    if skill_gap.experience_gap:
        recommendations.append(
            SkillRecommendation(
                skill="Experience",
                priority="High",
                reason="Your current experience does not fully meet the job requirement.",
                action="Build relevant projects, internships, freelance work, or other practical experience related to the target role.",
            )
        )

    if skill_gap.education_gap:
        recommendations.append(
            SkillRecommendation(
                skill="Education",
                priority="Medium",
                reason="Your current education does not clearly match the stated requirement.",
                action="Review the education requirement and consider relevant coursework, certifications, or further education where appropriate.",
            )
        )

    return recommendations


def generate_recommendations(
    match_result: MatchResult,
    skill_gap: SkillGapResult,
) -> RecommendationResult:

    recommendations = generate_skill_recommendations(
        skill_gap
    )

    if match_result.overall_score >= 80:
        overall_advice = (
            "Your profile is a strong match. "
            "Focus on closing the remaining gaps and tailoring your resume "
            "to the target role."
        )
    elif match_result.overall_score >= 60:
        overall_advice = (
            "Your profile has a reasonable foundation for this role. "
            "Prioritize required skill gaps before preferred skills."
        )
    else:
        overall_advice = (
            "There are significant gaps between your profile and this role. "
            "Focus on the highest-priority missing skills and relevant experience."
        )

    return RecommendationResult(
        recommendations=recommendations,
        overall_advice=overall_advice,
    )