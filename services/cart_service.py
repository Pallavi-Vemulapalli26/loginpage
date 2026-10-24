import dao.cart_dao as cart_dao


def add_to_cart(user_id, product_id):

    cart_id = cart_dao.get_cart_id(user_id)

    cart_dao.add_to_cart(cart_id, product_id)

    print("Cart updated.")

    return True

def get_cart_items_for_user(user_id):

    cart_id = cart_dao.get_cart_id(user_id)
    
    return cart_dao.get_cart_items(cart_id)


if __name__ == "__main__":
    add_to_cart(1, 1)
