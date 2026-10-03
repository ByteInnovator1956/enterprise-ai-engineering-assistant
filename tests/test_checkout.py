from types import SimpleNamespace

from app.orders.checkout import checkout


def test_premium_user_checkout():
    user = SimpleNamespace(is_premium=True)
    order = SimpleNamespace(price=100, user=user)

    assert checkout(order) is True