
from fastapi import APIRouter, FastAPI

from app.core.config import settings


app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
)

api_router = APIRouter(prefix=settings.API_V1_PREFIX)


@api_router.get("/health", tags=["Health"])
async def health_check():
    return {
        "status": "healthy",
        "application": "JonoSeba",
        "version": settings.APP_VERSION,
        "message": "JonoSeba API is running successfully.",
    }


app.include_router(api_router)
