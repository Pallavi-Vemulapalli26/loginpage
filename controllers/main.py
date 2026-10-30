import sys
import sqlite3
import delete_user
import validate_login, re
import create_user 
import update_user
import delete_user
from flask import Flask
from controllers.product_controller import search_products, get_colors as get_product_colors
from flask import Flask, jsonify, request, render_template
from controllers.login_search_controller import search_users_db
from services.product_details_service import get_product_details
from controllers.cart_controller import (
    add_to_cart,
    get_cart,
    update_cart,
    remove_cart_product,
)
from controllers.order_controller import place_order, get_order, get_orders
app = Flask(
    __name__,
    template_folder="../templates",
    static_folder="../static"
)
@app.route('/')
def home():
    return render_template('login.html')


@app.route('/create-user', methods=['POST'])
def create_user_api():
    data = request.get_json()

    # Safely extract a name parameter or default to "World"
    username = data.get("username")
    password = data.get("password")
    email = data.get("email")

    result = create_user.check_user_creation(username, password, email)

    if result:
        return "User created successfully", 201
    else:
        return "Failed to create user", 400



@app.route('/update-user', methods=['PUT'])
def update_user_api():
    data = request.get_json()

    user_id = data.get("id")
    new_username = data.get("new_username")

    result = update_user.check_user_update(user_id, new_username)

    if result:
        return "User updated successfully", 200
    else:
        return "Failed to update user", 404

    
@app.route('/delete-user', methods=['DELETE'])
def delete_user_api():
    data = request.get_json()

    user_id = data.get("id")

    result = delete_user.check_user_delete(user_id)

    if result:
        return "User deleted successfully", 200
    else:
        return "Failed to delete user", 404
    

    
@app.route('/Login', methods=['GET'])
def hello_world():

    Username = request.args.get('Username')
    Password = request.args.get('Password')

    if not Username or not Password:
        return "Username and password are required", 400

    pattern = r"^[a-zA-Z0-9]{3,8}$"

    # Validate using fullmatch
    if re.fullmatch(pattern, Username):
        result = validate_login.check_user_existence(Username, Password)
        return result, 200

    else:
        return "Invalid username (must contain only letters and numbers)", 400

   


# Forgot Username
@app.route('/forgot-username', methods=['GET'])
def forgot_username():

    Email = request.args.get('Email')

    result = validate_login.check_email_existance(Email)

    if result == None:
        result = ""

    return render_template('/forgotlogin.html', username=result)
    


@app.route('/all_users')
def users():
    conn = sqlite3.connect("logindb.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id, username, email
    FROM logindetails
""")

    users = cursor.fetchall()
    conn.close()

    users_json = [
        {
            'id': user[0],
            'username': user[1],
            'email': user[2]
        }
        for user in users
    ]

    return jsonify(users_json), 200

@app.route('/users')
def users_page():
    return render_template('get_all_users.html')


@app.route('/search-users')
def search_users():

    search = request.args.get('username', '')

    users = []

    if search:
        users = search_users_db(search)

    return render_template(
        'search_users.html',
        users=users,
        searched=bool(search)
    )


@app.route("/api/products", methods=["GET"])
def products():
    return search_products()
@app.route("/colors", methods=["GET"])
def colors():
    product_id = request.args.get("product_id")
    if not product_id:
        return jsonify({"error": "product_id is required"}), 400

    return get_product_colors(product_id)

@app.route("/products", methods=["GET"])
def products_page():
    return render_template("products.html")


@app.route("/api/product-details", methods=["GET"])
def product_details_api():
    product_id = request.args.get("product_id")
    if not product_id:
        return jsonify({"error": "product_id is required"}), 400

    product = get_product_details(product_id)
    if product is None:
        return jsonify({"error": "product not found"}), 404

    return jsonify(product)


@app.route("/product-details", methods=["GET"])
def product_details_page():
    return render_template("product_details.html")



@app.route("/api/cart/add", methods=["POST"])
def add_product_to_cart():
    data = request.get_json()

    user_id = data.get("user_id")
    product_id = data.get("product_id")

    result = add_to_cart(user_id, product_id)

    if result:
        return jsonify({"message": "Product added to cart"}), 200

    return jsonify({"error": "Unable to add product"}), 400

@app.route("/cart")
def cart_page():
    return render_template("cart.html")


@app.route("/api/cart", methods=["GET"])
def get_cart_api():
    user_id = request.args.get("user_id", type=int)

    if not user_id:
        return jsonify({"error": "user_id is required"}), 400

    return get_cart(user_id)

from controllers.order_controller import place_order, get_order, get_orders

@app.route("/api/cart/update", methods=["PUT"])
def update_cart_api():
    data = request.get_json()
    return update_cart(
        data["user_id"],
        data["product_id"],
        data["quantity"]
    )


@app.route("/api/cart/remove", methods=["DELETE"])
def remove_cart_api():
    data = request.get_json()
    return remove_cart_product(
        data["user_id"],
        data["product_id"]
    )


@app.route("/api/order/place", methods=["POST"])
def place_order_api():
    data = request.get_json()
    return place_order(
        data["user_id"],
        data["billing"],
        data["delivery"],
        data["payment_method"]
    )


@app.route("/api/orders/<int:user_id>")
def get_orders_api(user_id):
    return get_orders(user_id)


@app.route("/api/order/<int:order_id>/<int:user_id>")
def get_order_api(order_id, user_id):
    return get_order(order_id, user_id)

@app.route("/checkout")
def checkout_page():
    return render_template("checkout.html")

@app.route("/orders")
def orders_page():
    return render_template("order.html")

if __name__ == '__main__':
    app.run(debug=True)