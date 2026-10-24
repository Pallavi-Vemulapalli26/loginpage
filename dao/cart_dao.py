
import sqlite3

DB_PATH = "logindb.db"


def create_cart(user_id):

    conn = sqlite3.connect(DB_PATH)

    query = """
        INSERT INTO cart (user_id)
        VALUES (?)
    """

    cursor = conn.execute(query, (user_id,))
    conn.commit()

    cart_id = cursor.lastrowid

    conn.close()

    return cart_id

# User ki already cart undo check cheyyadam
def get_cart_id(user_id):

    conn = sqlite3.connect(DB_PATH)

    query = """
        SELECT cart_id
        FROM cart
        WHERE user_id = ?
    """

    cart = conn.execute(query, (user_id,)).fetchone()

    conn.close()

    # Cart unte cart_id return cheyyadam
    if cart:
        return cart[0]

    # Cart lekapothe new cart create cheyyadam
    return create_cart(user_id)

# Product already cart lo undo check chesi add cheyyadam
def add_to_cart(cart_id, product_id):

    conn = sqlite3.connect(DB_PATH)

    query = """
        SELECT quantity
        FROM cart_items
        WHERE cart_id = ? AND product_id = ?
    """

    item = conn.execute(
        query, (cart_id, product_id)
    ).fetchone()

    # Product already unte quantity increase cheyyadam
    if item:
        query = """
            UPDATE cart_items
            SET quantity = quantity + 1
            WHERE cart_id = ? AND product_id = ?
        """

        conn.execute(query, (cart_id, product_id))

    # Product lekapothe new item insert cheyyadam
    else:
        query = """
            INSERT INTO cart_items (cart_id, product_id, quantity)
            VALUES (?, ?, 1)
        """

        conn.execute(query, (cart_id, product_id))

    conn.commit()
    conn.close()

# Cart lo unna products details retrieve cheyyadam
def get_cart_items(cart_id):

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    query = """
        SELECT
            ci.product_id,
            ci.quantity,
            p.product_name,
            p.price,
            p.image
        FROM cart_items ci
        JOIN products p
        ON ci.product_id = p.product_id
        WHERE ci.cart_id = ?
    """

    items = conn.execute(query, (cart_id,)).fetchall()

    conn.close()

    return [dict(item) for item in items]

# Cart lo product quantity update cheyyadam
def update_quantity(cart_id, product_id, quantity):

    conn = sqlite3.connect(DB_PATH)

    query = """
        UPDATE cart_items
        SET quantity = ?
        WHERE cart_id = ? AND product_id = ?
    """

    conn.execute(query, (quantity, cart_id, product_id))

    conn.commit()
    conn.close()

# Cart nunchi product remove cheyyadam
def remove_from_cart(cart_id, product_id):

    conn = sqlite3.connect(DB_PATH)

    query = """
        DELETE FROM cart_items
        WHERE cart_id = ? AND product_id = ?
    """

    conn.execute(query, (cart_id, product_id))

    conn.commit()
    conn.close()
