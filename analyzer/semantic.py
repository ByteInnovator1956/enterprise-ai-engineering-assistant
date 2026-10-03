from analyzer.models import GraphNode, SemanticDocument
from analyzer.evidence import build_source_evidence


def build_semantic_document(node):
    if (
        node.file is None
        or node.line is None
        or node.end_line is None
    ):
        return None

    source_evidence = build_source_evidence(
        file_path=node.file,
        symbol=node.id,
        start_line=node.line,
        end_line=node.end_line,
    )

    text = (
        f"Entity type: {node.type}\n"
        f"Name: {node.name}\n"
        f"Qualified name: {node.id}\n"
        f"File: {node.file.replace(chr(92), '/')}\n"
        f"\n"
        f"Source:\n"
        f"{source_evidence.content}"
    )

    return SemanticDocument(
        node_id=node.id,
        text=text,
    )