from typing import Annotated
from fastapi import Depends
from app.core.exceptions import ForbiddenError
from app.modules.auth.dependencies import get_current_user
from app.modules.auth.models import User, UserRole

async def require_admin(
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
) -> User:
    """Allow access only to active admin users."""

    if current_user.role != UserRole.ADMIN:
        raise ForbiddenError(
            "Admin access is required."
        )

    return current_user


AdminUserDep = Annotated[
    User,
    Depends(require_admin),
]
