def _build_search_text(node):
    parts = [
        node.name,
        node.id,
        node.file,
    ]

    return " ".join(
        part for part in parts
        if part is not None
    )


def _normalize_text(text):
    return text.lower().replace("_", " ").replace(".", " ").replace("/", " ").split()

STOPWORDS = {
    "a",
    "an",
    "the",
    "is",
    "are",
    "was",
    "were",
    "how",
    "what",
    "where",
    "which",
    "does",
    "do",
    "and",
    "or",
    "to",
    "of",
    "in",
    "for",
}

def _score_candidate(question_tokens, node):
    name_tokens = set(
        _normalize_text(node.name)
    )

    path_tokens = set(
        _normalize_text(
            f"{node.id} {node.file}"
        )
    )

    question_tokens = set(question_tokens)

    symbol_matches = (
        question_tokens & name_tokens
    )

    path_matches = (
        question_tokens & path_tokens
    )

    score = (
        2 * len(symbol_matches)
        + len(path_matches)
    )

    return score

def retrieve_candidates(question, graph):
    question_tokens = _normalize_text(question)

    scored_candidates = []

    for node in graph.nodes.values():
        score = _score_candidate(
            question_tokens,
            node,
        )

        if score == 0:
            continue

        scored_candidates.append(
            (score, node)
        )

    scored_candidates.sort(
        key=lambda item: (-item[0], item[1].id)
    )

    return [
        node
        for _, node in scored_candidates
    ]