import sqlite3


def create_user(user_name, password, email):

    conn = sqlite3.connect('logindb.db')

    cursor = conn.cursor()

    query = "INSERT INTO logindetails (username, password,email) VALUES (?, ?, ?)"

    cursor.execute(query, (user_name, password, email))
    conn.commit()

    result = cursor.rowcount

    print(result)

    cursor.close()

    conn.close()

    return result
def check_user_creation(user_name,password,email):

    result = create_user(user_name,password,email)

    creationresult = None

    if result == 1:
        creationresult = True
    else:
        creationresult = False

    return creationresult








#     {
#     "user_name": "testuser",
#     "password": "test123",
#     "email": "testuser@gmail.com"
# }