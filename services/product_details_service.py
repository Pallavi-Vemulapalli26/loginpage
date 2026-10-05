import dao.product_dao as product_dao

def get_product_details(product_id):

    print("\n========== PRODUCT DETAILS ==========")

    product = product_dao.get_product_details(product_id)
    if product is None:
        print("Product not found")
        return None
    print("Product:")
    print(product)

    print("\n========== OFFERS ==========")

    offers = product_dao.get_offers(product_id)

    print("Offers:")
    print(offers)

    product["offers"] = offers

    print("\n========== COLORS ==========")

    colors = product_dao.get_colors(product_id)

    print("Colors:")
    print(colors)

    product["colors"] = colors

    print("\n========== FINAL PRODUCT ==========")

    print(product)

    return product


def get_colors(product_id):
    return product_dao.get_colors(product_id)


def get_offers(product_id):
    return product_dao.get_offers(product_id)



get_product_details(1)