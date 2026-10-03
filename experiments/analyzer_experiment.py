import ast

from analyzer.extractor import extract_classes
from analyzer.extractor import extract_imports
from analyzer.extractor import extract_calls
file_path = "app/orders/checkout.py"

with open(file_path, "r") as file:
    source = file.read()

tree = ast.parse(source)

classes, methods = extract_classes(tree, file_path)
imports = extract_imports(tree, file_path)
relationships = extract_calls(tree, file_path)
print("Relationships:")

for relationship in relationships:
    print(relationship)


for import_info in imports:
    print(import_info)

print("Classes:")

for class_info in classes:
    print(class_info)

print("Methods:")

for method in methods:
    print(method)