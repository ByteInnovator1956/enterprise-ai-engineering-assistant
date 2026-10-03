from analyzer.evidence import (
    build_source_evidence,
    build_evidence_bundle,
    build_relationship_evidence,

)
from analyzer.graph import get_dependencies_within_depth

from analyzer.models import (
    AssemblyContext,
    EvidenceBundle,
    EvidenceItem,
    
)

def _build_source_evidence_for_node(node):
    if (
        node.file is None
        or node.line is None
        or node.end_line is None
    ):
        return None

    return build_source_evidence(
        file_path=node.file,
        symbol=node.id,
        start_line=node.line,
        end_line=node.end_line,
    )

def assemble_evidence(context, expansion_depth=2):
    items = []
    included_node_ids = set()

    for node in context.candidate_nodes:

        evidence = _build_source_evidence_for_node(node)

        if evidence is not None:
            items.append(evidence)
            included_node_ids.add(node.id)

        dependency_ids = get_dependencies_within_depth(
            context.graph,
            node.id,
            expansion_depth,
        )

        for dependency_id in dependency_ids:

            dependency_node = context.graph.nodes.get(
                dependency_id
            )

            if dependency_node is None:
                continue

            if dependency_id in included_node_ids:
                continue

            dependency_evidence = (
                _build_source_evidence_for_node(
                    dependency_node
                )
            )

            if dependency_evidence is not None:
                items.append(dependency_evidence)
                included_node_ids.add(dependency_node.id)

    relationship_items = _build_relationship_evidence_for_nodes(
        context.graph,
        included_node_ids,
    )

    items.extend(relationship_items)

    return build_evidence_bundle(items)

def _build_relationship_evidence_for_nodes(
    graph,
    node_ids,
):
    items = []

    for relationship in graph.relationships:
        if (
            relationship.source in node_ids
            and relationship.target in node_ids
            and relationship.type in {"calls", "instantiates"}
        ):
            items.append(
                build_relationship_evidence(
                    relationship
                )
            )

    return items