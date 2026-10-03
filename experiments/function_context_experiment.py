import ast

from analyzer.extractor import extract_functions


source = """
def outer():

    def inner():
        pass
"""

tree = ast.parse(source)

functions = extract_functions(
    tree,
    "experiments/function_context_experiment.py"
)

for function in functions:
    print(function)