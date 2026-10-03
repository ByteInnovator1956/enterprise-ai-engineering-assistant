from pathlib import Path

from analyzer.parser import parse_file
from analyzer.extractor import (
    extract_functions,
    extract_classes,
    extract_imports,
    extract_calls,
    build_symbol_table,
    build_local_symbol_map,
    extract_test_relationships,
)
from analyzer.models import AnalyzedFile, RepositoryAnalysis


def discover_python_files(repository_path, include_paths):
    repository = Path(repository_path)

    files = []

    for include_path in include_paths:
        directory = repository / include_path

        files.extend(directory.rglob("*.py"))

    return files


def analyze_repository(repository_path):
    files = discover_python_files(
        repository_path,
        ["app", "tests"]
    )

    analyzed_files = []

    # Phase 1: discover repository structure
    for file_path in files:
        tree = parse_file(file_path)

        functions = extract_functions(
            tree,
            str(file_path)
        )

        classes, methods = extract_classes(
            tree,
            str(file_path)
        )

        imports = extract_imports(
            tree,
            str(file_path)
        )

        analyzed_file = AnalyzedFile(
            path=str(file_path),
            functions=functions,
            classes=classes,
            methods=methods,
            imports=imports,
        )

        analyzed_files.append(analyzed_file)

    # Build complete symbol table
    analysis = RepositoryAnalysis(
        files=analyzed_files,
        relationships=[],
    )

    symbols = build_symbol_table(analysis)

    # Phase 2: discover relationships
    relationships = []

    for file_path in files:
        tree = parse_file(file_path)

        local_symbols = {}

        for analyzed_file in analyzed_files:

            if analyzed_file.path == str(file_path):
                local_symbols = build_local_symbol_map(
                    analyzed_file
                )
                break


        file_relationships = extract_calls(
            tree,
            str(file_path),
            symbols,
            local_symbols,
        )

        relationships.extend(file_relationships)

        test_relationships = extract_test_relationships(
            tree,
            str(file_path),
            symbols,
            local_symbols,
        )

        relationships.extend(test_relationships)

    return RepositoryAnalysis(
        files=analyzed_files,
        relationships=relationships,
    )


