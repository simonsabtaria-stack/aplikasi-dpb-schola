import streamlit as st
from docxtpl import DocxTemplate InlineImage
from docx.shared import Mm
import io
import requests  
from data_kurikulum import bank_kurikulum
import google.generativeai as genai
from data_sfd import bank_sfd
from data_kko import bank_kko

st.set_page_config(page_title="DPB Schola Amoris", page_icon="📝", layout="wide")

st.image("banner_schola.png", use_container_width=True)
st.divider()
st.title("Penyusun DPB Schola Amoris 🎓")
st.write("Rancangan yang Anda buat akan otomatis tercatat di Katalog Bank Modul Sekolah.")

URL_DATABASE = "https://script.google.com/macros/s/AKfycbyi9lnZJplhJDHV9RkkGq8mmILR7zIn7XfNTLN8Qf49XJuyRr8H5LAgr-vlrP6gyDnfjw/exec"

st.sidebar.subheader("🤖 Pengaturan Asisten AI")
api_key_guru = st.sidebar.text_input("🔑 Kunci API Gemini:", type="password")
st.sidebar.divider()
st.sidebar.subheader("⚙️ Kustomisasi Gaya AI")
instruksi_khusus = st.sidebar.text_area("Instruksi Tambahan (Opsional):", placeholder="Contoh: Fokuskan pada metode diskusi kelompok.")
st.sidebar.divider()

st.markdown("""
    <style>
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { background-color: #f1f5f9; border-radius: 8px 8px 0px 0px; padding: 10px 20px; box-shadow: inset 0 -2px 0 0 #cbd5e1; transition: all 0.3s ease; }
    .stTabs [aria-selected="true"] { background-color: #1e293b; color: #ffffff !important; box-shadow: 0 -4px 10px rgba(0,0,0,0.1); }
    .stTabs [data-baseweb="tab"]:hover { background-color: #e2e8f0; }
    .stTextInput input, .stTextArea textarea, .stSelectbox [data-baseweb="select"] { border-radius: 8px !important; box-shadow: 0 2px 5px rgba(0,0,0,0.05) !important; border: 1px solid #e2e8f0 !important; transition: all 0.3s ease; }
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

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📋 1. Identitas", "🏫 2. Lingkungan", "🧠 3. Kognitif", "❤️ 4. Afektif", "🖨️ 5. Cetak"
])

# ================= TAB 1 =================
with tab1:
    st.subheader("A. Identitas Guru & Jenjang")
    simpan_teks('Nama_Guru', st.text_input("Nama Guru Penyusun (Wajib diisi):"))
    
    col1, col2, col3 = st.columns(3)
    with col1: simpan_teks('Jenjang', st.selectbox("Jenjang:", ["Pilih...", "TK", "SD", "SMP", "SMA/SMK"]))
    with col2: simpan_teks('Fase', st.selectbox("Fase:", ["-", "Fase Fondasi", "Fase A", "Fase B", "Fase C", "Fase D", "Fase E", "Fase F"]))
    with col3: simpan_teks('Kelas', st.text_input("Kelas / Semester:"))
        
    foto_sdgs = st.file_uploader("Upload Logo SDGs", type=['png', 'jpg', 'jpeg'])

    st.subheader("B. Data Umum & Konten")
    daftar_mapel = list(bank_kurikulum.keys()) if 'bank_kurikulum' in globals() else ["Pendidikan Pancasila", "Matematika"]
    mapel_terpilih = st.selectbox("Mata Pelajaran:", daftar_mapel)
    simpan_teks('MAPEL', mapel_terpilih)
    
    c_elemen, c_materi = st.columns(2)
    with c_elemen:
        daftar_elemen = bank_kurikulum[mapel_terpilih] if 'bank_kurikulum' in globals() else ["Elemen 1", "Elemen 2"]
        elemen_terpilih = st.selectbox(f"Elemen ({mapel_terpilih}):", daftar_elemen)
        simpan_teks('Elemen', elemen_terpilih)
    with c_materi:
        materi_terpilih = st.text_input("Materi Esensial:")
        simpan_teks('Materi', materi_terpilih)
        
    simpan_teks('Judul', st.text_input("Judul Modul:"))
    
    st.divider()
    st.subheader("🎯 Capaian Pembelajaran & Target SDGs")
    
    # 1. Capaian Pembelajaran (CP)
    cp_input = st.text_area("1. Capaian Pembelajaran (CP):", height=150)
    simpan_teks('Capaian_Pembelajaran', cp_input)
    
    # 2. Capaian SDGs (Dropdown 17 Target)
    opsi_sdgs = [
        "Pilih...",
        "1. Tanpa Kemiskinan",
        "2. Tanpa Kelaparan",
        "3. Kehidupan Sehat dan Sejahtera",
        "4. Pendidikan Berkualitas",
        "5. Kesetaraan Gender",
        "6. Air Bersih dan Sanitasi Layak",
        "7. Energi Bersih dan Terjangkau",
        "8. Pekerjaan Layak dan Pertumbuhan Ekonomi",
        "9. Industri, Inovasi dan Infrastruktur",
        "10. Berkurangnya Kesenjangan",
        "11. Kota dan Permukiman yang Berkelanjutan",
        "12. Konsumsi dan Produksi yang Bertanggung Jawab",
        "13. Penanganan Perubahan Iklim",
        "14. Ekosistem Lautan",
        "15. Ekosistem Daratan",
        "16. Perdamaian, Keadilan dan Kelembagaan yang Tangguh",
        "17. Kemitraan untuk Mencapai Tujuan"
    ]
    pilihan_sdgs = st.selectbox("2. Capaian SDGs:", opsi_sdgs)
    simpan_teks('Capaian_SDGs', pilihan_sdgs if pilihan_sdgs != "Pilih..." else "")
    
    # 3. Tujuan Pembelajaran SDGs
    tp_sdgs_input = st.text_area("3. Tujuan Pembelajaran (TP) SDGs:", height=100)
    simpan_teks('TP_SDGs', tp_sdgs_input)
    
# ================= TAB 2 =================
with tab2:
    st.subheader("Lingkungan & Praktik Pembelajaran")
    simpan_teks('Kemitraan_Pembelajaran', st.text_area("Kemitraan Pembelajaran:"))
    simpan_teks('Praktik_Pedagogis', st.text_area("Praktik Pedagogis (Model Belajar):"))
    simpan_teks('Urutan_Sintkas', st.text_area("Urutan Sintaks Pembelajaran:", height=150))
    simpan_teks('Ruang_Fisik', st.text_area("Ruang Fisik:"))
    simpan_teks('Ruang_Virtual', st.text_area("Ruang Virtual:"))
    simpan_teks('Budaya_Belajar', st.text_area("Budaya Belajar:"))

# ================= TAB 3 =================
with tab3:
    st.subheader("Aspek Kognitif")
    with st.expander("💡 Buka Contekan KKO Kognitif (C1-C6)"):
        for level, kata in bank_kko["KOGNITIF (C)"].items():
            st.markdown(f"**{level}**: {kata}")
    tp_kognitif = st.text_area("TP Kognitif:")
    simpan_teks('TP_KOGNITIF', tp_kognitif)
    indikator_kognitif = st.text_area("Indikator Kognitif:")
    simpan_teks('Indikator_Kognitif', indikator_kognitif)
    
    if st.button("✨ Rumuskan Pengalaman Kognitif (AI)", key="btn_kog"):
        if not api_key_guru: st.error("Masukkan Kunci API di Sidebar!")
        else:
            with st.spinner("Merancang aktivitas kognitif..."):
                try:
                    konteks = f"Materi: {materi_terpilih}\nCP: {cp_input}\n"
                    prompt = f"Berdasarkan {konteks}, buat skenario 'Pengalaman Belajar' (Kegiatan Inti) untuk mencapai indikator: {indikator_kognitif}. Buat aktivitas eksplorasi dalam 3-4 poin praktis."
                    st.session_state.draft_kognitif = panggil_ai(prompt)
                except Exception as e: st.error(e)
                    
    simpan_teks('Pengalaman_Belajar', st.text_area("Pengalaman Belajar Kognitif:", value=st.session_state.draft_kognitif, height=150))
    c1, c2 = st.columns(2)
    with c1: simpan_teks('Asesmen_Formatif', st.text_area("Asesmen Formatif (Kognitif):"))
    with c2: simpan_teks('Asesmen_Sumatif', st.text_area("Asesmen Sumatif (Kognitif):"))

    st.divider()
    
    st.subheader("Aspek Psikomotorik")
    with st.expander("💡 Buka Contekan KKO Psikomotorik (P1-P5)"):
        for level, kata in bank_kko["PSIKOMOTORIK (P)"].items():
            st.markdown(f"**{level}**: {kata}")
    tp_psikomotorik = st.text_area("TP Psikomotorik:")
    simpan_teks('TP_Psikomotorik', tp_psikomotorik)
    indikator_psikomotorik = st.text_area("Indikator Psikomotorik:")
    simpan_teks('Indikator_Psikomotorik', indikator_psikomotorik)
    
    if st.button("✨ Rumuskan Pengalaman Psikomotorik (AI)", key="btn_psi"):
        if not api_key_guru: st.error("Masukkan Kunci API di Sidebar!")
        else:
            with st.spinner("Merancang aktivitas psikomotorik..."):
                try:
                    konteks = f"Materi: {materi_terpilih}\nCP: {cp_input}\nKegiatan Kognitif Sebelumnya: {st.session_state.draft_kognitif}\n"
                    prompt = f"Berdasarkan {konteks}, buat skenario unjuk kerja/proyek untuk mencapai indikator psikomotorik: {indikator_psikomotorik}. Tuliskan dalam 3-4 poin praktis."
                    st.session_state.draft_psikomotor = panggil_ai(prompt)
                except Exception as e: st.error(e)

    simpan_teks('Pengalaman_Belajar_Psikomotorik', st.text_area("Pengalaman Belajar Psikomotorik:", value=st.session_state.draft_psikomotor, height=150))
    c3, c4 = st.columns(2)
    with c3: simpan_teks('Asesmen_Formatif_Psikomotorik', st.text_area("Asesmen Formatif (Psikomotorik):"))
    with c4: simpan_teks('Asesmen_Sumatif_Psikomotorik', st.text_area("Asesmen Sumatif (Psikomotorik):"))

# ================= TAB 4 (ROMBAK TOTAL AFEKTIF) =================
with tab4:
    st.subheader("A. Identitas Karakter & Nilai Yayasan")
    col_kiri, col_kanan = st.columns(2)
    
    with col_kiri:
        st.markdown("##### 1. Profil Pelajar Pancasila (P3)")
        opsi_p3 = ["Beriman & Bertakwa", "Berkebinekaan Global", "Bergotong Royong", "Mandiri", "Bernalar Kritis", "Kreatif", "Lainnya"]
        pilihan_p3 = st.selectbox("Dimensi P3:", opsi_p3)
        simpan_teks('Dimensi', st.text_input("Ketik Dimensi P3:") if pilihan_p3 == "Lainnya" else pilihan_p3)
        simpan_teks('Elemen', st.text_input("Elemen P3:", placeholder="Contoh: Akhlak bernegara"))
        simpan_teks('Sub_elemen', st.text_input("Sub Elemen P3:"))
        simpan_teks('Capaian_P3', st.text_area("Capaian P3:"))
        
        st.divider()
        st.markdown("##### 2. Santo / Santa Pelindung")
        opsi_santo = ["Santo Fransiskus Asisi", "Santa Clara", "Santa Maria", "Lainnya"]
        pilihan_santo = st.selectbox("Pilih Pelindung:", opsi_santo)
        simpan_teks('Santo_Santa_Pelindung', st.text_input("Ketik Nama Pelindung:") if pilihan_santo == "Lainnya" else pilihan_santo)

    with col_kanan:
        st.markdown("##### 3. Kearifan Lokal")
        opsi_kearifan = ["Belum Bahadat", "Huma Betang", "Handep", "Lainnya"]
        pilihan_kearifan = st.selectbox("Pilih Kearifan Lokal:", opsi_kearifan)
        simpan_teks('Kearifan_Lokal', st.text_input("Ketik Kearifan Lokal:") if pilihan_kearifan == "Lainnya" else pilihan_kearifan)
        
        st.divider()
        st.markdown("##### 4. 7 Kebiasaan Anak Indonesia Hebat")
        opsi_7kaih = ["Bangun Pagi", "Beribadah", "Berolahraga", "Makan Sehat dan Bergizi", "Gemar Belajar", "Bermasyarakat", "Tidur Cepat"]
        pilihan_7kaih = st.selectbox("Pilih 7KAIH:", opsi_7kaih)
        simpan_teks('KAIH', st.text_input("Ketik 7KAIH:") if pilihan_7kaih == "Lainnya" else pilihan_7kaih)
        
        st.divider()
        st.markdown("##### 5. Dimensi Profil Lulusan")
        opsi_profil = ["Keimanan & Ketakwaan Kepada Tuhan Yang Maha Esa", "Kewargaan", "Penalaran Kritis", "Kreativitas", "Kolaborasi", "Kemandirian", "Kesehatan", "Komunikasi", "Lainnya"]
        pilihan_profil = st.selectbox("Profil Lulusan:", opsi_profil)
        simpan_teks('Dimensi_Lulusan', st.text_input("Ketik Profil:") if pilihan_profil == "Lainnya" else pilihan_profil)
        simpan_teks('Sub_Dimensi', st.text_input("Sub Dimensi:"))
        simpan_teks('Kompetensi', st.text_input("Kompetensi Lulusan:"))

    st.divider()
    st.subheader("B. Core Values / Ke-SFD-an")
    st.info("Capaian Nilai (CN) akan otomatis ditarik sebagai narasi utuh menyesuaikan Jenjang dan Keutamaan yang dipilih.")
    
    # Menarik data jenjang dari Tab 1
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
            
            # Mesin langsung menarik narasi CN tanpa perlu dropdown Praksis Moral lagi!
            if jenjang_terpilih in ["TK", "SD", "SMP"]:
                teks_cn_otomatis = bank_sfd[pilihan_nilai][pilihan_keutamaan].get(jenjang_terpilih, "Data tidak ditemukan.")
            elif jenjang_terpilih == "SMA/SMK":
                teks_cn_otomatis = "Capaian Nilai (CN) Ke-SFD-an untuk jenjang SMA saat ini masih dalam tahap perumusan oleh Yayasan."
            else:
                teks_cn_otomatis = "⚠️ Silakan kembali ke Tab 1 dan pilih Jenjang (TK/SD/SMP/SMA) terlebih dahulu."
            
            # Kotak teks otomatis
            cn_input = st.text_area("3. Capaian Nilai (Otomatis Terisi & Bisa Diedit):", value=teks_cn_otomatis, height=120)
            simpan_teks('Capaian_Nilai', cn_input)
    else:
        # Kosongkan data jika dikembalikan ke "Pilih..."
        simpan_teks('Nilai', "")
        simpan_teks('Keutamaan', "")
        simpan_teks('Capaian_Nilai', "")

    st.divider()
    st.subheader("C. Rencana Pembelajaran Afektif")
    with st.expander("💡 Buka Contekan KKO Afektif (A1-A5)"):
        for level, kata in bank_kko["AFEKTIF (A)"].items():
            st.markdown(f"**{level}**: {kata}")
    simpan_teks('TP_Afektif', st.text_area("TP Afektif:"))
    indikator_afektif = st.text_area("Indikator Afektif:")
    simpan_teks('Indikator_Afektif', indikator_afektif)
    
    if st.button("✨ Rumuskan Pengalaman Afektif (AI)", key="btn_afe"):
        if not api_key_guru: st.error("Masukkan Kunci API di Sidebar!")
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
    st.subheader("Perayaan Belajar & Media")
    simpan_teks('Membagikan_Pengalaman_Belajar', st.text_area("Membagikan Pengalaman Belajar:"))
    simpan_teks('Refleksi_Perkembangan_Kompetensi', st.text_area("Refleksi Perkembangan Kompetensi:"))
    simpan_teks('Apresiasi', st.text_area("Apresiasi:"))
    simpan_teks('Media_Pembelajaran', st.text_area("Media Pembelajaran:"))
    
    st.divider()
    st.subheader("🖨️ Rakit Dokumen & Simpan ke Database")
    
    if st.button("Rakit & Simpan Data", type="primary", use_container_width=True):
        if not st.session_state.data_isian.get('Nama_Guru'):
            st.error("Mohon isi Nama Guru Penyusun di Tab 1!")
        else:
            with st.spinner('Merakit dokumen dan mengirim ke database...'):
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
                            st.toast('Data Modul Tersimpan di Katalog!', icon='✅')
                        else:
                            st.warning(f"Error Database: {respon.status_code}")
                    except Exception as err:
                        st.warning(f"Gagal menyambung ke database Google Sheet: {err}")
                    
                    st.success("✅ Dokumen DPB berhasil dirakit dan siap diunduh:")
                    st.download_button(
                        label="📥 Download File DPB (.docx)",
                        data=bio.getvalue(),
                        file_name=f"DPB_{st.session_state.data_isian.get('MAPEL', 'Mapel')}.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        use_container_width=True
                    )
                except Exception as e:
                    st.error(f"Terjadi kesalahan perakitan Word: {e}\nPastikan nama variabel di template .docx sudah persis sama!")
