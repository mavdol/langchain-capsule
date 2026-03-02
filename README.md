# langchain-capsule

[Capsule](https://github.com/mavdol/capsule) integration for LangChain.

## What is this?

`langchain-capsule` gives LangChain agents the ability to safely execute Python and javascript code in an isolated WebAssembly sandbox.

The WebAssembly sandbox files (.wasm) are already bundled inside this package; no configuration or network request is necessary to execute the sandboxes dynamically.

## Installation

```bash
pip install langchain-capsule
```

## Usage

The package provides tools for executing code inside an isolated environment.

```python
import asyncio
from langchain_capsule import CapsulePythonTool, CapsuleJSTool

# Python Example
python_tool = CapsulePythonTool()
result = python_tool.run("1 + 1")
print(result) # "2"

# JavaScript / TypeScript Example
js_tool = CapsuleJSTool()
result = asyncio.run(js_tool.arun("1 + 2"))
print(result) # "3"
```

## Check our main repo

Visit [Capsule](https://github.com/mavdol/capsule) repository for more information.

## License

MIT License
