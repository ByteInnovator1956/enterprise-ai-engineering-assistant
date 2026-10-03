from sentence_transformers import SentenceTransformer
from analyzer.models import RetrievedCandidate


MODEL_NAME = "jinaai/jina-code-embeddings-0.5b"


def load_model():
    return SentenceTransformer(MODEL_NAME)


def retrieve_semantic_candidates(
    question,
    graph,
    model,
    index,
):
    if not index.documents:
        return []

    query_embedding = model.encode(
        question,
        prompt_name="nl2code_query",
        normalize_embeddings=True,
    )

    similarities = model.similarity(
        query_embedding,
        index.embeddings,
    )[0]

    ranked_indices = sorted(
        range(len(index.documents)),
        key=lambda index: similarities[index].item(),
        reverse=True,
    )

    return [
    RetrievedCandidate(
        node=graph.nodes[
            index.documents[document_index].node_id
        ],
        score=similarities[document_index].item(),
    )
    for document_index in ranked_indices
]