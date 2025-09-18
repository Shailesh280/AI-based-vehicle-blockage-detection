import sqlite3

def get_owner_by_vehicle(vehicle_number):
    conn = sqlite3.connect("vehicles.db")
    cursor = conn.cursor()
    cursor.execute("SELECT owner_name, email FROM vehicles WHERE number = ?", (vehicle_number,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {"owner": row[0], "email": row[1]}
    return None
