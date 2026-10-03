import ast


source = """
def login(user):

    session_manager = SessionManager()

    session_manager.create_session(user)
"""


tree = ast.parse(source)


for node in ast.walk(tree):

    if isinstance(node, ast.Call):

        print("CALL")

        if isinstance(node.func, ast.Attribute):

            print("Object:", node.func.value.id)
            print("Method:", node.func.attr)

        print("-" * 50)