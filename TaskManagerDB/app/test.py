import sqlite3

conn = sqlite3.connect('test.db')

cur = conn.cursor()

var = cur.execute("SELECT * FROM route;")

data = cur.fetchall()

print(data)

var1 = cur.execute("SELECT name FROM route WHERE route.distance > 100")
routes = var1.fetchall()
print(routes)

var3 = cur.execute("SELECT r.distance * a.consumption as distance_consumption  FROM route r JOIN waybill w ON r.id = w.id_route JOIN auto a ON w.id_auto = a.id_auto;")
distance_consumption = var3.fetchall()
print(distance_consumption)

cur.close()
conn.close()


