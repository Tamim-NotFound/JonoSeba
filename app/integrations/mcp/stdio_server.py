import logging
from app.db.session import engine
from app.integrations.mcp.server import mcp


def configure_stdio_server():
    """
    Prepare MCP for stdio transport.

    stdout must contain only MCP protocol messages.
    SQLAlchemy query logging must not interfere with
    the MCP client's JSON-RPC communication.
    """

    # Disable SQLAlchemy's echo-based SQL logging.
    engine.echo = False

    # Prevent SQL query messages from being emitted at INFO.
    logging.getLogger(
        "sqlalchemy.engine"
    ).setLevel(logging.WARNING)

    return mcp


def main() -> None:
    server = configure_stdio_server()
    server.run(transport="stdio")


if __name__ == "__main__":
    main()
