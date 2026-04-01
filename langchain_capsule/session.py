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

    async def import_file(self, source_path: str, destination_path: str) -> None:
        """Copy a file from the host filesystem into the session workspace."""
        await self._session.import_file(source_path, destination_path)

    async def export_file(self, source_path: str, destination_path: str) -> None:
        """Copy a file from the session workspace to the host filesystem."""
        await self._session.export_file(source_path, destination_path)

    async def delete_file(self, path: str) -> None:
        """Remove a file from the session workspace."""
        await self._session.delete_file(path)

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

    async def import_file(self, source_path: str, destination_path: str) -> None:
        """Copy a file from the host filesystem into the session workspace."""
        await self._session.import_file(source_path, destination_path)

    async def export_file(self, source_path: str, destination_path: str) -> None:
        """Copy a file from the session workspace to the host filesystem."""
        await self._session.export_file(source_path, destination_path)

    async def delete_file(self, path: str) -> None:
        """Remove a file from the session workspace."""
        await self._session.delete_file(path)

    async def reset(self) -> None:
        """Clear variable state without touching workspace files."""
        await self._session.reset()

    async def close(self) -> None:
        """Destroy the session and clean up all files."""
        await self._session.__aexit__(None, None, None)
