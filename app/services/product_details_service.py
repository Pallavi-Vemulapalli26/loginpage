import app.dao.product_dao as product_dao

def get_product_details(product_id):


    product = product_dao.get_product_details(product_id)
    if product is None:
        print("Product not found")
        return None
        # print("Product:")
        # print(product)


    offers = product_dao.get_offers(product_id)

    # print("Offers:")
    # print(offers)

    product["offers"] = offers


    colors = product_dao.get_colors(product_id)

    # print("Colors:")
    # print(colors)

    product["colors"] = colors


    # print(product)

    return product


def get_colors(product_id):
    return product_dao.get_colors(product_id)


def get_offers(product_id):
    return product_dao.get_offers(product_id)



# get_product_details(1)