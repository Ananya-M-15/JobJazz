"""
End-to-End Verification Script for JobJazz Phase 13.
Tests 3 distinct JDs + 1 sparse JD against a single resume profile.
"""
from fastapi.testclient import TestClient
from app.main import app
from app.database.database import SessionLocal
from app.database.models import User, Resume

def main():
    client = TestClient(app)

    # 1. Health
    res = client.get("/api/health")
    assert res.status_code == 200, res.text
    print("Health check status:", res.json()["status"])

    # 2. Database setup
    db = SessionLocal()
    user = db.query(User).filter(User.email == "test_e2e@jobjazz.local").first()
    if not user:
        user = User(email="test_e2e@jobjazz.local", name="Alex Mercer")
        db.add(user)
        db.flush()

    resume_profile = {
        "name": "Alex Mercer",
        "skills": ["Python", "FastAPI", "PostgreSQL", "Docker", "Git"],
        "experience": [
            {
                "company": "TechCorp",
                "role": "Backend Engineer",
                "start_date": "Jan 2022",
                "end_date": "Jan 2024",
                "description": "Built FastAPI microservices and maintained PostgreSQL databases."
            }
        ],
        "education": [
            {
                "institution": "State University",
                "degree": "Bachelor",
                "field_of_study": "Computer Science",
                "start_date": "2018",
                "end_date": "2022"
            }
        ]
    }

    resume = Resume(
        user_id=user.id,
        filename="alex_resume.pdf",
        raw_text="Alex Mercer Python Developer Resume",
        profile_data=resume_profile
    )
    db.add(resume)
    db.commit()
    db.refresh(resume)
    resume_id = str(resume.id)

    # 3. Test Cases: 3 materially different JDs + 1 sparse JD
    test_cases = [
        (
            "Case A (Strong Overlap - Python Backend)",
            """
            Python Backend Engineer
            Requirements:
            - Python
            - FastAPI
            - PostgreSQL
            - Docker

            Preferred:
            - AWS
            - Git

            Experience:
            2+ years of experience

            Education:
            Bachelor degree in Computer Science
            """
        ),
        (
            "Case B (Partial Overlap - Full Stack Engineer)",
            """
            Full Stack Engineer
            Requirements:
            - Python
            - React
            - TypeScript
            - PostgreSQL

            Preferred:
            - Docker
            - Kubernetes

            Experience:
            3+ years of experience

            Education:
            Bachelor degree in Computer Science
            """
        ),
        (
            "Case C (Weak Overlap - ML Scientist)",
            """
            Machine Learning Scientist
            Requirements:
            - Machine Learning
            - TensorFlow
            - PyTorch
            - Pandas

            Preferred:
            - Python
            - AWS

            Experience:
            4+ years of experience

            Education:
            Master degree in Artificial Intelligence
            """
        ),
        (
            "Case D (Sparse Valid JD)",
            """
            Software Developer
            We are looking for a software developer with Python and SQL knowledge.
            Responsibilities include writing clean code and testing.
            """
        )
    ]

    results_summary = []

    for label, jd_text in test_cases:
        # Step 1: Analyze JD
        jd_res = client.post("/job-description/analyze", json={"text": jd_text})
        assert jd_res.status_code == 200, f"JD analyze failed: {jd_res.text}"
        jd_data = jd_res.json()
        jd_id = jd_data["job_description_id"]
        jd_profile = jd_data["profile"]

        # Step 2: Match
        match_res = client.post("/matching/analyze", json={
            "resume_id": resume_id,
            "job_description_id": jd_id,
            "resume": resume_profile,
            "job": jd_profile
        })
        assert match_res.status_code == 200, f"Matching failed: {match_res.text}"
        match_data = match_res.json()
        analysis_id = match_data["analysis_id"]
        mr = match_data["match_result"]

        # Step 3: Skill Gap
        gap_res = client.post("/skill-gap/analyze", json={
            "analysis_id": analysis_id,
            "match_result": mr
        })
        assert gap_res.status_code == 200, f"Skill gap failed: {gap_res.text}"
        gap_data = gap_res.json()["skill_gap"]

        # Step 4: Recommendations
        rec_res = client.post("/recommendations/generate", json={
            "analysis_id": analysis_id,
            "match_result": mr,
            "skill_gap": gap_data
        })
        assert rec_res.status_code == 200, f"Recommendations failed: {rec_res.text}"
        rec_data = rec_res.json()

        results_summary.append({
            "label": label,
            "score": mr["overall_score"],
            "score_breakdown": mr.get("score_breakdown"),
            "matched_required": mr["matched_required_skills"],
            "missing_required": mr["missing_required_skills"],
            "matched_preferred": mr["matched_preferred_skills"],
            "missing_preferred": mr["missing_preferred_skills"],
            "experience_status": mr["experience_status"],
            "experience_notes": mr["experience_notes"],
            "education_status": mr["education_status"],
            "education_notes": mr["education_notes"],
            "rec_count": len(rec_data["recommendations"]["recommendations"]),
            "rec_source": rec_data["source"]
        })

    print("\n" + "=" * 60)
    print("END-TO-END PIPELINE VERIFICATION RESULTS")
    print("=" * 60)
    for res in results_summary:
        print(f"\n--- {res['label']} ---")
        print(f"Overall Match Score: {res['score']}%")
        print(f"Score Breakdown: {res['score_breakdown']}")
        print(f"Matched Required: {res['matched_required']}")
        print(f"Missing Required: {res['missing_required']}")
        print(f"Matched Preferred: {res['matched_preferred']}")
        print(f"Missing Preferred: {res['missing_preferred']}")
        print(f"Experience: {res['experience_status']} -> {res['experience_notes']}")
        print(f"Education: {res['education_status']} -> {res['education_notes']}")
        print(f"Recommendations ({res['rec_source']}): {res['rec_count']} items")

    # Assertions
    scores = [r["score"] for r in results_summary]
    # JD A > JD B > JD C
    assert scores[0] > scores[1] > scores[2], f"Scores are not ordered properly: {scores}"
    print("\nAll verification assertions PASSED successfully!")

if __name__ == "__main__":
    main()
