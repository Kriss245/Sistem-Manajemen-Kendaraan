from db import get_connection

def get_all_vehicles():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM vehicles ORDER BY created_at DESC")
    vehicles = cursor.fetchall()
    cursor.close()
    conn.close()
    return vehicles

def add_vehicle(nama, merek, tahun, plat, status):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO vehicles (nama_kendaraan, merek, tahun, plat_nomor, status) VALUES (%s, %s, %s, %s, %s)",
                   (nama, merek, tahun, plat, status))
    conn.commit()
    cursor.close()
    conn.close()

def update_vehicle(id, nama, merek, tahun, plat, status):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE vehicles SET nama_kendaraan=%s, merek=%s, tahun=%s, plat_nomor=%s, status=%s WHERE id=%s",
                   (nama, merek, tahun, plat, status, id))
    conn.commit()
    cursor.close()
    conn.close()
    
def delete_vehicle(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM vehicles WHERE id=%s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    
def get_vehicle_by_id(id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM vehicles WHERE id=%s", (id,))
    vehicle = cursor.fetchone()
    cursor.close()
    conn.close()
    return vehicle