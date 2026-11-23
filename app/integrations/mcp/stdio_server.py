"""MCP stdio entrypoint with clean JSON-RPC output."""

import logging
import sys

from app.integrations.mcp.server import mcp
from app.db.session import engine


def main() -> None:
    # SQLAlchemy must not print SQL statements to stdout.
    engine.sync_engine.echo = False

    logging.getLogger("sqlalchemy.engine").setLevel(
        logging.WARNING
    )

    # Route existing console logging to stderr.
    loggers = [logging.getLogger()]

    loggers.extend(
        logger
        for logger in logging.Logger.manager.loggerDict.values()
        if isinstance(logger, logging.Logger)
    )

    for logger in loggers:
        for handler in logger.handlers:
            if (
                isinstance(handler, logging.StreamHandler)
                and handler.stream is sys.stdout
            ):
                handler.setStream(sys.stderr)

    # stdout is reserved for MCP JSON-RPC messages.
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
