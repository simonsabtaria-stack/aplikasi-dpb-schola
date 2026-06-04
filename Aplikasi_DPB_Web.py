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

# --- KAMUS SINTAKS MODEL PEMBELAJARAN (FITUR BARU) ---
kamus_sintaks = {
    "Problem Based Learning (PBL)": "1. Orientasi peserta didik pada masalah\n2. Mengorganisasikan peserta didik untuk belajar\n3. Membimbing penyelidikan individu maupun kelompok\n4. Mengembangkan dan menyajikan hasil karya\n5. Menganalisis dan mengevaluasi proses pemecahan masalah",
    "Project Based Learning (PjBL)": "1. Penentuan pertanyaan mendasar\n2. Mendesain perencanaan proyek\n3. Menyusun jadwal (Time schedule)\n4. Memonitor peserta didik dan kemajuan proyek\n5. Menguji hasil\n6. Mengevaluasi pengalaman",
    "Inquiry/Discovery Learning": "1. Pemberian rangsangan (Stimulation)\n2. Pernyataan/Identifikasi masalah (Problem Statement)\n3. Pengumpulan data (Data Collection)\n4. Pengolahan data (Data Processing)\n5. Pembuktian (Verification)\n6. Menarik kesimpulan (Generalization)",
    "Teaching at the Right Level (TaRL)": "1. Asesmen diagnostik awal\n2. Pengelompokan peserta didik berdasarkan capaian\n3. Pendampingan dan pembelajaran berdiferensiasi\n4. Evaluasi formatif berkala\n5. Rotasi/Penyesuaian kelompok berkelanjutan",
    "Cooperative Learning": "1. Menyampaikan tujuan dan memotivasi peserta didik\n2. Menyajikan informasi\n3. Mengorganisasikan peserta didik ke dalam kelompok-kelompok belajar\n4. Membimbing kelompok bekerja dan belajar\n5. Evaluasi\n6. Memberikan penghargaan"
}

# --- SIDEBAR MEWAH ---
with st.sidebar:
    st.header("🤖 Pusat Kontrol AI")
    api_key_guru = st.text_input("🔑 Kunci API Gemini:", type="password", help="Dapatkan API dari Google AI Studio. Jika dikosongkan, sistem beralih ke Mode Pakar otomatis.")
    st.divider()
    st.subheader("⚙️ Kustomisasi Gaya AI")
    instruksi_khusus = st.text_area("Instruksi Tambahan (Opsional):", placeholder="Contoh: Fokuskan pada metode diskusi kelompok.", help="Hanya berlaku saat Mode Gemini aktif.")
    
    st.divider()
    st.markdown("**Status Sistem:**")
    if api_key_guru:
        st.success("✅ Mode Gemini Aktif (Online)")
    else:
        st.info("🤖 Mode Sistem Pakar Aktif (Offline/Tanpa Kuota)")

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
if 'draft_ind_kognitif' not in st.session_state: st.session_state.draft_ind_kognitif = ""
if 'draft_ind_psikomotorik' not in st.session_state: st.session_state.draft_ind_psikomotorik = ""
if 'draft_ind_afektif' not in st.session_state: st.session_state.draft_ind_afektif = ""

def simpan_teks(kunci, nilai):
    st.session_state.data_isian[kunci] = nilai

# --- OTAK CADANGAN (SISTEM PAKAR) ---
def fallback_generator(tipe):
    data = st.session_state.data_isian
    materi = data.get('Materi', 'materi pembelajaran') or 'materi pembelajaran'
    sdgs = data.get('Capaian_SDGs', 'target SDGs') or 'target SDGs'
    p3 = data.get('Capaian_P3', 'Profil Pelajar Pancasila') or 'Profil Pelajar Pancasila'
    nilai = data.get('Nilai', 'Nilai Keutamaan') or 'Nilai Keutamaan'
    keutamaan = data.get('Keutamaan', 'Karakter Baik') or 'Karakter Baik'
    kearifan = data.get('Kearifan_Lokal', 'kearifan lokal') or 'kearifan lokal'
    sintaks_terpilih = data.get('Urutan_Sintkas', '- Eksplorasi materi\n- Diskusi kelompok\n- Presentasi hasil')

    if tipe == "tp_kog":
        return f"1. Melalui eksplorasi dan diskusi mandiri, peserta didik mampu menguraikan serta menganalisis konsep {materi} secara kritis dan komprehensif.\n2. Peserta didik mampu merancang gagasan faktual terkait {materi} dengan tingkat pemahaman (HOTS) yang selaras dengan tujuan {sdgs}."
    elif tipe == "ind_kog":
        return f"- Menjelaskan konsep dasar mengenai {materi} (Pemahaman dasar)\n- Menerapkan prinsip {materi} dalam konteks sederhana (Penerapan)\n- Menganalisis dan mengevaluasi kasus faktual terkait {materi} (Target TP HOTS)"
    elif tipe == "pg_kog":
        # Mode Pakar sekarang menggunakan sintaks yang dipilih guru di Tab 2
        return f"Kegiatan Inti Pembelajaran (Mengikuti Sintaks Model):\n{sintaks_terpilih}\n\n*Catatan: Fasilitator mengarahkan setiap tahapan sintaks di atas agar berfokus pada materi {materi} sesuai indikator.*"
    elif tipe == "tp_afe":
        return f"Melalui keseluruhan proses pembelajaran, peserta didik mampu menginternalisasi dan menunjukkan sikap nyata yang selaras dengan nilai {nilai} ({keutamaan}), mencerminkan karakter mulia ({p3}), serta mempraktikkan semangat {kearifan} dalam interaksi sehari-hari."
    elif tipe == "ind_afe":
        return f"- Menerima dan merespon arahan terkait nilai {keutamaan} (A1/A2)\n- Menghargai dan menunjukkan sikap {keutamaan} saat mempelajari {materi} (A3)\n- Menginternalisasi dan menjadikan nilai {keutamaan} serta semangat {kearifan} sebagai karakter harian (Target TP A4/A5)"
    elif tipe == "pg_afe":
        return f"- Refleksi Diri: Peserta didik menuliskan jurnal singkat mengenai pengalaman mempraktikkan nilai {keutamaan} saat mempelajari {materi}.\n- Aksi Nyata: Membagikan pandangannya dalam forum kelas untuk menunjukkan sikap saling menghargai berlandaskan semangat {kearifan}."
    elif tipe == "tp_psi":
        return f"1. Peserta didik terampil mendemonstrasikan unjuk kerja atau prosedur terkait {materi} dengan tingkat presisi dan kelancaran yang sesuai standar.\n2. Peserta didik mampu mengadaptasi dan memodifikasi keterampilan teknis mengenai {materi} untuk menghasilkan performa atau karya yang bermakna."
    elif tipe == "ind_psi":
        return f"- Meniru tahapan dasar secara terbimbing terkait {materi} (P1/P2)\n- Mendemonstrasikan keterampilan {materi} secara mandiri dan lancar (P3)\n- Memodifikasi dan menyempurnakan performa/karya {materi} secara kreatif (Target TP P4/P5)"
    elif tipe == "pg_psi":
        return f"- Persiapan: Peserta didik mengamati panduan unjuk kerja praktis mengenai {materi}.\n- Unjuk Kerja: Melakukan praktik secara bertahap sesuai panduan.\n- Gelar Karya: Menyempurnakan dan mempresentasikan hasil akhir."
    return "Data berhasil diproses."

# --- FUNGSI PENCARI REFERENSI PDF (RAG) ---
def ambil_referensi_rag(query):
    if not os.path.exists("faiss_index"): return ""
    try:
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        vector_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
        dokumen_cocok = vector_db.similarity_search(query, k=3)
        referensi_teks = "\n\n".join([doc.page_content for doc in dokumen_cocok])
        return f"\n\n====================\nBERPEDOMAN PADA BUKU PANDUAN SEKOLAH BERIKUT INI SEBAGAI REFERENSI UTAMAMU:\n{referensi_teks}\n====================\nPastikan jawabanmu mencerminkan atau selaras dengan referensi di atas."
    except Exception as e:
        return "" 

# --- FUNGSI AI HYBRID ANTI-ERROR (DENGAN RAG) ---
def panggil_ai(prompt, tipe=""):
    if not api_key_guru:
        st.toast("⚡ Menggunakan Otak Cadangan (Mode Sistem Pakar)", icon="🤖")
        return fallback_generator(tipe)
        
    try:
        genai.configure(api_key=api_key_guru)
        mesin_tersedia = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        mesin_flash = [m for m in mesin_tersedia if 'flash' in m.lower() and 'interactions' not in m.lower()]
        if not mesin_flash: raise Exception("API Key tidak memiliki akses ke model Flash.")
        nama_mesin = next((m for m in mesin_flash if '1.5' in m), mesin_flash[0])
        
        konteks_sekolah = ambil_referensi_rag(prompt)
        prompt_plus_pedoman = prompt + konteks_sekolah
        
        aturan = "\n\nATURAN FORMAT: Gunakan kalimat efektif, hindari UPPERCASE, gunakan list poin biasa tanpa simbol markdown rumit."
        if instruksi_khusus: aturan += f"\nINSTRUKSI KHUSUS GURU: {instruksi_khusus}"
        model = genai.GenerativeModel(nama_mesin)
        return model.generate_content(prompt_plus_pedoman + aturan).text
    except Exception as e:
        st.toast(f"⚠️ Gemini Error/Kuota Habis. Beralih otomatis ke Sistem Pakar...", icon="🔄")
        return fallback_generator(tipe)

# --- SISTEM INDIKATOR PROGRES ---
kunci_wajib = ['Nama_Guru', 'MAPEL', 'Materi', 'Capaian_Pembelajaran', 'TP_KOGNITIF', 'TP_Psikomotorik', 'TP_Afektif']
terisi = sum(1 for k in kunci_wajib if st.session_state.data_isian.get(k) and str(st.session_state.data_isian.get(k)).strip() != "")
progres_persen = int((terisi / len(kunci_wajib)) * 100)

st.markdown(f"**📈 Progres Penyusunan DPB: {progres_persen}%**")
st.progress(progres_persen)
st.write("") 

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📋 1. Identitas", "🏫 2. Lingkungan", "🧠 3. Kognitif", "❤️ 4. Afektif", "🏃 5. Psikomotorik", "🖨️ 6. Pratinjau & Cetak"
])

# ================= TAB 1 =================
with tab1:
    with st.container(border=True):
        st.subheader("A. Identitas Guru & Jenjang")
        simpan_teks('Nama_Guru', st.text_input("Nama Guru Penyusun (Wajib diisi):", help="Ketikkan nama lengkap beserta gelar untuk dicetak di modul."))
        
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1: simpan_teks('Jenjang', st.selectbox("Jenjang:", ["Pilih...", "TK", "SD", "SMP", "SMA/SMK"], help="Pilih jenjang untuk menyesuaikan Capaian Nilai SFD nanti."))
        with col2: simpan_teks('Fase', st.selectbox("Fase:", ["-", "Fase Fondasi", "Fase A", "Fase B", "Fase C", "Fase D", "Fase E", "Fase F"]))
        with col3: simpan_teks('Kelas', st.selectbox("Kelas", ["Pilih...", "TK A", "TK B", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "Lainnya"]))
        with col4: simpan_teks('Semester', st.selectbox("Semester:", ["Ganjil", "Genap"]))
        with col5: simpan_teks('Alokasi_Waktu', st.text_input("Alokasi Waktu:", help="Contoh: 2 JP (2 x 40 Menit)"))
            
        col_profil, col_sdgs = st.columns(2)
        with col_profil:
            daftar_dpl = list(bank_dpl.keys())
            pilihan_profil = st.selectbox("Dimensi Profil Lulusan:", ["Pilih..."] + daftar_dpl, help="Pilih target profil lulusan. Data ini akan otomatis tersambung ke Tab 4.")
            simpan_teks('Dimensi_Lulusan', pilihan_profil)
        
        with col_sdgs:
            foto_sdgs = st.file_uploader("Upload Logo SDGs (Opsional)", type=['png', 'jpg', 'jpeg'], help="Unggah ikon SDGs yang sesuai untuk disematkan di pojok dokumen.")

        st.divider()
        st.markdown("##### C. Identifikasi Peserta Didik")
        identifikasi_siswa = st.text_area("Hasil Asesmen Diagnostik:", help="Ketikkan pemetaan gaya belajar (Visual/Auditori/Kinestetik), minat, atau kesiapan belajar siswa di sini.")
        simpan_teks('Identifikasi_Peserta_Didik', identifikasi_siswa)

    with st.container(border=True):
        st.subheader("B. Data Umum & Konten")
        
        fase_terpilih = st.session_state.data_isian.get('Fase', '')
        daftar_mapel_db = list(bank_kurikulum.get(fase_terpilih, {}).keys()) if fase_terpilih else []
        opsi_mapel = ["Pilih..."] + daftar_mapel_db + ["Lainnya (Ketik Manual)"]
        pilihan_mapel = st.selectbox("Mata Pelajaran:", opsi_mapel, help="Pilih mapel yang tersedia untuk otomatisasi, atau pilih 'Lainnya' untuk mengetik manual.")
        
        if pilihan_mapel == "Lainnya (Ketik Manual)":
            mapel_terpilih = st.text_input("Ketik Nama Mata Pelajaran:")
            simpan_teks('MAPEL', mapel_terpilih)
            c_elemen, c_materi = st.columns(2)
            with c_elemen: simpan_teks('Elemen', st.text_input("Ketik Elemen:"))
            with c_materi: simpan_teks('Materi', st.text_input("Ketik Materi Esensial:"))
            st.session_state['temp_cp'] = "" 
            
        elif pilihan_mapel != "Pilih...":
            mapel_terpilih = pilihan_mapel
            simpan_teks('MAPEL', mapel_terpilih)
            daftar_elemen = list(bank_kurikulum[fase_terpilih][mapel_terpilih].keys())
            elemen_terpilih = st.multiselect(f"Elemen ({mapel_terpilih}):", daftar_elemen, help="Anda bisa memilih lebih dari satu Elemen.")
            
            if elemen_terpilih: 
                simpan_teks('Elemen', ", ".join(elemen_terpilih))
                list_data_cp_combined = []
                for el in elemen_terpilih:
                    list_data_cp_combined.extend(bank_kurikulum[fase_terpilih][mapel_terpilih][el])
                
                daftar_teks_cp = [data["cp"] for data in list_data_cp_combined]
                cp_terpilih = st.multiselect("Pilih Capaian Pembelajaran (CP):", daftar_teks_cp, help="Anda bisa memilih lebih dari satu CP.")
                
                if cp_terpilih:
                    st.session_state['temp_cp'] = "\n\n".join(cp_terpilih)
                    materi_options = []
                    for cp_teks in cp_terpilih:
                        for data in list_data_cp_combined:
                            if data["cp"] == cp_teks:
                                materi_options.extend(data["materi"])
                                
                    materi_options = list(dict.fromkeys(materi_options))
                    materi_terpilih = st.multiselect("Materi Esensial:", materi_options, help="Pilih materi esensial sebanyak yang dibutuhkan.")
                    simpan_teks('Materi', ", ".join(materi_terpilih))
                else:
                    st.session_state['temp_cp'] = ""
                    simpan_teks('Materi', "")
            else:
                st.session_state['temp_cp'] = ""
                simpan_teks('Elemen', "")
                simpan_teks('Materi', "")
        else:
            st.session_state['temp_cp'] = ""
            simpan_teks('MAPEL', "")
            simpan_teks('Elemen', "")
            simpan_teks('Materi', "")
            
        simpan_teks('Judul', st.text_input("Judul Modul:"))
    
    with st.container(border=True): 
        st.subheader("🎯 Capaian Pembelajaran & Target SDGs")
        teks_cp_otomatis = st.session_state.get('temp_cp', '')
        cp_input = st.text_area("1. Capaian Pembelajaran (Otomatis Tersedot & Bisa Diedit):", value=teks_cp_otomatis, height=150)
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
        pilihan_sdgs = st.selectbox("2. Capaian SDGs:", opsi_sdgs)
        simpan_teks('Capaian_SDGs', pilihan_sdgs if pilihan_sdgs != "Pilih..." else "")
        tp_sdgs_input = st.text_area("3. Tujuan Pembelajaran (TP) SDGs:", height=100)
        simpan_teks('TP_SDGs', tp_sdgs_input)

# ================= TAB 2 =================
with tab2:
    with st.container(border=True):
        st.subheader("Lingkungan & Praktik Pedagogis")
        col_mitra, col_peda = st.columns(2)
        with col_mitra:
            opsi_mitra = ["Pilih...", "Orang Tua/Wali Murid", "Komunitas Lokal", "Pakar/Praktisi", "Instansi Pemerintah/Puskesmas", "Lembaga Swadaya Masyarakat (LSM)", "Lainnya"]
            pilihan_mitra = st.selectbox("Kemitraan Pembelajaran:", opsi_mitra)
            simpan_teks('Kemitraan_Pembelajaran', st.text_input("Ketik Detail Kemitraan:") if pilihan_mitra == "Lainnya" else pilihan_mitra)
        
        with col_peda:
            # FITUR BARU: Pilih Model dan Tarik Sintaks Otomatis
            opsi_pedagogis = ["Pilih...", "Problem Based Learning (PBL)", "Project Based Learning (PjBL)", "Inquiry/Discovery Learning", "Teaching at the Right Level (TaRL)", "Cooperative Learning", "Lainnya"]
            pilihan_pedagogis = st.selectbox("Praktik Pedagogis (Model Belajar):", opsi_pedagogis)
            simpan_teks('Praktik_Pedagogis', st.text_input("Ketik Model Pedagogis:") if pilihan_pedagogis == "Lainnya" else pilihan_pedagogis)
        
        opsi_budaya = ["Pilih...", "Disiplin Positif & Restitusi", "Growth Mindset (Pola Pikir Berkembang)", "Kolaboratif & Inklusif", "Pembelajaran Berbasis Umpan Balik (Feedback)", "Lainnya"]
        pilihan_budaya = st.selectbox("Budaya Belajar:", opsi_budaya)
        simpan_teks('Budaya_Belajar', st.text_input("Ketik Budaya Belajar:") if pilihan_budaya == "Lainnya" else pilihan_budaya)

    with st.container(border=True):
        # FITUR BARU: Kotak teks Sintaks akan otomatis terisi berdasarkan Pilihan Model di atas
        sintaks_default = kamus_sintaks.get(pilihan_pedagogis, "") if pilihan_pedagogis in kamus_sintaks else ""
        sintaks_input = st.text_area("Urutan Sintaks Pembelajaran (Otomatis menyesuaikan model yang dipilih):", value=sintaks_default, height=150, help="Anda masih bisa mengedit langkah-langkah ini secara manual.")
        simpan_teks('Urutan_Sintkas', sintaks_input)
        
        col_fisik, col_virtual = st.columns(2)
        with col_fisik: simpan_teks('Ruang_Fisik', st.text_area("Ruang Fisik:"))
        with col_virtual: simpan_teks('Ruang_Virtual', st.text_area("Ruang Virtual:"))

# ================= TAB 3 =================
with tab3:
    with st.container(border=True): 
        st.subheader("🧠 Aspek Kognitif")
        with st.expander("💡 Buka Contekan KKO Kognitif (C1-C6)"):
            for level, kata in bank_kko["KOGNITIF (C)"].items():
                st.markdown(f"**{level}**: {kata}")
                
        if st.button("📈 Rumuskan TP Kognitif (Naik Level)", key="btn_tp_kog", use_container_width=True):
            with st.spinner("Memproses rumusan TP..."):
                cp_val = st.session_state.data_isian.get('Capaian_Pembelajaran', '')
                tp_sdgs_val = st.session_state.data_isian.get('TP_SDGs', '')
                prompt_tp_kog = f"Baca Capaian Pembelajaran ini: '{cp_val}'. Identifikasi level KKO kognitifnya (C1-C6). Kemudian, buatkan rumusan Tujuan Pembelajaran (TP) Kognitif yang menaikkan KKO-nya 1 atau 2 level lebih tinggi agar lebih menantang (HOTS). Integrasikan dengan semangat TP SDGs: '{tp_sdgs_val}'. Berikan 2 pilihan rumusan singkat."
                st.session_state['draft_tp_kognitif'] = panggil_ai(prompt_tp_kog, tipe="tp_kog")

        tp_kognitif = st.text_area("TP Kognitif:", value=st.session_state['draft_tp_kognitif'], height=100)
        simpan_teks('TP_KOGNITIF', tp_kognitif)
        
        if st.button("🪜 Rumuskan Indikator Kognitif (Berjenjang)", key="btn_ind_kog", use_container_width=True):
            with st.spinner("Membuat indikator berjenjang (scaffolding)..."):
                tp_val = st.session_state.data_isian.get('TP_KOGNITIF', '')
                prompt_ind_kog = f"Berdasarkan Tujuan Pembelajaran (TP) Kognitif ini: '{tp_val}', buatlah 3-4 Indikator Pencapaian Kompetensi yang berjenjang. Mulailah indikator pertama dari KKO level rendah (LOTS/MOTS) sebagai fondasi, lalu naik secara bertahap, hingga indikator terakhir menggunakan level KKO yang sama persis dengan TP tersebut (HOTS). Gunakan list poin sederhana."
                st.session_state['draft_ind_kognitif'] = panggil_ai(prompt_ind_kog, tipe="ind_kog")
        
        indikator_kognitif = st.text_area("Indikator Kognitif:", value=st.session_state['draft_ind_kognitif'], height=100)
        simpan_teks('Indikator_Kognitif', indikator_kognitif)
        
        if st.button("✨ Rumuskan Pengalaman Kognitif (Sesuai Sintaks)", key="btn_kog", use_container_width=True):
            with st.spinner("Merancang aktivitas berdasarkan Sintaks Model Pembelajaran..."):
                materi_val = st.session_state.data_isian.get('Materi', '')
                cp_val = st.session_state.data_isian.get('Capaian_Pembelajaran', '')
                ind_val = st.session_state.data_isian.get('Indikator_Kognitif', '')
                model_val = st.session_state.data_isian.get('Praktik_Pedagogis', '')
                sintaks_val = st.session_state.data_isian.get('Urutan_Sintkas', '')
                
                # FITUR BARU: Prompt AI dipaksa menggunakan Sintaks dari Tab 2
                konteks = f"Materi: {materi_val}\nModel Pembelajaran: {model_val}\nSintaks/Langkah Model:\n{sintaks_val}\nIndikator Pencapaian: {ind_val}"
                prompt = f"Berdasarkan {konteks}, rancanglah Skenario 'Pengalaman Belajar' (Kegiatan Inti Kognitif). PENTING: Anda WAJIB menjabarkan kegiatan belajar berdasarkan poin-poin 'Sintaks/Langkah Model' di atas secara berurutan. Di setiap langkah sintaks tersebut, jelaskan apa yang dilakukan siswa dan guru untuk mencapai Indikator."
                
                st.session_state.draft_kognitif = panggil_ai(prompt, tipe="pg_kog")
                        
        simpan_teks('Pengalaman_Belajar', st.text_area("Pengalaman Belajar Kognitif:", value=st.session_state.draft_kognitif, height=200))
        
        c1, c2 = st.columns(2)
        with c1: simpan_teks('Asesmen_Formatif', st.text_area("Asesmen Formatif (Kognitif):"))
        with c2: simpan_teks('Asesmen_Sumatif', st.text_area("Asesmen Sumatif (Kognitif):"))

# ================= TAB 4 =================
with tab4:
    with st.container(border=True): 
        st.subheader("A. Identitas Karakter & Nilai Yayasan")
        col_kiri, col_kanan = st.columns(2)
        with col_kiri:
            st.markdown("##### 1. Profil Pelajar Pancasila (P3)")
            fase_terpilih = st.session_state.data_isian.get('Fase', '')
            daftar_dimensi = list(bank_p3.keys())
            pilihan_dimensi = st.selectbox("Dimensi P3:", ["Pilih..."] + daftar_dimensi)
            if pilihan_dimensi != "Pilih...":
                simpan_teks('Dimensi', pilihan_dimensi)
                daftar_elemen = list(bank_p3[pilihan_dimensi].keys())
                pilihan_elemen = st.selectbox("Elemen P3:", ["Pilih..."] + daftar_elemen)
                if pilihan_elemen != "Pilih...":
                    simpan_teks('Elemen_P3', pilihan_elemen)
                    daftar_sub = list(bank_p3[pilihan_dimensi][pilihan_elemen].keys())
                    pilihan_sub = st.selectbox("Sub-elemen P3:", ["Pilih..."] + daftar_sub)
                    if pilihan_sub != "Pilih...":
                        simpan_teks('Sub_elemen', pilihan_sub)
                        teks_cp_p3 = bank_p3[pilihan_dimensi][pilihan_elemen][pilihan_sub].get(fase_terpilih, "Data belum tersedia.") if fase_terpilih in ["Fase Fondasi", "Fase A", "Fase B", "Fase C", "Fase D", "Fase E", "Fase F"] else "Pilih Fase di Tab 1."
                        cp_p3 = st.text_area("Capaian P3 (Otomatis Terisi):", value=teks_cp_p3, height=120)
                        simpan_teks('Capaian_P3', cp_p3)
                    else: simpan_teks('Sub_elemen', ""); simpan_teks('Capaian_P3', "")
                else: simpan_teks('Elemen_P3', ""); simpan_teks('Sub_elemen', ""); simpan_teks('Capaian_P3', "")
            else: simpan_teks('Dimensi', ""); simpan_teks('Elemen_P3', ""); simpan_teks('Sub_elemen', ""); simpan_teks('Capaian_P3', "")
            st.divider()
            st.markdown("##### 2. Santo / Santa Pelindung")
            pilihan_santo = st.selectbox("Pilih Pelindung:", ["Pilih...", "Santo Fransiskus Asisi", "Santa Clara", "Santa Maria", "Lainnya"])
            simpan_teks('Santo_Santa_Pelindung', st.text_input("Ketik Nama Pelindung:") if pilihan_santo == "Lainnya" else pilihan_santo)
            simpan_teks('Nilai_Keutamaan', st.text_input("Nilai/Keutamaan Pelindung:"))

        with col_kanan:
            st.markdown("##### 3. Kearifan Lokal")
            pilihan_kearifan = st.selectbox("Pilih Kearifan Lokal:", ["Pilih...", "Waja Sampai Kaputing", "kayuh Baimbai", "Isen Mulang", "Iya Mulik Bengkang Turan", "Dahani Dahanai Tuntung Tulus", "Belum Bahadat", "Huma Betang", "Handep Hapakat", "Lainnya"])
            simpan_teks('Kearifan_Lokal', st.text_input("Ketik Kearifan Lokal:") if pilihan_kearifan == "Lainnya" else pilihan_kearifan)
            st.divider()
            st.markdown("##### 4. 7 Kebiasaan Anak Indonesia Hebat")
            pilihan_7kaih = st.selectbox("Pilih 7KAIH:", ["Pilih...", "Bangun Pagi", "Beribadah", "Berolahraga", "Makan Sehat dan Bergizi", "Gemar Belajar", "Bermasyarakat", "Tidur Lebih Awal", "Lainnya"])
            simpan_teks('KAIH', st.text_input("Ketik 7KAIH:") if pilihan_7kaih == "Lainnya" else pilihan_7kaih)
            st.divider()
            st.markdown("##### 5. Dimensi Profil Lulusan")
            profil_terpilih = st.session_state.data_isian.get('Dimensi_Lulusan', '')
            if profil_terpilih and profil_terpilih != "Pilih..." and profil_terpilih in bank_dpl:
                pilihan_sub_dpl = st.selectbox("Pilih Sub Dimensi:", ["Pilih..."] + list(bank_dpl[profil_terpilih].keys()))
                if pilihan_sub_dpl != "Pilih...":
                    simpan_teks('Sub_Dimensi', pilihan_sub_dpl)
                    teks_kompetensi = bank_dpl[profil_terpilih][pilihan_sub_dpl].get(fase_terpilih, "Data belum tersedia.") if fase_terpilih in ["Fase Fondasi", "Fase A", "Fase B", "Fase C", "Fase D", "Fase E", "Fase F"] else "Pilih Fase di Tab 1."
                    simpan_teks('Kompetensi', st.text_area("Kompetensi Lulusan:", value=teks_kompetensi, height=120))
                else: simpan_teks('Sub_Dimensi', ""); simpan_teks('Kompetensi', "")
            else: simpan_teks('Sub_Dimensi', ""); simpan_teks('Kompetensi', "")

    with st.container(border=True):
        st.subheader("B. Core Values / Ke-SFD-an")
        jenjang_terpilih = st.session_state.data_isian.get('Jenjang', '')
        col_nilai, col_keutamaan = st.columns(2)
        with col_nilai: pilihan_nilai = st.selectbox("1. Pilih Nilai Ke-SFD-an:", ["Pilih..."] + list(bank_sfd.keys()))
        if pilihan_nilai != "Pilih...":
            simpan_teks('Nilai', pilihan_nilai)
            with col_keutamaan: pilihan_keutamaan = st.selectbox("2. Pilih Keutamaan:", ["Pilih..."] + list(bank_sfd[pilihan_nilai].keys()))
            if pilihan_keutamaan != "Pilih...":
                simpan_teks('Keutamaan', pilihan_keutamaan)
                if jenjang_terpilih in ["TK", "SD", "SMP"]: teks_cn_otomatis = bank_sfd[pilihan_nilai][pilihan_keutamaan].get(jenjang_terpilih, "Data tidak ditemukan.")
                elif jenjang_terpilih == "SMA/SMK": teks_cn_otomatis = "Capaian Nilai (CN) Ke-SFD-an SMA masih dirumuskan."
                else: teks_cn_otomatis = "Pilih Jenjang di Tab 1."
                simpan_teks('Capaian_Nilai', st.text_area("3. Capaian Nilai (Otomatis Terisi):", value=teks_cn_otomatis, height=120))
        else: simpan_teks('Nilai', ""); simpan_teks('Keutamaan', ""); simpan_teks('Capaian_Nilai', "")

    with st.container(border=True): 
        st.subheader("❤️ C. Rencana Pembelajaran Afektif")
        with st.expander("💡 Buka Contekan KKO Afektif (A1-A5)"):
            for level, kata in bank_kko["AFEKTIF (A)"].items(): st.markdown(f"**{level}**: {kata}")
        if st.button("📈 Rumuskan TP Afektif (Sintesis)", key="btn_tp_afe", use_container_width=True):
            with st.spinner("Memproses rumusan afektif..."):
                sfd_cn, nilai_pelindung, cp_p3_val, kearifan_val = st.session_state.data_isian.get('Capaian_Nilai', ''), st.session_state.data_isian.get('Nilai_Keutamaan', ''), st.session_state.data_isian.get('Capaian_P3', ''), st.session_state.data_isian.get('Kearifan_Lokal', '')
                prompt_tp_afe = f"Elemen afektif: P3 ({cp_p3_val}), Nilai SFD ({sfd_cn}), Keteladanan ({nilai_pelindung}), Kearifan ({kearifan_val}). Tolong sintesis menjadi satu rumusan TP Afektif yang kuat dengan menaikkan level KKO satu tingkat."
                st.session_state['draft_tp_afektif'] = panggil_ai(prompt_tp_afe, tipe="tp_afe")

        simpan_teks('TP_Afektif', st.text_area("TP Afektif:", value=st.session_state['draft_tp_afektif'], height=120))
        
        if st.button("🪜 Rumuskan Indikator Afektif (Berjenjang)", key="btn_ind_afe", use_container_width=True):
            with st.spinner("Membuat indikator sikap berjenjang..."):
                tp_val = st.session_state.data_isian.get('TP_Afektif', '')
                prompt_ind_afe = f"Berdasarkan TP Afektif ini: '{tp_val}', buat 3-4 Indikator Pencapaian Sikap yang berjenjang. Mulai dari level dasar (A1/A2), naik bertahap, hingga poin terakhir sama persis dengan KKO TP tersebut."
                st.session_state['draft_ind_afektif'] = panggil_ai(prompt_ind_afe, tipe="ind_afe")
        
        simpan_teks('Indikator_Afektif', st.text_area("Indikator Afektif:", value=st.session_state['draft_ind_afektif'], height=100))
        
        if st.button("✨ Rumuskan Pengalaman Afektif", key="btn_afe", use_container_width=True):
            with st.spinner("Merancang aktivitas karakter..."):
                materi_val, ind_val = st.session_state.data_isian.get('Materi', ''), st.session_state.data_isian.get('Indikator_Afektif', '')
                konteks = f"Materi: {materi_val}\nKognitif: {st.session_state.draft_kognitif}\nIndikator Afektif: {ind_val}\n"
                prompt = f"Berdasarkan {konteks}, rancang 'Pengalaman Belajar' afektif (sikap/karakter) untuk indikator tersebut. Buat aktivitas reflektif/empati dalam 3-4 poin praktis."
                st.session_state.draft_afektif = panggil_ai(prompt, tipe="pg_afe")

        simpan_teks('Pengalaman_Belajar_Afektif', st.text_area("Pengalaman Belajar Afektif:", value=st.session_state.draft_afektif, height=150))
        c11, c12 = st.columns(2)
        with c11: simpan_teks('Formatif', st.text_area("Asesmen Formatif (Afektif):"))
        with c12: simpan_teks('Sumatif', st.text_area("Asesmen Sumatif (Afektif):"))

# ================= TAB 5 =================
with tab5:
    with st.container(border=True): 
        st.subheader("🏃 Aspek Psikomotorik")
        with st.expander("💡 Buka Contekan KKO Psikomotorik (P1-P5)"):
            for level, kata in bank_kko["PSIKOMOTORIK (P)"].items(): st.markdown(f"**{level}**: {kata}")

        if st.button("📈 Rumuskan TP Psikomotorik (Naik Level)", key="btn_tp_psi", use_container_width=True):
            with st.spinner("Memproses rumusan psikomotorik..."):
                cp_val, tp_sdgs_val = st.session_state.data_isian.get('Capaian_Pembelajaran', ''), st.session_state.data_isian.get('TP_SDGs', '')
                prompt_tp_psi = f"Baca CP ini: '{cp_val}'. Buatkan rumusan TP Psikomotorik yang menaikkan KKO-nya 1 atau 2 level lebih tinggi. Integrasikan dengan semangat SDGs: '{tp_sdgs_val}'."
                st.session_state['draft_tp_psikomotor'] = panggil_ai(prompt_tp_psi, tipe="tp_psi")

        simpan_teks('TP_Psikomotorik', st.text_area("TP Psikomotorik:", value=st.session_state['draft_tp_psikomotor'], height=100))
        
        if st.button("🪜 Rumuskan Indikator Psikomotorik (Berjenjang)", key="btn_ind_psi", use_container_width=True):
            with st.spinner("Membuat indikator keterampilan berjenjang..."):
                tp_val = st.session_state.data_isian.get('TP_Psikomotorik', '')
                prompt_ind_psi = f"Berdasarkan TP Psikomotorik ini: '{tp_val}', buat 3-4 Indikator Pencapaian Keterampilan berjenjang. Mulai level dasar (P1/P2), naik bertahap, hingga poin terakhir menggunakan KKO yang sama dengan TP tersebut."
                st.session_state['draft_ind_psikomotorik'] = panggil_ai(prompt_ind_psi, tipe="ind_psi")

        simpan_teks('Indikator_Psikomotorik', st.text_area("Indikator Psikomotorik:", value=st.session_state['draft_ind_psikomotorik'], height=100))
        
        if st.button("✨ Rumuskan Pengalaman Psikomotorik", key="btn_psi", use_container_width=True):
            with st.spinner("Merancang aktivitas psikomotorik..."):
                materi_val, ind_val = st.session_state.data_isian.get('Materi', ''), st.session_state.data_isian.get('Indikator_Psikomotorik', '')
                konteks = f"Materi: {materi_val}\nIndikator Keterampilan: {ind_val}\nKegiatan Sebelumnya: {st.session_state.draft_kognitif}\n"
                prompt = f"Berdasarkan {konteks}, buat skenario unjuk kerja/proyek untuk pencapaian indikator tersebut dalam 3-4 poin praktis."
                st.session_state.draft_psikomotor = panggil_ai(prompt, tipe="pg_psi")

        simpan_teks('Pengalaman_Belajar_Psikomotorik', st.text_area("Pengalaman Belajar Psikomotorik:", value=st.session_state.draft_psikomotor, height=120))
        c3, c4 = st.columns(2)
        with c3: simpan_teks('Asesmen_Formatif_Psikomotorik', st.text_area("Asesmen Formatif (Psikomotorik):"))
        with c4: simpan_teks('Asesmen_Sumatif_Psikomotorik', st.text_area("Asesmen Sumatif (Psikomotorik):"))

# ================= TAB 6 =================
with tab6:
    with st.container(border=True): 
        st.subheader("Perayaan Belajar & Media")
        simpan_teks('Membagikan_Pengalaman_Belajar', st.text_area("Membagikan Pengalaman Belajar:"))
        simpan_teks('Refleksi_Perkembangan_Kompetensi', st.text_area("Refleksi Perkembangan Kompetensi:"))
        simpan_teks('Apresiasi', st.text_area("Apresiasi:"))
        simpan_teks('Media_Pembelajaran', st.text_area("Media Pembelajaran:"))
    
    with st.container(border=True): 
        st.subheader("👁️ Pratinjau Dokumen Sementara")
        with st.expander("Klik untuk memeriksa ringkasan isian Anda sebelum merakit dokumen", expanded=False):
            st.markdown(f"**Identitas:** {st.session_state.data_isian.get('Nama_Guru', '-')} | Jenjang {st.session_state.data_isian.get('Jenjang', '-')} | Fase {st.session_state.data_isian.get('Fase', '-')}\n**Mapel & Materi:** {st.session_state.data_isian.get('MAPEL', '-')} ({st.session_state.data_isian.get('Materi', '-')})\n**TP Kognitif:** {st.session_state.data_isian.get('TP_KOGNITIF', '-')}\n**Nilai SFD:** {st.session_state.data_isian.get('Nilai', '-')} - {st.session_state.data_isian.get('Keutamaan', '-')}")
        st.divider()
        st.subheader("🖨️ Rakit Dokumen & Simpan ke Database")
        if st.button("Rakit & Simpan Data", type="primary", use_container_width=True):
            if not st.session_state.data_isian.get('Nama_Guru'): st.error("❌ Mohon isi Nama Guru Penyusun di Tab 1 terlebih dahulu!")
            else:
                with st.spinner('Memproses dokumen cerdas Anda...'):
                    try:
                        doc = DocxTemplate("Template_DPB_Schola Amoris.docx")
                        if foto_sdgs is not None: st.session_state.data_isian['Gambar_SGDs'] = InlineImage(doc, foto_sdgs, width=Mm(30))
                        doc.render(st.session_state.data_isian)
                        bio = io.BytesIO()
                        doc.save(bio)
                        data_kirim = {"nama_guru": st.session_state.data_isian.get('Nama_Guru', '-'), "jenjang": st.session_state.data_isian.get('Jenjang', '-'), "kelas": st.session_state.data_isian.get('Kelas', '-'), "mapel": st.session_state.data_isian.get('MAPEL', '-'), "judul": st.session_state.data_isian.get('Judul', '-')}
                        try:
                            respon = requests.post(URL_DATABASE, json=data_kirim) 
                            if respon.status_code == 200: st.toast('Data berhasil tersinkronisasi!', icon='✅')
                        except: pass
                        st.success("🎉 Berhasil! Dokumen DPB Anda sudah siap diunduh.")
                        st.download_button(label="📥 Download File DPB (.docx)", data=bio.getvalue(), file_name=f"DPB_{st.session_state.data_isian.get('MAPEL', 'Mapel')}.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document", use_container_width=True)
                    except Exception as e: st.error(f"Terjadi kesalahan perakitan Word: {e}")
