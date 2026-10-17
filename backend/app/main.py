import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.health import router as health_router
from app.api.routes.resume import router as resume_router
from app.api.routes.job_description import router as job_description_router
from app.api.routes.matching import router as matching_router
from app.api.routes.skill_gap import router as skill_gap_router
from app.api.routes.recommendations import router as recommendations_router
from app.api.routes.roadmap import router as roadmap_router


app = FastAPI(
    title="JobJazz API",
    description="Backend API for JobJazz - Your career, in tune.",
    version="0.1.0",
)


# Configurable CORS origins for production and local development
cors_env = os.getenv("CORS_ORIGINS", "").strip()
if cors_env:
    allowed_origins = [origin.strip() for origin in cors_env.split(",") if origin.strip()]
else:
    allowed_origins = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:4173",
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "message": "Welcome to JobJazz API",
        "status": "running",
        "version": "0.1.0",
    }


@app.get("/health")
def root_health():
    """Root health endpoint for cloud load balancers and deployment probes."""
    return {
        "status": "healthy"
    }


app.include_router(health_router)
app.include_router(resume_router)
app.include_router(job_description_router)
app.include_router(matching_router)
app.include_router(skill_gap_router)
app.include_router(recommendations_router)
app.include_router(roadmap_router)
