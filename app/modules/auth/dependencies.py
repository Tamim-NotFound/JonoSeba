from typing import Annotated
from fastapi import Depends
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import UnauthorizedError
from app.core.security import decode_access_token
from app.db.session import get_db
from app.modules.auth.models import User
from app.modules.auth.repositories import UserRepository
from app.modules.auth.services import AuthService


bearer_scheme = HTTPBearer(auto_error=False)


def get_auth_service(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> AuthService:
    """Provide AuthService through dependency injection."""
    return AuthService(db)


async def get_current_user(
    credentials: Annotated[
        HTTPAuthorizationCredentials | None,
        Depends(bearer_scheme),
    ],
    db: Annotated[
        AsyncSession,
        Depends(get_db),
    ],
) -> User:
    """Validate JWT and return the active database user."""

    if credentials is None:
        raise UnauthorizedError(
            "Authentication required."
        )

    try:
        user_id = decode_access_token(
            credentials.credentials
        )
    except ValueError as exc:
        raise UnauthorizedError(
            "Invalid or expired access token."
        ) from exc

    repository = UserRepository(db)

    user = await repository.get_by_id(user_id)

    if user is None or not user.is_active:
        raise UnauthorizedError(
            "Invalid or expired access token."
        )

    return user


CurrentUserDep = Annotated[
    User,
    Depends(get_current_user),
]
