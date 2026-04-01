import pytest
from langchain_capsule import CapsuleJSREPLTool, CapsulePythonREPLTool
from langchain_capsule.session import JSSession, PythonSession


# ---- PythonSession unit tests ----

@pytest.mark.asyncio
async def test_python_session_variable_persistence():
    session = PythonSession()
    await session.run("x = 42")
    result = await session.run("x")
    assert str(result).strip() == "42"
    await session.close()


@pytest.mark.asyncio
async def test_python_session_function_persistence():
    session = PythonSession()
    await session.run("def greet(name): return f'Hello {name}'")
    result = await session.run("greet('Alice')")
    assert str(result).strip() == "Hello Alice"
    await session.close()


@pytest.mark.asyncio
async def test_python_session_import_persistence():
    session = PythonSession()
    await session.run("import json")
    result = await session.run('json.dumps({"key": "value"})')
    assert '"key"' in result
    assert '"value"' in result
    await session.close()


@pytest.mark.asyncio
async def test_python_session_accumulation():
    session = PythonSession()
    await session.run("total = 0")
    await session.run("total += 10")
    await session.run("total += 32")
    result = await session.run("total")
    assert str(result).strip() == "42"
    await session.close()


@pytest.mark.asyncio
async def test_python_session_get_state():
    session = PythonSession()
    await session.run("x = 1")
    await session.run("name = 'capsule'")
    state = await session.get_state()
    assert "x" in state
    assert "name" in state
    await session.close()


@pytest.mark.asyncio
async def test_python_session_reset_clears_state():
    session = PythonSession()
    await session.run("x = 99")
    await session.reset()
    try:
        await session.run("x")
    except Exception as e:
        assert "is not defined" in str(e)

    await session.close()


@pytest.mark.asyncio
async def test_python_sessions_are_isolated():
    session_a = PythonSession()
    session_b = PythonSession()
    await session_a.run("x = 1")
    await session_b.run("x = 99")
    assert str(await session_a.run("x")).strip() == "1"
    assert str(await session_b.run("x")).strip() == "99"
    await session_a.close()
    await session_b.close()


# ---- JSSession unit tests ----

@pytest.mark.asyncio
async def test_js_session_variable_persistence():
    session = JSSession()
    await session.run("let x = 42")
    result = await session.run("x")
    assert str(result).strip() == "42"
    await session.close()


@pytest.mark.asyncio
async def test_js_session_function_persistence():
    session = JSSession()
    await session.run("function greet(name) { return `Hello ${name}`; }")
    result = await session.run("greet('Alice')")
    assert str(result).strip() == "Hello Alice"
    await session.close()


@pytest.mark.asyncio
async def test_js_session_accumulation():
    session = JSSession()
    await session.run("let total = 0")
    await session.run("total += 10")
    await session.run("total += 32")
    result = await session.run("total")
    assert str(result).strip() == "42"
    await session.close()


@pytest.mark.asyncio
async def test_js_session_get_state():
    session = JSSession()
    await session.run("let x = 1")
    await session.run("let name = 'capsule'")
    state = await session.get_state()
    print("state", state)
    assert "x" in state
    assert "name" in state
    await session.close()


@pytest.mark.asyncio
async def test_js_session_reset_clears_state():
    session = JSSession()
    await session.run("let x = 99")
    await session.reset()
    try:
        await session.run("x")
    except Exception as e:
        assert "ReferenceError" in str(e) or "x" in str(e)

    await session.close()


@pytest.mark.asyncio
async def test_js_sessions_are_isolated():
    session_a = JSSession()
    session_b = JSSession()
    await session_a.run("let x = 1")
    await session_b.run("let x = 99")
    assert str(await session_a.run("x")).strip() == "1"
    assert str(await session_b.run("x")).strip() == "99"
    await session_a.close()
    await session_b.close()


# ---- CapsulePythonREPLTool integration tests ----

@pytest.mark.asyncio
async def test_python_tool_session_persistence():
    tool = CapsulePythonREPLTool()
    await tool._arun("x = 42")
    result = await tool._arun("x")
    assert str(result).strip() == "42"
    await tool.close()


@pytest.mark.asyncio
async def test_python_tool_get_state():
    tool = CapsulePythonREPLTool()
    await tool._arun("x = 1")
    state = await tool.get_state()
    assert "x" in state
    await tool.close()


def test_python_tool_session_sync():
    tool = CapsulePythonREPLTool()
    tool._run("value = 7")
    result = tool._run("value * 6")
    assert str(result).strip() == "42"


def test_python_tool_handle_tool_error_enabled():
    tool = CapsulePythonREPLTool()
    assert tool.handle_tool_error is True
    try:
        tool._run("1 / 0")
    except Exception as e:
        assert "division by zero" in str(e)



# ---- CapsuleJSREPLTool integration tests ----

@pytest.mark.asyncio
async def test_js_tool_session_persistence():
    tool = CapsuleJSREPLTool()
    await tool._arun("let x = 42")
    result = await tool._arun("x")
    assert str(result).strip() == "42"
    await tool.close()


@pytest.mark.asyncio
async def test_js_tool_get_state():
    tool = CapsuleJSREPLTool()
    await tool._arun("let x = 1")
    state = await tool.get_state()
    assert "x" in state
    await tool.close()


def test_js_tool_handle_tool_error_enabled():
    tool = CapsuleJSREPLTool()
    assert tool.handle_tool_error is True
    try:
        tool._run("null.property")
    except Exception as e:
        assert "can't access property \"property\" of null" in str(e)
