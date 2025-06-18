import sqlite3

conn = sqlite3.connect('to_do_data.db')

cur = conn.cursor()

var = cur.execute("SELECT * FROM task;")

data = cur.fetchall()

print(data)

cur.close()

conn.close()