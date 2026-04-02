import pytest
from unittest.mock import patch, AsyncMock

from langchain_core.tools import ToolException

from langchain_capsule.tools import (
    CapsulePythonTool,
    CapsuleJSTool,
)


# ── Async run ────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_python_tool_calls_run_python():
    with patch("langchain_capsule.tools.run_python", new_callable=AsyncMock) as mock:
        mock.return_value = "ok"
        result = await CapsulePythonTool().arun("x = 1")
        mock.assert_called_once_with(code="x = 1")
        assert result == "ok"


@pytest.mark.asyncio
async def test_js_tool_calls_run_javascript():
    with patch("langchain_capsule.tools.run_javascript", new_callable=AsyncMock) as mock:
        mock.return_value = "ok"
        result = await CapsuleJSTool().arun("let x = 1")
        mock.assert_called_once_with(code="let x = 1")
        assert result == "ok"


# ── Error handling ───────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_python_tool_arun_raises_tool_exception_on_error():
    with patch("langchain_capsule.tools.run_python", new_callable=AsyncMock) as mock:
        mock.side_effect = RuntimeError("sandbox crashed")
        with pytest.raises(ToolException, match="sandbox crashed"):
            await CapsulePythonTool()._arun("bad code")


@pytest.mark.asyncio
async def test_js_tool_arun_raises_tool_exception_on_error():
    with patch("langchain_capsule.tools.run_javascript", new_callable=AsyncMock) as mock:
        mock.side_effect = RuntimeError("sandbox crashed")
        with pytest.raises(ToolException, match="sandbox crashed"):
            await CapsuleJSTool()._arun("bad code")


@pytest.mark.asyncio
async def test_python_tool_arun_returns_error_string():
    """handle_tool_error=True means tool.arun() returns the error as a string instead of raising."""
    with patch("langchain_capsule.tools.run_python", new_callable=AsyncMock) as mock:
        mock.side_effect = RuntimeError("sandbox crashed")
        result = await CapsulePythonTool().arun("bad code")
        assert "sandbox crashed" in result


@pytest.mark.asyncio
async def test_js_tool_arun_returns_error_string():
    with patch("langchain_capsule.tools.run_javascript", new_callable=AsyncMock) as mock:
        mock.side_effect = RuntimeError("sandbox crashed")
        result = await CapsuleJSTool().arun("bad code")
        assert "sandbox crashed" in result


# ── Sync wrapper ─────────────────────────────────────────────────────

def test_python_tool_sync_run():
    with patch("langchain_capsule.tools.run_python", new_callable=AsyncMock) as mock:
        mock.return_value = "2"
        result = CapsulePythonTool().run("1+1")
        assert result == "2"


def test_js_tool_sync_run():
    with patch("langchain_capsule.tools.run_javascript", new_callable=AsyncMock) as mock:
        mock.return_value = "2"
        result = CapsuleJSTool().run("1+1")
        assert result == "2"


def test_python_tool_sync_run_raises_tool_exception_on_error():
    with patch("langchain_capsule.tools.run_python", new_callable=AsyncMock) as mock:
        mock.side_effect = RuntimeError("sandbox crashed")
        with pytest.raises(ToolException, match="sandbox crashed"):
            CapsulePythonTool()._run("bad code")


@pytest.mark.asyncio
async def test_python_tool_sync_run_from_async_context():
    """_run must work even when called from within a running event loop."""
    with patch("langchain_capsule.tools.run_python", new_callable=AsyncMock) as mock:
        mock.return_value = "42"
        result = CapsulePythonTool()._run("21 * 2")
        assert result == "42"


# ── Tool metadata ────────────────────────────────────────────────────

def test_python_tool_name():
    assert CapsulePythonTool().name == "python_execution"


def test_js_tool_name():
    assert CapsuleJSTool().name == "javascript_execution"


def test_python_tool_handle_tool_error_enabled():
    assert CapsulePythonTool().handle_tool_error is True


def test_js_tool_handle_tool_error_enabled():
    assert CapsuleJSTool().handle_tool_error is True
