from fastapi import FastAPI
from app.api.routes.health import router as health_router
from app.api.routes.resume import router as resume_router

app = FastAPI(
    title="JobJazz API",
    description="Backend API for JobJazz - Your career, in tune.",
    version="0.1.0",
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