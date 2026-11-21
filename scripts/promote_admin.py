
"""
JonoSeba — Manual Admin Promotion

Run locally by an authorized project operator.

Usage:
    uv run python scripts/promote_admin.py

This script:
- Only promotes an existing registered citizen
- Never asks for or changes a password
- Requires explicit confirmation
- Rejects inactive accounts
- Does not create new users
- Does not expose a public HTTP endpoint
"""

import asyncio
import logging

from sqlalchemy import select

from app.db.session import AsyncSessionLocal, engine
from app.modules.auth.models import User, UserRole


logging.basicConfig(
    level=logging.WARNING,
    format="%(levelname)s: %(message)s",
)


async def promote_admin() -> None:
    print()
    print("=" * 55)
    print("       JonoSeba — Admin Account Setup")
    print("=" * 55)
    print()
    print("Only authorized project operators should use this.")
    print("An existing account is required.")
    print()

    email = input(
        "Enter the registered officer email: "
    ).strip().lower()

    if not email or "@" not in email:
        print("\nInvalid email.")
        return

    async with AsyncSessionLocal() as db:
        async with db.begin():
            result = await db.execute(
                select(User)
                .where(User.email == email)
                .with_for_update()
            )

            user = result.scalar_one_or_none()

            if user is None:
                print(
                    "\nAccount not found. "
                    "Register the officer first."
                )
                return

            print("\nAccount found:")
            print(f"  User ID : {user.id}")
            print(f"  Name    : {user.full_name}")
            print(f"  Email   : {user.email}")
            print(f"  Role    : {user.role.value}")
            print(f"  Active  : {user.is_active}")

            if not user.is_active:
                print(
                    "\nInactive accounts cannot be promoted."
                )
                return

            if user.role == UserRole.ADMIN:
                print(
                    "\nThis account is already an Admin."
                )
                return

            if user.role != UserRole.CITIZEN:
                print(
                    "\nUnexpected user role. "
                    "Promotion cancelled."
                )
                return

            print()
            print("WARNING:")
            print(
                "Admin access allows managing "
                "citizen complaints."
            )
            print(
                "Verify the officer's identity "
                "and authorization first."
            )
            print()

            expected = f"PROMOTE {user.email}"

            confirmation = input(
                f"Type '{expected}' to confirm: "
            ).strip()

            if confirmation != expected:
                print(
                    "\nConfirmation did not match. "
                    "No changes made."
                )
                return

            user.role = UserRole.ADMIN

            await db.flush()

            print()
            print("Admin promotion completed.")
            print(f"  User ID : {user.id}")
            print(f"  Email   : {user.email}")
            print("  New role: admin")

    print()
    print("The officer can now sign in normally.")
    print("Admin dashboard: http://localhost:5173/admin")
    print()


async def main() -> None:
    try:
        await promote_admin()
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
