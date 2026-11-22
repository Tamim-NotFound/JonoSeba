from google.genai import types

LIST_DEPARTMENTS_DECLARATION = (
    types.FunctionDeclaration(
        name="list_departments",
        description=(
            "Get active JonoSeba municipal departments "
            "from the database. Use for department lists "
            "and issue routing."
        ),
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "search": types.Schema(
                    type=types.Type.STRING,
                    description=(
                        "Optional department name search; "
                        "empty to list all."
                    ),
                ),
            },
            required=[],
        ),
    )
)


GET_MY_COMPLAINT_STATUS_DECLARATION = (
    types.FunctionDeclaration(
        name="get_my_complaint_status",
        description=(
            "Find the status of a specific complaint ID, "
            "checking the authenticated citizen's "
            "ownership. Never accept a citizen_id."
        ),
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "complaint_id": types.Schema(
                    type=types.Type.INTEGER,
                    description=(
                        "Positive integer complaint ID."
                    ),
                ),
            },
            required=["complaint_id"],
        ),
    )
)


SEARCH_PUBLISHED_KNOWLEDGE_DECLARATION = (
    types.FunctionDeclaration(
        name="search_published_knowledge",
        description=(
            "Search municipal service knowledge with "
            "pgvector. First search published, "
            "source-linked knowledge using "
            "include_research=false. If nothing relevant "
            "is published, repeat with "
            "include_research=true to include JonoSeba's "
            "saved, UNVERIFIED user-provided birth/death "
            "and municipal-service research drafts. "
            "These drafts are NOT government-verified. "
            "Never claim exact fees, deadlines or "
            "mandatory document rules from unverified "
            "research."
        ),
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "query": types.Schema(
                    type=types.Type.STRING,
                    description=(
                        "Citizen's Bangla or English "
                        "service question, maximum "
                        "2000 characters."
                    ),
                ),
                "include_research": types.Schema(
                    type=types.Type.BOOLEAN,
                    description=(
                        "False by default: published "
                        "sources only. True: if no "
                        "published match, retrieve "
                        "labeled unverified research "
                        "drafts saved by the project owner."
                    ),
                ),
            },
            required=["query"],
        ),
    )
)


JONOSEBA_GEMINI_TOOLS = [
    types.Tool(
        function_declarations=[
            LIST_DEPARTMENTS_DECLARATION,
            GET_MY_COMPLAINT_STATUS_DECLARATION,
            SEARCH_PUBLISHED_KNOWLEDGE_DECLARATION,
        ]
    )
]
