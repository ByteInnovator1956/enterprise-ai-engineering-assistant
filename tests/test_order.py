from types import SimpleNamespace

from app.orders.order import create_order


def test_create_order():
    user = SimpleNamespace(is_premium=False)
    order = SimpleNamespace(price=100, user=user)

    assert create_order(order) is True