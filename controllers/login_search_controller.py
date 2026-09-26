import sqlite3

def search_users_db(search):

    conn = sqlite3.connect('logindb.db')
    cursor = conn.cursor()

    cursor.execute(
        "SELECT username FROM logindetails WHERE username LIKE ?",
        ('%' + search + '%',)
    )

    users = cursor.fetchall()

    conn.close()

    return users