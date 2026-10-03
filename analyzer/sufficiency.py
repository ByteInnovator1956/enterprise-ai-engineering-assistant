from analyzer.models import (
    EvidenceBundle,
    RetrievedCandidate,
)


def inspect_evidence_sufficiency(
    candidates: list[RetrievedCandidate],
    evidence: EvidenceBundle,
):
    top_score = 0.0

    if candidates:
        top_score = candidates[0].score

    return {
        "candidate_count": len(candidates),
        "top_score": top_score,
        "candidates": [
            {
                "node": candidate.node.id,
                "score": candidate.score,
            }
            for candidate in candidates
        ],
        "evidence_count": len(evidence.items),
        "evidence_types": [
            item.type
            for item in evidence.items
        ],
    }