from typing import Annotated
from fastapi import APIRouter, Depends, status
from app.modules.auth.dependencies import (
    CurrentUserDep,
    get_auth_service,
)
from app.modules.auth.schemas import (
    TokenResponse,
    UserLogin,
    UserRegister,
    UserResponse,
)
from app.modules.auth.services import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

AuthServiceDep = Annotated[
    AuthService,
    Depends(get_auth_service),
]


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register_user(
    data: UserRegister,
    service: AuthServiceDep,
):
    return await service.register(data)


@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
)
async def login_user(
    data: UserLogin,
    service: AuthServiceDep,
):
    return await service.login(data)


@router.get(
    "/me",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
async def get_my_profile(
    current_user: CurrentUserDep,
):
    return current_user
