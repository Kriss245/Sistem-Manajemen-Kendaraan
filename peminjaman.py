from db import get_connection

# READ - Ambil semua data peminjaman
def get_all_peminjaman():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT p.*, v.nama_kendaraan, v.plat_nomor 
        FROM peminjaman p
        JOIN vehicles v ON p.vehicle_id = v.id
        ORDER BY p.created_at DESC
    """)
    hasil = cursor.fetchall()
    conn.close()
    return hasil

# CREATE - Tambah peminjaman baru
def add_peminjaman(vehicle_id, nama_peminjam, tanggal_pinjam, tanggal_selesai, keterangan):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO peminjaman (vehicle_id, nama_peminjam, tanggal_pinjam, tanggal_selesai, keterangan)
        VALUES (%s, %s, %s, %s, %s)
    """, (vehicle_id, nama_peminjam, tanggal_pinjam, tanggal_selesai, keterangan))
    conn.commit()
    conn.close()

# UPDATE - Edit data peminjaman
def update_peminjaman(id, vehicle_id, nama_peminjam, tanggal_pinjam, tanggal_selesai, tanggal_kembali, status, keterangan):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE peminjaman
        SET vehicle_id=%s, nama_peminjam=%s, tanggal_pinjam=%s,
            tanggal_selesai=%s, tanggal_kembali=%s, status=%s, keterangan=%s
        WHERE id=%s
    """, (vehicle_id, nama_peminjam, tanggal_pinjam, tanggal_selesai, tanggal_kembali, status, keterangan, id))
    conn.commit()
    conn.close()

# DELETE - Hapus data peminjaman
def delete_peminjaman(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM peminjaman WHERE id=%s", (id,))
    conn.commit()
    conn.close()