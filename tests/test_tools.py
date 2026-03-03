import pytest
from unittest.mock import patch, AsyncMock

from langchain_core.tools import ToolException

from langchain_capsule.tools import (
    CapsulePythonTool,
    CapsuleJSTool,
    _invoke_sandbox,
    _parse_capsule_error,
)


@pytest.fixture
def run_mock():
    with patch("langchain_capsule.tools.run", new_callable=AsyncMock) as mock:
        yield mock


# ── _parse_capsule_error ─────────────────────────────────────────────

def test_parse_error_dict_with_message():
    assert _parse_capsule_error({"message": "bad input", "error_type": "ValueError"}) == "bad input"

def test_parse_error_dict_with_only_error_type():
    assert _parse_capsule_error({"error_type": "RuntimeError"}) == "RuntimeError"

def test_parse_error_dict_empty():
    result = _parse_capsule_error({})
    assert isinstance(result, str)

def test_parse_error_plain_string():
    assert _parse_capsule_error("something went wrong") == "something went wrong"


# ── _invoke_sandbox ──────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_invoke_sandbox_success(run_mock):
    run_mock.return_value = {"success": True, "result": "2", "error": None}

    result = await _invoke_sandbox("any.wasm", "1+1")

    assert result == "2"
    run_mock.assert_called_once_with(file="any.wasm", args=["1+1"])


@pytest.mark.asyncio
async def test_invoke_sandbox_error_raises(run_mock):
    run_mock.return_value = {
        "success": False,
        "result": None,
        "error": {"error_type": "SyntaxError", "message": "invalid syntax"},
    }

    with pytest.raises(ToolException, match="invalid syntax"):
        await _invoke_sandbox("any.wasm", "bad code")


# ── Tool wiring ──────────────────────────────────────────────────────

@pytest.mark.asyncio
@patch("langchain_capsule.tools.resources.path")
async def test_python_tool_uses_correct_wasm(mock_path, run_mock):
    run_mock.return_value = {"success": True, "result": "ok", "error": None}
    mock_path.return_value.__enter__.return_value = "/fake/sandbox_py.wasm"

    await CapsulePythonTool().arun("x")

    run_mock.assert_called_once_with(file="/fake/sandbox_py.wasm", args=["x"])


@pytest.mark.asyncio
@patch("langchain_capsule.tools.resources.path")
async def test_js_tool_uses_correct_wasm(mock_path, run_mock):
    run_mock.return_value = {"success": True, "result": "ok", "error": None}
    mock_path.return_value.__enter__.return_value = "/fake/sandbox_js.wasm"

    await CapsuleJSTool().arun("x")

    run_mock.assert_called_once_with(file="/fake/sandbox_js.wasm", args=["x"])


# ── Sync wrapper ─────────────────────────────────────────────────────

@patch("langchain_capsule.tools.resources.path")
def test_sync_run_delegates_to_async(mock_path, run_mock):
    run_mock.return_value = {"success": True, "result": "2", "error": None}
    mock_path.return_value.__enter__.return_value = "/fake/sandbox_py.wasm"

    result = CapsulePythonTool().run("1+1")

    assert result == "2"
