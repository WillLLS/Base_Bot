import sqlite3

con = sqlite3.connect('app/database/database.db')
cur = con.cursor()

# User Table
cur.execute("CREATE TABLE IF NOT EXISTS user (tm_id TEXT, tm_first_name TEXT, tm_username TEXT)")


con.commit()
con.close()