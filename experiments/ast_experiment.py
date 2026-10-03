import ast

with open("app/orders/checkout.py", "r") as file:
    source = file.read()

tree = ast.parse(source)

for node in ast.walk(tree):

    if isinstance(node, ast.FunctionDef):
        print("Function:", node.name)
        print("  Starts at line:", node.lineno)

    elif isinstance(node, ast.Call):
        if isinstance(node.func, ast.Name):
            print("Call:", node.func.id)
            print("  Starts at line:", node.lineno)