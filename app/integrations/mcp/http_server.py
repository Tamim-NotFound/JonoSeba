import os
from app.integrations.mcp.server import mcp


MCP_HTTP_HOST = os.getenv(
    "MCP_HTTP_HOST",
    "127.0.0.1",
)

MCP_HTTP_PORT = int(
    os.getenv("MCP_HTTP_PORT", "8001")
)

MCP_HTTP_PATH = "/mcp"


def configure_http_server():
    """
    Configure JonoSeba MCP HTTP transport.

    Local execution defaults to 127.0.0.1.

    Docker can use MCP_HTTP_HOST=0.0.0.0
    internally, while Docker Compose exposes
    the service only on host localhost.

    The MCP tools are not protected by
    HTTP authentication, so this server
    should not be exposed publicly.
    """

    mcp.settings.host = MCP_HTTP_HOST
    mcp.settings.port = MCP_HTTP_PORT

    mcp.settings.streamable_http_path = (
        MCP_HTTP_PATH
    )

    mcp.settings.stateless_http = True

    return mcp


def main() -> None:
    server = configure_http_server()

    server.run(
        transport="streamable-http"
    )


if __name__ == "__main__":
    main()
