"""
Capsule integration for running untrusted code securely in isolated WebAssembly sandboxes.
"""

import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import Optional

from capsule_adapter import run_javascript, run_python
from langchain_core.tools import BaseTool, ToolException
from pydantic import PrivateAttr

from .session import JSSession, PythonSession


def _run_sync(coro):
    """Run a coroutine synchronously, even when called from within a running event loop."""
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        return asyncio.run(coro)

    with ThreadPoolExecutor(max_workers=1) as pool:
        return pool.submit(asyncio.run, coro).result()


class CapsulePythonTool(BaseTool):
    """Execute Python code inside an isolated Capsule WebAssembly sandbox."""

    name: str = "python_execution"
    description: str = (
        "Execute Python code in a secure isolated WebAssembly sandbox. "
        "Each call is independent — no state is preserved between calls. "
        "Both standard output (print statements) and the last evaluated expression are returned. "
        "Supports pure Python only (no C extensions like numpy/pandas)."
    )
    handle_tool_error: bool = True

    def _run(self, query: str) -> str:
        try:
            return _run_sync(run_python(code=query))
        except Exception as e:
            raise ToolException(str(e)) from e

    async def _arun(self, query: str) -> str:
        try:
            return await run_python(code=query)
        except Exception as e:
            raise ToolException(str(e)) from e


class CapsuleJSTool(BaseTool):
    """Execute JavaScript code inside an isolated Capsule WebAssembly sandbox."""

    name: str = "javascript_execution"
    description: str = (
        "Execute JavaScript code in a secure isolated WebAssembly sandbox. "
        "Each call is independent — no state is preserved between calls. "
        "Both standard output (console.log) and the last evaluated expression are returned."
    )
    handle_tool_error: bool = True

    def _run(self, query: str) -> str:
        try:
            return _run_sync(run_javascript(code=query))
        except Exception as e:
            raise ToolException(str(e)) from e

    async def _arun(self, query: str) -> str:
        try:
            return await run_javascript(code=query)
        except Exception as e:
            raise ToolException(str(e)) from e


class CapsulePythonREPLTool(BaseTool):
    """Execute Python code in a persistent session, preserving state across calls."""

    name: str = "python_repl"
    description: str = (
        "Execute Python code in a persistent session. "
        "Variables, imports, and functions defined in previous calls remain available. "
        "File system access is limited to /workspace. "
        "Supports pure Python only (no C extensions like numpy/pandas)."
    )
    handle_tool_error: bool = True

    _session: Optional[PythonSession] = PrivateAttr(default=None)

    def _get_session(self) -> PythonSession:
        if self._session is None:
            self._session = PythonSession()
        return self._session

    def _run(self, query: str) -> str:
        try:
            return _run_sync(self._get_session().run(query))
        except Exception as e:
            raise ToolException(str(e)) from e

    async def _arun(self, query: str) -> str:
        try:
            return await self._get_session().run(query)
        except Exception as e:
            raise ToolException(str(e)) from e

    async def get_state(self) -> str:
        """Return current variable names and their types."""
        return await self._get_session().get_state()

    async def reset(self) -> None:
        """Clear variable state without touching workspace files."""
        await self._get_session().reset()

    async def close(self) -> None:
        """Destroy the session and clean up all files."""
        if self._session is not None:
            try:
                await self._session.close()
            finally:
                self._session = None


class CapsuleJSREPLTool(BaseTool):
    """Execute JavaScript code in a persistent session, preserving state across calls."""

    name: str = "javascript_repl"
    description: str = (
        "Execute JavaScript code in a persistent session. "
        "Variables and functions defined in previous calls remain available. "
        "File system access is limited to /workspace."
    )
    handle_tool_error: bool = True

    _session: Optional[JSSession] = PrivateAttr(default=None)

    def _get_session(self) -> JSSession:
        if self._session is None:
            self._session = JSSession()
        return self._session

    def _run(self, query: str) -> str:
        try:
            return _run_sync(self._get_session().run(query))
        except Exception as e:
            raise ToolException(str(e)) from e

    async def _arun(self, query: str) -> str:
        try:
            return await self._get_session().run(query)
        except Exception as e:
            raise ToolException(str(e)) from e

    async def get_state(self) -> str:
        """Return current variable names and their types."""
        return await self._get_session().get_state()

    async def reset(self) -> None:
        """Clear variable state without touching workspace files."""
        await self._get_session().reset()

    async def close(self) -> None:
        """Destroy the session and clean up all files."""
        if self._session is not None:
            try:
                await self._session.close()
            finally:
                self._session = None
