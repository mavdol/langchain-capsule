import ast
from capsule import task

@task(name="executeUntrustedCode", compute="HIGH")
def execute_untrusted_code(code: str):
    tree = ast.parse(code)

    if not tree.body:
        return None

    last_node = tree.body[-1]

    local_env = {}

    if isinstance(last_node, ast.Expr):
        tree.body.pop()
        exec(compile(tree, filename="<ast>", mode="exec"), local_env, local_env)
        result = eval(compile(ast.Expression(last_node.value), filename="<ast>", mode="eval"), local_env, local_env)
    else:
        exec(compile(tree, filename="<ast>", mode="exec"), local_env, local_env)
        result = local_env.get("result")

    return result

@task(name="main", compute="HIGH")
def main(code: str):
    response = execute_untrusted_code(code)
    if isinstance(response, dict) and "result" in response:
        return response["result"]
    return response
