import streamlit as st
from auth import login, logout, is_logged_in
from vehicles import get_all_vehicles, add_vehicle, update_vehicle, delete_vehicle
from peminjaman import get_all_peminjaman, add_peminjaman, update_peminjaman, delete_peminjaman

st.set_page_config(page_title="Vehicle Manager", page_icon="🚗", layout="wide")

st.markdown("""
    <style>
        [data-testid="stSidebar"] h1 {
            font-size: 20px !important;
            white-space: nowrap;
        }
    </style>
""", unsafe_allow_html=True)

# ==== HALAMAN LOGIN ====
def show_login_page():
    st.title("🚗 Vehicle Manager")
    st.subheader("Silakan Login. Masukkan username dan password Anda")

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")

    if submit:
        if login(username, password):
            st.success("Login berhasil!")
            st.rerun()
        else:
            st.error("Login gagal. Username atau password salah!")

# ==== HALAMAN DASHBOARD ====
def show_home():
    st.title("🏠 Dashboard Admin")
    st.write(f"Selamat datang, **{st.session_state['username']}!** 👋")
    st.divider()

    semua_kendaraan  = get_all_vehicles()
    semua_peminjaman = get_all_peminjaman()

    # Hitung status kendaraan
    tersedia  = len([k for k in semua_kendaraan if k['status'] == 'tersedia'])
    digunakan = len([k for k in semua_kendaraan if k['status'] == 'digunakan'])
    servis    = len([k for k in semua_kendaraan if k['status'] == 'servis'])

    # Hitung status peminjaman
    dipinjam = len([p for p in semua_peminjaman if p['status'] == 'dipinjam'])

    # ---- KARTU STATISTIK ----
    st.subheader("📊 Statistik")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Kendaraan", len(semua_kendaraan))
    col2.metric("Total Peminjaman", len(semua_peminjaman))
    col3.metric("Sedang Dipinjam", dipinjam)

    st.divider()

    col1, col2, col3 = st.columns(3)
    col1.metric("🟢 Tersedia", tersedia)
    col2.metric("🔵 Digunakan", digunakan)
    col3.metric("🔴 Servis", servis)

    st.divider()

    # ---- PEMINJAMAN AKTIF ----
    st.subheader("🔔 Peminjaman Aktif")
    aktif = [p for p in semua_peminjaman if p['status'] == 'dipinjam']
    if not aktif:
        st.info("Tidak ada peminjaman aktif saat ini.")
    else:
        for p in aktif:
            st.warning(f"🚘 **{p['nama_kendaraan']}** ({p['plat_nomor']}) — dipinjam oleh **{p['nama_peminjam']}** sejak {p['tanggal_pinjam']}")

# ==== HALAMAN KENDARAAN ====
def show_kendaraan():
    # Tampilkan pesan sukses kalau ada
    if 'pesan_kendaraan' in st.session_state:
        st.success(st.session_state['pesan_kendaraan'])
        del st.session_state['pesan_kendaraan']

    # ---- TAMBAH KENDARAAN ----
    st.subheader("➕ Tambah Kendaraan Baru")
    with st.form("add_vehicle_form"):
        col1, col2 = st.columns(2)
        with col1:
            nama = st.text_input("Nama Kendaraan")
            merek = st.text_input("Merek")
            tahun = st.number_input("Tahun", value=2026)
        with col2:
            plat = st.text_input("Plat Nomor")
            status = st.selectbox("Status", ["tersedia", "digunakan", "servis"])
        submit = st.form_submit_button("Tambah Kendaraan")

    if submit:
        if nama and merek and plat:
            add_vehicle(nama, merek, tahun, plat, status)
            st.session_state['pesan_kendaraan'] = f"Kendaraan {nama} berhasil ditambahkan!"
            st.rerun()
        else:
            st.warning("Semua field wajib diisi!")

    st.divider()

    # ---- DAFTAR KENDARAAN ----
    st.subheader("📋 Daftar Kendaraan")
    data = get_all_vehicles()

    if not data:
        st.info("Belum ada kendaraan yang terdaftar.")
    else:
        for vehicle in data:
            with st.expander(f"{vehicle['nama_kendaraan']} - {vehicle['plat_nomor']}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Merek:** {vehicle['merek']}")
                    st.write(f"**Tahun:** {vehicle['tahun']}")
                with col2:
                    st.write(f"**Plat Nomor:** {vehicle['plat_nomor']}")
                    st.write(f"**Status:** {vehicle['status']}")

                st.write("---")

                # ---- FORM EDIT ----
                with st.form(f"edit_form_{vehicle['id']}"):
                    st.write("✏️ **Edit Kendaraan**")
                    col1, col2 = st.columns(2)
                    with col1:
                        nama = st.text_input("Nama Kendaraan", value=vehicle['nama_kendaraan'])
                        merek = st.text_input("Merek", value=vehicle['merek'])
                        tahun = st.number_input("Tahun", value=int(vehicle['tahun']))
                    with col2:
                        plat = st.text_input("Plat Nomor", value=vehicle['plat_nomor'])
                        status_list = ["tersedia", "digunakan", "servis"]
                        status = st.selectbox("Status", status_list, index=status_list.index(vehicle['status']))
                    submit_edit = st.form_submit_button("💾 Simpan Perubahan")

                if submit_edit:
                    update_vehicle(vehicle['id'], nama, merek, tahun, plat, status)
                    st.session_state['pesan_kendaraan'] = "Data kendaraan berhasil diperbarui!"
                    st.rerun()

                # ---- TOMBOL HAPUS ----
                if st.button("🗑️ Hapus Kendaraan", key=f"hapus_{vehicle['id']}"):
                    delete_vehicle(vehicle['id'])
                    st.session_state['pesan_kendaraan'] = "Kendaraan berhasil dihapus!"
                    st.rerun()

# ==== HALAMAN PEMINJAMAN ====
def show_peminjaman():
    # Tampilkan pesan sukses kalau ada
    if 'pesan_peminjaman' in st.session_state:
        st.success(st.session_state['pesan_peminjaman'])
        del st.session_state['pesan_peminjaman']

    # ---- TAMBAH PEMINJAMAN ----
    st.subheader("➕ Tambah Peminjaman Baru")

    kendaraan_list    = get_all_vehicles()
    kendaraan_options = {f"{k['nama_kendaraan']} - {k['plat_nomor']}": k['id'] for k in kendaraan_list}

    with st.form("add_pinjam_form"):
        col1, col2 = st.columns(2)
        with col1:
            pilih_kendaraan = st.selectbox("Pilih Kendaraan", list(kendaraan_options.keys()))
            nama_peminjam   = st.text_input("Nama Peminjam")
        with col2:
            tanggal_pinjam  = st.date_input("Tanggal Pinjam")
            tanggal_selesai = st.date_input("Tanggal Selesai")
            keterangan      = st.text_area("Keterangan")
        submit = st.form_submit_button("Tambah Peminjaman")

    if submit:
        if nama_peminjam:
            if tanggal_selesai <= tanggal_pinjam:
                st.warning("Tanggal selesai harus setelah tanggal pinjam!")
            else:
                vehicle_id = kendaraan_options[pilih_kendaraan]
                add_peminjaman(vehicle_id, nama_peminjam, tanggal_pinjam, tanggal_selesai, keterangan)
                st.session_state['pesan_peminjaman'] = f"Peminjaman atas nama {nama_peminjam} berhasil ditambahkan!"
                st.rerun()
        else:
            st.warning("Nama peminjam wajib diisi!")

    st.divider()

    # ---- DAFTAR PEMINJAMAN ----
    st.subheader("📋 Daftar Peminjaman")
    data = get_all_peminjaman()

    if not data:
        st.info("Belum ada data peminjaman.")
    else:
        for pinjam in data:
            with st.expander(f"{pinjam['nama_peminjam']} - {pinjam['nama_kendaraan']} ({pinjam['plat_nomor']})"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Kendaraan:** {pinjam['nama_kendaraan']}")
                    st.write(f"**Plat Nomor:** {pinjam['plat_nomor']}")
                    st.write(f"**Tanggal Pinjam:** {pinjam['tanggal_pinjam']}")
                    st.write(f"**Tanggal Selesai:** {pinjam['tanggal_selesai']}")
                with col2:
                    st.write(f"**Tanggal Kembali:** {pinjam['tanggal_kembali'] or '-'}")
                    st.write(f"**Status:** {pinjam['status']}")
                    st.write(f"**Keterangan:** {pinjam['keterangan'] or '-'}")

                st.write("---")

                # ---- FORM EDIT ----
                with st.form(f"edit_pinjam_{pinjam['id']}"):
                    st.write("✏️ **Edit Peminjaman**")
                    col1, col2 = st.columns(2)
                    with col1:
                        e_kendaraan   = st.selectbox("Kendaraan", list(kendaraan_options.keys()))
                        e_nama        = st.text_input("Nama Peminjam", value=pinjam['nama_peminjam'])
                        e_tgl_pinjam  = st.date_input("Tanggal Pinjam", value=pinjam['tanggal_pinjam'])
                    with col2:
                        e_tgl_selesai = st.date_input("Tanggal Selesai", value=pinjam['tanggal_selesai'])
                        e_tgl_kembali = st.date_input("Tanggal Kembali", value=pinjam['tanggal_kembali'])
                        status_list   = ["dipinjam", "dikembalikan"]
                        e_status      = st.selectbox("Status", status_list, index=status_list.index(pinjam['status']))
                        e_keterangan  = st.text_area("Keterangan", value=pinjam['keterangan'] or '')
                    submit_edit = st.form_submit_button("💾 Simpan Perubahan")

                if submit_edit:
                    e_vehicle_id = kendaraan_options[e_kendaraan]
                    update_peminjaman(pinjam['id'], e_vehicle_id, e_nama, e_tgl_pinjam, e_tgl_selesai, e_tgl_kembali, e_status, e_keterangan)
                    st.session_state['pesan_peminjaman'] = "Data peminjaman berhasil diperbarui!"
                    st.rerun()

                # ---- TOMBOL HAPUS ----
                if st.button("🗑️ Hapus Peminjaman", key=f"hapus_pinjam_{pinjam['id']}"):
                    delete_peminjaman(pinjam['id'])
                    st.session_state['pesan_peminjaman'] = "Data peminjaman berhasil dihapus!"
                    st.rerun()

# ==== SIDEBAR & ROUTING ====
def show_dashboard():
    with st.sidebar:
        st.title("🚗 Vehicle Manager")
        st.write(f"👤 **{st.session_state['username']}**")
        st.divider()
        menu = st.radio("Navigasi", ["🏠 Dashboard", "🚘 Kendaraan", "📋 Peminjaman"])
        st.divider()
        if st.button("Logout"):
            logout()
            st.rerun()

    if menu == "🏠 Dashboard":
        show_home()
    elif menu == "🚘 Kendaraan":
        st.title("🚘 Manajemen Kendaraan")
        show_kendaraan()
    elif menu == "📋 Peminjaman":
        st.title("📋 Manajemen Peminjaman")
        show_peminjaman()

# ==== MAIN - CEK SESSION LOGIN ====
if is_logged_in():
    show_dashboard()
else:
    show_login_page()