def calculate_discount(price, user):
    if user.is_premium:
        return price * 0.80

    return price