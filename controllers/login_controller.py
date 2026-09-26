import sys
import sqlite3
import delete_user
import validate_login, re
import create_user 
import update_user
import delete_user
from flask import Flask, jsonify, request, render_template
from controllers.login_search_controller import search_users_db

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

from controllers.products_controller import product_bp
app.register_blueprint(product_bp)

if __name__ == '__main__':
    app.run(debug=True)