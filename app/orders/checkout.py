from app.discounts.discount import calculate_discount
from app.payments.payment import process_payment


def checkout(order):
    final_price = calculate_discount(order.price, order.user)
    return process_payment(final_price)