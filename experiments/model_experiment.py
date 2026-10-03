from analyzer.models import Function


function = Function(
    name="checkout",
    file="app/orders/checkout.py",
    line=5
)

print(function)