import sqlite3


def update_user(user_id, new_user_name):
    conn = sqlite3.connect('logindb.db')
    cursor = conn.cursor()

    query = "UPDATE logindetails SET username = ? WHERE id = ?"

    cursor.execute(query, (new_user_name, user_id))
    conn.commit()

    result = cursor.rowcount

    cursor.close()
    conn.close()

    return result


def check_user_update(user_id, new_user_name):
    result = update_user(user_id, new_user_name)
    return result == 1