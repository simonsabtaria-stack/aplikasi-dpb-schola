import streamlit as st
import pandas as pd # Tambahan untuk merapikan tabel perpustakaan
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm
import io
import requests  
import google.generativeai as genai
import os

# --- IMPOR UNTUK RAG & DATABASE SUPABASE ---
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from supabase import create_client, Client

# Impor Database Internal
from data_kurikulum import bank_kurikulum
from data_sfd import bank_sfd
from data_kko import bank_kko
from data_p3 import bank_p3
from data_dpl import bank_dpl

st.set_page_config(page_title="DPB Schola Amoris", page_icon="📝", layout="wide")

# ==========================================
# 🔐 PENGATURAN BRANKAS SUPABASE
# ==========================================
try:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    supabase: Client = create_client(url, key)
except Exception as e:
    supabase = None
    st.error("Koneksi Supabase belum diatur di Secrets Streamlit.")

# ==========================================
# KAMUS & INISIALISASI MEMORI
# ==========================================
kamus_sintaks = {
    "Problem Based Learning (PBL)": "1. Orientasi peserta didik pada masalah\n2. Mengorganisasikan peserta didik untuk belajar\n3. Membimbing penyelidikan individu maupun kelompok\n4. Mengembangkan dan menyajikan hasil karya\n5. Menganalisis dan mengevaluasi proses pemecahan masalah",
    "Project Based Learning (PjBL)": "1. Penentuan pertanyaan mendasar\n2. Mendesain perencanaan proyek\n3. Menyusun jadwal (Time schedule)\n4. Memonitor peserta didik dan kemajuan proyek\n5. Menguji hasil\n6. Mengevaluasi pengalaman",
    "Inquiry/Discovery Learning": "1. Pemberian rangsangan (Stimulation)\n2. Pernyataan/Identifikasi masalah (Problem Statement)\n3. Pengumpulan data (Data Collection)\n4. Pengolahan data (Data Processing)\n5. Pembuktian (Verification)\n6. Menarik kesimpulan (Generalization)",
    "Teaching at the Right Level (TaRL)": "1. Asesmen diagnostik awal\n2. Pengelompokan peserta didik berdasarkan capaian\n3. Pendampingan dan pembelajaran berdiferensiasi\n4. Evaluasi formatif berkala\n5. Rotasi/Penyesuaian kelompok berkelanjutan",
    "Cooperative Learning": "1. Menyampaikan tujuan dan memotivasi peserta didik\n2. Menyajikan informasi\n3. Mengorganisasikan peserta didik ke dalam kelompok-kelompok belajar\n4. Membimbing kelompok bekerja dan belajar\n5. Evaluasi\n6. Memberikan penghargaan"
}

def inisialisasi_memori():
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
    if "chat_amor" not in st.session_state:
        st.session_state.chat_amor = [{"role": "assistant", "content": "Halo Bapak/Ibu Guru yang luar biasa! 🌟 Saya Amor, asisten pribadi Anda. Ada yang bisa saya bantu hari ini?"}]
    if "username_aktif" not in st.session_state: st.session_state.username_aktif = None

inisialisasi_memori()

def simpan_teks(kunci, nilai):
    st.session_state.data_isian[kunci] = nilai

# ==========================================
# 💾 FUNGSI DATABASE (SIMPAN & MUAT DRAF)
# ==========================================
def simpan_draft_ke_awan():
    if supabase is None:
        st.error("Koneksi Supabase belum diatur!")
        return
    data_bersih = {k: v for k, v in st.session_state.data_isian.items() if k != 'Gambar_SGDs'}
    try:
        cek = supabase.table("draft_guru").select("*").eq("username", st.session_state.username_aktif).execute()
        if len(cek.data) > 0:
            supabase.table("draft_guru").update({"data_isian": data_bersih}).eq("username", st.session_state.username_aktif).execute()
        else:
            supabase.table("draft_guru").insert({"username": st.session_state.username_aktif, "data_isian": data_bersih}).execute()
        st.toast(f"Draf berhasil disimpan ke Brankas Awan, {st.session_state.username_aktif}! ☁️", icon="✅")
    except Exception as e:
        st.error(f"Gagal menyimpan ke awan: {e}")

def muat_draft_dari_awan(user):
    if supabase is None: return
    try:
        cek = supabase.table("draft_guru").select("data_isian").eq("username", user).execute()
        if len(cek.data) > 0:
            st.session_state.data_isian = cek.data[0]['data_isian']
            st.session_state.data_isian['Nama_Guru'] = user
            st.toast("Berhasil memuat pekerjaan Anda sebelumnya!", icon="📥")
        else:
            st.toast("Anda belum memiliki draf tersimpan. Memulai lembar baru.", icon="✨")
            st.session_state.data_isian['Nama_Guru'] = user
    except Exception as e:
        st.error(f"Gagal memuat draf: {e}")

# ==========================================
# 🚪 HALAMAN LOGIN
# ==========================================
if st.session_state.username_aktif is None:
    try:
        st.image("banner_schola.png", use_container_width=True)
    except:
        pass
    st.markdown("<h1 style='text-align: center;'>Pintu Gerbang Penyusun DPB 🎓</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        with st.container(border=True):
            st.markdown("### 🔐 Masuk ke Ruang Kerja")
            st.info("Ketik nama Anda untuk memulai. Pekerjaan Anda akan disimpan atas nama ini.")
            input_nama = st.text_input("Nama Guru / Username (Contoh: Bapak Budi):")
            if st.button("Mulai Merancang DPB 🚀", use_container_width=True, type="primary"):
                if input_nama.strip() == "":
                    st.warning("Nama tidak boleh kosong!")
                else:
                    st.session_state.username_aktif = input_nama.strip()
                    muat_draft_dari_awan(st.session_state.username_aktif)
                    st.rerun()
    st.stop() 

# JIKA SUDAH LOGIN, TAMPILKAN APLIKASI UTAMA
try:
    st.image("banner_schola.png", use_container_width=True)
except:
    pass
col_title, col_logout = st.columns([4,1])
with col_title:
    st.title("Penyusun DPB Schola Amoris 🎓")
    st.markdown(f"**Selamat bekerja, {st.session_state.username_aktif}!** Pekerjaan Anda aman di awan.")
with col_logout:
    if st.button("🚪 Keluar (Logout)"):
        st.session_state.username_aktif = None
        inisialisasi_memori() 
        st.rerun()

# ==========================================
# FUNGSI AI AMOR & PERUMUS
# ==========================================
def panggil_amor(pertanyaan, api_key):
    if not api_key: return "Mohon maaf Bapak/Ibu Guru, Amor butuh Kunci API Gemini untuk bisa membantu. 🙏"
    if not os.path.exists("faiss_amor"): return "Maaf Bapak/Ibu, otak referensi Amor belum diunggah. 😔"
    try:
        genai.configure(api_key=api_key)
        mesin_tersedia = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        nama_mesin = next((m for m in mesin_tersedia if 'flash' in m.lower() and '1.5' in m), mesin_tersedia[0])
        model = genai.GenerativeModel(nama_mesin)
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        vector_db = FAISS.load_local("faiss_amor", embeddings, allow_dangerous_deserialization=True)
        docs = vector_db.similarity_search(pertanyaan, k=4)
        referensi = "\n\n".join([doc.page_content for doc in docs])
        prompt_amor = f"Anda adalah 'Amor', asisten virtual senior Schola Amoris. Jawab berdasarkan REFERENSI ini saja:\n{referensi}\nPERTANYAAN: {pertanyaan}"
        return model.generate_content(prompt_amor).text
    except Exception as e: return f"Waduh, sepertinya ada gangguan teknis. (Error: {e}) 🛠️"

def fallback_generator(tipe):
    m = st.session_state.data_isian.get('Materi', 'materi')
    if tipe == "tp_kog": return f"Melalui eksplorasi mandiri, peserta didik mampu menguraikan konsep {m} secara kritis."
    elif tipe == "ind_kog": return f"- Menjelaskan konsep dasar {m}\n- Menganalisis kasus terkait {m}"
    elif tipe == "pg_kog": return f"Kegiatan Inti:\n{st.session_state.data_isian.get('Urutan_Sintkas', 'Eksplorasi')}"
    elif tipe == "tp_afe": return f"Peserta didik mampu menunjukkan sikap selaras dengan kearifan lokal."
    elif tipe == "ind_afe": return f"- Menerima arahan\n- Menginternalisasi karakter harian"
    elif tipe == "pg_afe": return f"- Refleksi Diri\n- Aksi Nyata"
    elif tipe == "tp_psi": return f"Peserta didik terampil mendemonstrasikan prosedur terkait {m}."
    elif tipe == "ind_psi": return f"- Meniru tahapan\n- Mendemonstrasikan keterampilan mandiri"
    elif tipe == "pg_psi": return f"- Persiapan\n- Unjuk Kerja\n- Gelar Karya"
    return "Data diproses."

def ambil_referensi_rag(query):
    if not os.path.exists("faiss_index"): return ""
    try:
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        vector_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
        return "\n\nREFERENSI:\n" + "\n\n".join([doc.page_content for doc in vector_db.similarity_search(query, k=3)])
    except: return "" 

def panggil_ai(prompt, tipe=""):
    if not api_key_guru: return fallback_generator(tipe)
    try:
        genai.configure(api_key=api_key_guru)
        m_list = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        m_name = next((m for m in m_list if 'flash' in m.lower() and '1.5' in m), m_list[0])
        return genai.GenerativeModel(m_name).generate_content(prompt + ambil_referensi_rag(prompt) + "\nATURAN: Gunakan list poin, hindari kapital semua.").text
    except: return fallback_generator(tipe)

# ==========================================
# SIDEBAR
# ==========================================
with st.sidebar:
    st.success(f"👤 Aktif sebagai: **{st.session_state.username_aktif}**")
    
    if st.button("☁️ Simpan Draf ke Awan", type="primary", use_container_width=True):
        with st.spinner("Menyimpan..."):
            simpan_draft_ke_awan()
            
    if st.button("🔄 Kosongkan Lembar (Mulai Baru)", use_container_width=True):
        st.session_state.data_isian = {}
        st.session_state.data_isian['Nama_Guru'] = st.session_state.username_aktif
        st.rerun()
        
    st.divider()
    st.header("🤖 Pusat Kontrol AI")
    api_key_guru = st.text_input("🔑 Kunci API Gemini:", type="password")
    st.divider()
    
    st.markdown("### 💬 Tanya Amor")
    wadah_chat = st.container(height=350)
    with wadah_chat:
        for msg in st.session_state.chat_amor:
            st.markdown(f"**{'🧡 Amor' if msg['role']=='assistant' else '👤 Anda'}:** {msg['content']}")
    
    pertanyaan_baru = st.chat_input("Tanya Amor di sini...")
    if pertanyaan_baru:
        st.session_state.chat_amor.append({"role": "user", "content": pertanyaan_baru})
        st.session_state.chat_amor.append({"role": "assistant", "content": panggil_amor(pertanyaan_baru, api_key_guru)})
        st.rerun() 

# ==========================================
# TABS UTAMA (DITAMBAH PERPUSTAKAAN)
# ==========================================
st.markdown("""<style>.stTabs [data-baseweb="tab-list"] { gap: 10px; } .stTabs [data-baseweb="tab"] { background-color: #f1f5f9; border-radius: 8px 8px 0px 0px; padding: 10px 20px; box-shadow: inset 0 -2px 0 0 #cbd5e1; } .stTabs [aria-selected="true"] { background-color: #1e293b; color: #ffffff !important; } .stTextInput input, .stTextArea textarea, .stSelectbox [data-baseweb="select"] { border-radius: 8px !important; } .stButton > button[kind="primary"] { border-radius: 8px; background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%); color: white; border: none; }</style>""", unsafe_allow_html=True)

with st.expander("📖 Panduan Singkat Penyusunan DPB (Klik untuk membuka)"):
    st.markdown("""
    **Selamat datang di asisten penyusun DPB! Berikut adalah langkah mudah penggunaannya:**
    1. **Isi Data Dasar (Tab 1 & 2):** Mulailah dengan melengkapi identitas Anda.
    2. **Gunakan Keajaiban AI (Tab 3, 4, 5):** Klik tombol biru **'Rumuskan...'**.
    3. **Cetak & Unduh (Tab 6):** Rakit dokumen menjadi Word.
    4. **Perpustakaan (Tab 7):** Cari referensi dan buku pelajaran.
    """)
    
kunci_wajib = ['Nama_Guru', 'MAPEL', 'Materi', 'Capaian_Pembelajaran', 'TP_KOGNITIF', 'TP_Psikomotorik', 'TP_Afektif']
terisi = sum(1 for k in kunci_wajib if st.session_state.data_isian.get(k) and str(st.session_state.data_isian.get(k)).strip() != "")
persentase = int((terisi / len(kunci_wajib)) * 100)

st.markdown(f"**Progres Kelengkapan DPB: {persentase}%**")
st.progress(persentase)

# --- TAB DITAMBAH MENJADI 7 ---
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["📋 1. Identitas", "🏫 2. Lingkungan", "🧠 3. Kognitif", "❤️ 4. Afektif", "🏃 5. Psikomotorik", "🖨️ 6. Pratinjau & Cetak", "📚 7. Perpustakaan"])

with tab1:
    with st.container(border=True):
        st.subheader("A. Identitas Guru & Jenjang")
        simpan_teks('Nama_Guru', st.text_input("Nama Guru Penyusun (Wajib diisi):", value=st.session_state.data_isian.get('Nama_Guru', st.session_state.username_aktif), disabled=True))
        col1, col2, col3, col4, col5 = st.columns(5)
        
        def get_idx(options, val, default=0): return options.index(val) if val in options else default
        
        opsi_jenjang = ["Pilih...", "TK", "SD", "SMP", "SMA/SMK"]
        with col1: simpan_teks('Jenjang', st.selectbox("Jenjang:", opsi_jenjang, index=get_idx(opsi_jenjang, st.session_state.data_isian.get('Jenjang'))))
        
        opsi_fase = ["-", "Fase Fondasi", "Fase A", "Fase B", "Fase C", "Fase D", "Fase E", "Fase F"]
        with col2: simpan_teks('Fase', st.selectbox("Fase:", opsi_fase, index=get_idx(opsi_fase, st.session_state.data_isian.get('Fase'))))
        
        opsi_kelas = ["Pilih...", "TK A", "TK B", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "Lainnya"]
        with col3: simpan_teks('Kelas', st.selectbox("Kelas", opsi_kelas, index=get_idx(opsi_kelas, st.session_state.data_isian.get('Kelas'))))
        
        opsi_sem = ["Ganjil", "Genap"]
        with col4: simpan_teks('Semester', st.selectbox("Semester:", opsi_sem, index=get_idx(opsi_sem, st.session_state.data_isian.get('Semester'))))
        
        with col5: simpan_teks('Alokasi_Waktu', st.text_input("Alokasi Waktu:", value=st.session_state.data_isian.get('Alokasi_Waktu', '')))
            
        col_profil, col_sdgs = st.columns(2)
        opsi_dpl = ["Pilih..."] + list(bank_dpl.keys())
        with col_profil: simpan_teks('Dimensi_Lulusan', st.selectbox("Dimensi Profil Lulusan:", opsi_dpl, index=get_idx(opsi_dpl, st.session_state.data_isian.get('Dimensi_Lulusan'))))
        with col_sdgs: foto_sdgs = st.file_uploader("Upload Logo SDGs (Opsional)", type=['png', 'jpg', 'jpeg'])
        st.divider()
        simpan_teks('Identifikasi_Peserta_Didik', st.text_area("Hasil Asesmen Diagnostik:", value=st.session_state.data_isian.get('Identifikasi_Peserta_Didik', '')))

    with st.container(border=True):
        st.subheader("B. Data Umum & Konten")
        fase_terpilih = st.session_state.data_isian.get('Fase', '')
        opsi_mapel = ["Pilih..."] + list(bank_kurikulum.get(fase_terpilih, {}).keys()) + ["Lainnya (Ketik Manual)"]
        
        val_mapel_db = st.session_state.data_isian.get('MAPEL', '')
        idx_mapel = get_idx(opsi_mapel, val_mapel_db) if val_mapel_db in opsi_mapel else (len(opsi_mapel)-1 if val_mapel_db else 0)
        pilihan_mapel = st.selectbox("Mata Pelajaran:", opsi_mapel, index=idx_mapel)
        
        if pilihan_mapel == "Lainnya (Ketik Manual)":
            simpan_teks('MAPEL', st.text_input("Ketik Nama Mata Pelajaran:", value=st.session_state.data_isian.get('MAPEL', '')))
            c_el, c_mat = st.columns(2)
            with c_el: simpan_teks('Elemen', st.text_input("Ketik Elemen:", value=st.session_state.data_isian.get('Elemen', '')))
            with c_mat: simpan_teks('Materi', st.text_input("Ketik Materi Esensial:", value=st.session_state.data_isian.get('Materi', '')))
            st.session_state['temp_cp'] = "" 
        elif pilihan_mapel != "Pilih...":
            simpan_teks('MAPEL', pilihan_mapel)
            elemen_tersedia = list(bank_kurikulum[fase_terpilih][pilihan_mapel].keys())
            elemen_terpilih = st.multiselect(f"Elemen ({pilihan_mapel}):", elemen_tersedia)
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
        
        simpan_teks('Judul', st.text_input("Judul Modul:", value=st.session_state.data_isian.get('Judul', '')))
    
    with st.container(border=True): 
        st.subheader("🎯 Capaian Pembelajaran & SDGs")
        if st.session_state.get('temp_cp') == "": st.session_state['temp_cp'] = st.session_state.data_isian.get('Capaian_Pembelajaran', '')
        simpan_teks('Capaian_Pembelajaran', st.text_area("1. Capaian Pembelajaran:", value=st.session_state.get('temp_cp', ''), height=150))
        opsi_sdgs = ["Pilih...", "1. Tanpa Kemiskinan", "2. Tanpa Kelaparan", "3. Kehidupan Sehat dan Sejahtera", "4. Pendidikan Berkualitas", "5. Kesetaraan Gender", "6. Air Bersih dan Sanitasi Layak", "7. Energi Bersih dan Terjangkau", "8. Pekerjaan Layak dan Pertumbuhan Ekonomi", "9. Industri, Inovasi dan Infrastruktur", "10. Berkurangnya Kesenjangan", "11. Kota dan Permukiman yang Berkelanjutan", "12. Konsumsi dan Produksi yang Bertanggung Jawab", "13. Penanganan Perubahan Iklim", "14. Ekosistem Lautan", "15. Ekosistem Daratan", "16. Perdamaian, Keadilan dan Kelembagaan yang Tangguh", "17. Kemitraan untuk Mencapai Tujuan"]
        simpan_teks('Capaian_SDGs', st.selectbox("2. Capaian SDGs:", opsi_sdgs, index=get_idx(opsi_sdgs, st.session_state.data_isian.get('Capaian_SDGs'))))
        simpan_teks('TP_SDGs', st.text_area("3. Tujuan Pembelajaran (TP) SDGs:", value=st.session_state.data_isian.get('TP_SDGs', '')))

with tab2:
    with st.container(border=True):
        col_mitra, col_peda = st.columns(2)
        with col_mitra:
            ops_m = ["Pilih...", "Orang Tua/Wali Murid", "Komunitas Lokal", "Pakar/Praktisi", "Instansi Pemerintah/Puskesmas", "Lembaga Swadaya Masyarakat (LSM)", "Lainnya"]
            val_m = st.session_state.data_isian.get('Kemitraan_Pembelajaran', '')
            pil_mitra = st.selectbox("Kemitraan Pembelajaran:", ops_m, index=get_idx(ops_m, val_m) if val_m in ops_m else (len(ops_m)-1 if val_m else 0))
            simpan_teks('Kemitraan_Pembelajaran', st.text_input("Ketik Kemitraan:", value=val_m if pil_mitra == "Lainnya" else "") if pil_mitra == "Lainnya" else pil_mitra)
        with col_peda:
            ops_p = ["Pilih...", "Problem Based Learning (PBL)", "Project Based Learning (PjBL)", "Inquiry/Discovery Learning", "Teaching at the Right Level (TaRL)", "Cooperative Learning", "Lainnya"]
            val_p = st.session_state.data_isian.get('Praktik_Pedagogis', '')
            pil_peda = st.selectbox("Praktik Pedagogis:", ops_p, index=get_idx(ops_p, val_p) if val_p in ops_p else (len(ops_p)-1 if val_p else 0))
            simpan_teks('Praktik_Pedagogis', st.text_input("Ketik Model:", value=val_p if pil_peda == "Lainnya" else "") if pil_peda == "Lainnya" else pil_peda)
        
        ops_b = ["Pilih...", "Disiplin Positif & Restitusi", "Growth Mindset", "Kolaboratif & Inklusif", "Pembelajaran Berbasis Umpan Balik (Feedback)", "Lainnya"]
        val_b = st.session_state.data_isian.get('Budaya_Belajar', '')
        pil_budaya = st.selectbox("Budaya Belajar:", ops_b, index=get_idx(ops_b, val_b) if val_b in ops_b else (len(ops_b)-1 if val_b else 0))
        simpan_teks('Budaya_Belajar', st.text_input("Ketik Budaya Belajar:", value=val_b if pil_budaya == "Lainnya" else "") if pil_budaya == "Lainnya" else pil_budaya)

    with st.container(border=True):
        sintaks_default = st.session_state.data_isian.get('Urutan_Sintkas', kamus_sintaks.get(pil_peda, ""))
        simpan_teks('Urutan_Sintkas', st.text_area("Urutan Sintaks Pembelajaran:", value=sintaks_default, height=150))
        c_f, c_v = st.columns(2)
        with c_f: simpan_teks('Ruang_Fisik', st.text_area("Ruang Fisik:", value=st.session_state.data_isian.get('Ruang_Fisik', '')))
        with c_v: simpan_teks('Ruang_Virtual', st.text_area("Ruang Virtual:", value=st.session_state.data_isian.get('Ruang_Virtual', '')))

with tab3:
    with st.container(border=True): 
        st.subheader("🧠 Aspek Kognitif")
        if st.button("📈 Rumuskan TP Kognitif", key="btn_tp_kog", use_container_width=True):
            with st.spinner("Memproses TP..."):
                st.session_state.data_isian['TP_KOGNITIF'] = panggil_ai(f"Baca CP: '{st.session_state.data_isian.get('Capaian_Pembelajaran', '')}'. Rumuskan TP Kognitif yang menaikkan KKO-nya (HOTS). Integrasikan SDGs: '{st.session_state.data_isian.get('TP_SDGs', '')}'.", "tp_kog")
        simpan_teks('TP_KOGNITIF', st.text_area("TP Kognitif:", value=st.session_state.data_isian.get('TP_KOGNITIF', ''), height=100))
        
        if st.button("🪜 Rumuskan Indikator Kognitif", key="btn_ind_kog", use_container_width=True):
            with st.spinner("Membuat indikator berjenjang..."):
                st.session_state.data_isian['Indikator_Kognitif'] = panggil_ai(f"Dari TP Kognitif: '{st.session_state.data_isian.get('TP_KOGNITIF', '')}', buat 3-4 Indikator berjenjang (scaffolding) dari LOTS ke HOTS.", "ind_kog")
        simpan_teks('Indikator_Kognitif', st.text_area("Indikator Kognitif:", value=st.session_state.data_isian.get('Indikator_Kognitif', ''), height=100))
        
        if st.button("✨ Rumuskan Pengalaman Kognitif", key="btn_kog", use_container_width=True):
            with st.spinner("Merancang aktivitas..."):
                st.session_state.data_isian['Pengalaman_Belajar'] = panggil_ai(f"Materi: {st.session_state.data_isian.get('Materi', '')}\nSintaks:\n{st.session_state.data_isian.get('Urutan_Sintkas', '')}\nIndikator: {st.session_state.data_isian.get('Indikator_Kognitif', '')}\nRancang Pengalaman Belajar wajib menjabarkan Sintaks.", "pg_kog")
        simpan_teks('Pengalaman_Belajar', st.text_area("Pengalaman Belajar Kognitif:", value=st.session_state.data_isian.get('Pengalaman_Belajar', ''), height=200))
        c1, c2 = st.columns(2)
        with c1: simpan_teks('Asesmen_Formatif', st.text_area("Asesmen Formatif (Kognitif):", value=st.session_state.data_isian.get('Asesmen_Formatif', '')))
        with c2: simpan_teks('Asesmen_Sumatif', st.text_area("Asesmen Sumatif (Kognitif):", value=st.session_state.data_isian.get('Asesmen_Sumatif', '')))

with tab4:
    with st.container(border=True): 
        col_kiri, col_kanan = st.columns(2)
        with col_kiri:
            st.markdown("##### 1. Profil Pelajar Pancasila (P3)")
            fase = st.session_state.data_isian.get('Fase', '')
            ops_dim = ["Pilih..."] + list(bank_p3.keys())
            pil_dim = st.selectbox("Dimensi P3:", ops_dim, index=get_idx(ops_dim, st.session_state.data_isian.get('Dimensi')))
            if pil_dim != "Pilih...":
                simpan_teks('Dimensi', pil_dim)
                ops_el = ["Pilih..."] + list(bank_p3[pil_dim].keys())
                pil_el = st.selectbox("Elemen P3:", ops_el, index=get_idx(ops_el, st.session_state.data_isian.get('Elemen_P3')))
                if pil_el != "Pilih...":
                    simpan_teks('Elemen_P3', pil_el)
                    ops_sub = ["Pilih..."] + list(bank_p3[pil_dim][pil_el].keys())
                    pil_sub = st.selectbox("Sub-elemen P3:", ops_sub, index=get_idx(ops_sub, st.session_state.data_isian.get('Sub_elemen')))
                    if pil_sub != "Pilih...":
                        simpan_teks('Sub_elemen', pil_sub)
                        cp_p3_teks = bank_p3[pil_dim][pil_el][pil_sub].get(fase, "Data belum tersedia.") if fase in ["Fase Fondasi", "Fase A", "Fase B", "Fase C", "Fase D", "Fase E", "Fase F"] else "Pilih Fase di Tab 1."
                        simpan_teks('Capaian_P3', st.text_area("Capaian P3:", value=st.session_state.data_isian.get('Capaian_P3', cp_p3_teks), height=120))
                    else: simpan_teks('Sub_elemen', ""); simpan_teks('Capaian_P3', "")
                else: simpan_teks('Elemen_P3', ""); simpan_teks('Sub_elemen', ""); simpan_teks('Capaian_P3', "")
            else: simpan_teks('Dimensi', ""); simpan_teks('Elemen_P3', ""); simpan_teks('Sub_elemen', ""); simpan_teks('Capaian_P3', "")
            
            st.divider()
            ops_santo = ["Pilih...", "Santo Fransiskus Asisi", "Santa Clara", "Santa Maria", "Lainnya"]
            val_santo = st.session_state.data_isian.get('Santo_Santa_Pelindung', '')
            pil_santo = st.selectbox("Pilih Pelindung:", ops_santo, index=get_idx(ops_santo, val_santo) if val_santo in ops_santo else (len(ops_santo)-1 if val_santo else 0))
            simpan_teks('Santo_Santa_Pelindung', st.text_input("Nama Pelindung:", value=val_santo if pil_santo=="Lainnya" else "") if pil_santo == "Lainnya" else pil_santo)
            simpan_teks('Nilai_Keutamaan', st.text_input("Nilai/Keutamaan Pelindung:", value=st.session_state.data_isian.get('Nilai_Keutamaan', '')))

        with col_kanan:
            ops_k = ["Pilih...", "Waja Sampai Kaputing", "kayuh Baimbai", "Isen Mulang", "Iya Mulik Bengkang Turan", "Dahani Dahanai Tuntung Tulus", "Belum Bahadat", "Huma Betang", "Handep Hapakat", "Lainnya"]
            val_k = st.session_state.data_isian.get('Kearifan_Lokal', '')
            pil_kearifan = st.selectbox("Kearifan Lokal:", ops_k, index=get_idx(ops_k, val_k) if val_k in ops_k else (len(ops_k)-1 if val_k else 0))
            simpan_teks('Kearifan_Lokal', st.text_input("Ketik Kearifan:", value=val_k if pil_kearifan=="Lainnya" else "") if pil_kearifan == "Lainnya" else pil_kearifan)
            st.divider()
            ops_7 = ["Pilih...", "Bangun Pagi", "Beribadah", "Berolahraga", "Makan Sehat dan Bergizi", "Gemar Belajar", "Bermasyarakat", "Tidur Lebih Awal", "Lainnya"]
            val_7 = st.session_state.data_isian.get('KAIH', '')
            pil_7kaih = st.selectbox("Pilih 7KAIH:", ops_7, index=get_idx(ops_7, val_7) if val_7 in ops_7 else (len(ops_7)-1 if val_7 else 0))
            simpan_teks('KAIH', st.text_input("Ketik 7KAIH:", value=val_7 if pil_7kaih=="Lainnya" else "") if pil_7kaih == "Lainnya" else pil_7kaih)
            st.divider()
            profil_lulus = st.session_state.data_isian.get('Dimensi_Lulusan', '')
            if profil_lulus and profil_lulus != "Pilih..." and profil_lulus in bank_dpl:
                ops_dsub = ["Pilih..."] + list(bank_dpl[profil_lulus].keys())
                pil_sub_dpl = st.selectbox("Pilih Sub Dimensi:", ops_dsub, index=get_idx(ops_dsub, st.session_state.data_isian.get('Sub_Dimensi')))
                if pil_sub_dpl != "Pilih...":
                    simpan_teks('Sub_Dimensi', pil_sub_dpl)
                    komp_teks = bank_dpl[profil_lulus][pil_sub_dpl].get(fase, "Data belum tersedia.") if fase in ["Fase Fondasi", "Fase A", "Fase B", "Fase C", "Fase D", "Fase E", "Fase F"] else "Pilih Fase di Tab 1."
                    simpan_teks('Kompetensi', st.text_area("Kompetensi Lulusan:", value=st.session_state.data_isian.get('Kompetensi', komp_teks), height=120))
                else: simpan_teks('Sub_Dimensi', ""); simpan_teks('Kompetensi', "")
            else: simpan_teks('Sub_Dimensi', ""); simpan_teks('Kompetensi', "")

    with st.container(border=True):
        jenjang = st.session_state.data_isian.get('Jenjang', '')
        c_n, c_k = st.columns(2)
        ops_sfd = ["Pilih..."] + list(bank_sfd.keys())
        with c_n: pil_nilai = st.selectbox("1. Pilih Nilai Ke-SFD-an:", ops_sfd, index=get_idx(ops_sfd, st.session_state.data_isian.get('Nilai')))
        if pil_nilai != "Pilih...":
            simpan_teks('Nilai', pil_nilai)
            ops_keut = ["Pilih..."] + list(bank_sfd[pil_nilai].keys())
            with c_k: pil_keut = st.selectbox("2. Pilih Keutamaan:", ops_keut, index=get_idx(ops_keut, st.session_state.data_isian.get('Keutamaan')))
            if pil_keut != "Pilih...":
                simpan_teks('Keutamaan', pil_keut)
                if jenjang in ["TK", "SD", "SMP"]: cn_teks = bank_sfd[pil_nilai][pil_keut].get(jenjang, "Data tidak ditemukan.")
                elif jenjang == "SMA/SMK": cn_teks = "Capaian Nilai (CN) SMA masih dirumuskan."
                else: cn_teks = "Pilih Jenjang di Tab 1."
                simpan_teks('Capaian_Nilai', st.text_area("3. Capaian Nilai:", value=st.session_state.data_isian.get('Capaian_Nilai', cn_teks), height=120))
        else: simpan_teks('Nilai', ""); simpan_teks('Keutamaan', ""); simpan_teks('Capaian_Nilai', "")

    with st.container(border=True): 
        st.subheader("❤️ C. Rencana Afektif")
        if st.button("📈 Rumuskan TP Afektif", key="btn_tp_afe", use_container_width=True):
            with st.spinner("Memproses afektif..."):
                s, p, p3, k = st.session_state.data_isian.get('Capaian_Nilai', ''), st.session_state.data_isian.get('Nilai_Keutamaan', ''), st.session_state.data_isian.get('Capaian_P3', ''), st.session_state.data_isian.get('Kearifan_Lokal', '')
                st.session_state.data_isian['TP_Afektif'] = panggil_ai(f"Elemen afektif: P3 ({p3}), Nilai SFD ({s}), Keteladanan ({p}), Kearifan ({k}). Sintesis menjadi satu TP Afektif yang kuat.", "tp_afe")
        simpan_teks('TP_Afektif', st.text_area("TP Afektif:", value=st.session_state.data_isian.get('TP_Afektif', ''), height=120))
        
        if st.button("🪜 Rumuskan Indikator Afektif", key="btn_ind_afe", use_container_width=True):
            with st.spinner("Membuat indikator sikap..."):
                st.session_state.data_isian['Indikator_Afektif'] = panggil_ai(f"Dari TP Afektif: '{st.session_state.data_isian.get('TP_Afektif', '')}', buat 3-4 Indikator berjenjang.", "ind_afe")
        simpan_teks('Indikator_Afektif', st.text_area("Indikator Afektif:", value=st.session_state.data_isian.get('Indikator_Afektif', ''), height=100))
        
        if st.button("✨ Rumuskan Pengalaman Afektif", key="btn_afe", use_container_width=True):
            with st.spinner("Merancang aktivitas..."):
                st.session_state.data_isian['Pengalaman_Belajar_Afektif'] = panggil_ai(f"Materi: {st.session_state.data_isian.get('Materi', '')}\nIndikator Afektif: {st.session_state.data_isian.get('Indikator_Afektif', '')}\nRancang 'Pengalaman Belajar' afektif.", "pg_afe")
        simpan_teks('Pengalaman_Belajar_Afektif', st.text_area("Pengalaman Belajar Afektif:", value=st.session_state.data_isian.get('Pengalaman_Belajar_Afektif', ''), height=150))
        c11, c12 = st.columns(2)
        with c11: simpan_teks('Formatif', st.text_area("Asesmen Formatif (Afektif):", value=st.session_state.data_isian.get('Formatif', '')))
        with c12: simpan_teks('Sumatif', st.text_area("Asesmen Sumatif (Afektif):", value=st.session_state.data_isian.get('Sumatif', '')))

with tab5:
    with st.container(border=True): 
        st.subheader("🏃 Aspek Psikomotorik")
        if st.button("📈 Rumuskan TP Psikomotorik", key="btn_tp_psi", use_container_width=True):
            with st.spinner("Memproses psikomotorik..."):
                st.session_state.data_isian['TP_Psikomotorik'] = panggil_ai(f"Baca CP: '{st.session_state.data_isian.get('Capaian_Pembelajaran', '')}'. Buatkan TP Psikomotorik (HOTS). Integrasikan SDGs: '{st.session_state.data_isian.get('TP_SDGs', '')}'.", "tp_psi")
        simpan_teks('TP_Psikomotorik', st.text_area("TP Psikomotorik:", value=st.session_state.data_isian.get('TP_Psikomotorik', ''), height=100))
        
        if st.button("🪜 Rumuskan Indikator Psikomotorik", key="btn_ind_psi", use_container_width=True):
            with st.spinner("Membuat indikator keterampilan..."):
                st.session_state.data_isian['Indikator_Psikomotorik'] = panggil_ai(f"Dari TP Psikomotorik: '{st.session_state.data_isian.get('TP_Psikomotorik', '')}', buat 3-4 Indikator berjenjang.", "ind_psi")
        simpan_teks('Indikator_Psikomotorik', st.text_area("Indikator Psikomotorik:", value=st.session_state.data_isian.get('Indikator_Psikomotorik', ''), height=100))
        
        if st.button("✨ Rumuskan Pengalaman Psikomotorik", key="btn_psi", use_container_width=True):
            with st.spinner("Merancang aktivitas..."):
                st.session_state.data_isian['Pengalaman_Belajar_Psikomotorik'] = panggil_ai(f"Materi: {st.session_state.data_isian.get('Materi', '')}\nIndikator: {st.session_state.data_isian.get('Indikator_Psikomotorik', '')}\nBuat skenario unjuk kerja/proyek.", "pg_psi")
        simpan_teks('Pengalaman_Belajar_Psikomotorik', st.text_area("Pengalaman Belajar Psikomotorik:", value=st.session_state.data_isian.get('Pengalaman_Belajar_Psikomotorik', ''), height=120))
        c3, c4 = st.columns(2)
        with c3: simpan_teks('Asesmen_Formatif_Psikomotorik', st.text_area("Asesmen Formatif (Psikomotorik):", value=st.session_state.data_isian.get('Asesmen_Formatif_Psikomotorik', '')))
        with c4: simpan_teks('Asesmen_Sumatif_Psikomotorik', st.text_area("Asesmen Sumatif (Psikomotorik):", value=st.session_state.data_isian.get('Asesmen_Sumatif_Psikomotorik', '')))

with tab6:
    with st.container(border=True): 
        st.subheader("Perayaan Belajar & Media")
        simpan_teks('Membagikan_Pengalaman_Belajar', st.text_area("Membagikan Pengalaman Belajar:", value=st.session_state.data_isian.get('Membagikan_Pengalaman_Belajar', '')))
        simpan_teks('Refleksi_Perkembangan_Kompetensi', st.text_area("Refleksi Perkembangan Kompetensi:", value=st.session_state.data_isian.get('Refleksi_Perkembangan_Kompetensi', '')))
        simpan_teks('Apresiasi', st.text_area("Apresiasi:", value=st.session_state.data_isian.get('Apresiasi', '')))
        simpan_teks('Media_Pembelajaran', st.text_area("Media Pembelajaran:", value=st.session_state.data_isian.get('Media_Pembelajaran', '')))
    
    with st.container(border=True): 
        st.subheader("🖨️ Rakit Dokumen & Simpan")
        if st.button("Rakit & Simpan Data", type="primary", use_container_width=True):
            if not st.session_state.data_isian.get('Nama_Guru'): st.error("❌ Nama Guru kosong!")
            else:
                with st.spinner('Memproses dokumen...'):
                    try:
                        doc = DocxTemplate("Template_DPB_Schola Amoris.docx")
                        if foto_sdgs is not None: st.session_state.data_isian['Gambar_SGDs'] = InlineImage(doc, foto_sdgs, width=Mm(30))
                        doc.render(st.session_state.data_isian)
                        bio = io.BytesIO()
                        doc.save(bio)
                        
                        simpan_draft_ke_awan() 
                        
                        st.success("🎉 Berhasil! Dokumen siap diunduh.")
                        st.download_button(label="📥 Download File DPB", data=bio.getvalue(), file_name=f"DPB_{st.session_state.data_isian.get('MAPEL', 'Mapel')}.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document", use_container_width=True)
                    except Exception as e: st.error(f"Terjadi kesalahan perakitan Word: {e}")

# ==========================================
# 📚 TAB 7: PERPUSTAKAAN DIGITAL
# ==========================================
with tab7:
    st.subheader("📚 Perpustakaan Digital Schola Amoris")
    st.write("Temukan dan kelola referensi buku, modul, serta bahan ajar di sini.")

    try:
        if supabase is not None:
            respon_buku = supabase.table("koleksi_buku").select("*").execute()
            data_buku = respon_buku.data

            if data_buku:
                df_buku = pd.DataFrame(data_buku)
                st.dataframe(
                    df_buku[["judul_buku", "kategori", "fase_kelas", "link_unduh"]],
                    column_config={
                        "judul_buku": "Judul Buku",
                        "kategori": "Kategori",
                        "fase_kelas": "Target Kelas",
                        "link_unduh": st.column_config.LinkColumn("Tautan Unduh / Baca")
                    },
                    hide_index=True,
                    use_container_width=True
                )
            else:
                st.info("📭 Perpustakaan saat ini masih kosong.")
        else:
            st.error("Koneksi ke brankas Supabase terputus. Pastikan konfigurasi rahasia sudah benar.")
    except Exception as e:
        st.error(f"Gagal memuat katalog buku: {e}")

    st.divider()
    
    with st.expander("➕ Tambah Buku Baru (Khusus Guru/Admin)"):
        st.write("Punya referensi baru? Masukkan ke perpustakaan!")
        baru_judul = st.text_input("Judul Buku/Materi:")
        baru_kategori = st.selectbox("Kategori:", ["Buku Teks Utama", "Modul Ajar", "Buku Cerita Digital", "LKPD", "Referensi Guru"])
        baru_fase = st.selectbox("Target Fase/Kelas:", ["Umum", "Fase Fondasi", "Fase A", "Fase B", "Fase C", "Fase D", "Fase E", "Fase F"])
        baru_link = st.text_input("Link Unduh (Google Drive / Tautan PDF):")
        
        if st.button("💾 Simpan Buku ke Perpustakaan", type="primary"):
            if baru_judul == "" or baru_link == "":
                st.warning("⚠️ Judul Buku dan Link Unduh wajib diisi!")
            else:
                with st.spinner("Menyimpan ke rak..."):
                    try:
                        data_buku_baru = {
                            "judul_buku": baru_judul,
                            "kategori": baru_kategori,
                            "fase_kelas": baru_fase,
                            "link_unduh": baru_link
                        }
                        supabase.table("koleksi_buku").insert(data_buku_baru).execute()
                        st.success("✅ Buku berhasil ditambahkan ke perpustakaan!")
                        st.rerun() 
                    except Exception as e:
                        st.error(f"❌ Gagal menyimpan buku: {e}")
