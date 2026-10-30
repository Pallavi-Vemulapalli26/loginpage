
import sqlite3

DB_PATH = "logindb.db"


# User ki new cart create cheyyadam
def create_cart(user_id):

    conn = sqlite3.connect(DB_PATH)

    query = """
        INSERT INTO cart_order (user_id, is_order)
        VALUES (?, 0)
    """

    cursor = conn.execute(query, (user_id,))
    conn.commit()

    cart_id = cursor.lastrowid

    conn.close()

    return cart_id


# User ki already active cart undo check cheyyadam
def get_cart_id(user_id):

    conn = sqlite3.connect(DB_PATH)

    query = """
        SELECT cart_order_id
        FROM cart_order
        WHERE user_id = ? AND is_order = 0
    """

    cart = conn.execute(query, (user_id,)).fetchone()

    conn.close()

    # Cart unte cart_id return cheyyadam
    if cart:
        return cart[0]

    # Cart lekapothe create cheyyakunda None return cheyyadam
    return None


# Product already cart lo undo check chesi add cheyyadam
def add_to_cart(cart_id, product_id):

    conn = sqlite3.connect(DB_PATH)

    query = """
        SELECT quantity
        FROM cart_order_items
        WHERE cart_order_id = ? AND product_id = ?
    """

    item = conn.execute(
        query, (cart_id, product_id)
    ).fetchone()

    # Product already unte quantity increase cheyyadam
    if item:

        query = """
            UPDATE cart_order_items
            SET quantity = quantity + 1,
                subtotal = price * (quantity + 1)
            WHERE cart_order_id = ? AND product_id = ?
        """

        conn.execute(query, (cart_id, product_id))

    # Product lekapothe new item insert cheyyadam
    else:

        query = """
            SELECT price
            FROM products
            WHERE product_id = ?
        """

        product = conn.execute(
            query, (product_id,)
        ).fetchone()

        if not product:
            conn.close()
            return False

        price = product[0]

        query = """
            INSERT INTO cart_order_items
            (cart_order_id, product_id, quantity, price, subtotal)
            VALUES (?, ?, 1, ?, ?)
        """

        conn.execute(
            query, (cart_id, product_id, price, price)
        )

    conn.commit()
    conn.close()

    return True


# Cart lo unna products details retrieve cheyyadam
def get_cart_items(cart_id):

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

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

    items = conn.execute(query, (cart_id,)).fetchall()

    conn.close()

    return [dict(item) for item in items]


# Cart lo product quantity update cheyyadam
def update_quantity(cart_id, product_id, quantity):

    if quantity <= 0:
        return False

    conn = sqlite3.connect(DB_PATH)

    query = """
        UPDATE cart_order_items
        SET quantity = ?,
            subtotal = price * ?
        WHERE cart_order_id = ? AND product_id = ?
    """

    conn.execute(
        query, (quantity, quantity, cart_id, product_id)
    )

    conn.commit()
    conn.close()

    return True


# Cart nunchi product remove cheyyadam
def remove_from_cart(cart_id, product_id):

    conn = sqlite3.connect(DB_PATH)

    query = """
        DELETE FROM cart_order_items
        WHERE cart_order_id = ? AND product_id = ?
    """

    conn.execute(query, (cart_id, product_id))

    conn.commit()
    conn.close()

    return True
