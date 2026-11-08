from flask import request, jsonify

from app.services.product_details_service import get_product_details as get_product_details_service


def get_product_details(product_id):

    # print(f"Product ID requested: {product_id}")

    product = get_product_details_service(product_id)
    
    # print(f"Product details: {product}")

    return jsonify(product)

# product_details(1)
