import asyncio
from sqlalchemy.engine import make_url
from app.core.config import settings
from app.db.base import Base
from app.db.session import engine
from app.modules.auth.models import User  # noqa: F401
from app.modules.complaints.models import Complaint  # noqa: F401
from app.modules.departments.models import Department  # noqa: F401
from app.modules.knowledge.models import KnowledgeChunk  # noqa: F401


async def main():
    production_url = make_url(settings.DATABASE_URL)

    test_url = production_url.set(
        database="jonoseba_test_db"
    )

    if test_url.database == production_url.database:
        raise RuntimeError(
            "Refusing to use the production database."
        )

    from sqlalchemy.ext.asyncio import create_async_engine

    test_engine = create_async_engine(test_url)

    try:
        async with test_engine.begin() as connection:
            await connection.run_sync(
                Base.metadata.create_all
            )

        print("Test database tables created successfully.")
        print("Database:", test_url.database)

    finally:
        await test_engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())