from analyzer.analyzer import analyze_repository
from analyzer.evidence import build_source_evidence
from analyzer.evidence import build_relationship_evidence
from analyzer.models import Relationship
from analyzer.graph import (
    build_graph,
    get_direct_dependencies,
    get_transitive_dependencies,
    get_direct_dependents,
    get_transitive_dependents,
    get_dependencies_within_depth,
)
def test_analyzer_discovers_session_manager():
    analysis = analyze_repository(".")

    classes = []

    for file in analysis.files:
        for class_info in file.classes:
            classes.append(class_info.name)

    assert "SessionManager" in classes

def test_analyzer_discovers_session_method():
    analysis = analyze_repository(".")

    methods = []

    for file in analysis.files:
        for method in file.methods:
            methods.append(method.name)

    assert "create_session" in methods

def test_login_instantiates_session_manager():
    analysis = analyze_repository(".")

    relationships = analysis.relationships

    assert any(
        relationship.source == "app.auth.login.login"
        and relationship.type == "instantiates"
        and relationship.target == "app.auth.session.SessionManager"
        for relationship in relationships
    )

def test_login_calls_create_session():
    analysis = analyze_repository(".")

    relationships = analysis.relationships

    assert any(
        relationship.source == "app.auth.login.login"
        and relationship.type == "calls"
        and relationship.target == "app.auth.session.SessionManager.create_session"
        for relationship in relationships
    )

def test_checkout_relationships():
    analysis = analyze_repository(".")

    relationships = analysis.relationships

    assert any(
        relationship.source == "app.orders.checkout.checkout"
        and relationship.type == "calls"
        and relationship.target == "app.discounts.discount.calculate_discount"
        for relationship in relationships
    )

    assert any(
        relationship.source == "app.orders.checkout.checkout"
        and relationship.type == "calls"
        and relationship.target == "app.payments.payment.process_payment"
        for relationship in relationships
    )

def test_checkout_is_tested_by_premium_checkout_test():
    analysis = analyze_repository(".")

    relationships = analysis.relationships

    assert any(
        relationship.source
        == "tests.test_checkout.test_premium_user_checkout"
        and relationship.type == "tests"
        and relationship.target
        == "app.orders.checkout.checkout"
        for relationship in relationships
    )


def test_process_payment_calls_validate_payment():
    analysis = analyze_repository(".")

    relationships = analysis.relationships

    assert any(
        relationship.source == "app.payments.payment.process_payment"
        and relationship.type == "calls"
        and relationship.target
        == "app.payments.payment.validate_payment"
        for relationship in relationships
    )


def test_direct_dependencies_of_checkout():
    analysis = analyze_repository(".")
    graph = build_graph(analysis)

    dependencies = get_direct_dependencies(
        graph,
        "app.orders.checkout.checkout"
    )

    assert dependencies == {
        "app.discounts.discount.calculate_discount",
        "app.payments.payment.process_payment",
    }

def test_transitive_dependencies_of_checkout():
    analysis = analyze_repository(".")
    graph = build_graph(analysis)

    dependencies = get_transitive_dependencies(
        graph,
        "app.orders.checkout.checkout"
    )

    assert dependencies == {
        "app.discounts.discount.calculate_discount",
        "app.payments.payment.process_payment",
        "app.payments.payment.validate_payment",
    }

def test_direct_dependents_of_checkout():
    analysis = analyze_repository(".")
    graph = build_graph(analysis)

    dependents = get_direct_dependents(
        graph,
        "app.orders.checkout.checkout"
    )

    assert dependents == {
        "app.orders.order.create_order",
    }

def test_transitive_dependents_of_checkout():
    analysis = analyze_repository(".")
    graph = build_graph(analysis)

    dependents = get_transitive_dependents(
        graph,
        "app.orders.checkout.checkout"
    )

    assert dependents == {
        "app.orders.order.create_order",
    }

def test_build_source_evidence():
    evidence = build_source_evidence(
        "app/orders/checkout.py",
        "app.orders.checkout.checkout",
        4,
        7,
    )

    assert evidence.type == "source"
    assert evidence.file == "app/orders/checkout.py"
    assert evidence.start_line == 4
    assert evidence.end_line == 7
    assert evidence.symbol == "app.orders.checkout.checkout"

    assert "def checkout(order):" in evidence.content
    assert "calculate_discount" in evidence.content
    assert "process_payment" in evidence.content


def test_build_relationship_evidence():
    relationship = Relationship(
        source="app.orders.checkout.checkout",
        type="calls",
        target="app.discounts.discount.calculate_discount",
        file="app/orders/checkout.py",
        line=5,
    )

    evidence = build_relationship_evidence(
        relationship
    )

    assert evidence.type == "relationship"
    assert evidence.content == (
        "app.orders.checkout.checkout "
        "calls "
        "app.discounts.discount.calculate_discount"
    )
    assert evidence.file == "app/orders/checkout.py"
    assert evidence.start_line == 5
    assert evidence.end_line == 5
    assert evidence.symbol == "app.orders.checkout.checkout"


def test_dependencies_within_depth_zero():
    analysis = analyze_repository(".")
    graph = build_graph(analysis)

    result = get_dependencies_within_depth(
        graph,
        "app.orders.checkout.checkout",
        0,
    )

    assert result == set()

def test_dependencies_within_depth_one():
    analysis = analyze_repository(".")
    graph = build_graph(analysis)

    result = get_dependencies_within_depth(
        graph,
        "app.orders.checkout.checkout",
        1,
    )

    assert result == {
        "app.discounts.discount.calculate_discount",
        "app.payments.payment.process_payment",
    }

def test_dependencies_within_depth_two():
    analysis = analyze_repository(".")
    graph = build_graph(analysis)

    result = get_dependencies_within_depth(
        graph,
        "app.orders.checkout.checkout",
        2,
    )

    assert result == {
        "app.discounts.discount.calculate_discount",
        "app.payments.payment.process_payment",
        "app.payments.payment.validate_payment",
    }