from app.integrations.mcp.server import mcp

MCP_HTTP_HOST = "127.0.0.1"
MCP_HTTP_PORT = 8001
MCP_HTTP_PATH = "/mcp"


def configure_http_server():
    """
    Configure JonoSeba MCP for local HTTP transport.

    Stateless HTTP avoids retaining session state between
    requests. Keep the server bound to localhost because
    its tools are not protected by HTTP authentication.
    """
    mcp.settings.host = MCP_HTTP_HOST
    mcp.settings.port = MCP_HTTP_PORT
    mcp.settings.streamable_http_path = MCP_HTTP_PATH

    # MCP SDK 1.30.0 supports stateless_http.
    mcp.settings.stateless_http = True

    return mcp


def main() -> None:
    server = configure_http_server()
    server.run(transport="streamable-http")


if __name__ == "__main__":
    main()
