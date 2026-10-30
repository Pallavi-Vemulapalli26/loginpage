
import sqlite3
import uuid

DB_PATH = "logindb.db"


# Cart ni Order ga convert chesi payment details save cheyyadam
def place_order(user_id, billing, delivery, payment_method):

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    try:

        # User active cart retrieve cheyyadam
        query = """
            SELECT cart_order_id
            FROM cart_order
            WHERE user_id = ? AND is_order = 0
        """

        cart = conn.execute(query, (user_id,)).fetchone()

        if not cart:
            conn.close()
            return None

        cart_id = cart["cart_order_id"]

        # Cart lo products retrieve cheyyadam
        query = """
            SELECT product_id, quantity, price
            FROM cart_order_items
            WHERE cart_order_id = ?
        """

        items = conn.execute(query, (cart_id,)).fetchall()

        if not items:
            conn.close()
            return None

        # Total amount calculate cheyyadam
        total_amount = sum(
            item["quantity"] * item["price"]
            for item in items
        )

        # Order parent record update cheyyadam
        query = """
            UPDATE cart_order
            SET is_order = 1,
                total_amount = ?,
                billing_name = ?,
                billing_phone = ?,
                billing_address = ?,
                billing_city = ?,
                billing_state = ?,
                billing_pincode = ?,
                delivery_name = ?,
                delivery_phone = ?,
                delivery_address = ?,
                delivery_city = ?,
                delivery_state = ?,
                delivery_pincode = ?,
                order_status = 'Placed'
            WHERE cart_order_id = ? AND user_id = ? AND is_order = 0
        """

        conn.execute(query, (
            total_amount,
            billing["name"],
            billing["phone"],
            billing["address"],
            billing["city"],
            billing["state"],
            billing["pincode"],
            delivery["name"],
            delivery["phone"],
            delivery["address"],
            delivery["city"],
            delivery["state"],
            delivery["pincode"],
            cart_id,
            user_id
        ))

        # Payment kosam dummy transaction ID generate cheyyadam
        transaction_id = "DUMMY-" + uuid.uuid4().hex[:12].upper()

        query = """
            INSERT INTO payments
            (cart_order_id, payment_method, transaction_id,
             payment_amount, payment_status)
            VALUES (?, ?, ?, ?, 'Success')
        """

        conn.execute(query, (
            cart_id,
            payment_method,
            transaction_id,
            total_amount
        ))

        conn.commit()

        conn.close()

        return {
            "order_id": cart_id,
            "total_amount": total_amount,
            "transaction_id": transaction_id,
            "payment_status": "Success"
        }

    except Exception:
        conn.rollback()
        conn.close()
        raise


# Particular order details retrieve cheyyadam
def get_order_details(order_id, user_id):

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    query = """
        SELECT *
        FROM cart_order
        WHERE cart_order_id = ?
        AND user_id = ?
        AND is_order = 1
    """

    order = conn.execute(
        query, (order_id, user_id)
    ).fetchone()

    if not order:
        conn.close()
        return None

    query = """
        SELECT
            ci.product_id,
            ci.quantity,
            ci.price,
            ci.subtotal,
            p.product_name,
            p.image
        FROM cart_order_items ci
        JOIN products p
        ON ci.product_id = p.product_id
        WHERE ci.cart_order_id = ?
    """

    items = conn.execute(
        query, (order_id,)
    ).fetchall()

    query = """
        SELECT payment_method, transaction_id,
               payment_amount, payment_status, payment_date
        FROM payments
        WHERE cart_order_id = ?
    """

    payment = conn.execute(
        query, (order_id,)
    ).fetchone()

    result = {
        "order": dict(order),
        "items": [dict(item) for item in items],
        "payment": dict(payment) if payment else None
    }

    conn.close()

    return result


# User order history retrieve cheyyadam
def get_user_orders(user_id):

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    query = """
        SELECT *
        FROM cart_order
        WHERE user_id = ? AND is_order = 1
        ORDER BY created_at DESC
    """

    orders = conn.execute(
        query, (user_id,)
    ).fetchall()

    conn.close()

    return [dict(order) for order in orders]
