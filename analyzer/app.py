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
from analyzer.sufficiency import (
    inspect_evidence_sufficiency,
)

def answer_question(question, repository_path="."):
    analysis = analyze_repository(repository_path)
    graph = build_graph(analysis)

    model = load_model()
    index_path = "semantic_index.json"

    try:
        index = load_semantic_index(index_path)
    except FileNotFoundError:
        index = build_semantic_index(
            graph,
            model,
        )

        save_semantic_index(
            index,
            index_path,
        )
    candidates = retrieve_semantic_candidates(
        question,
        graph,
        model,
        index,
    )
    context = AssemblyContext(
        candidate_nodes=[
            candidate.node
            for candidate in candidates[:3]
        ],
        graph=graph,
        repository_path=repository_path,
    )
    evidence_bundle = assemble_evidence(
        context,
        expansion_depth=2,
    )
    sufficiency = inspect_evidence_sufficiency(
        candidates[:3],
        evidence_bundle,
    )
    reasoner = OllamaReasoner()
    answer = reasoner.reason(
        question,
        evidence_bundle,
    )
    return {
    "answer": answer,
    "sufficiency": sufficiency,
    "evidence": evidence_bundle,
    }
