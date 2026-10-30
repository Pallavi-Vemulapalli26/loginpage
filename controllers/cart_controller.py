
from flask import jsonify
from services.cart_service import (
    add_to_cart as add_product_to_cart,
    get_cart_items_for_user,
    update_cart_item_quantity,
    remove_cart_item
)


def add_to_cart(user_id, product_id):

    result = add_product_to_cart(user_id, product_id)

    if result:
        return jsonify({"message": "Product added to cart"})

    return jsonify({"error": "Unable to add product"}), 400


def get_cart(user_id):

    items = get_cart_items_for_user(user_id)

    return jsonify({"items": items}), 200
def update_cart(user_id, product_id, quantity):
    result = update_cart_item_quantity(
        user_id, product_id, quantity
    )

    if result:
        return jsonify({"message": "Quantity updated"})

    return jsonify({"error": "Unable to update quantity"}), 400


def remove_cart_product(user_id, product_id):
    result = remove_cart_item(user_id, product_id)

    if result:
        return jsonify({"message": "Product removed"})

    return jsonify({"error": "Unable to remove product"}), 400