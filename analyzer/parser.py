import ast


def parse_file(file_path):
    with open(file_path, "r") as file:
        source = file.read()

    return ast.parse(source)