"""
Capsule integration for running untrusted code securely in isolated WebAssembly sandboxes.
"""

import asyncio
from importlib import resources
from typing import Any

from capsule import run
from langchain_core.tools import BaseTool, ToolException

def _get_wasm(filename: str) -> str:
    """Resolve the path to a .wasm file bundled inside this package."""
    with resources.path("langchain_capsule.sandboxes", filename) as path:
        return str(path)


def _parse_capsule_error(error: Any) -> str:
    """Extract a human-readable message from a Capsule error payload."""
    if isinstance(error, dict):
        return error.get("message") or error.get("error_type") or str(error)
    return str(error)


async def _invoke_sandbox(wasm_file: str, code: str) -> str:
    """Call the Capsule sandbox and return the result value only."""
    res = await run(file=wasm_file, args=[code])

    if res.get("success"):
        return str(res.get("result", ""))

    raise ToolException(_parse_capsule_error(res.get("error")))


class CapsulePythonTool(BaseTool):
    """Execute Python code inside an isolated Capsule WebAssembly sandbox."""

    name: str = "python_repl"
    description: str = (
        "Execute Python code in a secure isolated WebAssembly sandbox. "
        "Both standard output (print statements) and the last evaluated expression are returned. "
        "Supports pure Python only (no C extensions like numpy/pandas)."
    )
    handle_tool_error: bool = True

    def _run(self, query: str) -> str:
        return asyncio.run(_invoke_sandbox(_get_wasm("sandbox_py.wasm"), query))

    async def _arun(self, query: str) -> str:
        return await _invoke_sandbox(_get_wasm("sandbox_py.wasm"), query)


class CapsuleJSTool(BaseTool):
    """Execute JavaScript code inside an isolated Capsule WebAssembly sandbox."""

    name: str = "javascript_repl"
    description = (
        "Execute JavaScript code in a secure isolated WebAssembly sandbox. "
        "Both standard output (console logs) and the last evaluated expression are returned."
    )
    handle_tool_error: bool = True

    def _run(self, query: str) -> str:
        return asyncio.run(_invoke_sandbox(_get_wasm("sandbox_js.wasm"), query))

    async def _arun(self, query: str) -> str:
        return await _invoke_sandbox(_get_wasm("sandbox_js.wasm"), query)
