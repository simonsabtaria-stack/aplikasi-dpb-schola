import streamlit as st
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm
import io
import requests  
import google.generativeai as genai
import os

# --- IMPOR UNTUK OTAK RAG (VECTOR DATABASE) ---
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# Impor Database Internal
from data_kurikulum import bank_kurikulum
from data_sfd import bank_sfd
from data_kko import bank_kko
from data_p3 import bank_p3
from data_dpl import bank_dpl

st.set_page_config(page_title="DPB Schola Amoris", page_icon="📝", layout="wide")

st.image("banner_schola.png", use_container_width=True)
st.title("Penyusun DPB Schola Amoris 🎓")
st.markdown("*Rancangan yang Anda buat akan otomatis tercatat di Katalog Bank Modul Sekolah.*")
st.divider()

URL_DATABASE = "https://script.google.com/macros/s/AKfycbyi9lnZJplhJDHV9RkkGq8mmILR7zIn7XfNTLN8Qf49XJuyRr8H5LAgr-vlrP6gyDnfjw/exec"

# --- KAMUS SINTAKS MODEL PEMBELAJARAN ---
kamus_sintaks = {
    "Problem Based Learning (PBL)": "1. Orientasi peserta didik pada masalah\n2. Mengorganisasikan peserta didik untuk belajar\n3. Membimbing penyelidikan individu maupun kelompok\n4. Mengembangkan dan menyajikan hasil karya\n5. Menganalisis dan mengevaluasi proses pemecahan masalah",
    "Project Based Learning (PjBL)": "1. Penentuan pertanyaan mendasar\n2. Mendesain perencanaan proyek\n3. Menyusun jadwal (Time schedule)\n4. Memonitor peserta didik dan kemajuan proyek\n5. Menguji hasil\n6. Mengevaluasi pengalaman",
    "Inquiry/Discovery Learning": "1. Pemberian rangsangan (Stimulation)\n2. Pernyataan/Identifikasi masalah (Problem Statement)\n3. Pengumpulan data (Data Collection)\n4. Pengolahan data (Data Processing)\n5. Pembuktian (Verification)\n6. Menarik kesimpulan (Generalization)",
    "Teaching at the Right Level (TaRL)": "1. Asesmen diagnostik awal\n2. Pengelompokan peserta didik berdasarkan capaian\n3. Pendampingan dan pembelajaran berdiferensiasi\n4. Evaluasi formatif berkala\n5. Rotasi/Penyesuaian kelompok berkelanjutan",
    "Cooperative Learning": "1. Menyampaikan tujuan dan memotivasi peserta didik\n2. Menyajikan informasi\n3. Mengorganisasikan peserta didik ke dalam kelompok-kelompok belajar\n4. Membimbing kelompok bekerja dan belajar\n5. Evaluasi\n6. Memberikan penghargaan"
}

# --- INISIALISASI MEMORI ---
if 'data_isian' not in st.session_state: st.session_state.data_isian = {}
if 'draft_kognitif' not in st.session_state: st.session_state.draft_kognitif = ""
if 'draft_psikomotor' not in st.session_state: st.session_state.draft_psikomotor = ""
if 'draft_afektif' not in st.session_state: st.session_state.draft_afektif = ""
if 'draft_tp_kognitif' not in st.session_state: st.session_state.draft_tp_kognitif = ""
if 'draft_tp_psikomotor' not in st.session_state: st.session_state.draft_tp_psikomotor = ""
if 'draft_tp_afektif' not in st.session_state: st.session_state.draft_tp_afektif = ""
if 'draft_ind_kognitif' not in st.session_state: st.session_state.draft_ind_kognitif = ""
if 'draft_ind_psikomotorik' not in st.session_state: st.session_state.draft_ind_psikomotorik = ""
if 'draft_ind_afektif' not in st.session_state: st.session_state.draft_ind_afektif = ""

# Memori Khusus Percakapan Amor
if "chat_amor" not in st.session_state:
    st.session_state.chat_amor = [{"role": "assistant", "content": "Halo! Saya Amor 👋. Asisten pribadi Anda di Schola Amoris. Ada yang ingin didiskusikan tentang Visi-Misi, Kurikulum, atau cara menyusun DPB?"}]

def simpan_teks(kunci, nilai):
    st.session_state.data_isian[kunci] = nilai

# --- FUNGSI AI AMOR (ASISTEN PRIBADI) ---
def panggil_amor(pertanyaan, api_key):
    if not api_key: return "Amor butuh Kunci API Gemini untuk bisa berbicara. Tolong masukkan Kunci API di atas ya! 😊"
    if not os.path.exists("faiss_amor"): return "Maaf, otak Amor (database) belum diunggah. Silakan hubungi admin."
    
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        # Amor mencari jawabannya HANYA di faiss_amor (3 dokumen yayasan)
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        vector_db = FAISS.load_local("faiss_amor", embeddings, allow_dangerous_deserialization=True)
        docs = vector_db.similarity_search(pertanyaan, k=4)
        referensi = "\n\n".join([doc.page_content for doc in docs])
        
        prompt_amor = f"""
        Nama Anda adalah 'Amor', asisten virtual yang ramah, sopan, dan hangat milik Yayasan Santa Maria Banjarmasin. 
        Tugas Anda adalah memandu guru dan menjelaskan tentang Visi-Misi Yayasan, Kurikulum Amoris Schola, dan Panduan DPB.
        Jawablah pertanyaan berikut BERDASARKAN referensi di bawah ini saja. Jika tidak ada di referensi, jawablah dengan sopan bahwa Anda hanya fokus pada panduan kurikulum yayasan.
        
        REFERENSI BUKU PANDUAN:
        {referensi}
        
        PERTANYAAN GURU: {pertanyaan}
        """
        return model.generate_content(prompt_amor).text
    except Exception as e:
        return f"Maaf, Amor sedang mengalami gangguan teknis (Sinyal/Kuota habis). 😔"

# --- SIDEBAR MEWAH & AMOR ---
with st.sidebar:
    st.header("🤖 Pusat Kontrol AI")
    api_key_guru = st.text_input("🔑 Kunci API Gemini:", type="password", help="Dapatkan API dari Google AI Studio. Jika dikosongkan, sistem beralih ke Mode Pakar otomatis.")
    st.divider()
    
    # KOTAK CHAT AMOR DI SIDEBAR
    st.markdown("### 💬 Tanya Amor")
    st.markdown("*Asisten Panduan Kurikulum & DPB*")
    
    # Tampilkan riwayat chat Amor
    wadah_chat = st.container(height=300)
    with wadah_chat:
        for msg in st.session_state.chat_amor:
            if msg["role"] == "assistant":
                st.markdown(f"🧡 **Amor:** {msg['content']}")
            else:
                st.markdown(f"👤 **Anda:** {msg['content']}")
    
    # Input chat Amor
    pertanyaan_baru = st.chat_input("Tanya Amor di sini...")
    if pertanyaan_baru:
        # Simpan pertanyaan guru
        st.session_state.chat_amor.append({"role": "user", "content": pertanyaan_baru})
        # Panggil Amor
        jawaban_amor = panggil_amor(pertanyaan_baru, api_key_guru)
        # Simpan jawaban Amor
        st.session_state.chat_amor.append({"role": "assistant", "content": jawaban_amor})
        st.rerun() # Refresh agar chat muncul
        
    st.divider()
    st.subheader("⚙️ Kustomisasi Gaya AI (Perumus DPB)")
    instruksi_khusus = st.text_area("Instruksi Tambahan (Opsional):", placeholder="Contoh: Fokuskan pada metode diskusi kelompok.")

# --- FUNGSI PERUMUS DPB (SAMA SEPERTI SEBELUMNYA) ---
def fallback_generator(tipe):
    data = st.session_state.data_isian
    materi = data.get('Materi', 'materi pembelajaran') or 'materi pembelajaran'
    sdgs = data.get('Capaian_SDGs', 'target SDGs') or 'target SDGs'
    p3 = data.get('Capaian_P3', 'Profil Pelajar Pancasila') or 'Profil Pelajar Pancasila'
    nilai = data.get('Nilai', 'Nilai Keutamaan') or 'Nilai Keutamaan'
    keutamaan = data.get('Keutamaan', 'Karakter Baik') or 'Karakter Baik'
    kearifan = data.get('Kearifan_Lokal', 'kearifan lokal') or 'kearifan lokal'
    sintaks_terpilih = data.get('Urutan_Sintkas', '- Eksplorasi materi\n- Diskusi kelompok\n- Presentasi hasil')

    if tipe == "tp_kog": return f"1. Melalui eksplorasi mandiri, peserta didik mampu menguraikan konsep {materi} secara kritis.\n2. Peserta didik mampu merancang gagasan faktual terkait {materi} yang selaras dengan tujuan {sdgs}."
    elif tipe == "ind_kog": return f"- Menjelaskan konsep dasar mengenai {materi}\n- Menerapkan prinsip {materi} dalam konteks sederhana\n- Menganalisis dan mengevaluasi kasus faktual terkait {materi}"
    elif tipe == "pg_kog": return f"Kegiatan Inti Pembelajaran (Mengikuti Sintaks Model):\n{sintaks_terpilih}\n\n*Catatan: Fasilitator mengarahkan setiap tahapan sintaks di atas agar berfokus pada materi {materi}.*"
    elif tipe == "tp_afe": return f"Melalui proses pembelajaran, peserta didik mampu menunjukkan sikap yang selaras dengan nilai {nilai} ({keutamaan}), karakter ({p3}), dan semangat {kearifan}."
    elif tipe == "ind_afe": return f"- Menerima arahan terkait nilai {keutamaan}\n- Menghargai dan menunjukkan sikap {keutamaan} saat mempelajari {materi}\n- Menginternalisasi nilai {keutamaan} sebagai karakter harian"
    elif tipe == "pg_afe": return f"- Refleksi Diri: Menulis jurnal pengalaman mempraktikkan nilai {keutamaan}.\n- Aksi Nyata: Menunjukkan sikap kepedulian berlandaskan semangat {kearifan}."
    elif tipe == "tp_psi": return f"Peserta didik terampil mendemonstrasikan prosedur terkait {materi} dengan presisi dan mampu memodifikasinya menjadi karya bermakna."
    elif tipe == "ind_psi": return f"- Meniru tahapan dasar terkait {materi}\n- Mendemonstrasikan keterampilan {materi} secara mandiri\n- Memodifikasi karya {materi} secara kreatif"
    elif tipe == "pg_psi": return f"- Persiapan: Mengamati panduan unjuk kerja {materi}.\n- Unjuk Kerja: Melakukan praktik secara bertahap.\n- Gelar Karya: Menyempurnakan hasil akhir."
    return "Data berhasil diproses."

def ambil_referensi_rag(query):
    if not os.path.exists("faiss_index"): return ""
    try:
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        vector_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
        docs = vector_db.similarity_search(query, k=3)
        referensi = "\n\n".join([doc.page_content for doc in docs])
        return f"\n\n====================\nBERPEDOMAN PADA REFERENSI INI:\n{referensi}\n===================="
    except Exception as e: return "" 

def panggil_ai(prompt, tipe=""):
    if not api_key_guru: return fallback_generator(tipe)
    try:
        genai.configure(api_key=api_key_guru)
        model = genai.GenerativeModel("gemini-1.5-flash")
        konteks = ambil_referensi_rag(prompt)
        aturan = "\n\nATURAN: Gunakan list poin, hindari kapital semua." + (f"\nINSTRUKSI GURU: {instruksi_khusus}" if instruksi_khusus else "")
        return model.generate_content(prompt + konteks + aturan).text
    except Exception as e: return fallback_generator(tipe)

st.markdown("""
    <style>
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { background-color: #f1f5f9; border-radius: 8px 8px 0px 0px; padding: 10px 20px; box-shadow: inset 0 -2px 0 0 #cbd5e1; transition: all 0.3s ease; }
    .stTabs [aria-selected="true"] { background-color: #1e293b; color: #ffffff !important; }
    .stTextInput input, .stTextArea textarea, .stSelectbox [data-baseweb="select"] { border-radius: 8px !important; }
    .stButton > button[kind="primary"] { border-radius: 8px; background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%); color: white; border: none; }
    </style>
""", unsafe_allow_html=True)

# SISTEM INDIKATOR PROGRES
kunci_wajib = ['Nama_Guru', 'MAPEL', 'Materi', 'Capaian_Pembelajaran', 'TP_KOGNITIF', 'TP_Psikomotorik', 'TP_Afektif']
terisi = sum(1 for k in kunci_wajib if st.session_state.data_isian.get(k) and str(st.session_state.data_isian.get(k)).strip() != "")
st.progress(int((terisi / len(kunci_wajib)) * 100))

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["📋 1. Identitas", "🏫 2. Lingkungan", "🧠 3. Kognitif", "❤️ 4. Afektif", "🏃 5. Psikomotorik", "🖨️ 6. Pratinjau & Cetak"])

# TAB 1 - 6 (KODE SAMA PERSIS SEPERTI SEBELUMNYA)
with tab1:
    with st.container(border=True):
        st.subheader("A. Identitas Guru & Jenjang")
        simpan_teks('Nama_Guru', st.text_input("Nama Guru Penyusun (Wajib diisi):"))
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1: simpan_teks('Jenjang', st.selectbox("Jenjang:", ["Pilih...", "TK", "SD", "SMP", "SMA/SMK"]))
        with col2: simpan_teks('Fase', st.selectbox("Fase:", ["-", "Fase Fondasi", "Fase A", "Fase B", "Fase C", "Fase D", "Fase E", "Fase F"]))
        with col3: simpan_teks('Kelas', st.selectbox("Kelas", ["Pilih...", "TK A", "TK B", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "Lainnya"]))
        with col4: simpan_teks('Semester', st.selectbox("Semester:", ["Ganjil", "Genap"]))
        with col5: simpan_teks('Alokasi_Waktu', st.text_input("Alokasi Waktu:"))
            
        col_profil, col_sdgs = st.columns(2)
        with col_profil: simpan_teks('Dimensi_Lulusan', st.selectbox("Dimensi Profil Lulusan:", ["Pilih..."] + list(bank_dpl.keys())))
        with col_sdgs: foto_sdgs = st.file_uploader("Upload Logo SDGs (Opsional)", type=['png', 'jpg', 'jpeg'])
        st.divider()
        simpan_teks('Identifikasi_Peserta_Didik', st.text_area("Hasil Asesmen Diagnostik:"))

    with st.container(border=True):
        st.subheader("B. Data Umum & Konten")
        fase_terpilih = st.session_state.data_isian.get('Fase', '')
        pilihan_mapel = st.selectbox("Mata Pelajaran:", ["Pilih..."] + list(bank_kurikulum.get(fase_terpilih, {}).keys()) + ["Lainnya (Ketik Manual)"])
        
        if pilihan_mapel == "Lainnya (Ketik Manual)":
            simpan_teks('MAPEL', st.text_input("Ketik Nama Mata Pelajaran:"))
            c_el, c_mat = st.columns(2)
            with c_el: simpan_teks('Elemen', st.text_input("Ketik Elemen:"))
            with c_mat: simpan_teks('Materi', st.text_input("Ketik Materi Esensial:"))
            st.session_state['temp_cp'] = "" 
        elif pilihan_mapel != "Pilih...":
            simpan_teks('MAPEL', pilihan_mapel)
            elemen_terpilih = st.multiselect(f"Elemen ({pilihan_mapel}):", list(bank_kurikulum[fase_terpilih][pilihan_mapel].keys()))
            if elemen_terpilih: 
                simpan_teks('Elemen', ", ".join(elemen_terpilih))
                list_data_cp = [data for el in elemen_terpilih for data in bank_kurikulum[fase_terpilih][pilihan_mapel][el]]
                cp_terpilih = st.multiselect("Pilih CP:", [data["cp"] for data in list_data_cp])
                if cp_terpilih:
                    st.session_state['temp_cp'] = "\n\n".join(cp_terpilih)
                    mats = list(dict.fromkeys([m for cp in cp_terpilih for d in list_data_cp if d["cp"] == cp for m in d["materi"]]))
                    simpan_teks('Materi', ", ".join(st.multiselect("Materi Esensial:", mats)))
                else: st.session_state['temp_cp'] = ""; simpan_teks('Materi', "")
            else: st.session_state['temp_cp'] = ""; simpan_teks('Elemen', ""); simpan_teks('Materi', "")
        else: st.session_state['temp_cp'] = ""; simpan_teks('MAPEL', ""); simpan_teks('Elemen', ""); simpan_teks('Materi', "")
        simpan_teks('Judul', st.text_input("Judul Modul:"))
    
    with st.container(border=True): 
        st.subheader("🎯 Capaian Pembelajaran & SDGs")
        simpan_teks('Capaian_Pembelajaran', st.text_area("1. Capaian Pembelajaran:", value=st.session_state.get('temp_cp', ''), height=150))
        opsi_sdgs = ["Pilih...", "1. Tanpa Kemiskinan", "2. Tanpa Kelaparan", "3. Kehidupan Sehat dan Sejahtera", "4. Pendidikan Berkualitas", "5. Kesetaraan Gender", "6. Air Bersih dan Sanitasi Layak", "7. Energi Bersih dan Terjangkau", "8. Pekerjaan Layak dan Pertumbuhan Ekonomi", "9. Industri, Inovasi dan Infrastruktur", "10. Berkurangnya Kesenjangan", "11. Kota dan Permukiman yang Berkelanjutan", "12. Konsumsi dan Produksi yang Bertanggung Jawab", "13. Penanganan Perubahan Iklim", "14. Ekosistem Lautan", "15. Ekosistem Daratan", "16. Perdamaian, Keadilan dan Kelembagaan yang Tangguh", "17. Kemitraan untuk Mencapai Tujuan"]
        simpan_teks('Capaian_SDGs', st.selectbox("2. Capaian SDGs:", opsi_sdgs))
        simpan_teks('TP_SDGs', st.text_area("3. Tujuan Pembelajaran (TP) SDGs:"))

with tab2:
    with st.container(border=True):
        col_mitra, col_peda = st.columns(2)
        with col_mitra:
            pil_mitra = st.selectbox("Kemitraan Pembelajaran:", ["Pilih...", "Orang Tua/Wali Murid", "Komunitas Lokal", "Pakar/Praktisi", "Instansi Pemerintah/Puskesmas", "Lembaga Swadaya Masyarakat (LSM)", "Lainnya"])
            simpan_teks('Kemitraan_Pembelajaran', st.text_input("Ketik Kemitraan:") if pil_mitra == "Lainnya" else pil_mitra)
        with col_peda:
            pil_peda = st.selectbox("Praktik Pedagogis (Model Belajar):", ["Pilih...", "Problem Based Learning (PBL)", "Project Based Learning (PjBL)", "Inquiry/Discovery Learning", "Teaching at the Right Level (TaRL)", "Cooperative Learning", "Lainnya"])
            simpan_teks('Praktik_Pedagogis', st.text_input("Ketik Model:") if pil_peda == "Lainnya" else pil_peda)
        
        pil_budaya = st.selectbox("Budaya Belajar:", ["Pilih...", "Disiplin Positif & Restitusi", "Growth Mindset", "Kolaboratif & Inklusif", "Pembelajaran Berbasis Umpan Balik (Feedback)", "Lainnya"])
        simpan_teks('Budaya_Belajar', st.text_input("Ketik Budaya Belajar:") if pil_budaya == "Lainnya" else pil_budaya)

    with st.container(border=True):
        sintaks_default = kamus_sintaks.get(pil_peda, "") if pil_peda in kamus_sintaks else ""
        simpan_teks('Urutan_Sintkas', st.text_area("Urutan Sintaks Pembelajaran:", value=sintaks_default, height=150))
        c_f, c_v = st.columns(2)
        with c_f: simpan_teks('Ruang_Fisik', st.text_area("Ruang Fisik:"))
        with c_v: simpan_teks('Ruang_Virtual', st.text_area("Ruang Virtual:"))

with tab3:
    with st.container(border=True): 
        st.subheader("🧠 Aspek Kognitif")
        with st.expander("💡 Buka Contekan KKO Kognitif (C1-C6)"):
            for level, kata in bank_kko["KOGNITIF (C)"].items(): st.markdown(f"**{level}**: {kata}")
        if st.button("📈 Rumuskan TP Kognitif", key="btn_tp_kog", use_container_width=True):
            with st.spinner("Memproses TP..."):
                cp_val, tp_sdgs_val = st.session_state.data_isian.get('Capaian_Pembelajaran', ''), st.session_state.data_isian.get('TP_SDGs', '')
                st.session_state['draft_tp_kognitif'] = panggil_ai(f"Baca CP: '{cp_val}'. Rumuskan TP Kognitif yang menaikkan KKO-nya agar menantang (HOTS). Integrasikan dengan SDGs: '{tp_sdgs_val}'.", "tp_kog")
        simpan_teks('TP_KOGNITIF', st.text_area("TP Kognitif:", value=st.session_state['draft_tp_kognitif'], height=100))
        
        if st.button("🪜 Rumuskan Indikator Kognitif", key="btn_ind_kog", use_container_width=True):
            with st.spinner("Membuat indikator berjenjang..."):
                tp_val = st.session_state.data_isian.get('TP_KOGNITIF', '')
                st.session_state['draft_ind_kognitif'] = panggil_ai(f"Dari TP Kognitif: '{tp_val}', buat 3-4 Indikator Pencapaian Kompetensi berjenjang (scaffolding) dari LOTS ke HOTS.", "ind_kog")
        simpan_teks('Indikator_Kognitif', st.text_area("Indikator Kognitif:", value=st.session_state['draft_ind_kognitif'], height=100))
        
        if st.button("✨ Rumuskan Pengalaman Kognitif", key="btn_kog", use_container_width=True):
            with st.spinner("Merancang aktivitas sesuai Sintaks..."):
                mat, mod, sin, ind = st.session_state.data_isian.get('Materi', ''), st.session_state.data_isian.get('Praktik_Pedagogis', ''), st.session_state.data_isian.get('Urutan_Sintkas', ''), st.session_state.data_isian.get('Indikator_Kognitif', '')
                st.session_state.draft_kognitif = panggil_ai(f"Materi: {mat}\nModel: {mod}\nSintaks:\n{sin}\nIndikator: {ind}\nRancang Pengalaman Belajar wajib menjabarkan poin Sintaks tersebut secara berurutan.", "pg_kog")
        simpan_teks('Pengalaman_Belajar', st.text_area("Pengalaman Belajar Kognitif:", value=st.session_state.draft_kognitif, height=200))
        c1, c2 = st.columns(2)
        with c1: simpan_teks('Asesmen_Formatif', st.text_area("Asesmen Formatif (Kognitif):"))
        with c2: simpan_teks('Asesmen_Sumatif', st.text_area("Asesmen Sumatif (Kognitif):"))

with tab4:
    with st.container(border=True): 
        col_kiri, col_kanan = st.columns(2)
        with col_kiri:
            st.markdown("##### 1. Profil Pelajar Pancasila (P3)")
            fase = st.session_state.data_isian.get('Fase', '')
            pil_dim = st.selectbox("Dimensi P3:", ["Pilih..."] + list(bank_p3.keys()))
            if pil_dim != "Pilih...":
                simpan_teks('Dimensi', pil_dim)
                pil_el = st.selectbox("Elemen P3:", ["Pilih..."] + list(bank_p3[pil_dim].keys()))
                if pil_el != "Pilih...":
                    simpan_teks('Elemen_P3', pil_el)
                    pil_sub = st.selectbox("Sub-elemen P3:", ["Pilih..."] + list(bank_p3[pil_dim][pil_el].keys()))
                    if pil_sub != "Pilih...":
                        simpan_teks('Sub_elemen', pil_sub)
                        cp_p3_teks = bank_p3[pil_dim][pil_el][pil_sub].get(fase, "Data belum tersedia.") if fase in ["Fase Fondasi", "Fase A", "Fase B", "Fase C", "Fase D", "Fase E", "Fase F"] else "Pilih Fase di Tab 1."
                        simpan_teks('Capaian_P3', st.text_area("Capaian P3:", value=cp_p3_teks, height=120))
                    else: simpan_teks('Sub_elemen', ""); simpan_teks('Capaian_P3', "")
                else: simpan_teks('Elemen_P3', ""); simpan_teks('Sub_elemen', ""); simpan_teks('Capaian_P3', "")
            else: simpan_teks('Dimensi', ""); simpan_teks('Elemen_P3', ""); simpan_teks('Sub_elemen', ""); simpan_teks('Capaian_P3', "")
            
            st.divider()
            pil_santo = st.selectbox("Pilih Pelindung:", ["Pilih...", "Santo Fransiskus Asisi", "Santa Clara", "Santa Maria", "Lainnya"])
            simpan_teks('Santo_Santa_Pelindung', st.text_input("Nama Pelindung:") if pil_santo == "Lainnya" else pil_santo)
            simpan_teks('Nilai_Keutamaan', st.text_input("Nilai/Keutamaan Pelindung:"))

        with col_kanan:
            pil_kearifan = st.selectbox("Kearifan Lokal:", ["Pilih...", "Waja Sampai Kaputing", "kayuh Baimbai", "Isen Mulang", "Iya Mulik Bengkang Turan", "Dahani Dahanai Tuntung Tulus", "Belum Bahadat", "Huma Betang", "Handep Hapakat", "Lainnya"])
            simpan_teks('Kearifan_Lokal', st.text_input("Ketik Kearifan:") if pil_kearifan == "Lainnya" else pil_kearifan)
            st.divider()
            pil_7kaih = st.selectbox("Pilih 7KAIH:", ["Pilih...", "Bangun Pagi", "Beribadah", "Berolahraga", "Makan Sehat dan Bergizi", "Gemar Belajar", "Bermasyarakat", "Tidur Lebih Awal", "Lainnya"])
            simpan_teks('KAIH', st.text_input("Ketik 7KAIH:") if pil_7kaih == "Lainnya" else pil_7kaih)
            st.divider()
            profil_lulus = st.session_state.data_isian.get('Dimensi_Lulusan', '')
            if profil_lulus and profil_lulus != "Pilih..." and profil_lulus in bank_dpl:
                pil_sub_dpl = st.selectbox("Pilih Sub Dimensi:", ["Pilih..."] + list(bank_dpl[profil_lulus].keys()))
                if pil_sub_dpl != "Pilih...":
                    simpan_teks('Sub_Dimensi', pil_sub_dpl)
                    komp_teks = bank_dpl[profil_lulus][pil_sub_dpl].get(fase, "Data belum tersedia.") if fase in ["Fase Fondasi", "Fase A", "Fase B", "Fase C", "Fase D", "Fase E", "Fase F"] else "Pilih Fase di Tab 1."
                    simpan_teks('Kompetensi', st.text_area("Kompetensi Lulusan:", value=komp_teks, height=120))
                else: simpan_teks('Sub_Dimensi', ""); simpan_teks('Kompetensi', "")
            else: simpan_teks('Sub_Dimensi', ""); simpan_teks('Kompetensi', "")

    with st.container(border=True):
        jenjang = st.session_state.data_isian.get('Jenjang', '')
        c_n, c_k = st.columns(2)
        with c_n: pil_nilai = st.selectbox("1. Pilih Nilai Ke-SFD-an:", ["Pilih..."] + list(bank_sfd.keys()))
        if pil_nilai != "Pilih...":
            simpan_teks('Nilai', pil_nilai)
            with c_k: pil_keut = st.selectbox("2. Pilih Keutamaan:", ["Pilih..."] + list(bank_sfd[pil_nilai].keys()))
            if pil_keut != "Pilih...":
                simpan_teks('Keutamaan', pil_keut)
                if jenjang in ["TK", "SD", "SMP"]: cn_teks = bank_sfd[pil_nilai][pil_keut].get(jenjang, "Data tidak ditemukan.")
                elif jenjang == "SMA/SMK": cn_teks = "Capaian Nilai (CN) Ke-SFD-an SMA masih dirumuskan."
                else: cn_teks = "Pilih Jenjang di Tab 1."
                simpan_teks('Capaian_Nilai', st.text_area("3. Capaian Nilai:", value=cn_teks, height=120))
        else: simpan_teks('Nilai', ""); simpan_teks('Keutamaan', ""); simpan_teks('Capaian_Nilai', "")

    with st.container(border=True): 
        st.subheader("❤️ C. Rencana Afektif")
        if st.button("📈 Rumuskan TP Afektif", key="btn_tp_afe", use_container_width=True):
            with st.spinner("Memproses afektif..."):
                sfd, pelindung, p3, kearifan = st.session_state.data_isian.get('Capaian_Nilai', ''), st.session_state.data_isian.get('Nilai_Keutamaan', ''), st.session_state.data_isian.get('Capaian_P3', ''), st.session_state.data_isian.get('Kearifan_Lokal', '')
                st.session_state['draft_tp_afektif'] = panggil_ai(f"Elemen afektif: P3 ({p3}), Nilai SFD ({sfd}), Keteladanan ({pelindung}), Kearifan ({kearifan}). Sintesis menjadi satu TP Afektif yang kuat.", "tp_afe")
        simpan_teks('TP_Afektif', st.text_area("TP Afektif:", value=st.session_state['draft_tp_afektif'], height=120))
        
        if st.button("🪜 Rumuskan Indikator Afektif", key="btn_ind_afe", use_container_width=True):
            with st.spinner("Membuat indikator sikap..."):
                st.session_state['draft_ind_afektif'] = panggil_ai(f"Dari TP Afektif: '{st.session_state.data_isian.get('TP_Afektif', '')}', buat 3-4 Indikator Pencapaian Sikap berjenjang.", "ind_afe")
        simpan_teks('Indikator_Afektif', st.text_area("Indikator Afektif:", value=st.session_state['draft_ind_afektif'], height=100))
        
        if st.button("✨ Rumuskan Pengalaman Afektif", key="btn_afe", use_container_width=True):
            with st.spinner("Merancang aktivitas karakter..."):
                mat, ind = st.session_state.data_isian.get('Materi', ''), st.session_state.data_isian.get('Indikator_Afektif', '')
                st.session_state.draft_afektif = panggil_ai(f"Materi: {mat}\nKognitif: {st.session_state.draft_kognitif}\nIndikator Afektif: {ind}\nRancang 'Pengalaman Belajar' afektif (reflektif/empati) yang selaras dengan kognitif.", "pg_afe")
        simpan_teks('Pengalaman_Belajar_Afektif', st.text_area("Pengalaman Belajar Afektif:", value=st.session_state.draft_afektif, height=150))
        c11, c12 = st.columns(2)
        with c11: simpan_teks('Formatif', st.text_area("Asesmen Formatif (Afektif):"))
        with c12: simpan_teks('Sumatif', st.text_area("Asesmen Sumatif (Afektif):"))

with tab5:
    with st.container(border=True): 
        st.subheader("🏃 Aspek Psikomotorik")
        if st.button("📈 Rumuskan TP Psikomotorik", key="btn_tp_psi", use_container_width=True):
            with st.spinner("Memproses psikomotorik..."):
                cp, sdgs = st.session_state.data_isian.get('Capaian_Pembelajaran', ''), st.session_state.data_isian.get('TP_SDGs', '')
                st.session_state['draft_tp_psikomotor'] = panggil_ai(f"Baca CP: '{cp}'. Buatkan TP Psikomotorik yang dinaikkan KKO-nya. Integrasikan dengan SDGs: '{sdgs}'.", "tp_psi")
        simpan_teks('TP_Psikomotorik', st.text_area("TP Psikomotorik:", value=st.session_state['draft_tp_psikomotor'], height=100))
        
        if st.button("🪜 Rumuskan Indikator Psikomotorik", key="btn_ind_psi", use_container_width=True):
            with st.spinner("Membuat indikator keterampilan..."):
                st.session_state['draft_ind_psikomotorik'] = panggil_ai(f"Dari TP Psikomotorik: '{st.session_state.data_isian.get('TP_Psikomotorik', '')}', buat 3-4 Indikator berjenjang.", "ind_psi")
        simpan_teks('Indikator_Psikomotorik', st.text_area("Indikator Psikomotorik:", value=st.session_state['draft_ind_psikomotorik'], height=100))
        
        if st.button("✨ Rumuskan Pengalaman Psikomotorik", key="btn_psi", use_container_width=True):
            with st.spinner("Merancang aktivitas psikomotorik..."):
                mat, ind = st.session_state.data_isian.get('Materi', ''), st.session_state.data_isian.get('Indikator_Psikomotorik', '')
                st.session_state.draft_psikomotor = panggil_ai(f"Materi: {mat}\nIndikator: {ind}\nBuat skenario unjuk kerja/proyek.", "pg_psi")
        simpan_teks('Pengalaman_Belajar_Psikomotorik', st.text_area("Pengalaman Belajar Psikomotorik:", value=st.session_state.draft_psikomotor, height=120))
        c3, c4 = st.columns(2)
        with c3: simpan_teks('Asesmen_Formatif_Psikomotorik', st.text_area("Asesmen Formatif (Psikomotorik):"))
        with c4: simpan_teks('Asesmen_Sumatif_Psikomotorik', st.text_area("Asesmen Sumatif (Psikomotorik):"))

with tab6:
    with st.container(border=True): 
        st.subheader("Perayaan Belajar & Media")
        simpan_teks('Membagikan_Pengalaman_Belajar', st.text_area("Membagikan Pengalaman Belajar:"))
        simpan_teks('Refleksi_Perkembangan_Kompetensi', st.text_area("Refleksi Perkembangan Kompetensi:"))
        simpan_teks('Apresiasi', st.text_area("Apresiasi:"))
        simpan_teks('Media_Pembelajaran', st.text_area("Media Pembelajaran:"))
    
    with st.container(border=True): 
        st.subheader("🖨️ Rakit Dokumen & Simpan")
        if st.button("Rakit & Simpan Data", type="primary", use_container_width=True):
            if not st.session_state.data_isian.get('Nama_Guru'): st.error("❌ Mohon isi Nama Guru Penyusun di Tab 1 terlebih dahulu!")
            else:
                with st.spinner('Memproses dokumen...'):
                    try:
                        doc = DocxTemplate("Template_DPB_Schola Amoris.docx")
                        if foto_sdgs is not None: st.session_state.data_isian['Gambar_SGDs'] = InlineImage(doc, foto_sdgs, width=Mm(30))
                        doc.render(st.session_state.data_isian)
                        bio = io.BytesIO()
                        doc.save(bio)
                        data_kirim = {"nama_guru": st.session_state.data_isian.get('Nama_Guru', '-'), "jenjang": st.session_state.data_isian.get('Jenjang', '-'), "kelas": st.session_state.data_isian.get('Kelas', '-'), "mapel": st.session_state.data_isian.get('MAPEL', '-'), "judul": st.session_state.data_isian.get('Judul', '-')}
                        try:
                            respon = requests.post(URL_DATABASE, json=data_kirim) 
                            if respon.status_code == 200: st.toast('Data tersinkronisasi!', icon='✅')
                        except: pass
                        st.success("🎉 Berhasil! Dokumen siap diunduh.")
                        st.download_button(label="📥 Download File DPB", data=bio.getvalue(), file_name=f"DPB_{st.session_state.data_isian.get('MAPEL', 'Mapel')}.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document", use_container_width=True)
                    except Exception as e: st.error(f"Terjadi kesalahan perakitan Word: {e}")
