import sys
import time
from analyzer.sufficiency import (
    inspect_evidence_sufficiency,
)
from analyzer.analyzer import analyze_repository
from analyzer.graph import build_graph
from analyzer.assembly import assemble_evidence
from analyzer.models import AssemblyContext
from analyzer.reasoner import OllamaReasoner
from analyzer.semantic_retriever import (
    load_model,
    retrieve_semantic_candidates,
)
from analyzer.semantic_index import (
    build_semantic_index,
    save_semantic_index,
    load_semantic_index,
)

start = time.perf_counter()

analysis = analyze_repository(".")

print(
    f"\nRepository analysis: "
    f"{time.perf_counter() - start:.3f}s"
)

graph = build_graph(analysis)

question = sys.argv[1]

start = time.perf_counter()

model = load_model()

print(
    f"Model loading: "
    f"{time.perf_counter() - start:.3f}s"
)

index_path = "semantic_index.json"

try:
    start = time.perf_counter()

    index = load_semantic_index(index_path)

    print(
        f"Index loading: "
        f"{time.perf_counter() - start:.3f}s"
    )

    print("\nLoaded existing semantic index.")

except FileNotFoundError:
    print("\nBuilding semantic index...")

    index = build_semantic_index(
        graph,
        model,
    )

    save_semantic_index(
        index,
        index_path,
    )

    print("Semantic index saved.")


start = time.perf_counter()

candidates = retrieve_semantic_candidates(
    question,
    graph,
    model,
    index,
)

print(
    f"Semantic retrieval: "
    f"{time.perf_counter() - start:.3f}s"
)

context = AssemblyContext(
    candidate_nodes=[
        candidate.node
        for candidate in candidates[:3]
    ],
    graph=graph,
    repository_path=".",
)

start = time.perf_counter()

evidence_bundle = assemble_evidence(
    context,
    expansion_depth=2,
)

print(
    f"Evidence assembly: "
    f"{time.perf_counter() - start:.3f}s"
)

sufficiency = inspect_evidence_sufficiency(
    candidates[:3],
    evidence_bundle,
)

print("\nEvidence inspection:")
print(sufficiency)

reasoner = OllamaReasoner()

start = time.perf_counter()

answer = reasoner.reason(
    question,
    evidence_bundle,
)

print(
    f"LLM reasoning: "
    f"{time.perf_counter() - start:.3f}s"
)

print("\nAnswer:")
print(answer)