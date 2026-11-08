
import app.dao.order_dao as order_dao


# Order place cheyyadam
def place_order(user_id, billing, delivery, payment_method):

    result = order_dao.place_order(
        user_id, billing, delivery, payment_method
    )

    return result


# User order details retrieve cheyyadam
def get_order_details(order_id, user_id):

    return order_dao.get_order_details(order_id, user_id)


# User order history retrieve cheyyadam
def get_user_orders(user_id):

    return order_dao.get_user_orders(user_id)


def save_billing_address(user_id, address):
    return order_dao.save_billing_address(user_id, address)


def save_delivery_address(user_id, address):
    return order_dao.save_delivery_address(user_id, address)
