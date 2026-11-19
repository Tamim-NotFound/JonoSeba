from fastapi import APIRouter, FastAPI
from app.core.config import settings
from app.core.exception_handlers import register_exception_handlers
from app.modules.auth.controllers import router as auth_router
from app.modules.complaints.controllers import router as complaints_router
from app.modules.departments.controllers import router as departments_router
from app.modules.chat.controllers import router as chat_router


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=settings.APP_DESCRIPTION,
    debug=settings.DEBUG,
)

register_exception_handlers(app)

api_router = APIRouter(
    prefix=settings.API_V1_PREFIX,
)


@api_router.get(
    "/health",
    tags=["Health"],
)
async def health_check():
    return {
        "status": "ok",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
    }


api_router.include_router(departments_router)
api_router.include_router(auth_router)
api_router.include_router(complaints_router)
api_router.include_router(chat_router)

app.include_router(api_router)
