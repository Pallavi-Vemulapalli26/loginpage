
from flask import jsonify
from app.services.order_service import (
    place_order as create_order,
    get_order_details,
    get_user_orders,
    save_billing_address as store_billing_address,
    save_delivery_address as store_delivery_address
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


def save_billing_address(user_id, address):
    result = store_billing_address(user_id, address)

    if result:
        return jsonify({"message": "Billing address saved"}), 200

    return jsonify({"error": "No active cart found"}), 400


def save_delivery_address(user_id, address):
    result = store_delivery_address(user_id, address)

    if result:
        return jsonify({"message": "Delivery address saved"}), 200

    return jsonify({"error": "No active cart found"}), 400
