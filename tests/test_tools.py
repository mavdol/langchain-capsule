import pytest
from unittest.mock import patch, AsyncMock

from langchain_capsule.tools import CapsulePythonTool, CapsuleJSTool

@pytest.fixture
def run_mock():
    with patch("langchain_capsule.tools.run", new_callable=AsyncMock) as mock:
        yield mock


@pytest.mark.asyncio
@patch("langchain_capsule.tools.resources.path")
async def test_python_arun_success(mock_path, run_mock):
    run_mock.return_value = {"success": True, "result": "Hello World", "error": None}
    mock_path.return_value.__enter__.return_value = "../langchain_capsule/sandboxes/sandbox_py.wasm"

    result = await CapsulePythonTool().arun("1+1")

    assert result == "Hello World"
    run_mock.assert_called_once_with(
        file="../langchain_capsule/sandboxes/sandbox_py.wasm",
        args=["1+1"]
    )

@patch("langchain_capsule.tools.resources.path")
def test_python_run_success(mock_path, run_mock):
    run_mock.return_value = {"success": True, "result": "Sync Hello World", "error": None}
    mock_path.return_value.__enter__.return_value = "../langchain_capsule/sandboxes/sandbox_py.wasm"

    result = CapsulePythonTool().run("1+1")

    assert result == "Sync Hello World"
    run_mock.assert_called_once_with(
        file="../langchain_capsule/sandboxes/sandbox_py.wasm",
        args=["1+1"]
    )

@pytest.mark.asyncio
@patch("langchain_capsule.tools.resources.path")
async def test_python_arun_syntax_error(mock_path, run_mock):
    run_mock.return_value = {
        "success": False,
        "result": None,
        "error": {"error_type": "SyntaxError", "message": "invalid syntax"}
    }
    mock_path.return_value.__enter__.return_value = "../langchain_capsule/sandboxes/sandbox_py.wasm"

    result = await CapsulePythonTool().arun("def broken(")

    assert isinstance(result, str)
    assert "invalid syntax" in result




@pytest.mark.asyncio
@patch("langchain_capsule.tools.resources.path")
async def test_js_arun_success(mock_path, run_mock):
    run_mock.return_value = {"success": True, "result": "JS Hello World", "error": None}
    mock_path.return_value.__enter__.return_value = "../langchain_capsule/sandboxes/sandbox_js.wasm"

    result = await CapsuleJSTool().arun("1+1")

    assert result == "JS Hello World"
    run_mock.assert_called_once_with(
        file="../langchain_capsule/sandboxes/sandbox_js.wasm",
        args=["1+1"]
    )

@patch("langchain_capsule.tools.resources.path")
def test_js_run_success(mock_path, run_mock):
    run_mock.return_value = {"success": True, "result": "Sync JS Hello World", "error": None}
    mock_path.return_value.__enter__.return_value = "../langchain_capsule/sandboxes/sandbox_js.wasm"

    result = CapsuleJSTool().run("1+1")

    assert result == "Sync JS Hello World"
    run_mock.assert_called_once_with(
        file="../langchain_capsule/sandboxes/sandbox_js.wasm",
        args=["1+1"]
    )


@pytest.mark.asyncio
@patch("langchain_capsule.tools.resources.path")
async def test_js_arun_syntax_error(mock_path, run_mock):
    run_mock.return_value = {
        "success": False,
        "result": None,
        "error": {"error_type": "SyntaxError", "message": "missing formal parameter"}
    }
    mock_path.return_value.__enter__.return_value = "../langchain_capsule/sandboxes/sandbox_js.wasm"

    result = await CapsuleJSTool().arun("function broken(")

    assert isinstance(result, str)
    assert "missing formal parameter" in result
