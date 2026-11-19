from google.genai import types

LIST_DEPARTMENTS_DECLARATION = types.FunctionDeclaration(
    name="list_departments",
    description=(
        "Get the list of active municipal departments "
        "available in JonoSeba. "
        "Use this tool when a citizen asks which department "
        "handles a particular municipal issue, or wants "
        "to know which departments are available. "
        "The results come from the JonoSeba database."
    ),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "search": types.Schema(
                type=types.Type.STRING,
                description=(
                    "Optional department name search term. "
                    "For example: Water, Roads, Waste. "
                    "Use an empty string to list all departments."
                ),
            ),
        },
        required=[],
    ),
)


GET_MY_COMPLAINT_STATUS_DECLARATION = types.FunctionDeclaration(
    name="get_my_complaint_status",
    description=(
        "Look up the current status of a complaint in "
        "the JonoSeba database. "
        "Use this tool when a citizen asks about a "
        "specific complaint ID. "
        "The backend checks the authenticated user's "
        "permission before returning any complaint data. "
        "Never ask for or provide a citizen_id."
    ),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "complaint_id": types.Schema(
                type=types.Type.INTEGER,
                description=(
                    "The positive integer complaint ID "
                    "provided by the citizen."
                ),
            ),
        },
        required=["complaint_id"],
    ),
)


JONOSEBA_GEMINI_TOOLS = [
    types.Tool(
        function_declarations=[
            LIST_DEPARTMENTS_DECLARATION,
            GET_MY_COMPLAINT_STATUS_DECLARATION,
        ]
    )
]
