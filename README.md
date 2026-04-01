# langchain-capsule

Capsule integration for LangChain — run Python and JavaScript code in isolated WebAssembly sandboxes.

## What is this?

`langchain-capsule` gives LangChain agents the ability to safely execute code in isolated WebAssembly sandboxes. The sandbox binaries are bundled inside the package — no configuration or network request required.

## Installation

```bash
pip install langchain-capsule
```

## Tools

| Tool | Name | Description |
|---|---|---|
| `CapsulePythonTool` | `python_execution` | Stateless Python execution — each call is independent |
| `CapsuleJSTool` | `javascript_execution` | Stateless JavaScript execution — each call is independent |
| `CapsulePythonREPLTool` | `python_repl` | Persistent Python session — state is preserved across calls |
| `CapsuleJSREPLTool` | `javascript_repl` | Persistent JavaScript session — state is preserved across calls |

## Usage

### Stateless execution

Each call runs in a fresh sandbox. No state is preserved between calls.

```python
from langchain_capsule import CapsulePythonTool, CapsuleJSTool

python_tool = CapsulePythonTool()
print(python_tool.run("1 + 1"))  # "2"

js_tool = CapsuleJSTool()
print(js_tool.run("1 + 2"))  # "3"
```

### Session-based execution

The session tools preserve variables, imports, and function definitions across calls — useful for multi-step computations or when the agent needs to build up state incrementally.

```python
import asyncio
from langchain_capsule import CapsulePythonREPLTool, CapsuleJSREPLTool

async def main():
    # Python session
    py = CapsulePythonREPLTool()
    await py._arun("total = 0")
    await py._arun("total += 10")
    await py._arun("total += 32")
    print(await py._arun("total"))  # "42"

    # Inspect variables currently in scope
    print(await py.get_state())  # {"total": "int"}

    # Clear state without destroying the session
    await py.reset()

    # Destroy the session and release resources
    await py.close()

    # JavaScript session
    js = CapsuleJSREPLTool()
    await js._arun("let total = 0")
    await js._arun("total += 10")
    await js._arun("total += 32")
    print(await js._arun("total"))  # "42"
    await js.close()

asyncio.run(main())
```

### With a LangChain agent

```python
from langchain_capsule import CapsulePythonREPLTool
from langchain_core.language_models.chat_models import BaseChatModel

tool = CapsulePythonREPLTool()

# Pass the tool to any LangChain agent
agent = your_llm.bind_tools([tool])
```

## More information

Visit the [Capsule](https://github.com/mavdol/capsule) repository for more information.

## License

MIT License
