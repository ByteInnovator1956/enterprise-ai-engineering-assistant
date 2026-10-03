from analyzer.analyzer import analyze_repository
from analyzer.graph import build_graph
from analyzer.semantic_index import (
    build_semantic_index,
)
from analyzer.semantic_retriever import load_model


analysis = analyze_repository(".")

graph = build_graph(analysis)

model = load_model()

index = build_semantic_index(
    graph,
    model,
)

print("\nSemantic Index:")

print(
    f"Documents: {len(index.documents)}"
)

print(
    f"Embeddings: {len(index.embeddings)}"
)

print(
    f"First document: "
    f"{index.documents[0].node_id}"
)

print(
    f"First embedding dimensions: "
    f"{index.embeddings[0].shape}"
)

