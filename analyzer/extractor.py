import ast
from pathlib import Path

from analyzer.models import (
    Function,
    Class,
    Method,
    Import,
    Relationship,
)


def extract_classes(tree, file_path):
    classes = []
    methods = []

    for node in ast.walk(tree):

        if isinstance(node, ast.ClassDef):

            module_name = (
                Path(file_path)
                .with_suffix("")
                .as_posix()
                .replace("/", ".")
                .replace("\\", ".")
            )

            class_info = Class(
                name=node.name,
                qualified_name=f"{module_name}.{node.name}",
                file=file_path,
                line=node.lineno,
                end_line=node.end_lineno,
            )

            classes.append(class_info)

            for child in node.body:

                if isinstance(child, ast.FunctionDef):

                    method = Method(
                        name=child.name,
                        class_name=node.name,
                        class_qualified_name=(
                            f"{module_name}.{node.name}"
                        ),
                        qualified_name=(
                            f"{module_name}.{node.name}.{child.name}"
                        ),
                        file=file_path,
                        line=child.lineno,
                        end_line=child.end_lineno,

                    )

                    methods.append(method)

    return classes, methods


def extract_imports(tree, file_path):
    imports = []

    for node in ast.walk(tree):

        if isinstance(node, ast.ImportFrom):

            for imported in node.names:

                import_info = Import(
                    module=node.module,
                    name=imported.name,
                    file=file_path,
                    line=node.lineno,
                )

                imports.append(import_info)

    return imports


def extract_functions(tree, file_path):
    functions = []

    module_name = (
        Path(file_path)
        .with_suffix("")
        .as_posix()
        .replace("/", ".")
        .replace("\\", ".")
    )

    def visit(node, inside_class=False):

        if isinstance(node, ast.ClassDef):
            inside_class = True

        if isinstance(node, ast.FunctionDef):

            if not inside_class:

                function = Function(
                    name=node.name,
                    qualified_name=f"{module_name}.{node.name}",
                    file=file_path,
                    line=node.lineno,
                    end_line=node.end_lineno,
                )

                functions.append(function)

        for child in ast.iter_child_nodes(node):
            visit(child, inside_class)

    visit(tree)

    return functions


def build_symbol_table(analysis):
    symbols = {}

    for file in analysis.files:

        for function in file.functions:
            symbols[function.qualified_name] = "function"

        for class_info in file.classes:
            symbols[class_info.qualified_name] = "class"

        for method in file.methods:
            symbols[method.qualified_name] = "method"

    return symbols


def build_local_symbol_map(analyzed_file):
    symbols = {}

    # Imported symbols
    for import_info in analyzed_file.imports:

        qualified_name = (
            f"{import_info.module}.{import_info.name}"
        )

        symbols[import_info.name] = qualified_name

    # Functions defined in this file
    for function in analyzed_file.functions:
        symbols[function.name] = function.qualified_name

    # Classes defined in this file
    for class_info in analyzed_file.classes:
        symbols[class_info.name] = class_info.qualified_name

    return symbols


def extract_variable_bindings(tree, symbols, local_symbols):
    bindings = {}

    for node in ast.walk(tree):

        if not isinstance(node, ast.Assign):
            continue

        if len(node.targets) != 1:
            continue

        target = node.targets[0]
        value = node.value

        if not isinstance(target, ast.Name):
            continue

        if not isinstance(value, ast.Call):
            continue

        if not isinstance(value.func, ast.Name):
            continue

        local_name = value.func.id

        qualified_name = local_symbols.get(local_name)

        if qualified_name is None:
            continue

        if symbols.get(qualified_name) == "class":

            bindings[target.id] = qualified_name

    return bindings


def extract_calls(tree, file_path, symbols, local_symbols):
    relationships = []

    module_name = (
        Path(file_path)
        .with_suffix("")
        .as_posix()
        .replace("/", ".")
        .replace("\\", ".")
    )

    bindings = extract_variable_bindings(
        tree,
        symbols,
        local_symbols,
    )

    for function in ast.walk(tree):

        if not isinstance(function, ast.FunctionDef):
            continue

        if function.name.startswith("test_"):
            continue

        function_qualified_name = f"{module_name}.{function.name}"

        for node in ast.walk(function):

            if not isinstance(node, ast.Call):
                continue

            # -------------------------------------------------
            # Direct function/class call
            # Example:
            # calculate_discount(...)
            # SessionManager()
            # -------------------------------------------------

            if isinstance(node.func, ast.Name):

                local_name = node.func.id

                qualified_name = local_symbols.get(local_name)

                if qualified_name is not None:

                    symbol_type = symbols.get(qualified_name)
                    target = qualified_name

                else:

                    symbol_type = None
                    target = local_name

                if symbol_type == "class":

                    relationship_type = "instantiates"

                elif symbol_type == "function":

                    relationship_type = "calls"

                else:

                    relationship_type = "unknown"

                relationships.append(
                    Relationship(
                        source=function_qualified_name,
                        type=relationship_type,
                        target=target,
                        file=file_path,
                        line=node.lineno,
                    )
                )

            # -------------------------------------------------
            # Method call
            # Example:
            # session_manager.create_session(...)
            # -------------------------------------------------

            elif isinstance(node.func, ast.Attribute):

                if isinstance(node.func.value, ast.Name):

                    object_name = node.func.value.id
                    method_name = node.func.attr

                    class_qualified_name = bindings.get(
                        object_name
                    )

                    if class_qualified_name is not None:

                        target = (
                            f"{class_qualified_name}.{method_name}"
                        )

                        relationship_type = "calls"

                    else:

                        target = method_name
                        relationship_type = "unknown"

                else:

                    target = node.func.attr
                    relationship_type = "unknown"

                relationships.append(
                    Relationship(
                        source=function_qualified_name,
                        type=relationship_type,
                        target=target,
                        file=file_path,
                        line=node.lineno,
                    )
                )

    return relationships


def extract_test_relationships(
    tree,
    file_path,
    symbols,
    local_symbols,
):
    relationships = []

    module_name = (
        Path(file_path)
        .with_suffix("")
        .as_posix()
        .replace("/", ".")
        .replace("\\", ".")
    )

    for function in ast.walk(tree):

        if not isinstance(function, ast.FunctionDef):
            continue

        if not function.name.startswith("test_"):
            continue

        function_qualified_name = (
            f"{module_name}.{function.name}"
        )

        for node in ast.walk(function):

            if not isinstance(node, ast.Call):
                continue

            if not isinstance(node.func, ast.Name):
                continue

            local_name = node.func.id
            qualified_name = local_symbols.get(local_name)

            if qualified_name is None:
                continue

            if qualified_name not in symbols:
                continue

            relationships.append(
                Relationship(
                    source=function_qualified_name,
                    type="tests",
                    target=qualified_name,
                    file=file_path,
                    line=node.lineno,
                )
            )

    return relationships