import pytest
from mcp.server.fastmcp import FastMCP
from app.integrations.mcp.server import (
    mcp,
    build_service_overview,
    build_about_resource,
    build_citizen_prompt,
)


def test_mcp_server_is_initialized():
    assert isinstance(mcp, FastMCP)


def test_demo_overview_is_not_official():
    result = build_service_overview()

    assert result["name"] == "JonoSeba"
    assert result["mode"] == "demonstration"
    assert result["supported_languages"] == ["bn", "en"]

    assert "not an official government service" in (
        result["notice"]
    )


def test_about_resource_describes_platform():
    content = build_about_resource()

    assert "JonoSeba" in content
    assert "complaints" in content
    assert "demonstration platform" in content


def test_bilingual_prompt_and_invalid_language():
    bangla = build_citizen_prompt("bn")
    english = build_citizen_prompt("en")

    assert "নাগরিকসেবা" in bangla
    assert "citizen-service assistant" in english

    with pytest.raises(ValueError):
        build_citizen_prompt("fr")
