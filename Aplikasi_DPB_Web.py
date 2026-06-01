import streamlit as st
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm
import io


st.set_page_config(page_title="DPB Schola Amoris", page_icon="📝", layout="wide")

st.title("Penyusun DPB Schola Amoris 🎓")
st.write("Silakan lengkapi rancangan pembelajaran pada setiap tab. Data akan tersimpan sementara selama halaman ini tidak di-refresh.")
st.divider()

if 'data_isian' not in st.session_state:
    st.session_state.data_isian = {}


tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📋 1. Identitas & Konten", 
    "🏫 2. Lingkungan & Praktik", 
    "🧠 3. Kognitif & Psikomotorik", 
    "❤️ 4. Afektif & Karakter", 
    "🖨️ 5. Perayaan & Cetak"
])

def simpan_teks(kunci, nilai):
    st.session_state.data_isian[kunci] = nilai


with tab1:
    st.subheader("A. Identitas & Jenjang")
    col1, col2, col3 = st.columns(3)
    with col1:
        jenjang = st.selectbox("Jenjang:", ["Pilih...", "TK", "SD", "SMP"])
        simpan_teks('Jenjang', jenjang)
    with col2:
        simpan_teks('Fase', st.selectbox("Fase:", ["-", "Fase Fondasi", "Fase A", "Fase B", "Fase C", "Fase D"]))
    with col3:
        simpan_teks('Kelas', st.text_input("Kelas / Semester:"))
        
    foto_sdgs = st.file_uploader("Upload Logo SDGs (Opsional - .png/.jpg)", type=['png', 'jpg', 'jpeg'])

    st.subheader("B. Data Umum & Konten")
    c1, c2, c3 = st.columns(3)
    with c1: simpan_teks('Tahun_Ajaran', st.text_input("Tahun Ajaran:"))
    with c2: simpan_teks('Semester', st.text_input("Semester:"))
    with c3: simpan_teks('JP', st.text_input("Alokasi Waktu (JP):"))

    c4, c5 = st.columns(2)
    with c4: simpan_teks('MAPEL', st.text_input("Mata Pelajaran:"))
    with c5: simpan_teks('Judul', st.text_input("Judul Modul:"))

    simpan_teks('Identifikasi_Peserta_Didik', st.text_area("Identifikasi Peserta Didik:"))
    simpan_teks('CP', st.text_area("Capaian Pembelajaran (CP):"))
    simpan_teks('Materi_Esensial', st.text_area("Materi Esensial:"))
    simpan_teks('Dimensi_Profil_Lulusan', st.text_area("Dimensi Profil Lulusan:"))
    
    c6, c7 = st.columns(2)
    with c6: simpan_teks('CP_SGDs', st.text_area("CP SDGs:"))
    with c7: simpan_teks('TP_SGDs', st.text_area("TP SDGs:"))


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
    simpan_teks('TP_KOGNITIF', st.text_area("TP Kognitif:"))
    simpan_teks('Indikator_Kognitif', st.text_area("Indikator Kognitif:"))
    simpan_teks('Pengalaman_Belajar', st.text_area("Pengalaman Belajar Kognitif:"))
    c1, c2 = st.columns(2)
    with c1: simpan_teks('Asesmen_Formatif', st.text_area("Asesmen Formatif (Kognitif):"))
    with c2: simpan_teks('Asesmen_Sumatif', st.text_area("Asesmen Sumatif (Kognitif):"))

    st.divider()
    st.subheader("Aspek Psikomotorik")
    simpan_teks('TP_Psikomotorik', st.text_area("TP Psikomotorik:"))
    simpan_teks('Indikator_Psikomotorik', st.text_area("Indikator Psikomotorik:"))
    simpan_teks('Pengalaman_Belajar_Psikomotorik', st.text_area("Pengalaman Belajar Psikomotorik:"))
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
    simpan_teks('TP_Afektif', st.text_area("TP Afektif:"))
    simpan_teks('Indikator_Afektif', st.text_area("Indikator Afektif:"))
    simpan_teks('Pengalaman_Belajar_Afektif', st.text_area("Pengalaman Belajar Afektif:"))
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
    st.subheader("🖨️ Mesin Pencetak Dokumen")
    st.info("Pastikan seluruh Tab telah terisi. Klik tombol di bawah untuk menyatukan seluruh data Anda ke dalam file Word.")
    
    if st.button("Rakit Dokumen DPB", type="primary", use_container_width=True):
        try:
            doc = DocxTemplate("Template_DPB_Schola Amoris.docx")
            
            
            if foto_sdgs is not None:
                st.session_state.data_isian['Gambar_SGDs'] = InlineImage(doc, foto_sdgs, width=Mm(30))
            else:
                st.session_state.data_isian['Gambar_SGDs'] = ""
            
            
            doc.render(st.session_state.data_isian)
            
            
            bio = io.BytesIO()
            doc.save(bio)
            
            st.success("✅ Dokumen berhasil dirakit dengan sempurna!")
            st.download_button(
                label="📥 Download File DPB (.docx)",
                data=bio.getvalue(),
                file_name=f"DPB_{st.session_state.data_isian.get('MAPEL', 'Mata_Pelajaran')}_{st.session_state.data_isian.get('Kelas', 'Kelas')}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True
            )
        except FileNotFoundError:
            st.error("⚠️ Error: File 'Template_DPB_Schola_Amoris.docx' tidak ditemukan di folder yang sama!")
        except Exception as e:
            st.error(f"⚠️ Terjadi kesalahan sistem saat merakit dokumen: {e}")
