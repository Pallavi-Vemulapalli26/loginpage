import app.dao.cart_dao as cart_dao


def add_to_cart(user_id, product_id):

    cart_id = cart_dao.get_cart_id(user_id)

    # Cart lekapothe Add to Cart click chesinappude create cheyyadam
    if cart_id is None:
        cart_id = cart_dao.create_cart(user_id)

    cart_dao.add_to_cart(cart_id, product_id)

    print("Cart updated.")

    return True


def get_cart_items_for_user(user_id):

    cart_id = cart_dao.get_cart_id(user_id)

    # Cart lekapothe empty list return cheyyadam
    if cart_id is None:
        return []

    return cart_dao.get_cart_items(cart_id)


def update_cart_item_quantity(user_id, product_id, quantity):
    cart_id = cart_dao.get_cart_id(user_id)
    if cart_id is None:
        return False
    return cart_dao.update_quantity(cart_id, product_id, quantity)


def remove_cart_item(user_id, product_id):
    cart_id = cart_dao.get_cart_id(user_id)
    if cart_id is None:
        return False
    return cart_dao.remove_from_cart(cart_id, product_id)


if __name__ == "__main__":
    add_to_cart(1, 1)