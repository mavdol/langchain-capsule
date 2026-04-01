"""
Session management for persistent Capsule sandbox execution.
"""

from capsule_adapter import Session


class PythonSession:
    """Persistent Python sandbox session with state introspection."""

    def __init__(self):
        self._session = Session("python")

    async def run(self, code: str) -> str:
        """Execute code, preserving state across calls."""
        return await self._session.run(code)

    async def get_state(self) -> str:
        """Return current variable names and their types."""
        return await self._session.run(
            "{k: type(v).__name__ for k, v in vars().items() if not k.startswith('_')}"
        )

    async def reset(self) -> None:
        """Clear variable state without touching workspace files."""
        await self._session.reset()

    async def close(self) -> None:
        """Destroy the session and clean up all files."""
        await self._session.__aexit__(None, None, None)


class JSSession:
    """Persistent JavaScript sandbox session with state introspection."""

    def __init__(self):
        self._session = Session("javascript")

    async def run(self, code: str) -> str:
        """Execute code, preserving state across calls."""
        return await self._session.run(code)

    async def get_state(self) -> str:
        """Return current variable names and their types."""
        with open(self._session._state_file, "r") as f:
            return f.read()

    async def reset(self) -> None:
        """Clear variable state without touching workspace files."""
        await self._session.reset()

    async def close(self) -> None:
        """Destroy the session and clean up all files."""
        await self._session.__aexit__(None, None, None)
