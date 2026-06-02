import streamlit as st
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm
import io
import requests  
from data_kurikulum import bank_kurikulum
import google.generativeai as genai

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
instruksi_khusus = st.sidebar.text_area("Instruksi Tambahan (Opsional):")
st.sidebar.divider()

st.markdown("""
    <style>
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #f1f5f9;
        border-radius: 8px 8px 0px 0px;
        padding: 10px 20px;
        box-shadow: inset 0 -2px 0 0 #cbd5e1;
        transition: all 0.3s ease;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1e293b;
        color: #ffffff !important;
        box-shadow: 0 -4px 10px rgba(0,0,0,0.1);
    }
    .stTabs [data-baseweb="tab"]:hover { background-color: #e2e8f0; }
    .stTextInput input, .stTextArea textarea, .stSelectbox [data-baseweb="select"] {
        border-radius: 8px !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05) !important;
        border: 1px solid #e2e8f0 !important;
        transition: all 0.3s ease;
    }
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2) !important;
    }
    .stButton > button[kind="primary"] {
        border-radius: 8px;
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        color: white;
        border: none;
        box-shadow: 0 4px 10px rgba(37, 99, 235, 0.3);
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .stButton > button[kind="primary"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(37, 99, 235, 0.4);
    }
    </style>
""", unsafe_allow_html=True)

if 'data_isian' not in st.session_state:
    st.session_state.data_isian = {}
if 'draft_kognitif' not in st.session_state:
    st.session_state.draft_kognitif = ""
if 'draft_psikomotor' not in st.session_state:
    st.session_state.draft_psikomotor = ""
if 'draft_afektif' not in st.session_state:
    st.session_state.draft_afektif = ""

def simpan_teks(kunci, nilai):
    st.session_state.data_isian[kunci] = nilai

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📋 1. Identitas", "🏫 2. Lingkungan", "🧠 3. Kognitif", "❤️ 4. Afektif", "🖨️ 5. Cetak"
])

with tab1:
    st.subheader("A. Identitas Guru & Jenjang")
    simpan_teks('Nama_Guru', st.text_input("Nama Guru Penyusun (Wajib diisi):"))
    
    col1, col2, col3 = st.columns(3)
    with col1: simpan_teks('Jenjang', st.selectbox("Jenjang:", ["Pilih...", "TK", "SD", "SMP", "SMA/SMK"]))
    with col2: simpan_teks('Fase', st.selectbox("Fase:", ["-", "Fase Fondasi", "Fase A", "Fase B", "Fase C", "Fase D", "Fase E", "Fase F"]))
    with col3: simpan_teks('Kelas', st.text_input("Kelas / Semester:"))
        
    foto_sdgs = st.file_uploader("Upload Logo SDGs", type=['png', 'jpg', 'jpeg'])

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
        materi_terpilih = st.text_input("Materi Esensial:")
        simpan_teks('Materi', materi_terpilih)
        
    simpan_teks('Judul', st.text_input("Judul Modul:"))
    
    st.divider()
    st.subheader("🎯 Capaian Pembelajaran & Target SDGs")
    simpan_teks('Capaian_Pembelajaran', st.text_area("Capaian Pembelajaran (CP):", height=150))
    simpan_teks('Capaian_SDGs', st.text_input("Capaian SDGs:"))
    simpan_teks('TP_SDGs', st.text_area("Tujuan Pembelajaran (TP) SDGs:", height=100))

with tab2:
    st.subheader("Lingkungan & Praktik Pembelajaran")
    simpan_teks('Kemitraan_Pembelajaran', st.text_area("Kemitraan Pembelajaran:"))
    simpan_teks('Praktik_Pedagogis', st.text_area("Praktik Pedagogis:"))
    simpan_teks('Urutan_Sintkas', st.text_area("Urutan Sintaks Pembelajaran:", height=150))
    simpan_teks('Ruang_Fisik', st.text_area("Ruang Fisik:"))
    simpan_teks('Ruang_Virtual', st.text_area("Ruang Virtual:"))
    simpan_teks('Budaya_Belajar', st.text_area("Budaya Belajar:"))

with tab3:
    st.subheader("Aspek Kognitif")
    tp_kognitif = st.text_area("TP Kognitif:")
    simpan_teks('TP_KOGNITIF', tp_kognitif)
    
    indikator_kognitif = st.text_area("Indikator Kognitif:")
    simpan_teks('Indikator_Kognitif', indikator_kognitif)
    
    if st.button("✨ Rumuskan Pengalaman Kognitif (AI)", key="btn_kog"):
        if not api_key_guru:
            st.error("Masukkan Kunci API di Sidebar!")
        elif not indikator_kognitif:
            st.warning("Isi Indikator Kognitif terlebih dahulu!")
        else:
            with st.spinner("Merancang aktivitas..."):
                try:
                    genai.configure(api_key=api_key_guru)
                    nama_mesin = None
                    for m in genai.list_models():
                        if 'generateContent' in m.supported_generation_methods:
                            nama_mesin = m.name
                            if 'flash' in m.name.lower():
                                break
                    if not nama_mesin:
                        raise Exception("Tidak ada model AI.")
                    model = genai.GenerativeModel(nama_mesin)
                    
                    prompt = f"Sebagai ahli desain instruksional, buatkan skenario 'Pengalaman Belajar' (Kegiatan Inti) untuk mencapai indikator kognitif berikut: {indikator_kognitif}. Buat aktivitas eksplorasi yang menyenangkan dan memancing rasa ingin tahu. Tuliskan dalam bentuk 3-4 poin langkah kegiatan yang praktis."
                    if instruksi_khusus:
                        prompt += f"\n\nPENTING - Ikuti instruksi tambahan dari guru berikut ini: {instruksi_khusus}"
                        
                    respon = model.generate_content(prompt)
                    st.session_state.draft_kognitif = respon.text
                except Exception as e:
                    st.error(f"Gagal memanggil AI: {e}")
                    
    pengalaman_kognitif = st.text_area("Pengalaman Belajar Kognitif:", value=st.session_state.draft_kognitif, height=200)
    simpan_teks('Pengalaman_Belajar', pengalaman_kognitif)
    
    c1, c2 = st.columns(2)
    with c1: simpan_teks('Asesmen_Formatif', st.text_area("Asesmen Formatif (Kognitif):"))
    with c2: simpan_teks('Asesmen_Sumatif', st.text_area("Asesmen Sumatif (Kognitif):"))

    st.divider()
    
    st.subheader("Aspek Psikomotorik")
    tp_psikomotorik = st.text_area("TP Psikomotorik:")
    simpan_teks('TP_Psikomotorik', tp_psikomotorik)
    
    indikator_psikomotorik = st.text_area("Indikator Psikomotorik:")
    simpan_teks('Indikator_Psikomotorik', indikator_psikomotorik)
    
    if st.button("✨ Rumuskan Pengalaman Psikomotorik (AI)", key="btn_psi"):
        if not api_key_guru:
            st.error("Masukkan Kunci API di Sidebar!")
        elif not indikator_psikomotorik:
            st.warning("Isi Indikator Psikomotorik terlebih dahulu!")
        else:
            with st.spinner("Merancang aktivitas..."):
                try:
                    genai.configure(api_key=api_key_guru)
                    nama_mesin = None
                    for m in genai.list_models():
                        if 'generateContent' in m.supported_generation_methods:
                            nama_mesin = m.name
                            if 'flash' in m.name.lower():
                                break
                    if not nama_mesin:
                        raise Exception("Tidak ada model AI.")
                    model = genai.GenerativeModel(nama_mesin)
                    
                    prompt = f"Sebagai ahli desain instruksional, buatkan skenario 'Pengalaman Belajar' (Praktik/Kinerja) untuk mencapai indikator psikomotorik berikut: {indikator_psikomotorik}. Buat aktivitas unjuk kerja, karya, atau proyek yang terstruktur. Tuliskan dalam bentuk 3-4 poin praktis."
                    if instruksi_khusus:
                        prompt += f"\n\nPENTING - Ikuti instruksi tambahan dari guru berikut ini: {instruksi_khusus}"
                        
                    respon = model.generate_content(prompt)
                    st.session_state.draft_psikomotor = respon.text
                except Exception as e:
                    st.error(f"Gagal memanggil AI: {e}")

    pengalaman_psikomotorik = st.text_area("Pengalaman Belajar Psikomotorik:", value=st.session_state.draft_psikomotor, height=200)
    simpan_teks('Pengalaman_Belajar_Psikomotorik', pengalaman_psikomotorik)
    
    c3, c4 = st.columns(2)
    with c3: simpan_teks('Asesmen_Formatif_Psikomotorik', st.text_area("Asesmen Formatif (Psikomotorik):"))
    with c4: simpan_teks('Asesmen_Sumatif_Psikomotorik', st.text_area("Asesmen Sumatif (Psikomotorik):"))

with tab4:
    st.subheader("A. Profil Pelajar Pancasila (P3)")
    c1, c2, c3 = st.columns(3)
    with c1: simpan_teks('Dimensi', st.text_input("Dimensi P3:"))
    with c2: simpan_teks('Elemen', st.text_input("Elemen P3:"))
    with c3: simpan_teks('Sub_elemen', st.text_input("Sub Elemen P3:"))
    simpan_teks('Capaian_P3', st.text_area("Capaian P3:"))

    st.subheader("B. Kearifan Lokal & Pelindung")
    c4, c5 = st.columns(2)
    with c4: simpan_teks('Santo_Santa_Pelindung', st.text_input("Santo/Santa Pelindung:"))
    with c5: simpan_teks('Kearifan_Lokal', st.text_input("Kearifan Lokal:"))
    c6, c7, c8 = st.columns(3)
    with c6: simpan_teks('KAIH', st.text_input("KAIH:"))
    with c7: simpan_teks('Sub_Dimensi', st.text_input("Sub Dimensi:"))
    with c8: simpan_teks('Kompetensi', st.text_input("Kompetensi:"))

    st.subheader("C. Core Values / Ke-SFD-an")
    c9, c10 = st.columns(2)
    with c9: simpan_teks('Nilai', st.text_input("Nilai Ke-SFD-an:"))
    with c10: simpan_teks('Keutamaan', st.text_input("Keutamaan:"))
    simpan_teks('Capaian_Nilai', st.text_area("Capaian Nilai:"))

    st.subheader("D. Rencana Pembelajaran Afektif")
    tp_afektif = st.text_area("TP Afektif:")
    simpan_teks('TP_Afektif', tp_afektif)
    
    indikator_afektif = st.text_area("Indikator Afektif:")
    simpan_teks('Indikator_Afektif', indikator_afektif)
    
    if st.button("✨ Rumuskan Pengalaman Afektif (AI)", key="btn_afe"):
        if not api_key_guru:
            st.error("Masukkan Kunci API di Sidebar!")
        elif not indikator_afektif:
            st.warning("Isi Indikator Afektif terlebih dahulu!")
        else:
            with st.spinner("Merancang aktivitas..."):
                try:
                    genai.configure(api_key=api_key_guru)
                    nama_mesin = None
                    for m in genai.list_models():
                        if 'generateContent' in m.supported_generation_methods:
                            nama_mesin = m.name
                            if 'flash' in m.name.lower():
                                break
                    if not nama_mesin:
                        raise Exception("Tidak ada model AI.")
                    model = genai.GenerativeModel(nama_mesin)
                    
                    prompt = f"Sebagai ahli desain instruksional, buatkan skenario 'Pengalaman Belajar' untuk mencapai indikator afektif (sikap/karakter) berikut: {indikator_afektif}. Rancang aktivitas yang memancing empati, refleksi diri, atau diskusi nilai moral yang bermakna. Tuliskan dalam bentuk 3-4 poin langkah kegiatan."
                    if instruksi_khusus:
                        prompt += f"\n\nPENTING - Ikuti instruksi tambahan dari guru berikut ini: {instruksi_khusus}"
                        
                    respon = model.generate_content(prompt)
                    st.session_state.draft_afektif = respon.text
                except Exception as e:
                    st.error(f"Gagal memanggil AI: {e}")

    pengalaman_afektif = st.text_area("Pengalaman Belajar Afektif:", value=st.session_state.draft_afektif, height=200)
    simpan_teks('Pengalaman_Belajar_Afektif', pengalaman_afektif)
    
    c11, c12 = st.columns(2)
    with c11: simpan_teks('Formatif', st.text_area("Asesmen Formatif (Afektif):"))
    with c12: simpan_teks('Sumatif', st.text_area("Asesmen Sumatif (Afektif):"))

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
            with st.spinner('Merakit dokumen...'):
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
                            st.toast('Tersimpan di Katalog!', icon='💾')
                        else:
                            st.warning(f"Error Database: {respon.status_code}")
                    except Exception as err:
                        st.warning(f"Koneksi Database gagal: {err}")
                    
                    st.success("Dokumen siap diunduh:")
                    st.download_button(
                        label="📥 Download File DPB (.docx)",
                        data=bio.getvalue(),
                        file_name=f"DPB_{st.session_state.data_isian.get('MAPEL', 'Mapel')}.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        use_container_width=True
                    )
                except Exception as e:
                    st.error(f"Terjadi kesalahan perakitan: {e}")
