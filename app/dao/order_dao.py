
import sqlite3
import uuid

DB_PATH = "logindb.db"


def _save_address(user_id, address, table, id_column):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    cart = conn.execute(f"""
        SELECT cart_order_id, {id_column}
        FROM cart_order
        WHERE user_id = ? AND is_order = 0
    """, (user_id,)).fetchone()

    if not cart:
        conn.close()
        return None

    address_id = cart[id_column]
    values = (
        address["name"], address["phone"], address["address"],
        address["city"], address["state"], address["pincode"]
    )

    if address_id:
        conn.execute(f"""
            UPDATE {table}
            SET name = ?, phone = ?, address = ?,
                city = ?, state = ?, pincode = ?
            WHERE {id_column} = ?
        """, values + (address_id,))
    else:
        cursor = conn.execute(f"""
            INSERT INTO {table}
            (name, phone, address, city, state, pincode)
            VALUES (?, ?, ?, ?, ?, ?)
        """, values)
        address_id = cursor.lastrowid

        conn.execute(f"""
            UPDATE cart_order SET {id_column} = ?
            WHERE cart_order_id = ?
        """, (address_id, cart["cart_order_id"]))

    conn.commit()
    conn.close()
    return address_id


def save_billing_address(user_id, address):
    return _save_address(
        user_id, address, "billing_addresses", "billing_address_id"
    )


def save_delivery_address(user_id, address):
    return _save_address(
        user_id, address, "delivery_addresses", "delivery_address_id"
    )


# Convert the user's active cart into an order
# and save dummy payment details
def place_order(user_id, billing, delivery, payment_method):

    # Connect to the database
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    # Get the user's active cart
    cart = conn.execute("""
        SELECT cart_order_id, billing_address_id, delivery_address_id
        FROM cart_order
        WHERE user_id = ? AND is_order = 0
    """, (user_id,)).fetchone()

    # Stop if the user has no active cart
    if not cart:
        conn.close()
        return None

    cart_id = cart["cart_order_id"]

    # Get all products from the cart
    items = conn.execute("""
        SELECT quantity, price FROM cart_order_items
        WHERE cart_order_id = ?
    """, (cart_id,)).fetchall()

    # Stop if the cart is empty
    if not items:
        conn.close()
        return None

    if not cart["billing_address_id"] or not cart["delivery_address_id"]:
        conn.close()
        return None

    # Calculate the total order amount
    total = sum(item["quantity"] * item["price"] for item in items)

    conn.execute("""
        UPDATE cart_order SET
        is_order = 1,
        total_amount = ?,
        order_status = 'Placed'
        WHERE cart_order_id = ?
    """, (total, cart_id))

    # Generate a unique dummy transaction ID
    transaction_id = "DUMMY-" + uuid.uuid4().hex[:12].upper()

    # Save the payment details in the payments table
    conn.execute("""
        INSERT INTO payments
        (cart_order_id, payment_method, transaction_id,
         payment_amount, payment_status)
        VALUES (?, ?, ?, ?, 'Success')
    """, (cart_id, payment_method, transaction_id, total))

    # Save all database changes
    conn.commit()
    conn.close()

    # Return the order and payment details
    return {
        "order_id": cart_id,
        "total_amount": total,
        "transaction_id": transaction_id,
        "payment_status": "Success"
    }


# Retrieve the details of a particular order
def get_order_details(order_id, user_id):

    # Connect to the database
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    # Get the order belonging to the given user
    order = conn.execute("""
        SELECT
            co.cart_order_id,
            co.user_id,
            co.is_order,
            co.total_amount,
            b.name AS billing_name,
            b.phone AS billing_phone,
            b.address AS billing_address,
            b.city AS billing_city,
            b.state AS billing_state,
            b.pincode AS billing_pincode,
            d.name AS delivery_name,
            d.phone AS delivery_phone,
            d.address AS delivery_address,
            d.city AS delivery_city,
            d.state AS delivery_state,
            d.pincode AS delivery_pincode,
            co.order_status,
            co.created_at
        FROM cart_order co
        LEFT JOIN billing_addresses b
            ON b.billing_address_id = co.billing_address_id
        LEFT JOIN delivery_addresses d
            ON d.delivery_address_id = co.delivery_address_id
        WHERE co.cart_order_id = ? AND co.user_id = ? AND co.is_order = 1
    """, (order_id, user_id)).fetchone()

    # Return None if the order does not exist
    if not order:
        conn.close()
        return None

    # Get the products included in this order
    items = conn.execute("""
        SELECT ci.*, p.product_name, p.image
        FROM cart_order_items ci
        JOIN products p ON ci.product_id = p.product_id
        WHERE ci.cart_order_id = ?
    """, (order_id,)).fetchall()

    # Get the payment details of this order
    payment = conn.execute("""
        SELECT * FROM payments WHERE cart_order_id = ?
    """, (order_id,)).fetchone()

    conn.close()

    # Return order, product and payment information
    return {
        "order": dict(order),
        "items": [dict(item) for item in items],
        "payment": dict(payment) if payment else None
    }


# Retrieve all placed orders of a particular user
def get_user_orders(user_id):

    # Connect to the database
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    # Get all orders placed by the user
    # Display the latest orders first
    orders = conn.execute("""
        SELECT
            co.cart_order_id,
            co.user_id,
            co.is_order,
            co.total_amount,
            b.name AS billing_name,
            b.phone AS billing_phone,
            b.address AS billing_address,
            b.city AS billing_city,
            b.state AS billing_state,
            b.pincode AS billing_pincode,
            d.name AS delivery_name,
            d.phone AS delivery_phone,
            d.address AS delivery_address,
            d.city AS delivery_city,
            d.state AS delivery_state,
            d.pincode AS delivery_pincode,
            co.order_status,
            co.created_at
        FROM cart_order co
        LEFT JOIN billing_addresses b
            ON b.billing_address_id = co.billing_address_id
        LEFT JOIN delivery_addresses d
            ON d.delivery_address_id = co.delivery_address_id
        WHERE co.user_id = ? AND co.is_order = 1
        ORDER BY co.created_at DESC
    """, (user_id,)).fetchall()

    conn.close()

    # Convert database rows into a list of dictionaries
    return [dict(order) for order in orders]
