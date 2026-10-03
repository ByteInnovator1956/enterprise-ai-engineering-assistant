import ast

from analyzer.parser import parse_file


file_path = "app/orders/checkout.py"

tree = parse_file(file_path)

print(type(tree))
print(isinstance(tree, ast.Module))