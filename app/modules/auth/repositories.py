from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.auth.models import User, UserRole

class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(
        self,
        user_id: int,
    ) -> User | None:
        """Find a user by their database ID."""
        return await self.db.get(User, user_id)

    async def get_by_email(
        self,
        email: str,
    ) -> User | None:
        """Find a user by email address."""
        statement = select(User).where(
            User.email == email.lower()
        )

        result = await self.db.execute(statement)

        return result.scalar_one_or_none()

    async def create(
        self,
        full_name: str,
        email: str,
        hashed_password: str,
    ) -> User:
        """Create a new citizen user."""

        user = User(
            full_name=full_name,
            email=email.lower(),
            hashed_password=hashed_password,
            role=UserRole.CITIZEN,
        )

        self.db.add(user)

        await self.db.flush()
        await self.db.refresh(user)

        return user
