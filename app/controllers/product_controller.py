from flask import request, jsonify
import re
# from app.services.product_service import get_products_with_offers
from app.services.product_service import (
    get_products_with_offers,
    get_colors as get_product_colors,
)
def find_category(query):

    categories = [
        "Clothes",
        "Shoes",
        "Electronics",
        "Books",
        "Beauty",
        "Home Appliances",
        "Accessories",
        "Sports"
    ]

    for category in categories:
        if category.lower() in query.lower():
            return category

    return None


def search_products():

    query = request.args.get("q", "")

    category = find_category(query)

    price_match = re.search(r"\bunder\s*([\d,]+)", query, re.IGNORECASE)
    max_price = int(price_match.group(1).replace(",", "")) if price_match else None
    search = None

    products = get_products_with_offers(
        category,
        max_price,
        search
    )

    return jsonify(products)

def get_colors(product_id):
    return jsonify(get_product_colors(product_id))
