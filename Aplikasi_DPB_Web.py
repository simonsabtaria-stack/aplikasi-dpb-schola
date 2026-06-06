import streamlit as st
import pandas as pd
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
from data_p3 import bank_p3
from data_dpl import bank_dpl
from data_kko import bank_kko

# --- DATABASE SDGs ANTI-KOSONG ---
try:
    from data_sdgs import bank_sdgs
except ImportError:
    bank_sdgs = {
        "1. Tanpa Kemiskinan": "Mengakhiri segala bentuk kemiskinan di mana pun.",
        "2. Tanpa Kelaparan": "Mengakhiri kelaparan, mencapai ketahanan pangan dan memperbaiki gizi dan mendorong pertanian berkelanjutan.",
        "3. Kehidupan Sehat dan Sejahtera": "Menjamin kehidupan yang sehat dan meningkatkan kesejahteraan bagi semua orang di segala usia.",
        "4. Pendidikan Berkualitas": "Menjamin pendidikan berkualitas yang inklusif dan adil serta mendorong kesempatan belajar seumur hidup bagi semua.",
        "5. Kesetaraan Gender": "Mencapai kesetaraan gender dan memberdayakan seluruh perempuan dan anak perempuan.",
        "6. Air Bersih dan Sanitasi Layak": "Menjamin ketersediaan dan pengelolaan air dan sanitasi berkelanjutan untuk semua.",
        "7. Energi Bersih dan Terjangkau": "Pastikan akses terhadap energi yang terjangkau, andal, berkelanjutan, dan bersih untuk semua.",
        "8. Pekerjaan Layak dan Pertumbuhan Ekonomi": "Mendorong pertumbuhan ekonomi yang berkelanjutan, inklusif dan berkelanjutan, lapangan kerja penuh dan produktif serta pekerjaan yang layak untuk semua.",
        "9. Industri, Inovasi dan Infrastruktur": "Membangun infrastruktur yang berketahanan, mendorong industrialisasi yang inklusif dan berkelanjutan, serta mendorong inovasi.",
        "10. Berkurangnya Kesenjangan": "Mengurangi ketimpangan di dalam dan di luar wilayah antar negara.",
        "11. Kota dan Permukiman yang Berkelanjutan": "Membangun kota dan pemukiman manusia yang inklusif, aman, berketahanan dan berkelanjutan.",
        "12. Konsumsi dan Produksi yang Bertanggung Jawab": "Memastikan pola konsumsi dan produksi yang berkelanjutan.",
        "13. Penanganan Perubahan Iklim": "Mengambil tindakan segera untuk memerangi perubahan iklim dan dampaknya.",
        "14. Ekosistem Lautan": "Melestarikan dan memanfaatkan sumber daya samudera, lautan, dan kelautan secara berkelanjutan untuk pembangunan berkelanjutan.",
        "15. Ekosistem Daratan": "Melindungi, memulihkan dan mendorong pemanfaatan ekosistem darat secara berkelanjutan, mengelola hutan secara berkelanjutan, memerangi penggurunan, dan menghentikan dan membalikkan degradasi lahan serta menghentikan hilangnya keanekaragaman hayati.",
        "16. Perdamaian, Keadilan dan Kelembagaan yang Tangguh": "Mempromosikan masyarakat yang damai dan inklusif untuk pembangunan berkelanjutan, memberikan akses terhadap keadilan bagi semua dan membangun Institusi yang efektif, akuntabel dan inklusif di semua tingkatan.",
        "17. Kemitraan untuk Mencapai Tujuan": "Memperkuat sarana implementasi dan merevitalisasi kemitraan global untuk pembangunan berkelanjutan."
    }

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

kamus_sintaks = {
    "Problem Based Learning (PBL)": "1. Orientasi peserta didik pada masalah\n2. Mengorganisasikan peserta didik untuk belajar\n3. Membimbing penyelidikan individu maupun kelompok\n4. Mengembangkan dan menyajikan hasil karya\n5. Menganalisis dan mengevaluasi proses pemecahan masalah",
    "Project Based Learning (PjBL)": "1. Penentuan pertanyaan mendasar\n2. Mendesain perencanaan proyek\n3. Menyusun jadwal (Time schedule)\n4. Memonitor peserta didik dan kemajuan proyek\n5. Menguji hasil\n6. Mengevaluasi pengalaman",
    "Inquiry/Discovery Learning": "1. Pemberian rangsangan (Stimulation)\n2. Pernyataan/Identifikasi masalah (Problem Statement)\n3. Pengumpulan data (Data Collection)\n4. Pengolahan data (Data Processing)\n5. Pembuktian (Verification)\n6. Menarik kesimpulan (Generalization)",
    "Teaching at the Right Level (TaRL)": "1. Asesmen diagnostik awal\n2. Pengelompokan peserta didik berdasarkan capaian\n3. Pendampingan dan pembelajaran berdiferensiasi\n4. Evaluasi formatif berkala\n5. Rotasi/Penyesuaian kelompok berkelanjutan",
    "Cooperative Learning": "1. Menyampaikan tujuan dan memotivasi peserta didik\n2. Menyajikan informasi\n3. Mengorganisasikan peserta didik ke dalam kelompok-kelompok belajar\n4. Membimbing kelompok bekerja dan belajar\n5. Evaluasi\n6. Memberikan penghargaan"
}

def inisialisasi_memori():
    if 'data_isian' not in st.session_state: st.session_state.data_isian = {}
    if 'chat_amor' not in st.session_state: st.session_state.chat_amor = [{"role": "assistant", "content": "Halo Bapak/Ibu Guru! 🌟 Saya Amor, asisten pribadi Anda. Ada yang bisa saya bantu?"}]
    if "username_aktif" not in st.session_state: st.session_state.username_aktif = None

inisialisasi_memori()

def simpan_teks(kunci, nilai):
    st.session_state.data_isian[kunci] = nilai

def get_idx(options, val, default=0): 
    return options.index(val) if val in options else default

def simpan_draft_ke_awan():
    if supabase is None:
        st.error("Koneksi Supabase belum diatur!")
        return
    st.session_state.data_isian['Pengalaman_Belajar'] = f"APERSEPSI:\n{st.session_state.data_isian.get('Apersepsi_Kog', '')}\n\nMENGIDENTIFIKASI KONTEKS:\n{st.session_state.data_isian.get('Konteks_Kog', '')}\n\nOLAH PIKIR, RASA, RAGA:\n{st.session_state.data_isian.get('Olah_Kog', '')}"
    st.session_state.data_isian['Pengalaman_Belajar_Afektif'] = f"APERSEPSI:\n{st.session_state.data_isian.get('Apersepsi_Afe', '')}\n\nMENGIDENTIFIKASI KONTEKS:\n{st.session_state.data_isian.get('Konteks_Afe', '')}\n\nOLAH PIKIR, RASA, RAGA:\n{st.session_state.data_isian.get('Olah_Afe', '')}"
    st.session_state.data_isian['Pengalaman_Belajar_Psikomotorik'] = f"APERSEPSI:\n{st.session_state.data_isian.get('Apersepsi_Psi', '')}\n\nMENGIDENTIFIKASI KONTEKS:\n{st.session_state.data_isian.get('Konteks_Psi', '')}\n\nOLAH PIKIR, RASA, RAGA:\n{st.session_state.data_isian.get('Olah_Psi', '')}"
    
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
    try: st.image("banner_schola.png", use_container_width=True)
    except: pass
    st.markdown("<h1 style='text-align: center;'>Pintu Gerbang Penyusun DPB 🎓</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        with st.container(border=True):
            st.markdown("### 🔐 Masuk ke Ruang Kerja")
            input_nama = st.text_input("Nama Guru / Username (Contoh: Bapak Budi):")
            if st.button("Mulai Merancang DPB 🚀", use_container_width=True, type="primary"):
                if input_nama.strip() != "":
                    st.session_state.username_aktif = input_nama.strip()
                    muat_draft_dari_awan(st.session_state.username_aktif)
                    st.rerun()
    st.stop() 

try: st.image("banner_schola.png", use_container_width=True)
except: pass
col_title, col_logout = st.columns([4,1])
with col_title:
    st.title("Penyusun DPB Schola Amoris 🎓")
with col_logout:
    if st.button("🚪 Keluar (Logout)"):
        st.session_state.username_aktif = None
        inisialisasi_memori() 
        st.rerun()

# ==========================================
# FUNGSI AI AMOR & PERUMUS (SINTAKS AMORIS)
# ==========================================
def panggil_amor(pertanyaan, api_key):
    if not api_key: return "Mohon maaf, Amor butuh Kunci API Gemini untuk membantu. 🙏"
    try:
        genai.configure(api_key=api_key)
        m_list = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        m_name = next((m for m in m_list if 'flash' in m.lower() and '1.5' in m), m_list[0])
        model = genai.GenerativeModel(m_name)
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        vector_db = FAISS.load_local("faiss_amor", embeddings, allow_dangerous_deserialization=True)
        docs = vector_db.similarity_search(pertanyaan, k=4)
        referensi = "\n\n".join([doc.page_content for doc in docs])
        return model.generate_content(f"Jawab berdasarkan REFERENSI ini saja:\n{referensi}\nPERTANYAAN: {pertanyaan}").text
    except Exception as e: return f"Waduh, ada gangguan teknis. (Error: {e}) 🛠️"

def fallback_generator(tipe):
    m = st.session_state.data_isian.get('Materi', 'materi')
    if tipe == "tp_kog": return f"Menguraikan konsep {m} secara kritis."
    elif tipe == "ind_kog": return f"- Menjelaskan dasar {m}\n- Menganalisis {m}"
    elif tipe == "pg_kog": return f"Menggali pengetahuan awal.\n|||\nMengidentifikasi masalah {m}.\n|||\nMendiskusikan hasil."
    elif tipe == "tp_afe": return f"Membuktikan sikap selaras dengan kearifan lokal."
    elif tipe == "ind_afe": return f"- Merespon arahan\n- Menginternalisasi karakter"
    elif tipe == "pg_afe": return "Merefleksikan nilai.\n|||\nMengamati lingkungan sosial.\n|||\nMelakukan aksi nyata kepedulian."
    elif tipe == "tp_psi": return f"Mendemonstrasikan prosedur terkait {m}."
    elif tipe == "ind_psi": return f"- Meniru tahapan\n- Melaksanakan secara mandiri"
    elif tipe == "pg_psi": return "Mengidentifikasi contoh karya.\n|||\nMenyiapkan alat dan bahan.\n|||\nMempraktikkan keterampilan."
    return "Data diproses."

def ambil_referensi_rag(query):
    if not os.path.exists("faiss_index"): return ""
    try:
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        vector_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
        return "\n\nREFERENSI:\n" + "\n\n".join([doc.page_content for doc in vector_db.similarity_search(query, k=3)])
    except: return "" 

def panggil_ai(prompt, tipe=""):
    if not st.session_state.get('kunci_api_guru'): 
        st.warning("⚠️ Kunci API Gemini belum dimasukkan di Pusat Kontrol AI (Sidebar)!")
        return fallback_generator(tipe)
    try:
        genai.configure(api_key=st.session_state.get('kunci_api_guru'))
        m_list = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        m_name = next((m for m in m_list if 'flash' in m.lower() and '1.5' in m), m_list[0])
        model = genai.GenerativeModel(m_name)
        
        referensi = ambil_referensi_rag(prompt)
        instruksi_hemat = st.session_state.data_isian.get('instruksi_tambahan', '')
        tambahan = f"\n\nINSTRUKSI KHUSUS DARI GURU (WAJIB DIIKUTI):\n{instruksi_hemat}" if instruksi_hemat else ""
        
        prompt_lengkap = prompt + referensi + tambahan + "\nATURAN MUTLAK:\n1. Gunakan list poin, hindari kapital semua.\n2. JANGAN bertele-tele, langsung berikan intinya saja tanpa kalimat pembuka.\n3. DILARANG KERAS MENGGUNAKAN KATA SUBJEK (Peserta Didik, Siswa, Guru).\n4. AWALI SETIAP KALIMAT LANGSUNG DENGAN KATA KERJA OPERASIONAL (KKO)."
        
        respon = model.generate_content(prompt_lengkap)
        return respon.text
    except Exception as e: 
        st.error(f"⚠️ AI Gagal Merumuskan. Detail Error: {e}")
        return fallback_generator(tipe)

# ==========================================
# SIDEBAR
# ==========================================
with st.sidebar:
    st.success(f"👤 Aktif sebagai: **{st.session_state.username_aktif}**")
    if st.button("☁️ Simpan Draf ke Awan", type="primary", use_container_width=True):
        with st.spinner("Menyimpan..."): simpan_draft_ke_awan()
    if st.button("🔄 Kosongkan Lembar (Mulai Baru)", use_container_width=True):
        st.session_state.data_isian = {'Nama_Guru': st.session_state.username_aktif}
        st.rerun()
    st.divider()
    
    st.header("🤖 Pusat Kontrol AI")
    api_key_guru = st.text_input("🔑 Kunci API Gemini:", type="password")
    if api_key_guru: st.session_state['kunci_api_guru'] = api_key_guru
        
    st.markdown("**⚙️ Pengaturan Output AI**")
    teks_bawaan = "Buatlah jawaban yang sangat singkat, padat, dan jelas. Hindari penjelasan panjang lebar. Cukup berikan maksimal 2 atau 3 poin pendek."
    instruksi_tambahan = st.text_area("📝 Instruksi Tambahan (Penghemat Kuota):", value=st.session_state.data_isian.get('instruksi_tambahan', teks_bawaan))
    simpan_teks('instruksi_tambahan', instruksi_tambahan)
    st.divider()
    
    st.markdown("### 💬 Tanya Amor")
    wadah_chat = st.container(height=350)
    with wadah_chat:
        for msg in st.session_state.chat_amor:
            st.markdown(f"**{'🧡 Amor' if msg['role']=='assistant' else '👤 Anda'}:** {msg['content']}")
    pertanyaan_baru = st.chat_input("Tanya Amor di sini...")
    if pertanyaan_baru:
        st.session_state.chat_amor.append({"role": "user", "content": pertanyaan_baru})
        st.session_state.chat_amor.append({"role": "assistant", "content": panggil_amor(pertanyaan_baru, st.session_state.get('kunci_api_guru'))})
        st.rerun() 

# ==========================================
# BUKU CONTEKAN & PANDUAN (DI ATAS TAB)
# ==========================================
st.markdown("""<style>.stTabs [data-baseweb="tab-list"] { gap: 10px; } .stTabs [data-baseweb="tab"] { background-color: #f1f5f9; border-radius: 8px 8px 0px 0px; padding: 10px 20px; box-shadow: inset 0 -2px 0 0 #cbd5e1; } .stTabs [aria-selected="true"] { background-color: #1e293b; color: #ffffff !important; }</style>""", unsafe_allow_html=True)

with st.expander("📖 Buka Kamus KKO & Sintaks (Buku Contekan)"):
    kategori_contekan = st.radio("Pilih Referensi:", ["🧠 KKO Kognitif", "❤️ KKO Afektif", "🏃 KKO Psikomotorik", "🧩 Sintaks Pembelajaran"], horizontal=True)
    st.divider()
    if kategori_contekan == "🧠 KKO Kognitif":
        for level, kata in bank_kko["KOGNITIF"].items():
            with st.expander(f"**{level}**"): st.write(", ".join(kata))
    elif kategori_contekan == "❤️ KKO Afektif":
        for level, kata in bank_kko["Afektif"].items():
            with st.expander(f"**{level}**"): st.write(", ".join(kata))
    elif kategori_contekan == "🏃 KKO Psikomotorik":
        for level, kata in bank_kko["Psikomotorik"].items():
            with st.expander(f"**{level}**"): st.write(", ".join(kata))
    elif kategori_contekan == "🧩 Sintaks Pembelajaran":
        for model, sintaks in kamus_sintaks.items():
            with st.expander(f"**{model}**"): st.text(sintaks)

kunci_wajib = ['Nama_Guru', 'MAPEL', 'Materi', 'Capaian_Pembelajaran', 'TP_Kognitif', 'TP_Psikomotorik', 'TP_Afektif']
terisi = sum(1 for k in kunci_wajib if st.session_state.data_isian.get(k) and str(st.session_state.data_isian.get(k)).strip() != "")
st.markdown(f"**Progres Kelengkapan DPB: {int((terisi / len(kunci_wajib)) * 100)}%**")
st.progress(int((terisi / len(kunci_wajib)) * 100))

# ==========================================
# TABS UTAMA (DESAIN LAYOUT MIRIP WORD)
# ==========================================
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["📋 1. Identitas", "🏫 2. Lingkungan", "🧠 3. Kognitif", "❤️ 4. Afektif", "🏃 5. Psikomotorik", "🖨️ 6. Pratinjau & Cetak", "📚 7. Perpustakaan"])

# --- TAB 1: IDENTIFIKASI ---
with tab1:
    with st.container(border=True):
        st.markdown("### IDENTIFIKASI")
        simpan_teks('Nama_Guru', st.text_input("Nama Guru:", value=st.session_state.data_isian.get('Nama_Guru', st.session_state.username_aktif), disabled=True))
        
        col_id1, col_id2, col_id3 = st.columns([1,1,2])
        with col_id1:
            simpan_teks('Tahun_Ajaran', st.text_input("Tahun Ajaran:", value=st.session_state.data_isian.get('Tahun_Ajaran', '')))
            opsi_jenjang = ["Pilih...", "TK", "SD", "SMP", "SMA/SMK"]
            simpan_teks('Jenjang', st.selectbox("Jenjang:", opsi_jenjang, index=get_idx(opsi_jenjang, st.session_state.data_isian.get('Jenjang'))))
            opsi_fase = ["-", "Fase Fondasi", "Fase A", "Fase B", "Fase C", "Fase D", "Fase E", "Fase F"]
            simpan_teks('Fase', st.selectbox("Fase:", opsi_fase, index=get_idx(opsi_fase, st.session_state.data_isian.get('Fase'))))
            
        with col_id2:
            opsi_sem = ["Ganjil", "Genap"]
            simpan_teks('Semester', st.selectbox("Semester:", opsi_sem, index=get_idx(opsi_sem, st.session_state.data_isian.get('Semester'))))
            opsi_kelas = ["Pilih...", "TK A", "TK B", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "Lainnya"]
            simpan_teks('Kelas', st.selectbox("Kelas:", opsi_kelas, index=get_idx(opsi_kelas, st.session_state.data_isian.get('Kelas'))))
            simpan_teks('Alokasi_Waktu', st.text_input("Total Waktu:", value=st.session_state.data_isian.get('Alokasi_Waktu', '')))
            
        with col_id3:
            simpan_teks('Identifikasi_Peserta_Didik', st.text_area("Identifikasi Peserta Didik:", value=st.session_state.data_isian.get('Identifikasi_Peserta_Didik', ''), height=130))
            simpan_teks('Judul', st.text_input("Judul Modul:", value=st.session_state.data_isian.get('Judul', '')))

        st.divider()
        st.markdown("### CAPAIAN PEMBELAJARAN & MATERI ESENSIAL")
        col_cp1, col_cp2 = st.columns(2)
        with col_cp1:
            fase_terpilih = st.session_state.data_isian.get('Fase', '')
            opsi_mapel = ["Pilih..."] + list(bank_kurikulum.get(fase_terpilih, {}).keys()) + ["Lainnya (Ketik Manual)"]
            val_mapel_db = st.session_state.data_isian.get('MAPEL', '')
            pilihan_mapel = st.selectbox("Mata Pelajaran:", opsi_mapel, index=get_idx(opsi_mapel, val_mapel_db) if val_mapel_db in opsi_mapel else (len(opsi_mapel)-1 if val_mapel_db else 0))
            
            if pilihan_mapel == "Lainnya (Ketik Manual)":
                simpan_teks('MAPEL', st.text_input("Ketik Nama Mata Pelajaran:", value=st.session_state.data_isian.get('MAPEL', '')))
                simpan_teks('Elemen', st.text_input("Ketik Elemen:", value=st.session_state.data_isian.get('Elemen', '')))
                simpan_teks('Materi', st.text_input("Ketik Materi Esensial:", value=st.session_state.data_isian.get('Materi', '')))
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
            
            if st.session_state.get('temp_cp') == "": st.session_state['temp_cp'] = st.session_state.data_isian.get('Capaian_Pembelajaran', '')
            simpan_teks('Capaian_Pembelajaran', st.text_area("Capaian Pembelajaran:", value=st.session_state.get('temp_cp', ''), height=130))
            
        with col_cp2:
            opsi_dpl = ["Pilih..."] + list(bank_dpl.keys())
            simpan_teks('Dimensi_Lulusan', st.selectbox("Dimensi Profil Lulusan:", opsi_dpl, index=get_idx(opsi_dpl, st.session_state.data_isian.get('Dimensi_Lulusan'))))
            
            opsi_sdgs = ["Pilih..."] + list(bank_sdgs.keys())
            pil_sdgs = st.selectbox("Capaian SDGs:", opsi_sdgs, index=get_idx(opsi_sdgs, st.session_state.data_isian.get('Capaian_SDGs')))
            
            if pil_sdgs != "Pilih...":
                simpan_teks('Capaian_SDGs', pil_sdgs)
                kunci_pelacak_sdgs = f"{pil_sdgs}"
                if st.session_state.get('lacak_sdgs') != kunci_pelacak_sdgs:
                    st.session_state.data_isian['TP_SDGs'] = bank_sdgs.get(pil_sdgs, "")
                    st.session_state['lacak_sdgs'] = kunci_pelacak_sdgs
                simpan_teks('TP_SDGs', st.text_area("TP SDGs:", value=st.session_state.data_isian.get('TP_SDGs', ''), height=85))
            else:
                simpan_teks('Capaian_SDGs', ""); simpan_teks('TP_SDGs', "")
            
            foto_sdgs = st.file_uploader("Upload Logo SDGs", type=['png', 'jpg', 'jpeg'])

# --- TAB 2: LINGKUNGAN ---
with tab2:
    with st.container(border=True):
        st.markdown("### KEMITRAAN & PRAKTIK PEDAGOGIS")
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
            
        sintaks_default = st.session_state.data_isian.get('Urutan_Sintkas', kamus_sintaks.get(pil_peda, ""))
        simpan_teks('Urutan_Sintkas', st.text_area("Urutan Sintaks Pembelajaran:", value=sintaks_default, height=120))

    with st.container(border=True):
        st.markdown("### LINGKUNGAN PEMBELAJARAN")
        col_ling1, col_ling2, col_ling3 = st.columns(3)
        with col_ling1: simpan_teks('Ruang_Fisik', st.text_area("Ruang Fisik:", value=st.session_state.data_isian.get('Ruang_Fisik', '')))
        with col_ling2: simpan_teks('Ruang_Virtual', st.text_area("Ruang Virtual:", value=st.session_state.data_isian.get('Ruang_Virtual', '')))
        with col_ling3: 
            ops_b = ["Pilih...", "Disiplin Positif & Restitusi", "Growth Mindset", "Kolaboratif & Inklusif", "Pembelajaran Berbasis Umpan Balik (Feedback)", "Lainnya"]
            val_b = st.session_state.data_isian.get('Budaya_Belajar', '')
            pil_budaya = st.selectbox("Budaya Belajar:", ops_b, index=get_idx(ops_b, val_b) if val_b in ops_b else (len(ops_b)-1 if val_b else 0))
            simpan_teks('Budaya_Belajar', st.text_input("Ketik Budaya Belajar:", value=val_b if pil_budaya == "Lainnya" else "") if pil_budaya == "Lainnya" else pil_budaya)

# --- TAB 3: KOGNITIF (SINTAKS AMORIS) ---
with tab3:
    with st.container(border=True): 
        st.markdown("### ASPEK KOGNITIF (PEMAHAMAN KONSEP DAN APLIKATIF)")
        col_tk1, col_tk2, col_tk3, col_tk4 = st.columns([1,1,1.5,1])
        
        with col_tk1:
            st.markdown("**1. TP KOGNITIF**")
            if st.button("📈 Rumuskan TP", key="btn_tp_kog"):
                with st.spinner("Memproses..."):
                    prompt = f"Mata Pelajaran: {st.session_state.data_isian.get('MAPEL', '')}.\nBaca CP Umum: '{st.session_state.data_isian.get('Capaian_Pembelajaran', '')}'.\nRumuskan TEPAT 1 (satu) kalimat TP Kognitif yang menaikkan level KKO satu tingkat dari CP Umum, dan WAJIB mengintegrasikan narasi TP SDGs berikut: '{st.session_state.data_isian.get('TP_SDGs', '')}'.\nATURAN MUTLAK: Kalimat TP WAJIB diawali langsung dengan Kata Kerja Operasional (KKO) yang relevan tanpa subjek."
                    hasil_ai = panggil_ai(prompt, "tp_kog")
                    st.session_state.data_isian['TP_KOGNITIF'] = hasil_ai
                    st.session_state['ta_tp_kog'] = hasil_ai
            simpan_teks('TP_KOGNITIF', st.text_area("Isi TP:", value=st.session_state.data_isian.get('TP_KOGNITIF', ''), height=260, label_visibility="collapsed", key="ta_tp_kog"))
            
        with col_tk2:
            st.markdown("**2. INDIKATOR**")
            if st.button("🪜 Rumuskan Indikator", key="btn_ind_kog"):
                with st.spinner("Memproses..."):
                    prompt = f"Dari TP Kognitif: '{st.session_state.data_isian.get('TP_KOGNITIF', '')}', buatlah Indikator pencapaian kompetensi berjenjang (scaffolding) dari LOTS ke HOTS.\nATURAN MUTLAK: Setiap poin Indikator WAJIB diawali langsung dengan Kata Kerja Operasional (KKO) tanpa subjek."
                    hasil_ai = panggil_ai(prompt, "ind_kog")
                    st.session_state.data_isian['Indikator_Kognitif'] = hasil_ai
                    st.session_state['ta_ind_kog'] = hasil_ai
            simpan_teks('Indikator_Kognitif', st.text_area("Isi Indikator:", value=st.session_state.data_isian.get('Indikator_Kognitif', ''), height=260, label_visibility="collapsed", key="ta_ind_kog"))
            
        with col_tk3:
            st.markdown("**3. PENGALAMAN BELAJAR**")
            if st.button("✨ Rumuskan Sintaks", key="btn_kog"):
                with st.spinner("Memproses..."):
                    prompt = f"Materi: {st.session_state.data_isian.get('Materi', '')}\nIndikator: {st.session_state.data_isian.get('Indikator_Kognitif', '')}\nRancang Pengalaman Belajar Kognitif ke dalam TEPAT 3 tahap Sintaks Amoris. Gunakan '|||' sebagai pemisah.\nATURAN MUTLAK: DILARANG MENGGUNAKAN KATA SUBJEK (Peserta Didik/Siswa/Guru). Langsung awali poin dengan kata kerja desain instruksional (Contoh: 'Membaca...', 'Mengamati...', 'Menganalisis...'). HANYA KELUARKAN 3 BAGIAN DIPISAHKAN '|||' TANPA TEKS LAIN."
                    hasil_ai = panggil_ai(prompt, "pg_kog")
                    hasil_ai = hasil_ai.replace("```text", "").replace("```", "").strip()
                    parts = hasil_ai.split("|||")
                    if len(parts) >= 3:
                        st.session_state.data_isian['Apersepsi_Kog'] = parts[0].strip()
                        st.session_state.data_isian['Konteks_Kog'] = parts[1].strip()
                        st.session_state.data_isian['Olah_Kog'] = "|||".join(parts[2:]).strip()
                    else:
                        st.session_state.data_isian['Apersepsi_Kog'] = hasil_ai
                        st.session_state.data_isian['Konteks_Kog'] = ""
                        st.session_state.data_isian['Olah_Kog'] = ""
                    st.session_state['ta_apersepsi_kog'] = st.session_state.data_isian['Apersepsi_Kog']
                    st.session_state['ta_konteks_kog'] = st.session_state.data_isian['Konteks_Kog']
                    st.session_state['ta_olah_kog'] = st.session_state.data_isian['Olah_Kog']
            
            simpan_teks('Apersepsi_Kog', st.text_area("1. APERSEPSI", value=st.session_state.data_isian.get('Apersepsi_Kog', ''), height=70, key="ta_apersepsi_kog"))
            simpan_teks('Konteks_Kog', st.text_area("2. MENGIDENTIFIKASI KONTEKS", value=st.session_state.data_isian.get('Konteks_Kog', ''), height=70, key="ta_konteks_kog"))
            simpan_teks('Olah_Kog', st.text_area("3. OLAH PIKIR, RASA, RAGA", value=st.session_state.data_isian.get('Olah_Kog', ''), height=70, key="ta_olah_kog"))
            
        with col_tk4:
            st.markdown("**4. ASESMEN**")
            st.write("\n\n")
            simpan_teks('Asesmen_Formatif', st.text_area("Formatif:", value=st.session_state.data_isian.get('Asesmen_Formatif', ''), height=115, key="ta_form_kog"))
            simpan_teks('Asesmen_Sumatif', st.text_area("Sumatif:", value=st.session_state.data_isian.get('Asesmen_Sumatif', ''), height=115, key="ta_sum_kog"))

# --- TAB 4: AFEKTIF (SINTAKS AMORIS) ---
with tab4:
    with st.container(border=True):
        st.markdown("### ASPEK AFEKTIF (MENDALAMI NILAI-NILAI KARAKTER)")
        st.markdown("**PROFIL PELAJAR PANCASILA (P3)**")
        col_p1, col_p2, col_p3, col_p4 = st.columns(4)
        fase = st.session_state.data_isian.get('Fase', '')
        
        ops_dim = ["Pilih..."] + list(bank_p3.keys())
        with col_p1: pil_dim = st.selectbox("DIMENSI", ops_dim, index=get_idx(ops_dim, st.session_state.data_isian.get('Dimensi')))
        if pil_dim != "Pilih...":
            simpan_teks('Dimensi', pil_dim)
            ops_el = ["Pilih..."] + list(bank_p3[pil_dim].keys())
            with col_p2: pil_el = st.selectbox("ELEMEN", ops_el, index=get_idx(ops_el, st.session_state.data_isian.get('Elemen_P3')))
            if pil_el != "Pilih...":
                simpan_teks('Elemen_P3', pil_el)
                ops_sub = ["Pilih..."] + list(bank_p3[pil_dim][pil_el].keys())
                with col_p3: pil_sub = st.selectbox("SUB ELEMEN", ops_sub, index=get_idx(ops_sub, st.session_state.data_isian.get('Sub_elemen')))
                if pil_sub != "Pilih...":
                    simpan_teks('Sub_elemen', pil_sub)
                    kunci_pelacak_p3 = f"{pil_sub}_{fase}"
                    if st.session_state.get('lacak_p3') != kunci_pelacak_p3:
                        st.session_state.data_isian['Capaian_P3'] = bank_p3[pil_dim][pil_el][pil_sub].get(fase, "Data belum tersedia.") if fase in ["Fase Fondasi", "Fase A", "Fase B", "Fase C", "Fase D", "Fase E", "Fase F"] else "Pilih Fase di Tab 1."
                        st.session_state['lacak_p3'] = kunci_pelacak_p3
                    with col_p4: simpan_teks('Capaian_P3', st.text_area("CAPAIAN P3", value=st.session_state.data_isian.get('Capaian_P3', ''), height=100))
                else: simpan_teks('Sub_elemen', ""); simpan_teks('Capaian_P3', "")
            else: simpan_teks('Elemen_P3', ""); simpan_teks('Sub_elemen', ""); simpan_teks('Capaian_P3', "")
        else: simpan_teks('Dimensi', ""); simpan_teks('Elemen_P3', ""); simpan_teks('Sub_elemen', ""); simpan_teks('Capaian_P3', "")

        st.divider()
        col_a1, col_a2 = st.columns(2)
        with col_a1:
            ops_santo = ["Pilih...", "Santo Fransiskus Asisi", "Santa Clara", "Santa Maria", "Lainnya"]
            val_santo = st.session_state.data_isian.get('Santo_Santa_Pelindung', '')
            pil_santo = st.selectbox("SANTO/SANTA PELINDUNG:", ops_santo, index=get_idx(ops_santo, val_santo) if val_santo in ops_santo else (len(ops_santo)-1 if val_santo else 0))
            simpan_teks('Santo_Santa_Pelindung', st.text_input("Nama Pelindung:", value=val_santo if pil_santo=="Lainnya" else "", label_visibility="collapsed") if pil_santo == "Lainnya" else pil_santo)
            simpan_teks('Nilai_Keutamaan', st.text_input("Nilai/Keutamaan Pelindung:", value=st.session_state.data_isian.get('Nilai_Keutamaan', '')))
            
            ops_7 = ["Pilih...", "Bangun Pagi", "Beribadah", "Berolahraga", "Makan Sehat dan Bergizi", "Gemar Belajar", "Bermasyarakat", "Tidur Lebih Awal", "Lainnya"]
            val_7 = st.session_state.data_isian.get('KAIH', '')
            pil_7kaih = st.selectbox("7KAIH:", ops_7, index=get_idx(ops_7, val_7) if val_7 in ops_7 else (len(ops_7)-1 if val_7 else 0))
            simpan_teks('KAIH', st.text_input("Ketik 7KAIH:", value=val_7 if pil_7kaih=="Lainnya" else "", label_visibility="collapsed") if pil_7kaih == "Lainnya" else pil_7kaih)

        with col_a2:
            ops_k = ["Pilih...", "Waja Sampai Kaputing", "kayuh Baimbai", "Isen Mulang", "Iya Mulik Bengkang Turan", "Dahani Dahanai Tuntung Tulus", "Belum Bahadat", "Huma Betang", "Handep Hapakat", "Lainnya"]
            val_k = st.session_state.data_isian.get('Kearifan_Lokal', '')
            pil_kearifan = st.selectbox("KEARIFAN LOKAL:", ops_k, index=get_idx(ops_k, val_k) if val_k in ops_k else (len(ops_k)-1 if val_k else 0))
            simpan_teks('Kearifan_Lokal', st.text_input("Ketik Kearifan:", value=val_k if pil_kearifan=="Lainnya" else "", label_visibility="collapsed") if pil_kearifan == "Lainnya" else pil_kearifan)
            
            profil_lulus = st.session_state.data_isian.get('Dimensi_Lulusan', '')
            if profil_lulus and profil_lulus != "Pilih..." and profil_lulus in bank_dpl:
                ops_dsub = ["Pilih..."] + list(bank_dpl[profil_lulus].keys())
                pil_sub_dpl = st.selectbox("SUBDIMENSI (DPL):", ops_dsub, index=get_idx(ops_dsub, st.session_state.data_isian.get('Sub_Dimensi')))
                if pil_sub_dpl != "Pilih...":
                    simpan_teks('Sub_Dimensi', pil_sub_dpl)
                    kunci_pelacak_dpl = f"{pil_sub_dpl}_{fase}"
                    if st.session_state.get('lacak_dpl') != kunci_pelacak_dpl:
                        st.session_state.data_isian['Kompetensi'] = bank_dpl[profil_lulus][pil_sub_dpl].get(fase, "Data belum tersedia.") if fase in ["Fase Fondasi", "Fase A", "Fase B", "Fase C", "Fase D", "Fase E", "Fase F"] else "Pilih Fase di Tab 1."
                        st.session_state['lacak_dpl'] = kunci_pelacak_dpl
                    simpan_teks('Kompetensi', st.text_area("KOMPETENSI LULUSAN:", value=st.session_state.data_isian.get('Kompetensi', ''), height=85))
                else: simpan_teks('Sub_Dimensi', ""); simpan_teks('Kompetensi', "")
            else: simpan_teks('Sub_Dimensi', ""); simpan_teks('Kompetensi', "")

        st.divider()
        st.markdown("**CORE VALUES/NILAI INTI KE-SFD-AN**")
        jenjang = st.session_state.data_isian.get('Jenjang', '')
        c_n, c_k, c_cn = st.columns([1,1,2])
        ops_sfd = ["Pilih..."] + list(bank_sfd.keys())
        with c_n: pil_nilai = st.selectbox("NILAI", ops_sfd, index=get_idx(ops_sfd, st.session_state.data_isian.get('Nilai')))
        if pil_nilai != "Pilih...":
            simpan_teks('Nilai', pil_nilai)
            ops_keut = ["Pilih..."] + list(bank_sfd[pil_nilai].keys())
            with c_k: pil_keut = st.selectbox("KEUTAMAAN", ops_keut, index=get_idx(ops_keut, st.session_state.data_isian.get('Keutamaan')))
            if pil_keut != "Pilih...":
                simpan_teks('Keutamaan', pil_keut)
                if jenjang in ["TK", "SD", "SMP"]: 
                    teks_cn_saja = ""
                    for sikap, isi_jenjang in bank_sfd[pil_nilai][pil_keut].items():
                        if jenjang in isi_jenjang:
                            teks = isi_jenjang[jenjang]
                            if "CN:" in teks:
                                teks_cn_saja = teks.replace("CN: ", "").strip()
                                break
                    cn_teks = teks_cn_saja if teks_cn_saja else "Data CN tidak ditemukan."
                elif jenjang == "SMA/SMK": cn_teks = "Capaian Nilai (CN) SMA masih dirumuskan."
                else: cn_teks = "Pilih Jenjang di Tab 1."
                kunci_pelacak_sfd = f"{pil_keut}_{jenjang}"
                if st.session_state.get('lacak_sfd') != kunci_pelacak_sfd:
                    st.session_state.data_isian['Capaian_Nilai'] = cn_teks
                    st.session_state['lacak_sfd'] = kunci_pelacak_sfd
                with c_cn: simpan_teks('Capaian_Nilai', st.text_area("CAPAIAN NILAI", value=st.session_state.data_isian.get('Capaian_Nilai', ''), height=100))
            else: simpan_teks('Keutamaan', ""); simpan_teks('Capaian_Nilai', "")
        else: simpan_teks('Nilai', ""); simpan_teks('Keutamaan', ""); simpan_teks('Capaian_Nilai', "")

        st.divider()
        col_ta1, col_ta2, col_ta3, col_ta4 = st.columns([1,1,1.5,1])
        with col_ta1:
            st.markdown("**1. TP AFEKTIF**")
            if st.button("📈 Rumuskan TP", key="btn_tp_afe"):
                with st.spinner("Memproses..."):
                    s = st.session_state.data_isian.get('Capaian_Nilai', '')
                    p = st.session_state.data_isian.get('Nilai_Keutamaan', '')
                    p3 = st.session_state.data_isian.get('Capaian_P3', '')
                    k = st.session_state.data_isian.get('Kearifan_Lokal', '')
                    prompt = f"Mata Pelajaran: {st.session_state.data_isian.get('MAPEL', '')}.\nSintesiskan elemen berikut mnjd TEPAT 1 (satu) kalimat TP Afektif utuh:\nP3: {p3}\nDPL: {st.session_state.data_isian.get('Kompetensi', '')}\n7KAIH: {st.session_state.data_isian.get('KAIH', '')}\nSanto/a: {p}\nKearifan: {k}\nSFD: {s}.\nATURAN MUTLAK: Kalimat TP WAJIB diawali langsung dengan Kata Kerja Operasional (KKO) yang relevan tanpa subjek."
                    hasil_ai = panggil_ai(prompt, "tp_afe")
                    st.session_state.data_isian['TP_Afektif'] = hasil_ai
                    st.session_state['ta_tp_afe'] = hasil_ai
            simpan_teks('TP_Afektif', st.text_area("Isi TP:", value=st.session_state.data_isian.get('TP_Afektif', ''), height=260, label_visibility="collapsed", key="ta_tp_afe"))
            
        with col_ta2:
            st.markdown("**2. INDIKATOR**")
            if st.button("🪜 Rumuskan Indikator", key="btn_ind_afe"):
                with st.spinner("Memproses..."):
                    prompt = f"Dari TP Afektif: '{st.session_state.data_isian.get('TP_Afektif', '')}', buat 3-4 Indikator berjenjang.\nATURAN MUTLAK: Setiap poin Indikator WAJIB diawali langsung dengan Kata Kerja Operasional (KKO) tanpa subjek."
                    hasil_ai = panggil_ai(prompt, "ind_afe")
                    st.session_state.data_isian['Indikator_Afektif'] = hasil_ai
                    st.session_state['ta_ind_afe'] = hasil_ai
            simpan_teks('Indikator_Afektif', st.text_area("Isi Indikator:", value=st.session_state.data_isian.get('Indikator_Afektif', ''), height=260, label_visibility="collapsed", key="ta_ind_afe"))
            
        with col_ta3:
            st.markdown("**3. PENGALAMAN BELAJAR**")
            if st.button("✨ Rumuskan Sintaks", key="btn_afe"):
                with st.spinner("Memproses..."):
                    prompt = f"Materi: {st.session_state.data_isian.get('Materi', '')}\nIndikator Afektif: {st.session_state.data_isian.get('Indikator_Afektif', '')}\nRancang Pengalaman Belajar Afektif ke dalam TEPAT 3 tahap Sintaks Amoris. Gunakan '|||' sebagai pemisah.\nATURAN MUTLAK: DILARANG MENGGUNAKAN KATA SUBJEK (Peserta Didik/Siswa/Guru). Langsung awali poin dengan kata kerja desain instruksional.\nFormat Wajib Output:\n<Aktivitas Apersepsi>\n|||\n<Aktivitas Mengidentifikasi Konteks>\n|||\n<Aktivitas Olah Pikir,Rasa,Raga>"
                    hasil_ai = panggil_ai(prompt, "pg_afe")
                    hasil_ai = hasil_ai.replace("```text", "").replace("```", "").strip()
                    parts = hasil_ai.split("|||")
                    if len(parts) >= 3:
                        st.session_state.data_isian['Apersepsi_Afe'] = parts[0].strip()
                        st.session_state.data_isian['Konteks_Afe'] = parts[1].strip()
                        st.session_state.data_isian['Olah_Afe'] = "|||".join(parts[2:]).strip()
                    else:
                        st.session_state.data_isian['Apersepsi_Afe'] = hasil_ai
                        st.session_state.data_isian['Konteks_Afe'] = ""
                        st.session_state.data_isian['Olah_Afe'] = ""
                    st.session_state['ta_apersepsi_afe'] = st.session_state.data_isian['Apersepsi_Afe']
                    st.session_state['ta_konteks_afe'] = st.session_state.data_isian['Konteks_Afe']
                    st.session_state['ta_olah_afe'] = st.session_state.data_isian['Olah_Afe']
            
            simpan_teks('Apersepsi_Afe', st.text_area("1. APERSEPSI", value=st.session_state.data_isian.get('Apersepsi_Afe', ''), height=70, key="ta_apersepsi_afe"))
            simpan_teks('Konteks_Afe', st.text_area("2. MENGIDENTIFIKASI KONTEKS", value=st.session_state.data_isian.get('Konteks_Afe', ''), height=70, key="ta_konteks_afe"))
            simpan_teks('Olah_Afe', st.text_area("3. OLAH PIKIR, RASA, RAGA", value=st.session_state.data_isian.get('Olah_Afe', ''), height=70, key="ta_olah_afe"))
            
        with col_ta4:
            st.markdown("**4. ASESMEN**")
            st.write("\n\n")
            simpan_teks('Formatif', st.text_area("Formatif:", value=st.session_state.data_isian.get('Formatif', ''), height=115, key="ta_form_afe"))
            simpan_teks('Sumatif', st.text_area("Sumatif:", value=st.session_state.data_isian.get('Sumatif', ''), height=115, key="ta_sum_afe"))

# --- TAB 5: PSIKOMOTORIK (SINTAKS AMORIS) ---
with tab5:
    with st.container(border=True): 
        st.markdown("### ASPEK PSIKOMOTORIK")
        col_tp1, col_tp2, col_tp3, col_tp4 = st.columns([1,1,1.5,1])
        
        with col_tp1:
            st.markdown("**1. TP PSIKOMOTORIK**")
            if st.button("📈 Rumuskan TP", key="btn_tp_psi"):
                with st.spinner("Memproses..."):
                    prompt = f"Mata Pelajaran: {st.session_state.data_isian.get('MAPEL', '')}.\nBaca CP Umum: '{st.session_state.data_isian.get('Capaian_Pembelajaran', '')}'.\nRumuskan TEPAT 1 (satu) kalimat TP Psikomotorik (keterampilan/unjuk kerja), dan WAJIB mengintegrasikan narasi TP SDGs berikut: '{st.session_state.data_isian.get('TP_SDGs', '')}'.\nATURAN MUTLAK: Kalimat TP WAJIB diawali langsung dengan Kata Kerja Operasional (KKO) yang relevan tanpa subjek."
                    hasil_ai = panggil_ai(prompt, "tp_psi")
                    st.session_state.data_isian['TP_Psikomotorik'] = hasil_ai
                    st.session_state['ta_tp_psi'] = hasil_ai
            simpan_teks('TP_Psikomotorik', st.text_area("Isi TP:", value=st.session_state.data_isian.get('TP_Psikomotorik', ''), height=260, label_visibility="collapsed", key="ta_tp_psi"))
            
        with col_tp2:
            st.markdown("**2. INDIKATOR**")
            if st.button("🪜 Rumuskan Indikator", key="btn_ind_psi"):
                with st.spinner("Memproses..."):
                    prompt = f"Dari TP Psikomotorik: '{st.session_state.data_isian.get('TP_Psikomotorik', '')}', buat 3-4 Indikator keterampilan berjenjang.\nATURAN MUTLAK: Setiap poin Indikator WAJIB diawali langsung dengan Kata Kerja Operasional (KKO) tanpa subjek."
                    hasil_ai = panggil_ai(prompt, "ind_psi")
                    st.session_state.data_isian['Indikator_Psikomotorik'] = hasil_ai
                    st.session_state['ta_ind_psi'] = hasil_ai
            simpan_teks('Indikator_Psikomotorik', st.text_area("Isi Indikator:", value=st.session_state.data_isian.get('Indikator_Psikomotorik', ''), height=260, label_visibility="collapsed", key="ta_ind_psi"))
            
        with col_tp3:
            st.markdown("**3. PENGALAMAN BELAJAR**")
            if st.button("✨ Rumuskan Sintaks", key="btn_psi"):
                with st.spinner("Memproses..."):
                    prompt = f"Materi: {st.session_state.data_isian.get('Materi', '')}\nIndikator Psikomotorik: {st.session_state.data_isian.get('Indikator_Psikomotorik', '')}\nRancang Pengalaman Belajar (Unjuk kerja) ke dalam TEPAT 3 tahap Sintaks Amoris. Gunakan '|||' sebagai pemisah.\nATURAN MUTLAK: DILARANG MENGGUNAKAN KATA SUBJEK (Peserta Didik/Siswa/Guru). Langsung awali poin dengan kata kerja desain instruksional.\nFormat Wajib Output:\n<Aktivitas Apersepsi>\n|||\n<Aktivitas Mengidentifikasi Konteks>\n|||\n<Aktivitas Olah Pikir,Rasa,Raga>"
                    hasil_ai = panggil_ai(prompt, "pg_psi")
                    hasil_ai = hasil_ai.replace("```text", "").replace("```", "").strip()
                    parts = hasil_ai.split("|||")
                    if len(parts) >= 3:
                        st.session_state.data_isian['Apersepsi_Psi'] = parts[0].strip()
                        st.session_state.data_isian['Konteks_Psi'] = parts[1].strip()
                        st.session_state.data_isian['Olah_Psi'] = "|||".join(parts[2:]).strip()
                    else:
                        st.session_state.data_isian['Apersepsi_Psi'] = hasil_ai
                        st.session_state.data_isian['Konteks_Psi'] = ""
                        st.session_state.data_isian['Olah_Psi'] = ""
                    st.session_state['ta_apersepsi_psi'] = st.session_state.data_isian['Apersepsi_Psi']
                    st.session_state['ta_konteks_psi'] = st.session_state.data_isian['Konteks_Psi']
                    st.session_state['ta_olah_psi'] = st.session_state.data_isian['Olah_Psi']
            
            simpan_teks('Apersepsi_Psi', st.text_area("1. APERSEPSI", value=st.session_state.data_isian.get('Apersepsi_Psi', ''), height=70, key="ta_apersepsi_psi"))
            simpan_teks('Konteks_Psi', st.text_area("2. MENGIDENTIFIKASI KONTEKS", value=st.session_state.data_isian.get('Konteks_Psi', ''), height=70, key="ta_konteks_psi"))
            simpan_teks('Olah_Psi', st.text_area("3. OLAH PIKIR, RASA, RAGA", value=st.session_state.data_isian.get('Olah_Psi', ''), height=70, key="ta_olah_psi"))
            
        with col_tp4:
            st.markdown("**4. ASESMEN**")
            st.write("\n\n")
            simpan_teks('Asesmen_Formatif_Psikomotorik', st.text_area("Formatif:", value=st.session_state.data_isian.get('Asesmen_Formatif_Psikomotorik', ''), height=115, key="ta_form_psi"))
            simpan_teks('Asesmen_Sumatif_Psikomotorik', st.text_area("Sumatif:", value=st.session_state.data_isian.get('Asesmen_Sumatif_Psikomotorik', ''), height=115, key="ta_sum_psi"))

# --- TAB 6: PERAYAAN BELAJAR & CETAK ---
with tab6:
    with st.container(border=True): 
        st.markdown("### PERAYAAN BELAJAR (MEREFLEKSI)")
        simpan_teks('Membagikan_Pengalaman_Belajar', st.text_area("MEMBAGIKAN PENGALAMAN BELAJAR:", value=st.session_state.data_isian.get('Membagikan_Pengalaman_Belajar', '')))
        simpan_teks('Refleksi_Perkembangan_Kompetensi', st.text_area("REFLEKSI PERKEMBANGAN KOMPETENSI:", value=st.session_state.data_isian.get('Refleksi_Perkembangan_Kompetensi', '')))
        simpan_teks('Apresiasi', st.text_area("APRESIASI:", value=st.session_state.data_isian.get('Apresiasi', '')))
        simpan_teks('Media_Pembelajaran', st.text_area("MEDIA PEMBELAJARAN:", value=st.session_state.data_isian.get('Media_Pembelajaran', '')))
    
    with st.container(border=True): 
        st.subheader("🖨️ Rakit Dokumen & Simpan")
        if st.button("Rakit & Simpan Data", type="primary", use_container_width=True):
            if not st.session_state.data_isian.get('Nama_Guru'): st.error("❌ Nama Guru kosong!")
            else:
                with st.spinner('Memproses dokumen...'):
                    try:
                        st.session_state.data_isian['Pengalaman_Belajar'] = f"APERSEPSI:\n{st.session_state.data_isian.get('Apersepsi_Kog', '')}\n\nMENGIDENTIFIKASI KONTEKS:\n{st.session_state.data_isian.get('Konteks_Kog', '')}\n\nOLAH PIKIR, RASA, RAGA:\n{st.session_state.data_isian.get('Olah_Kog', '')}"
                        st.session_state.data_isian['Pengalaman_Belajar_Afektif'] = f"APERSEPSI:\n{st.session_state.data_isian.get('Apersepsi_Afe', '')}\n\nMENGIDENTIFIKASI KONTEKS:\n{st.session_state.data_isian.get('Konteks_Afe', '')}\n\nOLAH PIKIR, RASA, RAGA:\n{st.session_state.data_isian.get('Olah_Afe', '')}"
                        st.session_state.data_isian['Pengalaman_Belajar_Psikomotorik'] = f"APERSEPSI:\n{st.session_state.data_isian.get('Apersepsi_Psi', '')}\n\nMENGIDENTIFIKASI KONTEKS:\n{st.session_state.data_isian.get('Konteks_Psi', '')}\n\nOLAH PIKIR, RASA, RAGA:\n{st.session_state.data_isian.get('Olah_Psi', '')}"
                        
                        doc = DocxTemplate("Template_DPB_Schola Amoris.docx")
                        if foto_sdgs is not None: st.session_state.data_isian['Gambar_SGDs'] = InlineImage(doc, foto_sdgs, width=Mm(30))
                        doc.render(st.session_state.data_isian)
                        bio = io.BytesIO()
                        doc.save(bio)
                        simpan_draft_ke_awan() 
                        st.success("🎉 Berhasil! Dokumen siap diunduh.")
                        st.download_button(label="📥 Download File DPB", data=bio.getvalue(), file_name=f"DPB_{st.session_state.data_isian.get('MAPEL', 'Mapel')}.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document", use_container_width=True)
                    except Exception as e: st.error(f"Terjadi kesalahan perakitan Word: {e}")

# --- TAB 7: PERPUSTAKAAN ---
with tab7:
    st.subheader("📚 Perpustakaan Digital Schola Amoris")
    st.write("Temukan dan kelola referensi buku, modul, serta bahan ajar di sini.")
    try:
        if supabase is not None:
            respon_buku = supabase.table("koleksi_buku").select("*").execute()
            data_buku = respon_buku.data
            if data_buku:
                df_buku = pd.DataFrame(data_buku)
                st.dataframe(df_buku[["judul_buku", "kategori", "fase_kelas", "link_unduh"]], column_config={"judul_buku": "Judul Buku", "kategori": "Kategori", "fase_kelas": "Target Kelas", "link_unduh": st.column_config.LinkColumn("Tautan Unduh / Baca")}, hide_index=True, use_container_width=True)
            else: st.info("📭 Perpustakaan saat ini masih kosong.")
        else: st.error("Koneksi ke brankas Supabase terputus.")
    except Exception as e: st.error(f"Gagal memuat katalog buku: {e}")
    st.divider()
    with st.expander("➕ Tambah Buku Baru (Khusus Guru/Admin)"):
        baru_judul = st.text_input("Judul Buku/Materi:")
        baru_kategori = st.selectbox("Kategori:", ["Buku Teks Utama", "Modul Ajar", "Buku Cerita Digital", "LKPD", "Referensi Guru"])
        baru_fase = st.selectbox("Target Fase/Kelas:", ["Umum", "Fase Fondasi", "Fase A", "Fase B", "Fase C", "Fase D", "Fase E", "Fase F"])
        baru_link = st.text_input("Link Unduh (Google Drive / Tautan PDF):")
        if st.button("💾 Simpan Buku ke Perpustakaan", type="primary"):
            if baru_judul == "" or baru_link == "": st.warning("⚠️ Judul Buku dan Link Unduh wajib diisi!")
            else:
                with st.spinner("Menyimpan ke rak..."):
                    try:
                        supabase.table("koleksi_buku").insert({"judul_buku": baru_judul, "kategori": baru_kategori, "fase_kelas": baru_fase, "link_unduh": baru_link}).execute()
                        st.success("✅ Buku berhasil ditambahkan ke perpustakaan!")
                        st.rerun() 
                    except Exception as e: st.error(f"❌ Gagal menyimpan buku: {e}")
