from services.cart_service import add_to_cart as add_product_to_cart
from flask import jsonify
from services.cart_service import (
    add_to_cart as add_product_to_cart,
    get_cart_items_for_user
)



def add_to_cart(user_id, product_id):
    result = add_product_to_cart(user_id, product_id)

    if result:
        return jsonify({"message": "Product added to cart"})

    return jsonify({"error": "Unable to add product"}), 400


def get_cart(user_id):
    items = get_cart_items_for_user(user_id)
    return jsonify({"items": items}), 200