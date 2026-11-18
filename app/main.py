from fastapi import APIRouter, FastAPI
from app.core.config import settings
from app.core.exception_handlers import register_exception_handlers
from app.modules.departments.controllers import (
    router as departments_router,
)

# Step 1: Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
)

# Step 2: Register global exception handlers
register_exception_handlers(app)

api_router = APIRouter(prefix=settings.API_V1_PREFIX)

@api_router.get("/health", tags=["Health"])
async def health_check():
    return {
        "status": "healthy",
        "application": "JonoSeba",
        "version": settings.APP_VERSION,
        "message": "JonoSeba API is running successfully.",
    }

# Step 4: Register department routes
api_router.include_router(departments_router)

# Step 5: Register API router with FastAPI
app.include_router(api_router)