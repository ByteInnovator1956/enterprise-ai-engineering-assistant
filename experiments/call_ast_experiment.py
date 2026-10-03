import ast


source = """
def example():

    foo()

    SessionManager()

    session_manager.create_session()
"""


tree = ast.parse(source)


for node in ast.walk(tree):

    if isinstance(node, ast.Call):

        print("CALL")
        print("Node:", ast.dump(node, indent=4))
        print("-" * 50)