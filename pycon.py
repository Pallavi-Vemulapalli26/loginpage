import sqlite3

def get_user(user_name):
    conn = sqlite3.connect('logindb.db') 
    cursor = conn.cursor()
    query = "SELECT * FROM logindetails WHERE username = ?"
    
    cursor.execute(query, (user_name,))
    
    data = cursor.fetchone()
    print(data)
    
    cursor.close()
    conn.close()

get_user('ammu')
