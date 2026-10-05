from flask import request, jsonify

# from services.product_service import get_products_with_offers
from services.product_service import (
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

    max_price = None
    search = None

    products = get_products_with_offers(
        category,
        max_price,
        search
    )

    return jsonify(products)

def get_colors(product_id):
    return jsonify(get_product_colors(product_id))
