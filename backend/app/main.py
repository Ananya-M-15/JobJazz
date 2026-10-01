from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.health import router as health_router
from app.api.routes.resume import router as resume_router
from app.api.routes.job_description import router as job_description_router
from app.api.routes.matching import router as matching_router
from app.api.routes.skill_gap import router as skill_gap_router
from app.api.routes.recommendations import router as recommendations_router


app = FastAPI(
    title="JobJazz API",
    description="Backend API for JobJazz - Your career, in tune.",
    version="0.1.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
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


app.include_router(health_router)
app.include_router(resume_router)
app.include_router(job_description_router)
app.include_router(matching_router)
app.include_router(skill_gap_router)
app.include_router(recommendations_router)