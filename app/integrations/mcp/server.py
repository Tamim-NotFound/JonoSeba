from mcp.server.fastmcp import FastMCP
from sqlalchemy import select
from app.db.session import AsyncSessionLocal
from app.integrations.llm.tools.knowledge import (
    search_published_knowledge as retrieve_published_knowledge,
)
from app.modules.departments.models import Department


mcp = FastMCP("JonoSeba")


def build_service_overview() -> dict:
    """
    Describe the JonoSeba demonstration platform.
    """
    return {
        "name": "JonoSeba",
        "name_bn": "জনসেবা",
        "mode": "demonstration",
        "supported_languages": ["bn", "en"],
        "features": [
            "Citizen complaint submission",
            "Complaint status tracking",
            "Municipal department information",
            "AI-assisted service guidance",
        ],
        "notice": (
            "This is a demonstration platform. "
            "It is not an official government service. "
            "Actual procedures, fees, and documents "
            "must be confirmed with the responsible authority."
        ),
    }


def build_about_resource() -> str:
    return (
        "JonoSeba (জনসেবা) is a bilingual Bangla-English "
        "municipal citizen-service demonstration platform. "
        "Citizens can submit complaints and track their "
        "status. The AI can assist with service navigation "
        "using available knowledge and authorized tools. "
        "Demo content must not be presented as an official "
        "government notice."
    )


def build_citizen_prompt(language: str = "bn") -> str:
    if language not in {"bn", "en"}:
        raise ValueError(
            "Language must be 'bn' or 'en'."
        )

    if language == "bn":
        return (
            "তুমি JonoSeba-এর বাংলা নাগরিকসেবা সহকারী। "
            "নাগরিককে সহজ বাংলায় সহায়তা করো। "
            "যাচাই করা তথ্য না থাকলে সেটি স্পষ্ট বলো। "
            "সরকারি ফি, প্রয়োজনীয় কাগজপত্র বা সময়সীমা "
            "নিজে বানিয়ে বলবে না। "
            "JonoSeba একটি ডেমো প্ল্যাটফর্ম; "
            "সরকারি কর্তৃপক্ষের পরিচয় দেবে না।"
        )

    return (
        "You are the English-language JonoSeba "
        "citizen-service assistant. "
        "Explain information clearly and helpfully. "
        "Do not invent official fees, required documents, "
        "deadlines, or procedures. "
        "Distinguish demo guidance from verified information. "
        "Never claim that JonoSeba is an official "
        "government service."
    )


async def fetch_active_departments() -> dict:
    """
    Fetch active departments from PostgreSQL.

    Only public department information is returned.
    """

    statement = (
        select(Department)
        .where(Department.is_active.is_(True))
        .order_by(Department.name.asc())
    )

    async with AsyncSessionLocal() as db:
        result = await db.execute(statement)
        departments = result.scalars().all()

    items = [
        {
            "id": department.id,
            "name": department.name,
            "description": department.description,
        }
        for department in departments
    ]

    return {
        "count": len(items),
        "departments": items,
        "notice": (
            "Department information comes from the "
            "JonoSeba demonstration database. "
            "It does not represent a confirmed list "
            "for every municipality in Bangladesh."
        ),
    }


async def fetch_municipal_knowledge(query: str) -> dict:
    """
    Search public JonoSeba knowledge through the
    existing RAG retrieval tool.

    No citizen accounts or private complaints are exposed.
    """

    if not isinstance(query, str) or not query.strip():
        raise ValueError(
            "Knowledge search query cannot be empty."
        )

    query = query.strip()

    if len(query) > 2000:
        raise ValueError(
            "Knowledge search query cannot exceed 2000 characters."
        )

    async with AsyncSessionLocal() as db:
        result = await retrieve_published_knowledge(
            db=db,
            query=query,
        )

    return {
        **result,
        "notice": (
            "This is JonoSeba demonstration knowledge. "
            "Retrieved sources have not been independently "
            "authenticated by this MCP tool. "
            "Confirm official procedures, fees, and "
            "document requirements with the authority."
        ),
    }


@mcp.tool()
def get_jonoseba_demo_overview() -> dict:
    """
    Get JonoSeba demonstration platform information.
    """
    return build_service_overview()


@mcp.tool()
async def get_active_departments() -> dict:
    """
    List active departments from JonoSeba PostgreSQL.

    Returns public department names and descriptions.
    No private citizen data is exposed.
    """
    return await fetch_active_departments()


@mcp.tool()
async def search_municipal_knowledge(query: str) -> dict:
    """
    Search published municipal knowledge using pgvector.

    Query may be in Bangla or English.

    Results are reference excerpts, not official
    instructions. Do not invent missing information.
    """
    return await fetch_municipal_knowledge(query)


@mcp.resource("jonoseba://about")
def jonoseba_about() -> str:
    """
    Read a description of JonoSeba.
    """
    return build_about_resource()


@mcp.prompt()
def citizen_service_assistant(
    language: str = "bn",
) -> str:
    """
    Get a Bangla or English citizen-service prompt.
    """
    return build_citizen_prompt(language)


if __name__ == "__main__":
    mcp.run(transport="stdio")
