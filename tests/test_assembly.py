from analyzer.analyzer import analyze_repository
from analyzer.graph import build_graph
from analyzer.assembly import assemble_evidence
from analyzer.models import AssemblyContext


def test_assemble_source_evidence_for_candidate():
    repository_path = "."

    analysis = analyze_repository(repository_path)
    graph = build_graph(analysis)

    node = graph.nodes["app.orders.checkout.checkout"]

    context = AssemblyContext(
        candidate_nodes=[node],
        graph=graph,
        repository_path=repository_path,
    )

    bundle = assemble_evidence(context)

    assert len(bundle.items) == 7

    symbols = {
        item.symbol
        for item in bundle.items
    }

    assert symbols == {
        "app.orders.checkout.checkout",
        "app.discounts.discount.calculate_discount",
        "app.payments.payment.process_payment",
        "app.payments.payment.validate_payment",
    }

    relationship_items = [
        item
        for item in bundle.items
        if item.type == "relationship"
    ]

    assert len(relationship_items) == 3

    relationships = {
        item.content
        for item in relationship_items
    }

    assert relationships == {
        "app.orders.checkout.checkout calls "
        "app.discounts.discount.calculate_discount",

        "app.orders.checkout.checkout calls "
        "app.payments.payment.process_payment",

        "app.payments.payment.process_payment calls "
        "app.payments.payment.validate_payment",
    }

    evidence = bundle.items[0]

    assert evidence.type == "source"



def test_assemble_evidence_respects_expansion_depth():
    repository_path = "."

    analysis = analyze_repository(repository_path)
    graph = build_graph(analysis)

    node = graph.nodes["app.orders.checkout.checkout"]

    context = AssemblyContext(
        candidate_nodes=[node],
        graph=graph,
        repository_path=repository_path,
    )

    bundle = assemble_evidence(
        context,
        expansion_depth=1,
    )
    assert len(bundle.items) == 5

    symbols = {
        item.symbol
        for item in bundle.items
    }

    assert symbols == {
        "app.orders.checkout.checkout",
        "app.discounts.discount.calculate_discount",
        "app.payments.payment.process_payment",
    }

    relationship_items = [
        item
        for item in bundle.items
        if item.type == "relationship"
    ]

    assert len(relationship_items) == 2

    relationships = {
        item.content
        for item in relationship_items
    }

    assert relationships == {
        "app.orders.checkout.checkout calls "
        "app.discounts.discount.calculate_discount",

        "app.orders.checkout.checkout calls "
        "app.payments.payment.process_payment",
    }