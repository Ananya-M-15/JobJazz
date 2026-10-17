import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database.database import DATABASE_URL
from app.schemas.roadmap import StepUpdateRequest, StepStatus


client = TestClient(app)


def test_root_health_endpoint():
    """Verify that root /health endpoint returns status healthy for cloud load balancers."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_api_health_endpoint():
    """Verify that /api/health continues to return healthy status."""
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_cors_origins_configuration(monkeypatch):
    """Verify that CORS origins can be configured via environment variable."""
    import os
    from app.main import allowed_origins

    # By default, dev origins are included
    assert "http://localhost:5173" in allowed_origins
    assert "http://127.0.0.1:5173" in allowed_origins


def test_database_url_postgres_scheme_normalization():
    """Verify that production normalize_database_url converts schemes and preserves query parameters."""
    from app.database.database import normalize_database_url

    # 1. Test postgres:// conversion with Neon SSL query parameter preservation
    raw_neon = "postgres://usr:pwd@ep-cool-forest-12345.us-east-2.aws.neon.tech/neondb?sslmode=require"
    normalized_neon = normalize_database_url(raw_neon)
    assert normalized_neon.startswith("postgresql://")
    assert not normalized_neon.startswith("postgres://")
    assert "?sslmode=require" in normalized_neon
    assert "ep-cool-forest-12345" in normalized_neon

    # 2. Test legacy postgresql+psycopg2:// conversion to standard postgresql://
    legacy_url = "postgresql+psycopg2://usr:pwd@host.cloud.com:5432/mydb"
    normalized_legacy = normalize_database_url(legacy_url)
    assert normalized_legacy.startswith("postgresql://")
    assert "+psycopg2" not in normalized_legacy

    # 3. Test standard postgresql:// URL remains unchanged
    standard_url = "postgresql://usr:pwd@host.cloud.com:5432/mydb"
    assert normalize_database_url(standard_url) == standard_url

    # 4. Test fallback to default when url is None or empty string
    assert normalize_database_url(None) == "postgresql://postgres:postgres@localhost:5432/jobjazz"
    assert normalize_database_url("") == "postgresql://postgres:postgres@localhost:5432/jobjazz"


def test_postgresql_driver_dialect_resolution():
    """Verify SQLAlchemy resolves postgresql:// to the psycopg (v3) driver cleanly."""
    from sqlalchemy.engine.url import make_url
    url = make_url("postgresql://user:password@localhost:5432/testdb")
    dialect_cls = url.get_dialect()
    assert dialect_cls.name == "postgresql"
    assert dialect_cls.driver == "psycopg"


def test_step_update_schema_accepts_user_notes():
    """Verify StepUpdateRequest schema validates user_notes correctly."""
    step_up = StepUpdateRequest(status=StepStatus.COMPLETED, user_notes="Completed module with GitHub repo link")
    assert step_up.status == StepStatus.COMPLETED
    assert step_up.user_notes == "Completed module with GitHub repo link"

    # Notes can also be updated without changing status
    step_notes_only = StepUpdateRequest(status=StepStatus.NOT_STARTED, user_notes="Started reading docs")
    assert step_notes_only.user_notes == "Started reading docs"


def test_roadmap_pdf_export_not_found():
    """Verify that requesting PDF for non-existent roadmap returns 404."""
    fake_id = "00000000-0000-0000-0000-000000000000"
    response = client.get(f"/roadmap/{fake_id}/pdf")
    assert response.status_code == 404
    assert "Roadmap not found" in response.json()["detail"]


def test_roadmap_pdf_generation_service():
    """Verify generate_roadmap_pdf produces valid multi-page PDF without candidate PII."""
    from app.services.roadmap_pdf_service import generate_roadmap_pdf

    sample_roadmap = {
        "summary": {
            "target_role": "Staff Platform Engineer",
            "progress_percentage": 50.0,
            "completed_steps": 2,
            "total_steps": 4,
            "total_hours": 24.0,
            "estimated_weeks": 3,
            "overall_strategy": "Master Kubernetes operators and Terraform state locking.",
        },
        "schedule": {
            "hours_per_week": 8,
            "is_feasible": True,
            "projected_completion_date": "2026-11-15",
            "weekly_schedule": [
                {
                    "week_number": 1,
                    "allocated_hours": 8.0,
                    "start_date": "2026-10-20",
                    "end_date": "2026-10-27",
                    "milestone": "Operator SDK setup",
                }
            ],
        },
        "modules": [
            {
                "title": "Kubernetes Custom Controllers",
                "priority": "High",
                "skills": ["Kubernetes", "Go"],
                "steps": [
                    {
                        "title": "Build a Custom Resource Definition (CRD)",
                        "status": "completed",
                        "stage": "Build",
                        "estimated_hours": 6.0,
                        "measurable_outcome": "Deploy CRD to local Kind cluster",
                        "resources": [
                            {
                                "provider": "Kubernetes Docs",
                                "title": "Custom Resources",
                                "url": "https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/",
                            }
                        ],
                    }
                ],
            }
        ],
    }

    pdf_bytes = generate_roadmap_pdf(sample_roadmap)
    assert isinstance(pdf_bytes, bytes)
    assert len(pdf_bytes) > 1000
    assert pdf_bytes.startswith(b"%PDF-")

    # Security check: ensure no candidate PII or secrets leaked
    assert b"candidate@secret.com" not in pdf_bytes
    assert b"AIzaSy" not in pdf_bytes
