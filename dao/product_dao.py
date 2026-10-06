import sqlite3
DB = "logindb.db"


def get_offers(product_id):

    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row

    query = """
        SELECT
            ot.offer_type,
            (p.price * o.discount_percentage / 100)
                AS discount_amount
        FROM offer o
        JOIN offer_type ot
        ON o.offer_type_id = ot.id
        JOIN products p
        ON o.product_id = p.product_id
        WHERE o.product_id = ?
    """

    offers = conn.execute(
        query,
        (product_id,)
    ).fetchall()

    conn.close()

    return [dict(offer) for offer in offers]

def get_colors(product_id):
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row

    
    query = """
            SELECT  color_name  FROM product_color pc JOIN color c
 ON pc.color_id = c.color_id WHERE pc.product_id = ? ;
        """
    
    colors = conn.execute(
            query,
            (product_id,)
        ).fetchall()
    
    conn.close()
    return [dict(color) for color in colors]



def get_product_details(product_id):
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
        WHERE p.product_id = ?
    """

    product = conn.execute(
        query,
        (product_id,)
    ).fetchone()
    # print("DAO product:", dict(product) if product else None)

    conn.close()
    return dict(product) if product is not None else None    


# if __name__ == "__main__":
#     product_id = 1
#     result = get_product_details(product_id)
#     print("Final result:", result)