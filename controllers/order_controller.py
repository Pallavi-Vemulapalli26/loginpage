
from flask import jsonify
from services.order_service import (
    place_order as create_order,
    get_order_details,
    get_user_orders
)


# Order place cheyyadam
def place_order(user_id, billing, delivery, payment_method):

    result = create_order(
        user_id, billing, delivery, payment_method
    )

    if result:
        return jsonify(result), 200

    return jsonify({"error": "Unable to place order"}), 400


# Particular order details retrieve cheyyadam
def get_order(order_id, user_id):

    result = get_order_details(order_id, user_id)

    if result:
        return jsonify(result), 200

    return jsonify({"error": "Order not found"}), 404


# User order history retrieve cheyyadam
def get_orders(user_id):

    result = get_user_orders(user_id)

    return jsonify({"orders": result}), 200
