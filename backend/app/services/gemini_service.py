import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from app.models.match_result import MatchResult
from app.models.skill_gap import SkillGapResult
from app.models.recommendation import RecommendationResult


load_dotenv()


def get_gemini_client():
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is not configured."
        )

    return genai.Client(api_key=api_key)


def build_recommendation_prompt(
    match_result: MatchResult,
    skill_gap: SkillGapResult,
) -> str:

    return f"""
You are JobJazz, a career analysis assistant.

Your task is to provide practical, objective career recommendations
based ONLY on the structured information provided below.

Do not change or reinterpret the match score.

Do not invent skills, experience, education, certifications,
projects, or achievements that are not provided.

Prioritize:
1. Missing required skills
2. Experience gaps
3. Missing preferred skills
4. Education gaps

Keep recommendations realistic and actionable.

MATCH RESULT:
Overall score: {match_result.overall_score}

Matched required skills:
{match_result.matched_required_skills}

Missing required skills:
{match_result.missing_required_skills}

Matched preferred skills:
{match_result.matched_preferred_skills}

Missing preferred skills:
{match_result.missing_preferred_skills}

Experience match:
{match_result.experience_match}

Education match:
{match_result.education_match}

SKILL GAP RESULT:

Strengths:
{skill_gap.strengths}

Critical gaps:
{skill_gap.critical_gaps}

Preferred gaps:
{skill_gap.preferred_gaps}

Experience gap:
{skill_gap.experience_gap}

Education gap:
{skill_gap.education_gap}

Generate recommendations ONLY for the gaps explicitly identified
in the SKILL GAP RESULT above.

Allowed recommendation areas are:

1. Critical gaps:
{skill_gap.critical_gaps}

2. Preferred gaps:
{skill_gap.preferred_gaps}

3. Experience:
Include this only if experience_gap is true.

4. Education:
Include this only if education_gap is true.

Do NOT create additional skills, gaps, categories, or recommendation
areas that are not explicitly present above.

Do NOT create duplicate recommendations for the same area.

For every recommendation provide:
- skill: the exact skill or area being addressed
- priority: High, Medium, or Low
- reason: why this matters for the target role
- action: a concrete next step the candidate can take

Priority rules:
- Critical gaps → High
- Experience gap → High
- Preferred gaps → Medium
- Education gap → Medium

Also provide concise overall advice.

Return ONLY valid JSON matching the RecommendationResult schema.
"""


def generate_ai_recommendations(
    match_result: MatchResult,
    skill_gap: SkillGapResult,
) -> RecommendationResult:

    client = get_gemini_client()

    prompt = build_recommendation_prompt(
        match_result,
        skill_gap,
    )

    response = client.models.generate_content(
    model="gemini-3.1-flash-lite",
    contents=prompt,
    config=types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=RecommendationResult,
    ),
)

    return RecommendationResult.model_validate_json(
        response.text
    )