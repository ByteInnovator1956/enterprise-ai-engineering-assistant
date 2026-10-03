from analyzer.evidence import build_evidence_bundle
from analyzer.models import EvidenceItem
from analyzer.evidence import build_test_evidence
from analyzer.evidence import build_documentation_evidence

def test_build_evidence_bundle():
    source_evidence = EvidenceItem(
        type="source",
        content="def checkout(order):",
        file="app/orders/checkout.py",
        start_line=4,
        end_line=4,
        symbol="app.orders.checkout.checkout",
    )

    relationship_evidence = EvidenceItem(
        type="relationship",
        content=(
            "app.orders.checkout.checkout "
            "calls "
            "app.discounts.discount.calculate_discount"
        ),
        file="app/orders/checkout.py",
        start_line=5,
        end_line=5,
        symbol="app.orders.checkout.checkout",
    )

    bundle = build_evidence_bundle(
        [
            source_evidence,
            relationship_evidence,
        ]
    )

    assert len(bundle.items) == 2
    assert bundle.items[0] == source_evidence
    assert bundle.items[1] == relationship_evidence


def test_build_test_evidence():
    evidence = build_test_evidence(
        "tests/test_checkout.py",
        "tests.test_checkout.test_premium_user_checkout",
        6,
        10,
    )

    assert evidence.type == "test"
    assert evidence.file == "tests/test_checkout.py"
    assert evidence.start_line == 6
    assert evidence.end_line == 10
    assert evidence.symbol == (
        "tests.test_checkout.test_premium_user_checkout"
    )

    assert "def test_premium_user_checkout():" in evidence.content
    assert "checkout(order)" in evidence.content




def test_build_documentation_evidence():
    evidence = build_documentation_evidence(
        "docs/architecture.md",
        3,
        8,
    )

    assert evidence.type == "documentation"
    assert evidence.file == "docs/architecture.md"
    assert evidence.start_line == 3
    assert evidence.end_line == 8
    assert evidence.symbol is None

    assert "customer orders" in evidence.content
    assert "checkout workflow" in evidence.content