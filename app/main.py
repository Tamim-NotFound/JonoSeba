from fastapi import APIRouter, FastAPI
from app.core.config import settings
from app.core.exception_handlers import register_exception_handlers
from app.modules.auth.controllers import (
    router as auth_router,
)
from app.modules.departments.controllers import (
    router as departments_router,
)


app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
)


# Register centralized exception handlers.
register_exception_handlers(app)


# All API endpoints use /api/v1.
api_router = APIRouter(
    prefix=settings.API_V1_PREFIX,
)


@api_router.get("/health", tags=["Health"])
async def health_check():
    return {
        "status": "healthy",
        "application": "JonoSeba",
        "version": settings.APP_VERSION,
        "message": "JonoSeba API is running successfully.",
    }

# Register feature routers.
api_router.include_router(departments_router)
api_router.include_router(auth_router)

# Attach versioned routes to the application.
app.include_router(api_router)