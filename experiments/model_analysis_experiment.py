from analyzer.models import (
    AnalyzedFile,
    Function,
    RepositoryAnalysis,
    Relationship,
)


checkout_function = Function(
    name="checkout",
    file="app/orders/checkout.py",
    line=5,
)


checkout_file = AnalyzedFile(
    path="app/orders/checkout.py",
    functions=[checkout_function],
    classes=[],
    methods=[],
    imports=[],
)


relationship = Relationship(
    source="checkout",
    type="calls",
    target="calculate_discount",
    file="app/orders/checkout.py",
    line=6,
)


analysis = RepositoryAnalysis(
    files=[checkout_file],
    relationships=[relationship],
)


print(analysis)