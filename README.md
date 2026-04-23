# 🚗 SISTEM MANAJEMEN KENDARAAN (VEHICLE MANAGER)

# IDENTITAS MAHASISWA
- **Nama:** Kristian Abel Baptista
- **NIM:** 220103129
- **Kelas:** TI22-A4
- **Keterangan:** Tugas Praktik Uji Kompetensi (Kelompok 3)

-----

# TEMA PROYEK
Aplikasi web untuk mengelola data kendaraan secara efisien, yang cocok digunakan dalam keperluan inventaris kendaraan, rental kendaraan, dan sebagainya.

# TEKNOLOGI YANG DIGUNAKAN
- Python + Streamlit (UI).
- MySQL via XAMPP/phpMyAdmin (Database).
- Bcrypt (Enkripsi Password).
- Streamlit Session State (Autentikasi).

# STRUKTUR FOLDER PROYEK
VehicleManager/
│
├── app.py            ← file tampilan utama Streamlit.
├── db.py             ← koneksi ke database.
├── auth.py           ← fungsi login dan session.
├── README.md         ← identitas dan penjelasan terkait proyek.
└── vehicles.py       ← fungsi CRUD kendaraan.

# FITUR APLIKASI
- Login dengan enkripsi password bcrypt.
- Sistem autentikasi berbasis Session.
- Halaman CRUD hanya bisa diakses setelah login.
- Tambah data kendaraan baru.
- Lihat semua data kendaraan.
- Edit dan hapus data kendaraan.
- Logout.

# CARA MENJALANKAN
1. Install XAMPP, lalu aktifkan Apache dan MySQL.
2. Import database `dbvm.sql` ke phpMyAdmin.
3. Install dependencies `pip install streamlit mysql-connector-python bcrypt`.
4. Jalankan di terminal `streamlit run app.py`.
5. Buka `http://localhost:8501` 
6. Login dengan username: `admin`, password: `admin`.