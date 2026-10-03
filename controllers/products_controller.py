
import re
from flask import request
from controllers.products_service import get_products

def search_products():
    query = request.args.get("q", "").strip()
    remaining = query

    categories = [
        "Clothes",
        "Shoes",
        "Electronics",
        "Books",
        "Beauty",
        "Home Appliances",
        "Accessories",
        "Sports",
    ]

    category = next(
        (item for item in categories if item.lower() in query.lower()),
        None,
    )

    if category:
        remaining = re.sub(
            re.escape(category), "", remaining, flags=re.IGNORECASE
        )

    price_match = re.search(
        r"\b(?:under|below)\s+(\d+(?:\.\d+)?k?)\b",
        remaining,
        flags=re.IGNORECASE,
    )

    max_price = None
    if price_match:
        price_text = price_match.group(1).lower()
        max_price = (
            float(price_text[:-1]) * 1000
            if price_text.endswith("k")
            else float(price_text)
        )
        remaining = remaining.replace(price_match.group(0), "")

    search = remaining.strip() or None

    return get_products(
        category=category,
        max_price=max_price,
        search=search,
    )