from analyzer.analyzer import analyze_repository
from analyzer.graph import build_graph
from analyzer.semantic_retriever import (
    load_model,
    retrieve_semantic_candidates,
)


KNOWN_QUESTIONS = [
    "How does checkout work?",
    "Where is the discount calculated?",
    "How is payment validated?",
    "Which function creates an order?",
    "How does login create a session?",
    "Where is the price reduction for premium users implemented?",
    "What happens after the discount is calculated?",
    "Which class manages user sessions?",
]


UNKNOWN_QUESTIONS = [
    "Where is the email notification service implemented?",
    "How do I send an email to a customer?",
]


analysis = analyze_repository(".")
graph = build_graph(analysis)

model = load_model()

def get_retrieval_scores(question, graph, model):
    semantic_documents = []
    document_embeddings = []

    from analyzer.semantic import build_semantic_document

    for node in graph.nodes.values():
        document = build_semantic_document(node)

        if document is None:
            continue

        embedding = model.encode(
            document.text,
            prompt_name="nl2code_document",
            normalize_embeddings=True,
        )

        semantic_documents.append(document)
        document_embeddings.append(embedding)

    query_embedding = model.encode(
        question,
        prompt_name="nl2code_query",
        normalize_embeddings=True,
    )

    similarities = model.similarity(
        query_embedding,
        document_embeddings,
    )[0]

    ranked_indices = sorted(
        range(len(semantic_documents)),
        key=lambda index: similarities[index].item(),
        reverse=True,
    )

    return [
        (
            semantic_documents[index].node_id,
            similarities[index].item(),
        )
        for index in ranked_indices
    ]

print("\n=== KNOWN QUESTIONS ===")

for question in KNOWN_QUESTIONS:
    results = get_retrieval_scores(
        question,
        graph,
        model,
    )

    top_candidate, top_score = results[0]

    print(f"\nQuestion: {question}")
    print(f"Top candidate: {top_candidate}")
    print(f"Top score: {top_score:.4f}")


print("\n=== UNKNOWN QUESTIONS ===")

for question in UNKNOWN_QUESTIONS:
    results = get_retrieval_scores(
        question,
        graph,
        model,
    )

    top_candidate, top_score = results[0]

    print(f"\nQuestion: {question}")
    print(f"Top candidate: {top_candidate}")
    print(f"Top score: {top_score:.4f}")