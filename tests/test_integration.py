import pytest
from langchain_capsule import CapsulePythonTool, CapsuleJSTool


# ---- Python : Basic tests ----
@pytest.mark.asyncio
async def test_python_basic_async():
    result = await CapsulePythonTool().arun("1 + 1")
    assert str(result).strip() == "2"

def test_python_basic_sync():
    result = CapsulePythonTool().run("2 + 2")
    assert str(result).strip() == "4"


# ---- Python : Multi-line & variables test ----
@pytest.mark.asyncio
async def test_python_multiline():
    code = """
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)

factorial(6)
"""
    result = await CapsulePythonTool().arun(code)
    assert str(result).strip() == "720"

@pytest.mark.asyncio
async def test_python_variables():
    code = """
x = 10
y = 32
x + y
"""
    result = await CapsulePythonTool().arun(code)
    assert str(result).strip() == "42"

@pytest.mark.asyncio
async def test_python_list_comprehension():
    code = "[i ** 2 for i in range(5)]"
    result = await CapsulePythonTool().arun(code)
    assert str(result).strip() == "[0, 1, 4, 9, 16]"

@pytest.mark.asyncio
async def test_python_stdlib():
    code = """
import json
data = {"hello": "world", "number": 42}
json.dumps(data)
"""
    result = await CapsulePythonTool().arun(code)
    print("result", result)
    assert '"hello"' in result
    assert '"world"' in result

@pytest.mark.asyncio
async def test_python_print_output():
    code = """
print("Hello")
print("World")
print("Test")
42
"""
    result = await CapsulePythonTool().arun(code)
    assert "Hello" in result
    assert "World" in result
    assert "Test" in result
    assert "42" in result


# ---- Python : Errors test ----
@pytest.mark.asyncio
async def test_python_syntax_error():
    try:
        await CapsulePythonTool().arun("def broken(")
    except Exception as e:
        assert "was never closed" in str(e)

@pytest.mark.asyncio
async def test_python_runtime_error():
    try:
        await CapsulePythonTool().arun("1 / 0")
    except Exception as e:
        assert "division by zero" in str(e)

@pytest.mark.asyncio
async def test_python_name_error():
    try:
        await CapsulePythonTool().arun("undefined_variable")
    except Exception as e:
        assert "undefined_variable" in str(e)


# ---- Python : handle_tool_error test ----
def test_python_handle_tool_error_enabled():
    tool = CapsulePythonTool()
    assert tool.handle_tool_error is True
    try:
        result = tool.run("1 / 0")
        assert isinstance(result, str)
        assert len(result) > 0
    except Exception as e:
        assert "division by zero" in str(e)


# ---- JavaScript : Basic tests ----
@pytest.mark.asyncio
async def test_js_basic_async():
    result = await CapsuleJSTool().arun("1 + 2")
    assert str(result).strip() == "3"

def test_js_basic_sync():
    result = CapsuleJSTool().run("3 + 3")
    assert str(result).strip() == "6"


# ---- JavaScript : Multi-line & variables test ----
@pytest.mark.asyncio
async def test_js_multiline():
    code = """
function factorial(n) {
    if (n <= 1) return 1;
    return n * factorial(n - 1);
}
factorial(6)
"""
    result = await CapsuleJSTool().arun(code)
    print("result", result)
    assert str(result).strip() == "720"

@pytest.mark.asyncio
async def test_js_variables():
    code = """
const x = 10;
const y = 32;
x + y
"""
    result = await CapsuleJSTool().arun(code)
    assert str(result).strip() == "42"

@pytest.mark.asyncio
async def test_js_array_operations():
    code = "[1, 2, 3, 4, 5].map(x => x ** 2)"
    result = await CapsuleJSTool().arun(code)
    assert str(result).strip() == "[1, 4, 9, 16, 25]"

@pytest.mark.asyncio
async def test_js_object():
    code = """
const data = { hello: "world", number: 42 };
JSON.stringify(data)
"""
    result = await CapsuleJSTool().arun(code)
    assert "hello" in result
    assert "world" in result

@pytest.mark.asyncio
async def test_js_console_output():
    code = """
console.log("Hello");
console.log("World");
console.log("Test");
42
"""
    result = await CapsuleJSTool().arun(code)
    assert "Hello" in result
    assert "World" in result
    assert "Test" in result
    assert "42" in result


# ---- JavaScript : Errors test ----
@pytest.mark.asyncio
async def test_js_syntax_error():
    result = await CapsuleJSTool().arun("function broken(")
    assert "missing formal parameter" in result

@pytest.mark.asyncio
async def test_js_runtime_error():
    result = await CapsuleJSTool().arun("null.property")
    assert "null" in result

@pytest.mark.asyncio
async def test_js_reference_error():
    try:
        await CapsuleJSTool().arun("undefinedVariable")
    except Exception as e:
        assert "undefinedVariable" in str(e)


# ---- JavaScript : handle_tool_error test ----
def test_js_handle_tool_error_enabled():
    tool = CapsuleJSTool()
    assert tool.handle_tool_error is True
    result = tool.run("null.property")
    assert isinstance(result, str)
    assert len(result) > 0
