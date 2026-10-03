from analyzer.models import Function, Class


functions = [
    Function(
        name="calculate_discount",
        file="app/discounts/discount.py",
        line=1,
    )
]

classes = [
    Class(
        name="SessionManager",
        file="app/auth/session.py",
        line=1,
    )
]


symbols = {}

for function in functions:
    symbols[function.name] = "function"

for class_info in classes:
    symbols[class_info.name] = "class"


calls = [
    "calculate_discount",
    "SessionManager",
    "foo",
]


for call in calls:

    symbol_type = symbols.get(call)

    if symbol_type == "function":
        relationship = "calls"

    elif symbol_type == "class":
        relationship = "instantiates"

    else:
        relationship = "unknown"

    print(call, "→", relationship)