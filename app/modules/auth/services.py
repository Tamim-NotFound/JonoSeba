from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import ConflictError, UnauthorizedError
from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.modules.auth.models import User
from app.modules.auth.repositories import UserRepository
from app.modules.auth.schemas import (
    TokenResponse,
    UserLogin,
    UserRegister,
)

class UserAlreadyExistsError(ConflictError):
    """Raised when an email is already registered."""


class InvalidCredentialsError(UnauthorizedError):
    """Raised when login credentials are invalid."""


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repository = UserRepository(db)

    async def register(
        self,
        data: UserRegister,
    ) -> User:
        """Register a new citizen account."""

        existing_user = await self.repository.get_by_email(
            data.email
        )

        if existing_user is not None:
            raise UserAlreadyExistsError(
                "An account with this email already exists."
            )

        hashed_password = hash_password(data.password)

        try:
            user = await self.repository.create(
                full_name=data.full_name,
                email=data.email,
                hashed_password=hashed_password,
            )

            await self.db.commit()
            return user

        except IntegrityError as exc:
            await self.db.rollback()

            raise UserAlreadyExistsError(
                "An account with this email already exists."
            ) from exc

        except Exception:
            await self.db.rollback()
            raise

    async def login(
        self,
        data: UserLogin,
    ) -> TokenResponse:
        """Authenticate a user and return a JWT token."""

        # Use the same message for all invalid credentials.
        invalid_credentials_message = (
            "Invalid email or password."
        )

        user = await self.repository.get_by_email(
            data.email
        )

        # Avoid revealing whether an email is registered.
        if user is None:
            raise InvalidCredentialsError(
                invalid_credentials_message
            )

        # Verify the submitted password against its Argon2 hash.
        if not verify_password(
            data.password,
            user.hashed_password,
        ):
            raise InvalidCredentialsError(
                invalid_credentials_message
            )

        # Inactive accounts cannot log in.
        if not user.is_active:
            raise InvalidCredentialsError(
                invalid_credentials_message
            )

        access_token = create_access_token(
            user_id=user.id
        )

        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
        )
