from analyzer.models import EvidenceBundle
from ollama import chat

SYSTEM_PROMPT = """
You are a codebase reasoning assistant.

Answer the user's question using only the repository evidence provided to you.

Rules:
1. Do not invent files, functions, classes, dependencies, or behavior.
2. Base repository claims on the supplied evidence.
3. Clearly distinguish directly supported facts from reasonable inferences.
4. When the evidence is insufficient to answer the question, say so explicitly.
5. When possible, cite the relevant file and line range from the evidence.
6. Do not claim that code exists if it is not present in the evidence.
"""


def build_reasoning_prompt(
    question: str,
    evidence: EvidenceBundle,
) -> str:
    evidence_text = []

    for item in evidence.items:
        location = item.file

        if (
            item.start_line is not None
            and item.end_line is not None
        ):
            location += (
                f":{item.start_line}-{item.end_line}"
            )

        evidence_text.append(
            f"[{item.type}] {location}\n"
            f"{item.content}"
        )

    joined_evidence = "\n\n".join(
        evidence_text
    )

    return (
        f"Question:\n"
        f"{question}\n\n"
        f"Repository Evidence:\n"
        f"{joined_evidence}\n\n"
        f"Answer the question using only this evidence."
    )


class Reasoner:

    def reason(
        self,
        question: str,
        evidence: EvidenceBundle,
    ) -> str:
        raise NotImplementedError

class OllamaReasoner(Reasoner):

    def __init__(self, model_name="qwen3:4b-instruct"):
        self.model_name = model_name

    def reason(
        self,
        question: str,
        evidence: EvidenceBundle,
    ) -> str:

        response = chat(
            model=self.model_name,
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT,
                },
                {
                    "role": "user",
                    "content": build_reasoning_prompt(
                        question,
                        evidence,
                    ),
                },
            ],
            think=False,
        )

        return response.message.content