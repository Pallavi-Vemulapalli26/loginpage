import sqlite3


def delete_user(user_id):
    conn = sqlite3.connect('logindb.db')
    cursor = conn.cursor()

    query = "DELETE FROM logindetails WHERE id = ?"

    cursor.execute(query, (user_id,))
    conn.commit()

    result = cursor.rowcount

    cursor.close()
    conn.close()

    return result


def check_user_delete(user_id):
    result = delete_user(user_id)
    return result == 1