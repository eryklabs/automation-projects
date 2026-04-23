import sqlite3

con = sqlite3.connect("float_tracker.db")
cur = con.cursor()

cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
print(cur.fetchall())

cur.execute("SELECT * FROM float_snapshots LIMIT 10")
print(cur.fetchall())