import ast


source = """
def login(user):

    session_manager = SessionManager()

    other = SomethingElse()
"""


tree = ast.parse(source)


symbols = {
    "SessionManager": "class",
}


for node in ast.walk(tree):

    if isinstance(node, ast.Assign):

        target = node.targets[0]
        value = node.value

        if isinstance(target, ast.Name):

            if isinstance(value, ast.Call):

                if isinstance(value.func, ast.Name):

                    variable = target.id
                    created_from = value.func.id

                    symbol_type = symbols.get(created_from)

                    if symbol_type == "class":

                        print(
                            variable,
                            "→ instance of →",
                            created_from
                        )

                    else:

                        print(
                            variable,
                            "→ unknown type"
                        )