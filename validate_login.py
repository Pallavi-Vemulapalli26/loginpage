import sqlite3


def validate_user(user_name, password):

    conn = sqlite3.connect('logindb.db')

    cursor = conn.cursor()

    query = "SELECT * FROM logindetails WHERE username = ? AND password = ?"

    cursor.execute(query, (user_name, password))

    result = cursor.fetchone()

    print(result)

    cursor.close()

    conn.close()

    return result


def check_user_existence(user_name, password):

    result = validate_user(user_name, password)

    loginresult = None

    if result == None:
        loginresult = "Invalid username/password"
    else:
        loginresult = "Login Successful"

    return loginresult


def get_username_by_email(email):

    conn = sqlite3.connect("logindb.db")

    cursor = conn.cursor()

    query = "SELECT username FROM logindetails WHERE email = ?"

    cursor.execute(query, (email,))

    emailresult = cursor.fetchone()

    cursor.close()

    conn.close()

    return emailresult