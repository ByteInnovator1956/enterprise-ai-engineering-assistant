import json
import numpy as np
from dataclasses import dataclass

from analyzer.models import SemanticDocument
from analyzer.semantic import build_semantic_document


@dataclass
class SemanticIndex:
    documents: list[SemanticDocument]
    embeddings: list

def is_indexable_node(node):
    if node.file is None:
        return False

    normalized_path = node.file.replace("\\", "/")

    if normalized_path.startswith("tests/test_analyzer.py"):
        return False

    return True


def save_semantic_index(index, path):
    data = {
        "documents": [
            {
                "node_id": document.node_id,
                "text": document.text,
            }
            for document in index.documents
        ],
        "embeddings": index.embeddings.tolist(),
    }

    with open(path, "w") as file:
        json.dump(data, file)


def load_semantic_index(path):
    with open(path, "r") as file:
        data = json.load(file)

    documents = [
        SemanticDocument(
            node_id=document["node_id"],
            text=document["text"],
        )
        for document in data["documents"]
    ]

    embeddings = np.array(
        data["embeddings"],
        dtype=np.float32,
    )

    return SemanticIndex(
        documents=documents,
        embeddings=embeddings,
    )


def build_semantic_index(graph, model):
    documents = []
    texts = []

    for node in graph.nodes.values():

        if not is_indexable_node(node):
            continue

        document = build_semantic_document(node)

        if document is None:
            continue

        documents.append(document)
        texts.append(document.text)

    if not documents:
        return SemanticIndex(
            documents=[],
            embeddings=[],
        )

    embeddings = model.encode(
        texts,
        prompt_name="nl2code_document",
        normalize_embeddings=True,
    )

    return SemanticIndex(
        documents=documents,
        embeddings=embeddings,
    )