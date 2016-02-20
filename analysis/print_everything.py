import sqlite3
import time




# connect to db
conn = sqlite3.connect('wifidata.db')
c = conn.cursor()

for row in c.execute("SELECT * FROM wifidata;"):
    print(row)

conn.close()

