import streamlit as st
from auth import login, logout, is_logged_in
from vehicles import get_all_vehicles, update_vehicle, delete_vehicle

st.set_page_config(page_title="Vehicle Manager", page_icon="🚗", layout="wide")

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

# ==== HALAMAN UTAMA ====
def show_dashboard():
    st.title("🚗 Vehicle Manager Dashboard")
    st.write(f"👤 Selamat datang, **{st.session_state['username']}!**")
    
    if st.button("Logout"):
        logout()
        st.success("Anda telah logout.")
        st.rerun()

    st.divider()
    
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
            from vehicles import add_vehicle
            add_vehicle(nama, merek, tahun, plat, status)
            st.success(f"Kendaraan {nama} berhasil ditambahkan!")
            st.rerun()
        else:
            st.warning("Semua field wajib diisi!")
            
    st.divider()
    
    #---- DAFTAR KENDARAAN ----
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
    
                #---- TOMBOL EDIT ----
                with st.form(f"edit_form_{vehicle['id']}"):
                    st.write("✏️ **Edit Kendaraan**")
                    col1, col2 = st.columns(2)
                    with col1:
                        nama = st.text_input("Nama Kendaraan", value=vehicle['nama_kendaraan'])
                        merek = st.text_input("Merek", value=vehicle['merek'])
                        tahun = st.number_input("Tahun", value=int (vehicle['tahun']))
                    with col2:
                        plat = st.text_input("Plat Nomor", value=vehicle['plat_nomor'])
                        status_list = ["tersedia", "digunakan", "servis"]
                        status = st.selectbox("Status", status_list, index=status_list.index(vehicle['status']))
                    submit = st.form_submit_button("💾 Simpan Perubahan")

                if submit:
                    update_vehicle(vehicle['id'], nama, merek, tahun, plat, status)
                    st.success(f"Data berhasil diperbarui!")
                    st.rerun()
                    
                #---- TOMBOL HAPUS ----
                if st.button(f"🗑️ Hapus Kendaraan", key=f"hapus_{vehicle['id']}"):
                    delete_vehicle(vehicle['id'])
                    st.warning(f"Kendaraan berhasil dihapus!")
                    st.rerun()

# ==== MAIN - CEK SESSION LOGIN ====
if is_logged_in():
    show_dashboard()
else:
    show_login_page()