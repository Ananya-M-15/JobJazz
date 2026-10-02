from fastapi.testclient import TestClient
from app.main import app
import app.api.routes.job_description as jd_route

client = TestClient(app)

def test_job_description_validation_length():
    # Text under 100 characters should fail
    short_text = "Software Engineer with Python skills."
    response = client.post("/job-description/analyze", json={"text": short_text})
    
    assert response.status_code == 422
    assert "We couldn't read enough text" in response.json()["detail"]

def test_job_description_validation_content(monkeypatch):
    # Text is over 100 characters but has no meaningful skills, title, experience, or education
    long_text = "This is a random document that happens to be long enough but has absolutely nothing to do with a job description. " * 10
    
    class FakeEmptyJobProfile:
        def model_dump(self):
            return {
                "job_title": "Untitled Job Description",
                "required_skills": [],
                "preferred_skills": [],
                "experience_level": "",
                "education": "",
            }
        
        @property
        def job_title(self):
            return "Untitled Job Description"
            
        @property
        def required_skills(self):
            return []
            
        @property
        def preferred_skills(self):
            return []
            
        @property
        def experience_requirement(self):
            return ""
            
        @property
        def education_requirements(self):
            return []

    def fake_parse_job_description(text):
        return FakeEmptyJobProfile()

    monkeypatch.setattr(jd_route, "parse_job_description", fake_parse_job_description)

    response = client.post("/job-description/analyze", json={"text": long_text})
    
    assert response.status_code == 422
    assert "doesn't look like a job description" in response.json()["detail"]
