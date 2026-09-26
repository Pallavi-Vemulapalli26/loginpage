
from flask import Blueprint, request, render_template
import sqlite3

product_bp = Blueprint("products", __name__)


@product_bp.route("/products")
def products():

    search = request.args.get("q", "").lower()

    conn = sqlite3.connect("logindb.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = """
        SELECT products.*, category.category_name
        FROM products
        JOIN category
        ON products.category_id = category.category_id
        WHERE 1=1
    """

    values = []

    # Search by product name, description, or category
    if search:
        words = search.split()

        for word in words:

            # Ignore simple search words
            if word in ["show", "all", "products", "i", "want", "under", "below", "in", "for", "less", "than"]:
                continue

            # If word is a price, filter by price
            if word.isdigit():
                sql += " AND products.price <= ?"
                values.append(int(word))

            else:
                sql += """
                    AND (
                        LOWER(products.product_name) LIKE ?
                        OR LOWER(products.product_description) LIKE ?
                        OR LOWER(category.category_name) LIKE ?
                    )
                """

                values.extend([
                    "%" + word + "%",
                    "%" + word + "%",
                    "%" + word + "%"
                ])

    cursor.execute(sql, values)
    products = cursor.fetchall()

    conn.close()

    return render_template(
        "products.html",
        products=products,
        search=search
    )