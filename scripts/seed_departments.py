import asyncio
from sqlalchemy import select
from app.db.session import AsyncSessionLocal, engine
from app.modules.departments.models import Department


DEPARTMENTS = [
    {
        "name": "Water Supply",
        "description": (
            "Handles drinking water supply, pipeline maintenance, "
            "water shortages and water quality complaints."
        ),
    },
    {
        "name": "Waste Management",
        "description": (
            "Handles garbage collection, waste disposal, "
            "street cleaning and public sanitation."
        ),
    },
    {
        "name": "Roads and Infrastructure",
        "description": (
            "Handles damaged roads, potholes, footpaths, "
            "bridges and municipal infrastructure."
        ),
    },
    {
        "name": "Street Lighting",
        "description": (
            "Handles broken streetlights, lighting maintenance "
            "and poorly illuminated public areas."
        ),
    },
    {
        "name": "Drainage and Sewerage",
        "description": (
            "Handles blocked drains, waterlogging, sewerage "
            "problems and drainage maintenance."
        ),
    },
    {
        "name": "Public Health",
        "description": (
            "Handles public health concerns, mosquito control, "
            "hygiene and community sanitation."
        ),
    },
    {
        "name": "Parks and Recreation",
        "description": (
            "Handles public parks, playgrounds, green spaces "
            "and recreational facilities."
        ),
    },
    {
        "name": "Birth and Death Registration",
        "description": (
            "Handles municipal guidance and complaints related "
            "to birth and death registration services."
        ),
    },
]


async def seed_departments() -> None:
    created = 0
    skipped = 0

    async with AsyncSessionLocal() as db:
        try:
            for item in DEPARTMENTS:
                result = await db.execute(
                    select(Department).where(
                        Department.name == item["name"]
                    )
                )

                existing_department = result.scalar_one_or_none()

                if existing_department is not None:
                    print(f"SKIP: {item['name']}")
                    skipped += 1
                    continue

                department = Department(
                    name=item["name"],
                    description=item["description"],
                    is_active=True,
                )

                db.add(department)
                await db.flush()

                print(f"CREATE: {item['name']}")
                created += 1

            await db.commit()

            print()
            print("Department seeding completed!")
            print(f"Created: {created}")
            print(f"Skipped: {skipped}")

        except Exception:
            await db.rollback()
            raise


async def main() -> None:
    try:
        await seed_departments()
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
