from fastapi.testclient import TestClient

from app.main import app
from app.database.database import SessionLocal
from app.database.models import User, JobDescription


client = TestClient(app)


def test_job_description_is_saved_to_database():
    job_description_text = """
    Machine Learning Engineer

    We are looking for a Machine Learning Engineer with 2+ years
    of experience.

    Required Skills:
    Python, SQL, Machine Learning, Pandas, NumPy

    Preferred Skills:
    Docker, Git, AWS

    Education:
    Bachelor's degree in Computer Science or Engineering.
    """

    response = client.post(
        "/job-description/analyze",
        json={"text": job_description_text},
    )

    assert response.status_code == 200

    response_data = response.json()

    assert response_data["profile"]["job_title"] == "Machine Learning Engineer"

    db = SessionLocal()

    saved_job = None

    try:
        user = (
            db.query(User)
            .filter(User.email == "development@jobjazz.local")
            .first()
        )

        assert user is not None

        saved_job = (
            db.query(JobDescription)
            .filter(
                JobDescription.user_id == user.id,
                JobDescription.raw_text == job_description_text,
            )
            .first()
        )

        assert saved_job is not None
        assert saved_job.job_title == "Machine Learning Engineer"
        assert saved_job.raw_text == job_description_text
        assert saved_job.profile_data["job_title"] == "Machine Learning Engineer"

    finally:
        if saved_job is not None:
            db.delete(saved_job)
            db.commit()

        db.close()