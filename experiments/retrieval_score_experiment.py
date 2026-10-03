from analyzer.analyzer import analyze_repository
from analyzer.graph import build_graph
from analyzer.semantic_retriever import (
    load_model,
    retrieve_semantic_candidates,
)

analysis = analyze_repository(".")

graph = build_graph(analysis)

model = load_model()

question = "How does checkout work?"

candidates = retrieve_semantic_candidates(
    question,
    graph,
    model,
)

print("\nTop candidates:")

for candidate in candidates[:5]:
    print(
        f"{candidate.node.id} "
        f"-> {candidate.score:.4f}"
    )