import sqlite3
from app.dao.product_dao import get_colors as get_product_colors
from app.dao.product_dao import get_offers as get_product_offers
DB = "logindb.db"
import app.dao.product_dao as product_dao

def get_products(category=None, max_price=None, search=None):

    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row

    query = """
        SELECT
            p.product_id AS id,
            p.product_name AS name,
            p.price,
            p.product_description AS description,
            p.image
        FROM products p
        JOIN category c
        ON p.category_id = c.category_id
    """

    conditions = []
    params = []
    print("category:", category)
    print("max_price:", max_price)
    print("search:", search)
    if category:
        conditions.append("c.category_name = ?")
        params.append(category)

    if max_price is not None:
        conditions.append("p.price <= ?")
        params.append(max_price)

    if search:
        conditions.append("""
            (
                p.product_name LIKE ?
                OR p.product_description LIKE ?
            )
        """)

        params.append("%" + search + "%")
        params.append("%" + search + "%")
        

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += " ORDER BY p.price ASC"
    print("query:", query)
    products = conn.execute(query, params).fetchall()

    conn.close()
 
    return [dict(product) for product in products]


def get_offers(product_id):
    return product_dao.get_offers(product_id)

def get_products_with_offers(
    category=None,
    max_price=None,
    search=None
):

    products = get_products(
        category,
        max_price,
        search
    )
# Get the offers related to this product and place them in the 'Offers' section of the product
    for product in products:
        product["offers"] = get_offers(product["id"])

    return products

def get_colors(product_id):
    colors = get_product_colors(product_id)
    items = [color["color_name"] for color in colors]

    return {
        "count": len(items),
        "items": items
    }



