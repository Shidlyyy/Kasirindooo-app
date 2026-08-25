import streamlit as st

st.set_page_config(page_title="Kasir Minimarket", page_icon="🛒", layout="centered")

# Custom CSS Background & Styling
st.markdown(
    """
    <style>
    /* Background utama */
    .stApp {
        background: linear-gradient(135deg, #e0c3fc 0%, #8ec5fc 100%);
        background-attachment: fixed;
    }
    
    /* Mengubah latar belakang form/card agar transparan memikat */
    div[data-testid="stForm"], .stDataFrame, div.stButton > button {
        border-radius: 12px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Daftar barang
BARANG = {
    "1": ("Mie Instan", 3500, "Makanan"),
    "2": ("Roti Tawar", 15000, "Makanan"),
    "3": ("Minyak Goreng 1L", 18000, "Makanan"),
    "4": ("Air Mineral 600ml", 3000, "Minuman"),
    "5": ("Susu UHT 250ml", 7000, "Minuman"),
    "6": ("Teh Botol 450ml", 4000, "Minuman"),
    "7": ("Keripik Kentang", 10000, "Snack"),
    "8": ("Cokelat Batangan", 12500, "Snack"),
    "9": ("Sabun Mandi", 4500, "Perawatan"),
    "10": ("Sampo Botol", 18500, "Perawatan")
}

if "keranjang" not in st.session_state:
    st.session_state.keranjang = []

st.title("🛒 Kasir Minimarket")

# Section 1: Pilih Barang
st.header("1. Pilih Barang")
kategori_list = ["Semua Kategori"] + sorted(list(set(v[2] for v in BARANG.values())))
kategori_terpilih = st.selectbox("Filter Kategori:", kategori_list)

opsi_barang = {}
for k, v in BARANG.items():
    nama, harga, kat = v
    if kategori_terpilih == "Semua Kategori" or kat == kategori_terpilih:
        opsi_barang[f"[{kat}] {nama} - Rp{harga:,}"] = k

pilihan = st.selectbox("Pilih Produk:", list(opsi_barang.keys()))
jumlah = st.number_input("Jumlah Beli:", min_value=1, value=1, step=1)

if st.button("➕ Tambah ke Keranjang", use_container_width=True):
    kode = opsi_barang[pilihan]
    nama, harga, _ = BARANG[kode]
    subtotal = harga * jumlah
    
    st.session_state.keranjang.append({
        "Nama": nama,
        "Harga (Rp)": harga,
        "Jumlah": jumlah,
        "Subtotal (Rp)": subtotal
    })
    st.toast(f"Ditambahkan: {jumlah}x {nama}", icon="✅")

# Section 2: Struk Belanja
if st.session_state.keranjang:
    st.divider()
    st.header("2. 🧾 Struk Belanja")
    
    st.dataframe(st.session_state.keranjang, use_container_width=True)
    
    total = sum(item["Subtotal (Rp)"] for item in st.session_state.keranjang)
    st.subheader(f"Total Belanja: Rp{total:,}")
    
    bayar = st.number_input("Jumlah Uang Bayar (Rp):", min_value=0, step=1000)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("💳 Proses Pembayaran", type="primary", use_container_width=True):
            if bayar >= total:
                kembalian = bayar - total
                st.balloons()
                st.success(f"**Pembayaran Berhasil!**\n\nKembalian: **Rp{kembalian:,}**")
            else:
                st.error(f"Uang kurang **Rp{total - bayar:,}**!")

    with col2:
        if st.button("🗑️ Transaksi Baru", use_container_width=True):
            st.session_state.keranjang = []
            st.rerun()