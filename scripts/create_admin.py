import asyncio
import getpass
from pydantic import ValidationError
from sqlalchemy import select
from app.core.security import hash_password
from app.db.session import AsyncSessionLocal, engine
from app.modules.auth.models import User, UserRole
from app.modules.auth.schemas import UserRegister


async def provision_admin() -> None:
    print("\n=== JonoSeba Admin Provisioning ===\n")

    full_name = input("Admin full name: ").strip()
    email = input("Admin email: ").strip().lower()

    # Password is hidden while typing.
    password = getpass.getpass("Admin password: ")

    try:
        validated = UserRegister(
            full_name=full_name,
            email=email,
            password=password,
        )
    except ValidationError as exc:
        print("\nInvalid admin information:")
        for error in exc.errors():
            field = ".".join(str(x) for x in error["loc"])
            print(f"- {field}: {error['msg']}")
        return

    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(User).where(
                User.email == validated.email
            )
        )

        existing_user = result.scalar_one_or_none()

        if existing_user is not None:
            if existing_user.role == UserRole.ADMIN:
                print("\nThis account is already an admin.")
                return

            print("\nAn existing citizen account was found.")
            print(f"Email: {existing_user.email}")

            confirmation = input(
                "Promote this citizen to admin? "
                "Type YES to confirm: "
            ).strip()

            if confirmation != "YES":
                print("Promotion cancelled.")
                return

            existing_user.role = UserRole.ADMIN

            await db.commit()

            print("\nSUCCESS: Citizen promoted to admin.")
            return

        new_admin = User(
            full_name=validated.full_name,
            email=validated.email,
            hashed_password=hash_password(
                validated.password
            ),
            role=UserRole.ADMIN,
            is_active=True,
        )

        db.add(new_admin)
        await db.commit()
        await db.refresh(new_admin)

        print("\nSUCCESS: Admin account created.")
        print(f"Admin ID: {new_admin.id}")
        print(f"Email: {new_admin.email}")
        print(f"Role: {new_admin.role.value}")


async def main() -> None:
    try:
        await provision_admin()
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
