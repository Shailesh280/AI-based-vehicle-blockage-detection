import sqlite3

conn = sqlite3.connect("vehicles.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE vehicles (
    number TEXT PRIMARY KEY,
    owner_name TEXT,
    email TEXT
)
""")
cursor.executemany("""
INSERT INTO vehicles (number, owner_name, email) VALUES (?, ?, ?)
""", [
    ("XX00XX0000", "Your_Name", "name@gmail.com")
])
conn.commit()
conn.close()
