from analyzer.analyzer import analyze_repository
from analyzer.graph import build_graph
from analyzer.semantic_index import (
    build_semantic_index,
    save_semantic_index,
    load_semantic_index,
)
from analyzer.semantic_retriever import load_model


analysis = analyze_repository(".")

graph = build_graph(analysis)

model = load_model()

index = build_semantic_index(
    graph,
    model,
)

save_semantic_index(
    index,
    "semantic_index.json",
)

loaded_index = load_semantic_index(
    "semantic_index.json",
)

print("\nOriginal index:")
print(f"Documents: {len(index.documents)}")
print(f"Embeddings: {len(index.embeddings)}")

print("\nLoaded index:")
print(f"Documents: {len(loaded_index.documents)}")
print(f"Embeddings: {len(loaded_index.embeddings)}")

print("\nFirst document:")
print(loaded_index.documents[0].node_id)

print("\nEmbedding shape:")
print(loaded_index.embeddings[0].shape)