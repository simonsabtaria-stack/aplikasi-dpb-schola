import streamlit as st
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm
import io
import requests  
import google.generativeai as genai

# Impor Database Internal
from data_kurikulum import bank_kurikulum
from data_sfd import bank_sfd
from data_kko import bank_kko

st.set_page_config(page_title="DPB Schola Amoris", page_icon="📝", layout="wide")

st.image("banner_schola.png", use_container_width=True)
st.title("Penyusun DPB Schola Amoris 🎓")
st.markdown("*Rancangan yang Anda buat akan otomatis tercatat di Katalog Bank Modul Sekolah.*")
st.divider()

URL_DATABASE = "https://script.google.com/macros/s/AKfycbyi9lnZJplhJDHV9RkkGq8mmILR7zIn7XfNTLN8Qf49XJuyRr8H5LAgr-vlrP6gyDnfjw/exec"

# --- SIDEBAR MEWAH ---
with st.sidebar:
    st.header("🤖 Pusat Kontrol AI")
    api_key_guru = st.text_input("🔑 Kunci API Gemini:", type="password", help="Dapatkan API Key dari Google AI Studio")
    st.divider()
    st.subheader("⚙️ Kustomisasi Gaya AI")
    instruksi_khusus = st.text_area("Instruksi Tambahan (Opsional):", placeholder="Contoh: Fokuskan pada metode diskusi kelompok untuk anak kinestetik.", help="Perintah di sini akan selalu ditaati oleh AI di semua tab.")
    
    st.divider()
    st.markdown("**Status Sistem:**")
    if api_key_guru:
        st.success("✅ AI Terhubung")
    else:
        st.error("❌ API Key Belum Diisi")

st.markdown("""
    <style>
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { background-color: #f1f5f9; border-radius: 8px 8px 0px 0px; padding: 10px 20px; box-shadow: inset 0 -2px 0 0 #cbd5e1; transition: all 0.3s ease; }
    .stTabs [aria-selected="true"] { background-color: #1e293b; color: #ffffff !important; box-shadow: 0 -4px 10px rgba(0,0,0,0.1); }
    .stTabs [data-baseweb="tab"]:hover { background-color: #e2e8f0; }
    .stTextInput input, .stTextArea textarea, .stSelectbox [data-baseweb="select"] { border-radius: 8px !important; border: 1px solid #e2e8f0 !important; transition: all 0.3s ease; }
    .stTextInput input:focus, .stTextArea textarea:focus { border-color: #3b82f6 !important; box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2) !important; }
    .stButton > button[kind="primary"] { border-radius: 8px; background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%); color: white; border: none; box-shadow: 0 4px 10px rgba(37, 99, 235, 0.3); transition: transform 0.2s, box-shadow 0.2s; }
    .stButton > button[kind="primary"]:hover { transform: translateY(-2px); box-shadow: 0 6px 15px rgba(37, 99, 235, 0.4); }
    </style>
""", unsafe_allow_html=True)

# --- INISIALISASI MEMORI ---
if 'data_isian' not in st.session_state: st.session_state.data_isian = {}
if 'draft_kognitif' not in st.session_state: st.session_state.draft_kognitif = ""
if 'draft_psikomotor' not in st.session_state: st.session_state.draft_psikomotor = ""
if 'draft_afektif' not in st.session_state: st.session_state.draft_afektif = ""
if 'draft_tp_kognitif' not in st.session_state: st.session_state.draft_tp_kognitif = ""
if 'draft_tp_psikomotor' not in st.session_state: st.session_state.draft_tp_psikomotor = ""
if 'draft_tp_afektif' not in st.session_state: st.session_state.draft_tp_afektif = ""

def simpan_teks(kunci, nilai):
    st.session_state.data_isian[kunci] = nilai

# --- FUNGSI AI ANTI-ERROR ---
def panggil_ai(prompt):
    genai.configure(api_key=api_key_guru)
    mesin_tersedia = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    mesin_flash = [m for m in mesin_tersedia if 'flash' in m.lower() and 'interactions' not in m.lower()]
    if not mesin_flash: raise Exception("API Key tidak memiliki akses ke model Flash.")
    nama_mesin = next((m for m in mesin_flash if '1.5' in m), mesin_flash[0])
    aturan = "\n\nATURAN FORMAT: Gunakan kalimat efektif, hindari UPPERCASE, gunakan list poin biasa tanpa simbol markdown rumit."
    if instruksi_khusus: aturan += f"\nINSTRUKSI KHUSUS GURU: {instruksi_khusus}"
    model = genai.GenerativeModel(nama_mesin)
    return model.generate_content(prompt + aturan).text

# --- SISTEM INDIKATOR PROGRES (NEW) ---
kunci_wajib = ['Nama_Guru', 'MAPEL', 'Materi', 'Capaian_Pembelajaran', 'TP_KOGNITIF', 'TP_Psikomotorik', 'TP_Afektif']
terisi = sum(1 for k in kunci_wajib if st.session_state.data_isian.get(k) and str(st.session_state.data_isian.get(k)).strip() != "")
progres_persen = int((terisi / len(kunci_wajib)) * 100)

st.markdown(f"**📈 Progres Penyusunan DPB: {progres_persen}%**")
st.progress(progres_persen)
st.write("") # Spasi kosong

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📋 1. Identitas", "🏫 2. Lingkungan", "🧠 3. Kognitif", "❤️ 4. Afektif", "🖨️ 5. Pratinjau & Cetak"
])

# ================= TAB 1 =================
with tab1:
    with st.container(border=True): # --- KARTU 1 ---
        st.subheader("A. Identitas Guru & Jenjang")
        simpan_teks('Nama_Guru', st.text_input("Nama Guru Penyusun (Wajib diisi):", help="Ketikkan nama lengkap beserta gelar untuk dicetak di modul."))
        
        col1, col2, col3, col4 = st.columns(4)
        with col1: simpan_teks('Jenjang', st.selectbox("Jenjang:", ["Pilih...", "TK", "SD", "SMP", "SMA/SMK"], help="Pilih jenjang untuk menyesuaikan Capaian Nilai SFD nanti."))
        with col2: simpan_teks('Fase', st.selectbox("Fase:", ["-", "Fase Fondasi", "Fase A", "Fase B", "Fase C", "Fase D", "Fase E", "Fase F"]))
        with col3: simpan_teks('Kelas', st.text_input("Kelas (Contoh: 1, 2, VII):"))
        with col4: simpan_teks('Semester', st.selectbox("Semester:", ["Ganjil", "Genap"]))
            
        foto_sdgs = st.file_uploader("Upload Logo SDGs (Opsional)", type=['png', 'jpg', 'jpeg'], help="Unggah ikon SDGs yang sesuai untuk disematkan di pojok dokumen.")

    with st.container(border=True): # --- KARTU 2 ---
        st.subheader("B. Data Umum & Konten")
        daftar_mapel = list(bank_kurikulum.keys())
        mapel_terpilih = st.selectbox("Mata Pelajaran:", daftar_mapel)
        simpan_teks('MAPEL', mapel_terpilih)
        
        c_elemen, c_materi = st.columns(2)
        with c_elemen:
            daftar_elemen = bank_kurikulum[mapel_terpilih]
            elemen_terpilih = st.selectbox(f"Elemen ({mapel_terpilih}):", daftar_elemen)
            simpan_teks('Elemen', elemen_terpilih)
        with c_materi:
            materi_terpilih = st.text_input("Materi Esensial:", help="Topik inti yang akan dipelajari siswa.")
            simpan_teks('Materi', materi_terpilih)
            
        simpan_teks('Judul', st.text_input("Judul Modul:"))
    
    with st.container(border=True): # --- KARTU 3 ---
        st.subheader("🎯 Capaian Pembelajaran & Target SDGs")
        cp_input = st.text_area("1. Capaian Pembelajaran (CP):", height=120, help="Salin CP dari dokumen standar kurikulum nasional berdasarkan Fase.")
        simpan_teks('Capaian_Pembelajaran', cp_input)
        
        opsi_sdgs = [
            "Pilih...", "1. Tanpa Kemiskinan", "2. Tanpa Kelaparan", "3. Kehidupan Sehat dan Sejahtera", 
            "4. Pendidikan Berkualitas", "5. Kesetaraan Gender", "6. Air Bersih dan Sanitasi Layak", 
            "7. Energi Bersih dan Terjangkau", "8. Pekerjaan Layak dan Pertumbuhan Ekonomi", 
            "9. Industri, Inovasi dan Infrastruktur", "10. Berkurangnya Kesenjangan", 
            "11. Kota dan Permukiman yang Berkelanjutan", "12. Konsumsi dan Produksi yang Bertanggung Jawab", 
            "13. Penanganan Perubahan Iklim", "14. Ekosistem Lautan", "15. Ekosistem Daratan", 
            "16. Perdamaian, Keadilan dan Kelembagaan yang Tangguh", "17. Kemitraan untuk Mencapai Tujuan"
        ]
        pilihan_sdgs = st.selectbox("2. Capaian SDGs:", opsi_sdgs, help="Pilih 1 dari 17 Tujuan Pembangunan Berkelanjutan global.")
        simpan_teks('Capaian_SDGs', pilihan_sdgs if pilihan_sdgs != "Pilih..." else "")
        
        tp_sdgs_input = st.text_area("3. Tujuan Pembelajaran (TP) SDGs:", height=100, help="Rumuskan bagaimana materi ini berkontribusi pada target SDGs yang dipilih.")
        simpan_teks('TP_SDGs', tp_sdgs_input)

# ================= TAB 2 =================
with tab2:
    with st.container(border=True): # --- KARTU 1 ---
        st.subheader("Lingkungan & Praktik Pembelajaran")
        
        col_mitra, col_peda = st.columns(2)
        with col_mitra:
            opsi_mitra = ["Pilih...", "Orang Tua/Wali Murid", "Komunitas Lokal", "Pakar/Praktisi", "Instansi Pemerintah/Puskesmas", "Lembaga Swadaya Masyarakat (LSM)", "Lainnya"]
            pilihan_mitra = st.selectbox("Kemitraan Pembelajaran:", opsi_mitra)
            simpan_teks('Kemitraan_Pembelajaran', st.text_input("Ketik Detail Kemitraan:") if pilihan_mitra == "Lainnya" else pilihan_mitra)
        
        with col_peda:
            opsi_pedagogis = ["Pilih...", "Problem Based Learning (PBL)", "Project Based Learning (PjBL)", "Inquiry/Discovery Learning", "Teaching at the Right Level (TaRL)", "Cooperative Learning", "Lainnya"]
            pilihan_pedagogis = st.selectbox("Praktik Pedagogis (Model Belajar):", opsi_pedagogis)
            simpan_teks('Praktik_Pedagogis', st.text_input("Ketik Model Pedagogis:") if pilihan_pedagogis == "Lainnya" else pilihan_pedagogis)
        
        opsi_budaya = ["Pilih...", "Disiplin Positif & Restitusi", "Growth Mindset (Pola Pikir Berkembang)", "Kolaboratif & Inklusif", "Pembelajaran Berbasis Umpan Balik (Feedback)", "Lainnya"]
        pilihan_budaya = st.selectbox("Budaya Belajar:", opsi_budaya)
        simpan_teks('Budaya_Belajar', st.text_input("Ketik Budaya Belajar:") if pilihan_budaya == "Lainnya" else pilihan_budaya)

    with st.container(border=True): # --- KARTU 2 ---
        simpan_teks('Urutan_Sintkas', st.text_area("Urutan Sintaks Pembelajaran:", height=120, help="Langkah-langkah operasional dari model pedagogis yang dipilih."))
        
        col_fisik, col_virtual = st.columns(2)
        with col_fisik: simpan_teks('Ruang_Fisik', st.text_area("Ruang Fisik:", help="Contoh: Kelas dengan meja melingkar, laboratorium, taman."))
        with col_virtual: simpan_teks('Ruang_Virtual', st.text_area("Ruang Virtual:", help="Contoh: Google Classroom, Grup WhatsApp, Zoom."))

# ================= TAB 3 =================
with tab3:
    with st.container(border=True): # --- KARTU KOGNITIF ---
        st.subheader("🧠 Aspek Kognitif")
        with st.expander("💡 Buka Contekan KKO Kognitif (C1-C6)"):
            for level, kata in bank_kko["KOGNITIF (C)"].items():
                st.markdown(f"**{level}**: {kata}")
                
        if st.button("📈 Rumuskan TP Kognitif (Otomatis Naik Level KKO)", key="btn_tp_kog", use_container_width=True):
            if not api_key_guru: st.warning("⚠️ Masukkan Kunci API di Sidebar terlebih dahulu!")
            else:
                with st.spinner("Menganalisis KKO CP dan menaikkan level..."):
                    try:
                        prompt_tp_kog = f"Baca Capaian Pembelajaran ini: '{cp_input}'. Identifikasi level KKO kognitifnya (C1-C6). Kemudian, buatkan rumusan Tujuan Pembelajaran (TP) Kognitif yang menaikkan KKO-nya 1 atau 2 level lebih tinggi agar lebih menantang (HOTS). Integrasikan dengan semangat TP SDGs: '{tp_sdgs_input}'. Berikan 2 pilihan rumusan singkat."
                        st.session_state['draft_tp_kognitif'] = panggil_ai(prompt_tp_kog)
                    except Exception as e: st.error(e)

        tp_kognitif = st.text_area("TP Kognitif:", value=st.session_state['draft_tp_kognitif'], height=100)
        simpan_teks('TP_KOGNITIF', tp_kognitif)
        
        indikator_kognitif = st.text_area("Indikator Kognitif:", help="Turunan dari TP Kognitif yang bisa diukur pencapaiannya.")
        simpan_teks('Indikator_Kognitif', indikator_kognitif)
        
        if st.button("✨ Rumuskan Pengalaman Kognitif (AI)", key="btn_kog", use_container_width=True):
            if not api_key_guru: st.warning("⚠️ Masukkan Kunci API di Sidebar terlebih dahulu!")
            else:
                with st.spinner("Merancang aktivitas kognitif..."):
                    try:
                        konteks = f"Materi: {materi_terpilih}\nCP: {cp_input}\n"
                        prompt = f"Berdasarkan {konteks}, buat skenario 'Pengalaman Belajar' (Kegiatan Inti) untuk mencapai indikator: {indikator_kognitif}. Buat aktivitas eksplorasi dalam 3-4 poin praktis."
                        st.session_state.draft_kognitif = panggil_ai(prompt)
                    except Exception as e: st.error(e)
                        
        simpan_teks('Pengalaman_Belajar', st.text_area("Pengalaman Belajar Kognitif:", value=st.session_state.draft_kognitif, height=120))
        
        c1, c2 = st.columns(2)
        with c1: simpan_teks('Asesmen_Formatif', st.text_area("Asesmen Formatif (Kognitif):"))
        with c2: simpan_teks('Asesmen_Sumatif', st.text_area("Asesmen Sumatif (Kognitif):"))

    with st.container(border=True): # --- KARTU PSIKOMOTORIK ---
        st.subheader("🏃 Aspek Psikomotorik")
        with st.expander("💡 Buka Contekan KKO Psikomotorik (P1-P5)"):
            for level, kata in bank_kko["PSIKOMOTORIK (P)"].items():
                st.markdown(f"**{level}**: {kata}")

        if st.button("📈 Rumuskan TP Psikomotorik (Otomatis Naik Level KKO)", key="btn_tp_psi", use_container_width=True):
            if not api_key_guru: st.warning("⚠️ Masukkan Kunci API di Sidebar!")
            else:
                with st.spinner("Menganalisis KKO CP dan menaikkan level..."):
                    try:
                        prompt_tp_psi = f"Baca Capaian Pembelajaran ini: '{cp_input}'. Identifikasi level KKO psikomotoriknya (P1-P5). Kemudian, buatkan rumusan Tujuan Pembelajaran (TP) Psikomotorik yang menaikkan KKO-nya 1 atau 2 level lebih tinggi. Integrasikan dengan semangat TP SDGs: '{tp_sdgs_input}'. Berikan 2 pilihan rumusan singkat."
                        st.session_state['draft_tp_psikomotor'] = panggil_ai(prompt_tp_psi)
                    except Exception as e: st.error(e)

        tp_psikomotorik = st.text_area("TP Psikomotorik:", value=st.session_state['draft_tp_psikomotor'], height=100)
        simpan_teks('TP_Psikomotorik', tp_psikomotorik)
        
        indikator_psikomotorik = st.text_area("Indikator Psikomotorik:")
        simpan_teks('Indikator_Psikomotorik', indikator_psikomotorik)
        
        if st.button("✨ Rumuskan Pengalaman Psikomotorik (AI)", key="btn_psi", use_container_width=True):
            if not api_key_guru: st.warning("⚠️ Masukkan Kunci API di Sidebar!")
            else:
                with st.spinner("Merancang aktivitas psikomotorik..."):
                    try:
                        konteks = f"Materi: {materi_terpilih}\nCP: {cp_input}\nKegiatan Kognitif Sebelumnya: {st.session_state.draft_kognitif}\n"
                        prompt = f"Berdasarkan {konteks}, buat skenario unjuk kerja/proyek untuk mencapai indikator psikomotorik: {indikator_psikomotorik}. Tuliskan dalam 3-4 poin praktis."
                        st.session_state.draft_psikomotor = panggil_ai(prompt)
                    except Exception as e: st.error(e)

        simpan_teks('Pengalaman_Belajar_Psikomotorik', st.text_area("Pengalaman Belajar Psikomotorik:", value=st.session_state.draft_psikomotor, height=120))
        c3, c4 = st.columns(2)
        with c3: simpan_teks('Asesmen_Formatif_Psikomotorik', st.text_area("Asesmen Formatif (Psikomotorik):"))
        with c4: simpan_teks('Asesmen_Sumatif_Psikomotorik', st.text_area("Asesmen Sumatif (Psikomotorik):"))

# ================= TAB 4 =================
with tab4:
    with st.container(border=True): # --- KARTU IDENTITAS KARAKTER ---
        st.subheader("A. Identitas Karakter & Nilai Yayasan")
        col_kiri, col_kanan = st.columns(2)
        
        with col_kiri:
            st.markdown("##### 1. Profil Pelajar Pancasila (P3)")
            opsi_p3 = ["Pilih...", "Beriman & Bertakwa", "Berkebinekaan Global", "Bergotong Royong", "Mandiri", "Bernalar Kritis", "Kreatif", "Lainnya"]
            pilihan_p3 = st.selectbox("Dimensi P3:", opsi_p3)
            simpan_teks('Dimensi', st.text_input("Ketik Dimensi P3:") if pilihan_p3 == "Lainnya" else pilihan_p3)
            simpan_teks('Elemen', st.text_input("Elemen P3:"))
            simpan_teks('Sub_elemen', st.text_input("Sub Elemen P3:"))
            cp_p3 = st.text_area("Capaian P3:")
            simpan_teks('Capaian_P3', cp_p3)
            
            st.divider()
            st.markdown("##### 2. Santo / Santa Pelindung")
            opsi_santo = ["Pilih...", "Santo Fransiskus Asisi", "Santa Clara", "Santa Maria", "Lainnya"]
            pilihan_santo = st.selectbox("Pilih Pelindung:", opsi_santo)
            simpan_teks('Santo_Santa_Pelindung', st.text_input("Ketik Nama Pelindung:") if pilihan_santo == "Lainnya" else pilihan_santo)

        with col_kanan:
            st.markdown("##### 3. Kearifan Lokal")
            opsi_kearifan = ["Pilih...", "Belum Bahadat", "Huma Betang", "Handep", "Lainnya"]
            pilihan_kearifan = st.selectbox("Pilih Kearifan Lokal:", opsi_kearifan)
            kearifan_input = st.text_input("Ketik Kearifan Lokal:") if pilihan_kearifan == "Lainnya" else pilihan_kearifan
            simpan_teks('Kearifan_Lokal', kearifan_input)
            
            st.divider()
            st.markdown("##### 4. 7 Kebiasaan Anak Indonesia Hebat")
            opsi_7kaih = ["Pilih...", "Bermasyarakat", "Jadilah Proaktif", "Mulai dengan Tujuan Akhir", "Dahulukan yang Utama", "Berpikir Menang-Menang", "Sinergi", "Lainnya"]
            pilihan_7kaih = st.selectbox("Pilih 7KAIH:", opsi_7kaih)
            simpan_teks('KAIH', st.text_input("Ketik 7KAIH:") if pilihan_7kaih == "Lainnya" else pilihan_7kaih)
            
            st.divider()
            st.markdown("##### 5. Dimensi Profil Lulusan")
            opsi_profil = ["Pilih...", "Kewargaan", "Cerdas Intelektual", "Tangguh Berkarakter", "Lainnya"]
            pilihan_profil = st.selectbox("Profil Lulusan:", opsi_profil)
            simpan_teks('Dimensi_Lulusan', st.text_input("Ketik Profil:") if pilihan_profil == "Lainnya" else pilihan_profil)
            simpan_teks('Sub_Dimensi', st.text_input("Sub Dimensi:"))
            simpan_teks('Kompetensi', st.text_input("Kompetensi Lulusan:"))

    with st.container(border=True): # --- KARTU CORE VALUES ---
        st.subheader("B. Core Values / Ke-SFD-an")
        st.info("💡 Capaian Nilai (CN) otomatis menyesuaikan Jenjang dan Keutamaan yang dipilih.")
        
        jenjang_terpilih = st.session_state.data_isian.get('Jenjang', '')
        col_nilai, col_keutamaan = st.columns(2)
        
        with col_nilai:
            daftar_nilai = list(bank_sfd.keys())
            pilihan_nilai = st.selectbox("1. Pilih Nilai Ke-SFD-an:", ["Pilih..."] + daftar_nilai)
            
        if pilihan_nilai != "Pilih...":
            simpan_teks('Nilai', pilihan_nilai)
            with col_keutamaan:
                daftar_keutamaan = list(bank_sfd[pilihan_nilai].keys())
                pilihan_keutamaan = st.selectbox("2. Pilih Keutamaan:", ["Pilih..."] + daftar_keutamaan)
                
            if pilihan_keutamaan != "Pilih...":
                simpan_teks('Keutamaan', pilihan_keutamaan)
                if jenjang_terpilih in ["TK", "SD", "SMP"]:
                    teks_cn_otomatis = bank_sfd[pilihan_nilai][pilihan_keutamaan].get(jenjang_terpilih, "Data tidak ditemukan.")
                elif jenjang_terpilih == "SMA/SMK":
                    teks_cn_otomatis = "Capaian Nilai (CN) Ke-SFD-an untuk jenjang SMA saat ini masih dalam tahap perumusan oleh Yayasan."
                else:
                    teks_cn_otomatis = "⚠️ Silakan kembali ke Tab 1 dan pilih Jenjang (TK/SD/SMP/SMA) terlebih dahulu."
                
                cn_input = st.text_area("3. Capaian Nilai (Otomatis Terisi & Bisa Diedit):", value=teks_cn_otomatis, height=120)
                simpan_teks('Capaian_Nilai', cn_input)
        else:
            simpan_teks('Nilai', "")
            simpan_teks('Keutamaan', "")
            simpan_teks('Capaian_Nilai', "")

    with st.container(border=True): # --- KARTU RENCANA AFEKTIF ---
        st.subheader("❤️ C. Rencana Pembelajaran Afektif")
        with st.expander("💡 Buka Contekan KKO Afektif (A1-A5)"):
            for level, kata in bank_kko["AFEKTIF (A)"].items():
                st.markdown(f"**{level}**: {kata}")

        if st.button("📈 Rumuskan TP Afektif (Sintesis & Naik Level)", key="btn_tp_afe", use_container_width=True):
            if not api_key_guru: st.warning("⚠️ Masukkan Kunci API di Sidebar!")
            else:
                with st.spinner("Mereduksi nilai dan menaikkan level KKO..."):
                    try:
                        sfd_cn = st.session_state.data_isian.get('Capaian_Nilai', '')
                        prompt_tp_afe = f"Saya memiliki elemen afektif: P3 ({cp_p3}), Nilai SFD ({sfd_cn}), dan Kearifan Lokal ({kearifan_input}). Identifikasi level KKO afektif (A1-A5) pada Nilai SFD tersebut. Tolong reduksi/sintesis elemen-elemen ini menjadi satu rumusan Tujuan Pembelajaran (TP) Afektif yang kuat, dengan menaikkan level KKO satu tingkat lebih tinggi. Jadikan 1 paragraf padu yang elegan."
                        st.session_state['draft_tp_afektif'] = panggil_ai(prompt_tp_afe)
                    except Exception as e: st.error(e)

        tp_afektif = st.text_area("TP Afektif:", value=st.session_state['draft_tp_afektif'], height=120)
        simpan_teks('TP_Afektif', tp_afektif)
        indikator_afektif = st.text_area("Indikator Afektif:")
        simpan_teks('Indikator_Afektif', indikator_afektif)
        
        if st.button("✨ Rumuskan Pengalaman Afektif (AI)", key="btn_afe", use_container_width=True):
            if not api_key_guru: st.warning("⚠️ Masukkan Kunci API di Sidebar!")
            else:
                with st.spinner("Merancang aktivitas karakter..."):
                    try:
                        konteks = f"Materi: {materi_terpilih}\nKognitif: {st.session_state.draft_kognitif}\nPsikomotorik: {st.session_state.draft_psikomotor}\n"
                        prompt = f"Berdasarkan {konteks}, rancang 'Pengalaman Belajar' afektif (sikap/karakter) untuk indikator: {indikator_afektif}. Buat aktivitas reflektif/empati dalam 3-4 poin praktis yang selaras dengan kegiatan sebelumnya."
                        st.session_state.draft_afektif = panggil_ai(prompt)
                    except Exception as e: st.error(e)

        simpan_teks('Pengalaman_Belajar_Afektif', st.text_area("Pengalaman Belajar Afektif:", value=st.session_state.draft_afektif, height=150))
        c11, c12 = st.columns(2)
        with c11: simpan_teks('Formatif', st.text_area("Asesmen Formatif (Afektif):"))
        with c12: simpan_teks('Sumatif', st.text_area("Asesmen Sumatif (Afektif):"))

# ================= TAB 5 =================
with tab5:
    with st.container(border=True): # --- KARTU PERAYAAN BELAJAR ---
        st.subheader("Perayaan Belajar & Media")
        simpan_teks('Membagikan_Pengalaman_Belajar', st.text_area("Membagikan Pengalaman Belajar:", help="Bagaimana siswa merayakan hasil belajarnya? (Contoh: Pameran karya, presentasi, mading)."))
        simpan_teks('Refleksi_Perkembangan_Kompetensi', st.text_area("Refleksi Perkembangan Kompetensi:"))
        simpan_teks('Apresiasi', st.text_area("Apresiasi:"))
        simpan_teks('Media_Pembelajaran', st.text_area("Media Pembelajaran:", help="Alat, bahan, atau sumber belajar pendukung."))
    
    with st.container(border=True): # --- KARTU PRATINJAU & CETAK ---
        st.subheader("👁️ Pratinjau Dokumen Sementara")
        with st.expander("Klik untuk memeriksa ringkasan isian Anda sebelum merakit dokumen", expanded=False):
            st.markdown(f"""
            **Identitas:** {st.session_state.data_isian.get('Nama_Guru', '-')} | Jenjang {st.session_state.data_isian.get('Jenjang', '-')} | Fase {st.session_state.data_isian.get('Fase', '-')}
            **Mapel & Materi:** {st.session_state.data_isian.get('MAPEL', '-')} ({st.session_state.data_isian.get('Materi', '-')})
            **TP Kognitif:** {st.session_state.data_isian.get('TP_KOGNITIF', '-')}
            **Nilai SFD:** {st.session_state.data_isian.get('Nilai', '-')} - {st.session_state.data_isian.get('Keutamaan', '-')}
            """)
            if not st.session_state.data_isian.get('Nama_Guru'):
                st.warning("⚠️ Perhatian: Nama Guru belum diisi di Tab 1. Progres Anda mungkin belum 100%.")
        
        st.divider()
        st.subheader("🖨️ Rakit Dokumen & Simpan ke Database")
        
        if st.button("Rakit & Simpan Data", type="primary", use_container_width=True):
            if not st.session_state.data_isian.get('Nama_Guru'):
                st.error("❌ Mohon isi Nama Guru Penyusun di Tab 1 terlebih dahulu!")
            else:
                with st.spinner('Memproses dokumen cerdas Anda...'):
                    try:
                        doc = DocxTemplate("Template_DPB_Schola Amoris.docx")
                        if foto_sdgs is not None:
                            st.session_state.data_isian['Gambar_SGDs'] = InlineImage(doc, foto_sdgs, width=Mm(30))
                        
                        doc.render(st.session_state.data_isian)
                        bio = io.BytesIO()
                        doc.save(bio)
                        
                        data_kirim = {
                            "nama_guru": st.session_state.data_isian.get('Nama_Guru', '-'),
                            "jenjang": st.session_state.data_isian.get('Jenjang', '-'),
                            "kelas": st.session_state.data_isian.get('Kelas', '-'),
                            "mapel": st.session_state.data_isian.get('MAPEL', '-'),
                            "judul": st.session_state.data_isian.get('Judul', '-')
                        }
                        
                        try:
                            respon = requests.post(URL_DATABASE, json=data_kirim) 
                            if respon.status_code == 200:
                                st.toast('Data berhasil tersinkronisasi dengan Database Sekolah!', icon='✅')
                            else:
                                st.warning(f"Error Database: {respon.status_code}")
                        except Exception as err:
                            st.warning(f"Gagal menyambung ke database Google Sheet: {err}")
                        
                        st.success("🎉 Berhasil! Dokumen DPB Anda sudah siap diunduh.")
                        st.download_button(
                            label="📥 Download File DPB (.docx)",
                            data=bio.getvalue(),
                            file_name=f"DPB_{st.session_state.data_isian.get('MAPEL', 'Mapel')}.docx",
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                            use_container_width=True
                        )
                    except Exception as e:
                        st.error(f"Terjadi kesalahan perakitan Word: {e}\nPastikan nama variabel di template .docx sudah persis sama!")
