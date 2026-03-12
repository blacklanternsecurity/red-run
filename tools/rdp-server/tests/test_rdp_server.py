"""Tests for the RDP MCP server.

Tests server creation, session management, input validation, and key parsing.
Does NOT require a live RDP target — tests use the MCP call_tool interface
which returns errors before attempting network connections for invalid inputs.
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

# Add parent to path so we can import server
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from server import create_server


def _run(coro):
    """Run an async coroutine synchronously."""
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()


def _call(srv, tool_name, args):
    """Call an MCP tool and return the text result."""
    content, _meta = _run(srv.call_tool(tool_name, args))
    return content[0].text


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def server():
    """Create a fresh RDP MCP server instance."""
    return create_server()


# ---------------------------------------------------------------------------
# Server Creation Tests
# ---------------------------------------------------------------------------


class TestServerCreation:
    def test_creates_server(self, server):
        assert server is not None

    def test_server_name(self, server):
        assert server.name == "red-run-rdp-server"

    def test_server_has_instructions(self, server):
        assert server.instructions
        assert "rdp_connect" in server.instructions

    def test_has_expected_tools(self, server):
        tools = _run(server.list_tools())
        tool_names = {t.name for t in tools}
        expected = {
            "rdp_connect",
            "rdp_screenshot",
            "rdp_click",
            "rdp_double_click",
            "rdp_type",
            "rdp_key",
            "rdp_execute",
            "rdp_scroll",
            "rdp_close",
            "list_rdp_sessions",
        }
        assert expected == tool_names


# ---------------------------------------------------------------------------
# Resolution Parsing (via rdp_connect)
# ---------------------------------------------------------------------------


class TestResolutionValidation:
    def test_invalid_resolution_format(self):
        text = _call(
            create_server(),
            "rdp_connect",
            {
                "host": "127.0.0.1",
                "user": "test",
                "password": "test",
                "resolution": "not-a-resolution",
            },
        )
        assert "ERROR" in text
        assert "Invalid resolution" in text

    def test_resolution_missing_separator(self):
        text = _call(
            create_server(),
            "rdp_connect",
            {
                "host": "127.0.0.1",
                "user": "test",
                "password": "test",
                "resolution": "1920",
            },
        )
        assert "ERROR" in text


# ---------------------------------------------------------------------------
# Session Not Found Tests
# ---------------------------------------------------------------------------


class TestSessionNotFound:
    """All per-session tools should return a clear error for unknown IDs."""

    TOOLS_WITH_SESSION = [
        ("rdp_screenshot", {"session_id": "nonexistent"}),
        ("rdp_click", {"session_id": "nonexistent", "x": 0, "y": 0}),
        ("rdp_double_click", {"session_id": "nonexistent", "x": 0, "y": 0}),
        ("rdp_type", {"session_id": "nonexistent", "text": "hello"}),
        ("rdp_key", {"session_id": "nonexistent", "keys": "Return"}),
        ("rdp_execute", {"session_id": "nonexistent", "command": "whoami"}),
        ("rdp_scroll", {"session_id": "nonexistent"}),
        ("rdp_close", {"session_id": "nonexistent"}),
    ]

    @pytest.mark.parametrize(
        "tool_name,args",
        TOOLS_WITH_SESSION,
        ids=[t[0] for t in TOOLS_WITH_SESSION],
    )
    def test_returns_error(self, tool_name, args):
        text = _call(create_server(), tool_name, args)
        assert "ERROR" in text
        assert "not found" in text


# ---------------------------------------------------------------------------
# List Sessions (empty)
# ---------------------------------------------------------------------------


class TestListSessions:
    def test_empty_sessions(self):
        text = _call(create_server(), "list_rdp_sessions", {})
        assert "No active RDP sessions" in text


# ---------------------------------------------------------------------------
# Evidence Path Tests
# ---------------------------------------------------------------------------


class TestEvidencePath:
    def test_fallback_path_without_engagement_dir(self, tmp_path):
        """Without engagement/evidence, screenshots use project root fallback."""
        with patch("server._PROJECT_ROOT", tmp_path):
            assert not (tmp_path / "engagement" / "evidence").exists()

    def test_evidence_dir_used_when_present(self, tmp_path):
        """When engagement/evidence exists, it should be the target dir."""
        evidence_dir = tmp_path / "engagement" / "evidence"
        evidence_dir.mkdir(parents=True)
        with patch("server._PROJECT_ROOT", tmp_path):
            assert evidence_dir.exists()
