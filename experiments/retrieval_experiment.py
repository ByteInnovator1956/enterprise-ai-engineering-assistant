from analyzer.semantic import build_semantic_document
from sentence_transformers import SentenceTransformer
from analyzer.analyzer import analyze_repository
from analyzer.graph import build_graph
from analyzer.retriever import (
    retrieve_candidates,
)
BENCHMARK = [
    {
        "question": "How does checkout work?",
        "expected": "app.orders.checkout.checkout",
    },
    {
        "question": "Where is the discount calculated?",
        "expected": "app.discounts.discount.calculate_discount",
    },
    {
        "question": "How is payment validated?",
        "expected": "app.payments.payment.validate_payment",
    },
    {
        "question": "Which function creates an order?",
        "expected": "app.orders.order.create_order",
    },
    {
        "question": "How does login create a session?",
        "expected": "app.auth.login.login",
    },
    {
        "question": "Where is the price reduction for premium users implemented?",
        "expected": "app.discounts.discount.calculate_discount",
    },
    {
        "question": "What happens after the discount is calculated?",
        "expected": "app.payments.payment.process_payment",
    },
    {
        "question": "Which class manages user sessions?",
        "expected": "app.auth.session.SessionManager",
    },
]

analysis = analyze_repository(".")
graph = build_graph(analysis)

def evaluate_retrieval(benchmark, graph):
    results = []

    recall_at_1 = 0
    recall_at_3 = 0
    recall_at_5 = 0
    reciprocal_rank_total = 0

    for case in benchmark:
        question = case["question"]
        expected = case["expected"]

        candidates = retrieve_candidates(
            question,
            graph,
        )

        candidate_ids = [
            candidate.id
            for candidate in candidates
        ]

        rank = None

        for index, candidate_id in enumerate(
            candidate_ids,
            start=1,
        ):
            if candidate_id == expected:
                rank = index
                break

        if rank is not None:
            reciprocal_rank_total += 1 / rank

            if rank <= 1:
                recall_at_1 += 1

            if rank <= 3:
                recall_at_3 += 1

            if rank <= 5:
                recall_at_5 += 1

        results.append(
            {
                "question": question,
                "expected": expected,
                "ranked_candidates": candidate_ids,
                "rank": rank,
            }
        )

    total_questions = len(benchmark)

    metrics = {
        "recall_at_1": recall_at_1 / total_questions,
        "recall_at_3": recall_at_3 / total_questions,
        "recall_at_5": recall_at_5 / total_questions,
        "mrr": reciprocal_rank_total / total_questions,
    }

    return results, metrics

results, metrics = evaluate_retrieval(
    BENCHMARK,
    graph,
)

print(results)
print(metrics)

model = SentenceTransformer(
    "jinaai/jina-code-embeddings-0.5b"
)

query = (
    "Where is the price reduction for premium users implemented?"
)

document = build_semantic_document(
    graph.nodes[
        "app.discounts.discount.calculate_discount"
    ]
)

query_embedding = model.encode(
    query,
    prompt_name="nl2code_query",
    normalize_embeddings=True,
)

document_embedding = model.encode(
    document.text,
    prompt_name="nl2code_document",
    normalize_embeddings=True,
)

similarity = model.similarity(
    query_embedding,
    document_embedding,
)

print("Semantic similarity:", similarity.item())

candidate_ids = [
    "app.discounts.discount.calculate_discount",
    "app.orders.checkout.checkout",
    "app.payments.payment.process_payment",
    "app.payments.payment.validate_payment",
    "app.orders.order.create_order",
    "app.auth.session.SessionManager",
]

query_embedding = model.encode(
    query,
    prompt_name="nl2code_query",
    normalize_embeddings=True,
)

semantic_results = []

for candidate_id in candidate_ids:
    candidate = build_semantic_document(
        graph.nodes[candidate_id]
    )

    candidate_embedding = model.encode(
        candidate.text,
        prompt_name="nl2code_document",
        normalize_embeddings=True,
    )

    similarity = model.similarity(
        query_embedding,
        candidate_embedding,
    ).item()

    semantic_results.append(
        (similarity, candidate_id)
    )

semantic_results.sort(
    key=lambda item: item[0],
    reverse=True,
)

print("\nSemantic ranking:")

for similarity, candidate_id in semantic_results:
    print(
        f"{similarity:.4f} -> {candidate_id}"
    )

def evaluate_semantic_retrieval(benchmark, graph, model):
    semantic_documents = []
    document_embeddings = []

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

    results = []

    recall_at_1 = 0
    recall_at_3 = 0
    recall_at_5 = 0
    reciprocal_rank_total = 0

    for case in benchmark:
        question = case["question"]
        expected = case["expected"]

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

        ranked_candidates = [
            semantic_documents[index].node_id
            for index in ranked_indices
        ]

        rank = None

        for index, candidate_id in enumerate(
            ranked_candidates,
            start=1,
        ):
            if candidate_id == expected:
                rank = index
                break

        if rank is not None:
            reciprocal_rank_total += 1 / rank

            if rank <= 1:
                recall_at_1 += 1

            if rank <= 3:
                recall_at_3 += 1

            if rank <= 5:
                recall_at_5 += 1

        results.append(
            {
                "question": question,
                "expected": expected,
                "ranked_candidates": ranked_candidates,
                "rank": rank,
            }
        )

    total_questions = len(benchmark)

    metrics = {
        "recall_at_1": recall_at_1 / total_questions,
        "recall_at_3": recall_at_3 / total_questions,
        "recall_at_5": recall_at_5 / total_questions,
        "mrr": reciprocal_rank_total / total_questions,
    }

    return results, metrics

semantic_results, semantic_metrics = (
    evaluate_semantic_retrieval(
        BENCHMARK,
        graph,
        model,
    )
)

print("\nSemantic benchmark results:")

for result in semantic_results:
    print(result)

print("\nSemantic metrics:")
print(semantic_metrics)