from pathlib import Path

from analyzer.models import (
    GraphNode,
    RepositoryGraph,
    Relationship,
)


def build_graph(analysis):
    nodes = {}
    relationships = []

    for analyzed_file in analysis.files:

        file_id = analyzed_file.path

        nodes[file_id] = GraphNode(
            id=file_id,
            type="file",
            name=Path(file_id).name,
            file=file_id,
            line=None,
            end_line=None,
        )

        for class_info in analyzed_file.classes:

            nodes[class_info.qualified_name] = GraphNode(
                id=class_info.qualified_name,
                type="class",
                name=class_info.name,
                file=class_info.file,
                line=class_info.line,
                end_line=class_info.end_line,
            )

            relationships.append(
                Relationship(
                    source=file_id,
                    type="contains",
                    target=class_info.qualified_name,
                    file=class_info.file,
                    line=class_info.line,
                )
            )

        for method in analyzed_file.methods:

            nodes[method.qualified_name] = GraphNode(
                id=method.qualified_name,
                type="method",
                name=method.name,
                file=method.file,
                line=method.line,
                end_line=method.end_line,
            )

            relationships.append(
                Relationship(
                    source=method.class_qualified_name,
                    type="contains",
                    target=method.qualified_name,
                    file=method.file,
                    line=method.line,
                )
            )

        for function in analyzed_file.functions:

            nodes[function.qualified_name] = GraphNode(
                id=function.qualified_name,
                type="function",
                name=function.name,
                file=function.file,
                line=function.line,
                end_line=function.end_line,
            )

            relationships.append(
                Relationship(
                    source=file_id,
                    type="contains",
                    target=function.qualified_name,
                    file=function.file,
                    line=function.line,
                )
            )

    # Add behavioral relationships discovered by the analyzer
    for relationship in analysis.relationships:
        relationships.append(relationship)

    return RepositoryGraph(
        nodes=nodes,
        relationships=relationships
    )
    
def get_direct_dependencies(graph, node_id):
    dependencies = set()

    for relationship in graph.relationships:

        if relationship.source != node_id:
            continue

        if relationship.type not in {"calls", "instantiates"}:
            continue

        dependencies.add(relationship.target)

    return dependencies

def get_transitive_dependencies(graph, node_id):
    dependencies = set()
    visited = set()

    def visit(current_node):
        if current_node in visited:
            return

        visited.add(current_node)

        direct_dependencies = get_direct_dependencies(
            graph,
            current_node
        )

        for dependency in direct_dependencies:
            dependencies.add(dependency)
            visit(dependency)

    visit(node_id)

    return dependencies

def get_direct_dependents(graph, node_id):
    dependents = set()

    for relationship in graph.relationships:

        if relationship.target != node_id:
            continue

        if relationship.type not in {"calls", "instantiates"}:
            continue

        dependents.add(relationship.source)

    return dependents


def get_transitive_dependents(graph, node_id):
    dependents = set()
    visited = set()

    def visit(current_node):
        if current_node in visited:
            return

        visited.add(current_node)

        direct_dependents = get_direct_dependents(
            graph,
            current_node
        )

        for dependent in direct_dependents:
            dependents.add(dependent)
            visit(dependent)

    visit(node_id)

    return dependents


if __name__ == "__main__":
    from analyzer.analyzer import analyze_repository

    analysis = analyze_repository(".")
    graph = build_graph(analysis)

    dependents = get_direct_dependents(
        graph,
        "app.orders.checkout.checkout"
    )

    print("\nDIRECT DEPENDENTS OF CHECKOUT:")

    for dependent in dependents:
        print(dependent)

    transitive_dependents = get_transitive_dependents(
    graph,
    "app.orders.checkout.checkout"
    )

    print("\nTRANSITIVE DEPENDENTS OF CHECKOUT:")

    for dependent in transitive_dependents:
        print(dependent)

def get_dependencies_within_depth(graph, node_id, depth):
    dependencies = set()
    visited = set()

    def visit(current_node, current_depth):
        if current_node in visited:
            return

        visited.add(current_node)

        if current_depth >= depth:
            return

        direct_dependencies = get_direct_dependencies(
            graph,
            current_node,
        )

        for dependency in direct_dependencies:
            dependencies.add(dependency)
            visit(dependency, current_depth + 1)

    visit(node_id, 0)

    return dependencies


