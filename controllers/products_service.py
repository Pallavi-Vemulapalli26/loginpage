import sqlite3

DB = "logindb.db"


def get_products(category=None, max_price=None, search=None):

    # 1. Connect to database
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row

    # 2. Basic SQL
    query = """
        SELECT
            p.product_id,
            p.product_name,
            p.price,
            p.product_description,
            p.image,
            c.category_name
        FROM products p
        JOIN category c
        ON p.category_id = c.category_id
        WHERE 1 = 1
    """

    # 3. Values for ?
    params = []

    # 4. Category filter
    if category:
        query += " AND c.category_name = ?"
        params.append(category)

    # 5. Price filter
    if max_price:
        query += " AND p.price <= ?"
        params.append(max_price)

    # 6. Product search
    if search:
        query += """
            AND (
                p.product_name LIKE ?
                OR p.product_description LIKE ?
            )
        """

        params.append("%" + search + "%")
        params.append("%" + search + "%")

    # 7. Sort products by price
    query += " ORDER BY p.price ASC"

    # 8. Execute SQL
    products = conn.execute(
        query,
        params
    ).fetchall()

    # 9. Close database
    conn.close()

    # 10. Return data
    return [dict(product) for product in products]