from fastapi import APIRouter, FastAPI

app = FastAPI(
    title="JonoSeba API",
    description=(
        "AI-Powered Smart Citizen Services "
        "and Complaint Management Platform."
    ),
    version="0.1.0",
)

api_router = APIRouter(prefix="/api/v1")

@api_router.get("/health", tags=["Health"])
async def health_check():
    """Check whether the JonoSeba API is running."""
    return {
        "status": "healthy",
        "application": "JonoSeba",
        "version": "0.1.0",
        "message": "JonoSeba API is running successfully.",
    }

app.include_router(api_router)
