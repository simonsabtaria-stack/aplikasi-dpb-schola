# File: data_kurikulum.py
# Database Pemetaan Kurikulum (Fase -> Mapel -> Elemen -> CP & Materi Esensial)
# Sumber: Keputusan BSKAP Nomor 046/H/KR/2025[cite: 4]

bank_kurikulum = {
    "Fase Fondasi": {
        "Pendidikan PAUD": {
            "Nilai Agama dan Budi Pekerti": [
                {
                    "cp": "Murid percaya kepada Tuhan Yang Maha Esa sebagai pencipta dirinya, makhluk lain dan alam, serta mulai mengenal dan mempraktikkan ajaran pokok sesuai dengan agama dan kepercayaannya; Murid menghargai diri sendiri dan memiliki rasa syukur terhadap Tuhan YME sehingga dapat berpartisipasi aktif dalam menjaga kebersihan, kesehatan, dan keselamatan dirinya; Murid menghargai sesama manusia dengan berbagai perbedaannya sehingga mempraktikkan perilaku baik dan berakhlak mulia; dan Murid menghargai alam dan seluruh makhluk hidup ciptaan Tuhan Yang Maha Esa.",
                    "materi": ["Praktik ajaran pokok agama", "Menjaga kebersihan dan kesehatan diri", "Perilaku baik dan akhlak mulia terhadap sesama dan alam"]
                }
            ],
            "Jati Diri": [
                {
                    "cp": "Murid mengenali identitas dirinya yang terbentuk oleh karakteristik fisik dan gender, minat, kebutuhan, agama, dan sosial budaya; Murid mengenali kebiasaan-kebiasaan di lingkungan keluarga, satuan pendidikan, dan masyarakat; Murid mengenali, mengekspresikan, dan mengelola emosi diri, serta membangun hubungan sosial secara sehat; Murid mengenali perannya sebagai bagian dari keluarga, satuan pendidikan, masyarakat dan warga negara Indonesia sehingga dapat menyesuaikan diri dengan lingkungan, aturan dan norma yang berlaku, dan mengetahui keberadaan negara lain di dunia; dan Murid memiliki fungsi gerak (motorik kasar, halus, dan taktil) untuk merawat dirinya, membangun kemandirian dan berkegiatan).",
                    "materi": ["Identitas diri dan emosi", "Hubungan sosial sehat", "Motorik kasar, halus, dan taktil"]
                }
            ],
            "Dasar-dasar Literasi, Matematika, Sains, Teknologi, Rekayasa, dan Seni": [
                {
                    "cp": "Murid mengenali dan memahami berbagai informasi, mengomunikasikan perasaan dan pikiran secara lisan, tulisan, atau menggunakan berbagai media serta membangun percakapan, menunjukkan minat, dan berpartisipasi dalam kegiatan pramembaca; Murid memiliki kepekaaan bilangan; mengidentifikasi pola; memiliki kesadaran tentang bentuk, posisi, dan ruang; menyadari adanya persamaan dan perbedaan karakteristik antar objek; mampu melakukan pengukuran dengan satuan tidak baku; dan memiliki kesadaran mengenai waktu; Murid mampu mengamati, menyebutkan alasan, pilihan atau keputusannya, mampu memecahkan masalah sederhana, serta mengetahui hubungan sebab akibat dari suatu kondisi atau situasi yang dipengaruhi oleh hukum alam dan kondisi sosial; Murid menunjukkan kemampuan awal menggunakan dan merekayasa teknologi serta untuk mencari informasi, gagasan, dan keterampilan secara aman dan bertanggung jawab; dan Murid mengeksplorasi berbagai proses seni, mengekspresikannya, serta mengapresiasi karya seni.",
                    "materi": ["Pramembaca dan komunikasi lisan/tulis", "Kepekaan bilangan, pola, ruang, waktu", "Eksplorasi sains, rekayasa teknologi sederhana, dan proses seni"]
                }
            ]
        },
        "Muatan Lokal (Opsional)": {
            "Muatan Lokal": [
                {
                    "cp": "Capaian Pembelajaran Muatan Lokal disesuaikan dengan kebijakan satuan pendidikan.",
                    "materi": ["Materi Muatan Lokal"]
                }
            ]
        }
    },
    
    "Fase A": {
        "Pendidikan Agama Katolik dan Budi Pekerti": {
            "Pribadi Peserta Didik": [{"cp": "Memahami dirinya sebagai pribadi yang dicintai Tuhan, memiliki anggota tubuh yang berguna, memahami cara merawat tubuhnya; memahami teman-teman, lingkungan rumah dan satuan pendidikan sebagai tempat mengembangkan potensi diri.", "materi": ["Pribadi dicintai Tuhan", "Merawat anggota tubuh"]}],
            "Yesus Kristus": [{"cp": "Memahami bahwa Tuhan menciptakan langit, bumi, dan seluruh isinya; memahami tokoh-tokoh iman di dalam Perjanjian Lama (Nuh, Abraham, Ishak, dan Yakub); memahami kisah kelahiran Tuhan Yesus, kisah tiga orang Majus, masa kanak-kanak Yesus di Nazaret, Yesus dipersembahkan di Bait Allah, dan berada di Bait Allah pada umur 12 tahun.", "materi": ["Penciptaan", "Tokoh Perjanjian Lama", "Kelahiran dan masa kanak-kanak Yesus"]}],
            "Gereja": [{"cp": "Memahami imannya dengan cara membuat tanda salib, berdoa Bapa Kami, Salam Maria, dan Kemuliaan; memahami iman dengan melaksanakan perintah Allah, dan membiasakan diri dengan berdoa pujian, syukur dan permohonan.", "materi": ["Tanda salib dan doa dasar", "Berdoa pujian, syukur, permohonan"]}],
            "Masyarakat": [{"cp": "Memahami lingkungan keluarga, dan teman-teman, memiliki kebiasaan bekerja sama dengan anggota keluarga dan teman-teman; memahami iman di tengah masyarakat melalui kebiasaan hidup rukun dengan tetangga dan bergotong royong merawat lingkungan.", "materi": ["Kerjasama keluarga dan teman", "Hidup rukun dan gotong royong"]}]
        },
        "Pendidikan Pancasila": {
            "Pancasila": [{"cp": "Mengenal bendera negara, lagu kebangsaan, simbol dan sila-sila Pancasila dalam lambang negara Garuda Pancasila dan simbol Pancasila beserta sila-sila Pancasila; menerapkan nilai-nilai Pancasila di lingkungan keluarga.", "materi": ["Bendera, lagu, simbol negara", "Nilai Pancasila di keluarga"]}],
            "Undang-Undang Dasar Negara Republik Indonesia Tahun 1945": [{"cp": "Mengenal aturan di lingkungan keluarga; menunjukkan dan menceritakan sikap mematuhi aturan di lingkungan keluarga.", "materi": ["Aturan di lingkungan keluarga"]}],
            "Bhinneka Tunggal Ika": [{"cp": "Mengenal semboyan Bhinneka Tunggal Ika; mengidentifikasi dan menghargai identitas dirinya sesuai dengan jenis kelamin, hobi, bahasa, serta agama dan kepercayaan di lingkungan sekitar.", "materi": ["Semboyan Bhinneka Tunggal Ika", "Menghargai identitas diri dan sesama"]}],
            "Negara Kesatuan Republik Indonesia": [{"cp": "Mengenal karakteristik lingkungan tempat tinggal dan sekolah, sebagai bagian dari wilayah Negara Kesatuan Republik Indonesia; menceritakan dan mempraktikkan bekerja sama menjaga lingkungan sekitar dalam keberagaman.", "materi": ["Lingkungan tempat tinggal dan sekolah", "Kerjasama menjaga lingkungan"]}]
        },
        "Bahasa Indonesia": {
            "Menyimak": [{"cp": "Memahami informasi dari teks nonsastra berbentuk teks aural (teks yang dibacakan dan/atau didengarkan) berupa percakapan yang berkaitan dengan diri, keluarga, dan/atau lingkungan sekitar; dan memahami pesan teks sastra berbentuk teks aural.", "materi": ["Teks aural percakapan", "Pesan teks sastra aural"]}],
            "Membaca dan Memirsa": [{"cp": "Membaca kata-kata sederhana dengan fasih dari bacaan dan/atau tayangan yang dipirsa tentang diri, keluarga, kesehatan, dan/atau lingkungan sekitar; dan memahami isi bacaan dan/atau tayangan yang dipirsa tentang diri, keluarga, kesehatan, dan/atau lingkungan sekitar.", "materi": ["Membaca kata sederhana", "Memahami isi bacaan dan visual"]}],
            "Berbicara dan Mempresentasikan": [{"cp": "Merespons dengan bertanya tentang sesuatu, menjawab, dan menanggapi komentar orang lain (teman, pendidik, dan/atau orang dewasa) dengan baik dan santun dalam suatu percakapan tentang diri, keluarga, kesehatan, dan/atau lingkungan sekitar; mengungkapkan perasaan dan gagasan secara lisan dengan atau tanpa bantuan gambar; dan menceritakan kembali isi berbagai tipe teks yang dibaca, dipirsa, atau didengar tentang diri, keluarga, kesehatan, dan/atau lingkungan sekitar.", "materi": ["Bertanya dan menanggapi komentar", "Bercerita dan mengungkapkan gagasan lisan"]}],
            "Menulis": [{"cp": "Menulis permulaan dengan benar di atas kertas dan/atau melalui media digital; mengembangkan tulisan tangan yang semakin baik; dan menulis berbagai tipe teks sederhana tentang diri, keluarga, dan/atau lingkungan sekitar dengan beberapa kalimat sederhana.", "materi": ["Menulis permulaan", "Menulis kalimat sederhana"]}]
        },
        "Matematika": {
            "Bilangan": [{"cp": "Menunjukkan pemahaman dan memiliki intuisi bilangan (number sense) pada bilangan cacah sampai 100; membaca, menulis, menentukan nilai tempat, membandingkan, mengurutkan, serta melakukan komposisi (menyusun) dan dekomposisi (mengurai) bilangan; melakukan operasi penjumlahan dan pengurangan menggunakan benda-benda konkret yang banyaknya sampai 20; dan menunjukkan pemahaman pecahan sebagai bagian dari keseluruhan melalui konteks membagi sebuah benda atau kumpulan benda sama banyak (pecahan yang diperkenalkan adalah setengah dan seperempat).", "materi": ["Bilangan cacah sampai 100", "Penjumlahan dan pengurangan sampai 20", "Pecahan setengah dan seperempat"]}],
            "Aljabar": [{"cp": "Menunjukan pemahaman makna simbol matematika \"=\" dalam suatu kalimat matematika yang terkait dengan penjumlahan dan pengurangan bilangan cacah sampai 20 menggunakan gambar. Murid dapat mengenali, meniru, dan melanjutkan pola bukan bilangan (misalnya, gambar, warna, bunyi/suara).", "materi": ["Makna simbol = (sama dengan)", "Pola bukan bilangan"]}],
            "Pengukuran": [{"cp": "Membandingkan panjang dan berat benda secara langsung, dan membandingkan durasi waktu; mengukur dan mengestimasi panjang dan berat benda menggunakan satuan tidak baku.", "materi": ["Membandingkan panjang, berat, waktu", "Pengukuran satuan tidak baku"]}],
            "Geometri": [{"cp": "Mengenal berbagai bangun datar (segitiga, segiempat, segi banyak, lingkaran) dan bangun ruang (balok, kubus, kerucut, dan bola); melakukan komposisi (penyusunan) dan dekomposisi (penguraian) suatu bangun datar (segitiga, segiempat, dan segi banyak); dan menentukan posisi benda terhadap benda lain (kanan, kiri, depan belakang, bawah, atas).", "materi": ["Bangun datar dan bangun ruang", "Posisi benda"]}],
            "Analisis Data dan Peluang": [{"cp": "Mengurutkan, menyortir, mengelompokkan, membandingkan, dan menyajikan data dari banyak benda dengan menggunakan turus dan piktogram paling banyak 4 kategori.", "materi": ["Pengelompokan data", "Turus dan Piktogram"]}]
        },
        "Seni Musik": {
            "Mengalami": [{"cp": "Mengenali unsur-unsur musik (nada dan irama) menggunakan anggota tubuh maupun alat musik.", "materi": ["Unsur nada dan irama"]}],
            "Merefleksikan": [{"cp": "Melakukan umpan balik mengenai praktik bermain musik diri sendiri atau orang lain menggunakan bahasa sehari-hari.", "materi": ["Umpan balik praktik musik"]}],
            "Berpikir dan Bekerja Artistik": [{"cp": "Menirukan pola irama dan nada menggunakan alat musik ritmis atau melodis; mengenali ragam alat musik dan bunyi yang dihasilkan; mengenali cara memainkan dan membersihkan instrumen/alat musik.", "materi": ["Pola irama dan nada", "Ragam alat musik"]}],
            "Menciptakan": [{"cp": "Membuat pola irama menggunakan anggota tubuh atau alat musik ritmis yang tersedia di lingkungan sekitar.", "materi": ["Mencipta pola irama"]}],
            "Berdampak": [{"cp": "Menunjukkan ekspresi senang dalam kegiatan bermusik.", "materi": ["Ekspresi dalam bermusik"]}]
        },
        "Seni Rupa": {
            "Mengalami": [{"cp": "Mengenali dan menyebutkan unsur-unsur rupa dalam benda-benda di sekitar/karya seni rupa.", "materi": ["Unsur rupa lingkungan sekitar"]}],
            "Merefleksikan": [{"cp": "Merefleksikan dan mengapresiasi karya diri sendiri.", "materi": ["Apresiasi karya"]}],
            "Berpikir dan Bekerja Artistik": [{"cp": "Mengenali dan menguji coba alat dan/atau bahan yang dimiliki.", "materi": ["Alat dan bahan seni rupa"]}],
            "Menciptakan": [{"cp": "Membuat karya seni rupa berdasarkan pengalaman dan hasil pengamatan terhadap lingkungan sekitar.", "materi": ["Penciptaan karya pengamatan"]}],
            "Berdampak": [{"cp": "Menghasilkan karya seni rupa yang berdampak pada perasaan dirinya.", "materi": ["Dampak karya rupa"]}]
        },
        "Muatan Lokal (Opsional)": {
            "Muatan Lokal": [{"cp": "Capaian Pembelajaran disesuaikan dengan kebijakan satuan pendidikan.", "materi": ["Materi Muatan Lokal"]}]
        }
    },

    "Fase B": {
        "Pendidikan Agama Katolik dan Budi Pekerti": {
            "Pribadi Peserta Didik": [{"cp": "Memahami dirinya sebagai pribadi yang tumbuh dan berkembang, mewujudkan iman dengan cara melakukan perbuatan baik; memahami diri sebagai pribadi yang unik, bersyukur dan bersedia mengembangkan keunikan diri bersama orang lain dan lingkungan sekitar.", "materi": ["Pertumbuhan pribadi", "Mengembangkan keunikan diri"]}],
            "Yesus Kristus": [{"cp": "Memahami karya keselamatan Allah melalui tokoh-tokoh Yusuf, Musa, dan Yosua; memahami Sepuluh Perintah Allah sebagai pedoman hidup; memahami bangsa Israel memasuki tanah terjanji, Allah memberkati pemimpin Israel (Samuel, Saul, dan Daud); memahami Yesus sebagai pemenuhan janji Allah yang mewartakan Kerajaan Allah melalui perkataan, perbuatan, dan mukjizat", "materi": ["Tokoh Perjanjian Lama", "Sepuluh Perintah Allah", "Karya dan Mukjizat Yesus"]}],
            "Gereja": [{"cp": "Murid memahami sakramen baptis, sakramen ekaristi, dan sakramen tobat; mengungkapkan rasa syukur dalam doa pribadi dan doa bersama, mewujudkan makna doa melalui sikap dan tindakan dalam kehidupan sehari-hari.", "materi": ["Sakramen Inisiasi dan Tobat", "Doa pribadi dan bersama"]}],
            "Masyarakat": [{"cp": "Mewujudkan imannya di tengah masyarakat melalui kebiasaan menghormati pemimpin masyarakat, menghargai tradisi masyarakat, melestarikan lingkungan alam; mewujudkan rasa hormat terhadap orang tua, menghormati hidup pribadi, menghormati milik orang lain.", "materi": ["Menghormati pemimpin dan tradisi", "Kelestarian lingkungan"]}]
        },
        "Pendidikan Pancasila": {
            "Pancasila": [{"cp": "Mengidentifikasi makna sila-sila Pancasila, dan penerapannya dalam kehidupan sehari-hari; mengenal karakter para perumus Pancasila; menunjukkan sikap bangga menjadi anak Indonesia yang memiliki bahasa Indonesia sebagai bahasa persatuan di lingkungan sekitar.", "materi": ["Makna sila Pancasila", "Tokoh perumus Pancasila", "Bahasa persatuan"]}],
            "Undang-Undang Dasar Negara Republik Indonesia Tahun 1945": [{"cp": "Mengidentifikasi dan melaksanakan aturan di sekolah dan lingkungan tempat tinggal; mengidentifikasi dan menerapkan hak yang didapat dan kewajiban sebagai anggota keluarga dan sebagai warga sekolah.", "materi": ["Aturan sekolah dan rumah", "Hak dan kewajiban anak"]}],
            "Bhinneka Tunggal Ika": [{"cp": "Membedakan dan menghargai identitas, suku bangsa, bahasa, agama dan kepercayaannya di lingkungan sekitar keluarga, dan teman-temannya.", "materi": ["Menghargai keragaman identitas dan agama"]}],
            "Negara Kesatuan Republik Indonesia": [{"cp": "Mengidentifikasi lingkungan tempat tinggal (RT, RW, desa atau kelurahan, dan kecamatan) sebagai bagian dari wilayah Negara Kesatuan Republik Indonesia; menunjukkan perilaku bekerja sama dalam berbagai bentuk keberagaman suku bangsa, sosial, dan budaya di Indonesia yang terikat persatuan dan kesatuan di lingkungan sekitar.", "materi": ["Struktur pemerintahan desa/kelurahan", "Kerjasama keberagaman lokal"]}]
        },
        "Bahasa Indonesia": {
            "Menyimak": [{"cp": "Memahami ide pokok suatu informasi dari teks nonsastra berbentuk teks aural (teks yang dibacakan dan/atau didengarkan); dan memahami isi teks sastra berbentuk teks aural.", "materi": ["Ide pokok teks nonsastra aural", "Isi teks sastra aural"]}],
            "Membaca dan Memirsa": [{"cp": "Membaca kata-kata baru dengan fasih dari bacaan dan/atau tayangan yang dipirsa; dan memahami ide pokok, ide pendukung, pesan, dan informasi dalam teks sastra dan nonsastra berbentuk cetak dan/atau elektronik.", "materi": ["Membaca kata baru", "Ide pokok dan pendukung teks visual"]}],
            "Berbicara dan Mempresentasikan": [{"cp": "Menyajikan pendapat dengan pilihan kata dan sikap tubuh/gestur yang sesuai, menggunakan volume dan intonasi yang tepat sesuai konteks; menanggapi diskusi sesuai tata cara; dan menceritakan kembali isi dan/atau informasi dari berbagai tipe teks yang dibaca, dipirsa, atau didengar.", "materi": ["Menyajikan pendapat beretika", "Menceritakan kembali teks"]}],
            "Menulis": [{"cp": "Menulis berbagai tipe teks sederhana dengan rangkaian kalimat yang beragam; dan menggunakan kaidah kebahasaan dan kosakata baru yang memiliki makna denotatif untuk menulis teks sesuai dengan konteks.", "materi": ["Menulis teks sederhana", "Kosa kata bermakna denotatif"]}]
        },
        "Matematika": {
            "Bilangan": [{"cp": "Memiliki pemahaman dan intuisi bilangan (number sense) pada bilangan cacah sampai 10.000; membaca, menulis, membandingkan, dan mengurutkan bilangan; menentukan dan menggunakan nilai tempat; melakukan komposisi dan dekomposisi bilangan cacah sampai 10.000. Murid dapat melakukan dan menyelesaikan masalah operasi bilangan penjumlahan dan pengurangan bilangan cacah sampai 1.000; perkalian dan pembagian sampai 100. Mengenal kelipatan dan faktor, serta perbandingan pecahan dan desimal/persen.", "materi": ["Bilangan cacah sampai 10.000", "Operasi hitung dasar", "Pecahan senilai dan desimal"]}],
            "Aljabar": [{"cp": "Menemukan nilai yang tidak diketahui dalam kalimat matematika yang melibatkan penjumlahan dan pengurangan pada bilangan cacah sampai 100. Murid dapat mengidentifikasi, meniru, dan mengembangkan pola gambar atau objek sederhana dan pola bilangan membesar dan mengecil.", "materi": ["Nilai tidak diketahui dalam persamaan", "Pola gambar dan bilangan"]}],
            "Pengukuran": [{"cp": "Mengukur panjang dan berat benda menggunakan satuan baku; menentukan hubungan antar-satuan baku panjang (cm, m) dan antar-satuan berat (g, kg); serta mengukur dan mengestimasi luas dan volume menggunakan satuan tidak baku dan satuan baku berupa bilangan cacah.", "materi": ["Satuan baku panjang dan berat", "Estimasi luas dan volume"]}],
            "Geometri": [{"cp": "Mendeskripsikan ciri berbagai bentuk bangun datar (segiempat, segitiga, segi banyak); menyusun (komposisi) dan mengurai (dekomposisi) berbagai bangun datar dengan lebih dari satu cara jika memungkinkan.", "materi": ["Ciri bangun datar", "Komposisi dan dekomposisi bangun"]}],
            "Analisis Data dan Peluang": [{"cp": "Mengurutkan, membandingkan, menyajikan, menganalisis dan menginterpretasi data dalam bentuk tabel, diagram gambar, piktogram, dan diagram batang (skala satu satuan).", "materi": ["Diagram gambar dan batang", "Interpretasi data dasar"]}]
        },
        "Bahasa Inggris": {
            "Menyimak - Berbicara": [{"cp": "Memahami dan merespon teks lisan atau teks multimodal sederhana tentang kehidupan sehari-hari baik secara verbal atau non-verbal sesuai konteks.", "materi": ["Merespon teks lisan/multimodal", "Kosakata kehidupan sehari-hari"]}],
            "Membaca - Memirsa": [{"cp": "Memahami teks tulis pendek sederhana atau teks multimodal tentang kehidupan sehari-hari dan meresponsnya secara verbal atau non-verbal sesuai konteks.", "materi": ["Membaca teks pendek sederhana", "Merespon teks visual"]}],
            "Menulis - Mempresentasikan": [{"cp": "Mengomunikasikan gagasan tentang topik sehari-hari dalam teks tulis pendek atau teks multimodal sesuai konteks.", "materi": ["Menulis gagasan pendek", "Mempresentasikan ide sehari-hari"]}]
        },
        "Ilmu Pengetahuan Alam dan Sosial (IPAS)": {
            "Pemahaman IPAS": [{"cp": "Menjelaskan bentuk dan fungsi pancaindra; menganalisis siklus hidup makhluk hidup; upaya mitigasi perubahan iklim; menyimpulkan proses perubahan wujud zat; sumber dan bentuk energi; jenis gaya; interaksi sosial di sekitar; letak geografi konvensional/digital; ragam bentang alam dan profesi budaya; sejarah lokal; uang dan fungsi ekonomi.", "materi": ["Pancaindra dan siklus hidup", "Energi, wujud zat, dan gaya", "Geografi lokal, budaya, dan ekonomi dasar"]}],
            "Keterampilan Proses": [{"cp": "Mampu mengamati fenomena, mempertanyakan dan memprediksi, merencanakan dan melakukan penyelidikan, memproses, menganalisis data, mengevaluasi dan refleksi, serta mengomunikasikan hasil.", "materi": ["Siklus penyelidikan ilmiah sederhana"]}]
        },
        "Seni Musik": {
            "Mengalami": [{"cp": "Mengenali nada dan pola irama menggunakan anggota tubuh maupun alat musik.", "materi": ["Nada dan pola irama"]}],
            "Merefleksikan": [{"cp": "Melakukan umpan balik mengenai praktik bermusik diri sendiri atau orang lain menggunakan istilah musik.", "materi": ["Umpan balik musikal"]}],
            "Berpikir dan Bekerja Artistik": [{"cp": "Menirukan pola irama dan melodi menggunakan alat musik ritmis atau melodis; menyebutkan karakteristik ragam alat musik dan bunyi yang dihasilkan; mengetahui cara memainkan dan merawat alat musik.", "materi": ["Pola melodi", "Merawat alat musik"]}],
            "Menciptakan": [{"cp": "Membuat bunyi menggunakan anggota tubuh atau alat musik ritmis dan melodis yang tersedia di lingkungan sekitar.", "materi": ["Eksplorasi bunyi ritmis/melodis"]}],
            "Berdampak": [{"cp": "Menunjukkan minat dalam kegiatan bermusik.", "materi": ["Minat musikal"]}]
        },
        "Seni Rupa": {
            "Mengalami": [{"cp": "Mengidentifikasi unsur rupa dan prinsip desain dalam benda-benda di sekitar/karya seni rupa.", "materi": ["Unsur rupa dan prinsip desain"]}],
            "Merefleksikan": [{"cp": "Merefleksikan dan mengapresiasi karya diri sendiri dan teman sekelas menggunakan kosa kata seni rupa yang sesuai.", "materi": ["Kosa kata apresiasi seni"]}],
            "Berpikir dan Bekerja Artistik": [{"cp": "Mengenali dan menguji coba alat dan/atau bahan yang dimiliki serta prosedur penggunaannya.", "materi": ["Eksplorasi prosedur alat bahan"]}],
            "Menciptakan": [{"cp": "Membuat karya seni rupa berdasarkan pengalaman dan hasil pengamatan terhadap lingkungan sekitar.", "materi": ["Karya rupa observasi"]}],
            "Berdampak": [{"cp": "Menghasilkan karya seni rupa yang berdampak pada perasaan atau mewakili harapannya.", "materi": ["Karya seni representasi harapan"]}]
        },
        "Muatan Lokal (Opsional)": {
            "Muatan Lokal": [{"cp": "Capaian Pembelajaran disesuaikan dengan kebijakan satuan pendidikan.", "materi": ["Materi Muatan Lokal"]}]
        }
    },

    "Fase C": {
        "Pendidikan Agama Katolik dan Budi Pekerti": {
            "Pribadi Peserta Didik": [{"cp": "Memahami diri sebagai perempuan atau laki-laki sebagai citra Allah yang sederajat; memahami hak dan kewajiban dirinya sebagai warga negara dan bangga sebagai bangsa Indonesia; memahami diri sebagai warga dunia.", "materi": ["Citra Allah sederajat", "Hak kewajiban warga negara"]}],
            "Yesus Kristus": [{"cp": "Memahami perjuangan tokoh-tokoh kitab suci (Daud, Salomo, Ester, Maria); meneladani Yesus yang taat kepada Allah; mengajarkan pengampunan, memanggil orang berdosa; menderita, wafat, bangkit, mengutus Roh Kudus; memahami nabi Elia, Amos, Yesaya.", "materi": ["Tokoh dan Nabi Alkitab", "Ketaatan, Wafat dan Kebangkitan Yesus"]}],
            "Gereja": [{"cp": "Mewujudkan iman dalam kehidupan sehari-hari, melibatkan diri dalam kehidupan menggereja; memahami gereja yang satu, kudus, katolik, apostolik; persekutuan para kudus; pengampunan dosa, kebangkitan badan.", "materi": ["Sifat Gereja", "Persekutuan Para Kudus"]}],
            "Masyarakat": [{"cp": "Memahami pentingnya terlibat aktif dalam pelestarian lingkungan, bersikap jujur, bertindak menurut hati nurani, menegakkan keadilan, melakukan dialog antar umat beragama.", "materi": ["Hati nurani dan keadilan", "Dialog antar umat beragama"]}]
        },
        "Pendidikan Pancasila": {
            "Pancasila": [{"cp": "Memahami kronologi sejarah kelahiran Pancasila; meneladani sikap perumus Pancasila; menghubungkan sila-sila sebagai satu kesatuan utuh; menguraikan makna nilai Pancasila sebagai dasar negara.", "materi": ["Sejarah kelahiran Pancasila", "Kesatuan sila Pancasila"]}],
            "Undang-Undang Dasar Negara Republik Indonesia Tahun 1945": [{"cp": "Mengimplementasikan bentuk norma, hak, dan kewajiban; mengenal Pembukaan UUD 1945; mempraktikkan musyawarah untuk kesepakatan di keluarga dan sekolah.", "materi": ["Pembukaan UUD 1945", "Musyawarah mufakat"]}],
            "Bhinneka Tunggal Ika": [{"cp": "Menyajikan hasil identifikasi sikap menghormati, menjaga, dan melestarikan keberagaman budaya sesuai semboyan dalam bingkai Bhinneka Tunggal Ika di lingkungan sekitar.", "materi": ["Pelestarian budaya lokal"]}],
            "Negara Kesatuan Republik Indonesia": [{"cp": "Mengenal wilayahnya dalam konteks kabupaten/kota, dan provinsi sebagai bagian dari wilayah NKRI; menunjukkan perilaku gotong royong untuk menjaga persatuan di lingkungan sekolah dan sekitar sebagai wujud bela negara.", "materi": ["Geografi wilayah provinsi", "Gotong royong dan bela negara"]}]
        },
        "Bahasa Indonesia": {
            "Menyimak": [{"cp": "Menganalisis informasi dari teks nonsastra berbentuk teks aural (teks yang dibacakan dan/atau didengarkan); dan menganalisis isi teks sastra berbentuk teks aural.", "materi": ["Analisis informasi teks aural"]}],
            "Membaca dan Memirsa": [{"cp": "Membaca kata-kata dengan berbagai pola kombinasi huruf dengan fasih dari bacaan dan/atau tayangan yang dipirsa; dan menganalisis informasi serta nilai-nilai dalam teks sastra dan nonsastra berwujud teks visual dan/atau audiovisual.", "materi": ["Analisis teks sastra/nonsastra audiovisual"]}],
            "Berbicara dan Mempresentasikan": [{"cp": "Mempresentasikan gagasan dari berbagai tipe teks dengan efektif dan santun; dan menyampaikan perasaan berdasarkan fakta, imajinasi secara indah dan menarik dalam bentuk teks sastra.", "materi": ["Presentasi gagasan efektif", "Bercerita sastra imajinatif"]}],
            "Menulis": [{"cp": "Menulis berbagai tipe teks sederhana berdasarkan gagasan, hasil pengamatan, pengalaman, dan/atau imajinasi dengan rangkaian kalimat kompleks secara kreatif; menggunakan makna denotatif dan konotatif.", "materi": ["Menulis kalimat kompleks", "Makna konotatif dalam tulisan"]}]
        },
        "Matematika": {
            "Bilangan": [{"cp": "Menunjukkan pemahaman dan intuisi bilangan (number sense) bilangan cacah sampai 1.000.000; operasi hitung sampai 100.000; KPK dan FPB; membandingkan, mengurutkan, dan operasi hitung pecahan (campuran dan desimal).", "materi": ["Bilangan sampai 1.000.000", "KPK dan FPB", "Operasi Pecahan campuran/desimal"]}],
            "Aljabar": [{"cp": "Menemukan nilai yang belum diketahui dalam kalimat matematika yang melibatkan 4 operasi dasar cacah sampai 1000; pola bilangan membesar dan mengecil; bernalar proporsional/rasio satuan.", "materi": ["Aljabar dasar cacah", "Rasio dan Proporsi"]}],
            "Pengukuran": [{"cp": "Menentukan keliling dan luas berbagai bentuk bangun datar serta gabungannya; menghitung durasi waktu dan mengukur besar sudut pada bangun datar.", "materi": ["Keliling luas gabungan", "Pengukuran sudut"]}],
            "Geometri": [{"cp": "Mengkonstruksi dan mengurai bangun ruang (kubus, balok, dan gabungannya) dan mengenali visualisasi spasial; membandingkan karakteristik bangun ruang; menentukan lokasi pada peta sistem berpetak.", "materi": ["Bangun ruang dan visualisasi spasial", "Sistem koordinat berpetak"]}],
            "Analisis Data dan Peluang": [{"cp": "Mengurutkan, membandingkan, menyajikan, dan menganalisis data dalam bentuk gambar, piktogram, diagram batang, tabel frekuensi; menentukan kejadian peluang (lebih besar/kecil) dari percobaan acak.", "materi": ["Tabel frekuensi dan diagram batang", "Peluang eksperimen acak"]}]
        },
        "Bahasa Inggris": {
            "Menyimak - Berbicara": [{"cp": "Memahami alur informasi teks secara keseluruhan dan merespon teks lisan atau teks multimodal sederhana tentang topik sehari-hari secara lisan dengan kalimat pendek dan sederhana sesuai konteks.", "materi": ["Respons percakapan sehari-hari", "Kalimat pendek bahasa Inggris"]}],
            "Membaca - Memirsa": [{"cp": "Memahami alur informasi secara keseluruhan, gagasan utama dan informasi rinci dari beragam teks pendek atau teks multimodal tentang topik sehari-hari dan meresponnya sesuai konteks.", "materi": ["Gagasan utama teks pendek", "Informasi rinci teks visual"]}],
            "Menulis - Mempresentasikan": [{"cp": "Mengomunikasikan ide dan pengalamannya melalui berbagai jenis teks tulis sederhana atau teks multimodal tentang topik sehari-hari sesuai konteks.", "materi": ["Menulis pengalaman pribadi", "Presentasi topik sehari-hari"]}]
        },
        "Ilmu Pengetahuan Alam dan Sosial (IPAS)": {
            "Pemahaman IPAS": [{"cp": "Merefleksikan sistem organ tubuh manusia; menganalisis hubungan biotik-abiotik ekosistem; gelombang bunyi dan cahaya; energi alternatif mitigasi iklim; sistem tata surya, rotasi dan revolusi bumi; kondisi geografis Indonesia; sejarah perjuangan pahlawan; keragaman budaya dan kearifan lokal; kegiatan ekonomi masyarakat sekitar.", "materi": ["Sistem organ, ekosistem, gelombang", "Tata surya, geografis, sejarah, ekonomi lokal"]}],
            "Keterampilan Proses": [{"cp": "Mampu mengamati fenomena, mempertanyakan, merencanakan dan melakukan penyelidikan mandiri, memproses menganalisis data, mengevaluasi, serta mengomunikasikan hasil.", "materi": ["Investigasi ilmiah berargumen"]}]
        },
        "Seni Musik": {
            "Mengalami": [{"cp": "Mengenali dan menerapkan unsur-unsur musik (nada, irama dan melodi) menggunakan alat musik ritmis dan melodis serta menunjukkan tingkat kepekaan akan unsur-unsur musik.", "materi": ["Penerapan unsur musik", "Kepekaan nada"]}],
            "Merefleksikan": [{"cp": "Melakukan umpan balik mengenai karya dan kemampuan bermusik diri sendiri atau orang lain menggunakan istilah musik yang tepat.", "materi": ["Istilah musik formal"]}],
            "Berpikir dan Bekerja Artistik": [{"cp": "Mengeksplorasi variasi pola irama, tempo dan melodi dengan alat musik menggunakan notasi musik; menemukan alternatif bunyi sederhana.", "materi": ["Membaca notasi musik", "Eksplorasi bunyi"]}],
            "Menciptakan": [{"cp": "Membuat dan mengembangkan pola irama menggunakan anggota tubuh atau alat musik ritmis yang tersedia berdasarkan nilai kearifan lokal daerahnya.", "materi": ["Komposisi berbasis kearifan lokal"]}],
            "Berdampak": [{"cp": "Menunjukkan minat dan rasa ingin tahu dalam kegiatan bermusik.", "materi": ["Motivasi musikal"]}]
        },
        "Seni Rupa": {
            "Mengalami": [{"cp": "Menjelaskan unsur rupa dan prinsip desain dalam benda-benda di sekitar/karya seni rupa.", "materi": ["Penjelasan prinsip desain"]}],
            "Merefleksikan": [{"cp": "Merefleksikan dan mengapresiasi karya diri sendiri dan teman sekelas menggunakan kosa kata seni rupa yang sesuai.", "materi": ["Apresiasi seni terstruktur"]}],
            "Berpikir dan Bekerja Artistik": [{"cp": "Mengenali dan menguji coba variasi teknik penggunaan alat dan/atau bahan.", "materi": ["Variasi teknik seni rupa"]}],
            "Menciptakan": [{"cp": "Membuat karya seni rupa berdasarkan pengalaman dan/atau hasil pengamatan terhadap lingkungan sekitar melalui pengembangan imajinasi.", "materi": ["Karya rupa imajinatif"]}],
            "Berdampak": [{"cp": "Menghasilkan karya seni rupa yang mewakili minatnya.", "materi": ["Dampak karya berbasis minat"]}]
        },
        "Muatan Lokal (Opsional)": {
            "Muatan Lokal": [{"cp": "Capaian Pembelajaran disesuaikan dengan kebijakan satuan pendidikan.", "materi": ["Materi Muatan Lokal"]}]
        }
    },

    "Fase D": {
        "Pendidikan Agama Katolik dan Budi Pekerti": {
            "Pribadi Peserta Didik": [{"cp": "Memahami manusia sebagai citra Allah yang unik, laki-laki dan perempuan; kemampuan dan keterbatasan; tumbuh berkembang peran keluarga, teman, sekolah, dan gereja.", "materi": ["Manusia diciptakan sebagai Citra Allah", "Kemampuan dan Keterbatasan", "Peran lingkungan hidup"]}],
            "Yesus Kristus": [{"cp": "Memahami pribadi Yesus berbelas kasih, karya pemenuhan janji Allah, sengsara, wafat, kebangkitan; mengutus Roh Kudus.", "materi": ["Yesus berbelaskasih", "Yesus pemenuhan janji Allah", "Wafat dan kebangkitan Yesus", "Peran Roh Kudus"]}],
            "Gereja": [{"cp": "Memahami gereja sebagai komunitas, karya pelayanan; sakramen inisiasi, tobat, dan perkawinan.", "materi": ["Gereja sebagai komunitas dan sakramen", "Sakramen Inisiasi", "Sakramen Perkawinan dan Imamat"]}],
            "Masyarakat": [{"cp": "Memahami kebebasan sebagai anak Allah, sabda bahagia; hak kewajiban gereja-masyarakat; keluhuran martabat manusia, peduli alam (Laudato Si), dialog umat beragama.", "materi": ["Kebebasan Anak Allah dan Sabda Bahagia", "Hak dan Kewajiban masyarakat gereja", "Menjaga alam dan Dialog antar umat"]}]
        },
        "Pendidikan Pancasila": {
            "Pancasila": [{"cp": "Memahami sejarah kelahiran Pancasila; kedudukan Pancasila sebagai dasar negara, pandangan hidup bangsa, ideologi negara; keterkaitan dengan UUD 1945, Bhinneka Tunggal Ika, dan NKRI.", "materi": ["Sejarah dan Kedudukan Pancasila", "Hubungan 4 Pilar Kebangsaan"]}],
            "Undang-Undang Dasar Negara Republik Indonesia Tahun 1945": [{"cp": "Menerapkan norma dan aturan; tata urutan perundang-undangan; hak dan kewajiban warga negara; sejarah dan fungsi UUD 1945; kemerdekaan berpendapat di era keterbukaan.", "materi": ["Hierarki perundang-undangan", "Kemerdekaan berpendapat dan hak/kewajiban"]}],
            "Bhinneka Tunggal Ika": [{"cp": "Mengidentifikasi keberagaman suku, agama, ras, antargolongan; menerima keberagaman; pelestarian tradisi, kearifan lokal dalam masyarakat global.", "materi": ["Keberagaman SARA", "Pelestarian tradisi dan kearifan lokal"]}],
            "Negara Kesatuan Republik Indonesia": [{"cp": "Memahami Proklamasi Kemerdekaan RI; wilayah NKRI dalam konteks wawasan nusantara; berpartisipasi menjaga keutuhan wilayah NKRI.", "materi": ["Wawasan Nusantara", "Menjaga keutuhan wilayah NKRI"]}]
        },
        "Bahasa Indonesia": {
            "Menyimak": [{"cp": "Menganalisis gagasan, pandangan, arahan, dan/atau pesan dari teks nonsastra berbentuk teks aural; dan menganalisis unsur intrinsik teks sastra berbentuk teks aural.", "materi": ["Analisis gagasan teks aural", "Unsur intrinsik sastra aural"]}],
            "Membaca dan Memirsa": [{"cp": "Menganalisis informasi dari berbagai tipe teks visual/audiovisual untuk makna tersurat/tersirat; menginterpretasi kepedulian atau pro/kontra; mengevaluasi kualitas dan kredibilitas teks visual/audiovisual.", "materi": ["Analisis dan evaluasi teks visual", "Menguji kredibilitas informasi"]}],
            "Berbicara dan Mempresentasikan": [{"cp": "Mempresentasikan gagasan, pandangan untuk tujuan pengajuan usul dan solusi dalam bentuk monolog, dialog logis secara kritis dan kreatif; menyajikan ungkapan kepedulian.", "materi": ["Presentasi solusi argumentatif", "Dialog dan diskusi kritis"]}],
            "Menulis": [{"cp": "Menulis gagasan, pandangan, pengalaman dalam berbagai tipe teks secara logis, kritis, kreatif; menulis ungkapan kepedulian pro/kontra; menggunakan kosakata bermakna denotatif, konotatif, dan kiasan.", "materi": ["Menulis esai argumentatif", "Kosakata denotatif, konotatif, kiasan"]}]
        },
        "Matematika": {
            "Bilangan": [{"cp": "Membaca, menulis, membandingkan bilangan bulat, rasional, desimal, berpangkat bulat dan akar, notasi ilmiah; operasi aritmatika real, estimasi finansial; rasio (skala, proporsi, laju perubahan).", "materi": ["Bilangan bulat dan rasional", "Bentuk pangkat, akar, notasi ilmiah", "Rasio dan literasi finansial"]}],
            "Aljabar": [{"cp": "Menggeneralisasi pola susunan benda/bilangan; bentuk aljabar ekuivalen; relasi dan fungsi (grafik, himpunan pasangan berurutan); persamaan dan pertidaksamaan linear satu variabel; sistem persaman linear dua variabel.", "materi": ["Bentuk dan Operasi Aljabar", "Fungsi linear dan grafik", "Sistem Persamaan Linear Dua Variabel (SPLDV)"]}],
            "Pengukuran": [{"cp": "Menentukan keliling, luas, panjang busur, sudut dan luas juring lingkaran; luas permukaan dan volume bangun ruang (prisma, tabung, bola, limas, kerucut); pengaruh perubahan proporsional.", "materi": ["Lingkaran dan garis singgung", "Bangun ruang sisi datar dan lengkung"]}],
            "Geometri": [{"cp": "Membuat jaring-jaring bangun ruang; hubungan antar-sudut, kekongruenan dan kesebangunan pada segitiga dan segiempat; teorema Pythagoras; transformasi tunggal (refleksi, translasi, rotasi, dilatasi) pada koordinat Kartesius.", "materi": ["Kesebangunan dan Kongruenan", "Teorema Pythagoras", "Transformasi Geometri"]}],
            "Analisis Data dan Peluang": [{"cp": "Mengumpulkan, menyajikan, dan menganalisis data diagram batang/lingkaran; rerata (mean), median, modus, dan jangkauan (range); peluang dan frekuensi relatif/harapan satu kejadian acak sederhana.", "materi": ["Statistika dasar (Mean, Median, Modus)", "Peluang kejadian sederhana"]}]
        },
        "Bahasa Inggris": {
            "Menyimak - Berbicara": [{"cp": "Memahami alur informasi, gagasan utama teks lisan tentang topik sehari-hari/minat; menggunakan bahasa Inggris mengungkapkan gagasan lisan dalam kalimat sederhana dan majemuk formal maupun informal.", "materi": ["Gagasan utama teks lisan", "Percakapan formal dan informal"]}],
            "Membaca - Memirsa": [{"cp": "Memahami alur informasi, informasi tersurat dan tersirat dari berbagai jenis teks tertulis atau teks multimodal tentang topik sehari-hari atau sesuai minat dan meresponnya.", "materi": ["Informasi tersirat dari teks visual/tulis"]}],
            "Menulis - Mempresentasikan": [{"cp": "Mengomunikasikan gagasan secara tertulis atau multimodal tentang topik sehari-hari dengan kalimat sederhana dan majemuk; mengungkapkan pendapat dan mempertahankan argumen tentang suatu isu.", "materi": ["Menulis teks opini", "Presentasi argumen dalam Bahasa Inggris"]}]
        },
        "Ilmu Pengetahuan Alam (IPA)": {
            "Pemahaman IPA": [{"cp": "Menelaah makhluk hidup dan klasifikasi; sistem organisasi kehidupan dan gangguan organ; interaksi ekosistem pencegahan perubahan iklim; pewarisan sifat; bioteknologi; aspek fisis gerak, gaya, tekanan, usaha energi, kalor, gelombang, kelistrikan, kemagnetan; sistem tata surya mitigasi perubahan iklim; menghindari zat aditif/adiktif.", "materi": ["Biologi: Klasifikasi, Sistem Organ, Genetika", "Fisika: Gerak, Gaya, Energi, Kelistrikan", "Kimia: Zat Aditif dan Adiktif"]}],
            "Keterampilan Proses": [{"cp": "Mengamati fenomena, mempertanyakan, merencanakan metode observasi alat ukur akurat, memproses data ke dalam tabel/grafik/model, mengevaluasi sumber ketidakpastian, dan mengomunikasikan dengan bahasa yang sesuai.", "materi": ["Penyelidikan kuantitatif dengan alat ukur presisi"]}]
        },
        "Ilmu Pengetahuan Sosial (IPS)": {
            "Pemahaman Konsep": [{"cp": "Menjelaskan keberagaman kondisi geografis, konektivitas keruangan, eksploitasi SDA dan perubahan iklim SDGs; kegiatan ekonomi, pasar, perdagangan internasional, pertumbuhan era digital; interaksi sosial masyarakat majemuk; konsep sejarah lokal nusantara dan jalur rempah.", "materi": ["Geografi SDA dan SDGs Iklim", "Ekonomi digital dan perdagangan", "Sosiologi masyarakat majemuk", "Sejarah lokal jalur rempah"]}],
            "Keterampilan Proses": [{"cp": "Menerapkan pendekatan proses (mengamati, menanya, mengumpulkan informasi, berkolaborasi mengolah data), menguji konsep melalui eksperimen/simulasi sosial, mengevaluasi dan merencanakan tindak lanjut berbasis projek.", "materi": ["Riset dan eksperimen masalah sosial terpadu"]}]
        },
        "Informatika": {
            "Berpikir Komputasional": [{"cp": "Menerapkan berpikir komputasional untuk problem sehari-hari; konsep himpunan data terstruktur; lembar kerja pengolah data; menyelesaikan persoalan dataset bervolume kecil; menulis pseudocode dengan sekumpulan kosakata terbatas.", "materi": ["Berpikir Komputasional Dasar", "Himpunan data dan Pseudocode"]}],
            "Literasi Digital": [{"cp": "Memahami mesin pencari internet, kredibilitas sumber, ekosistem pers digital; fakta vs hoaks; perangkat pengolah dokumen, lembar kerja, presentasi; arsitektur komputer jaringan; menjaga rekam jejak digital, keamanan kata sandi, malware, data pribadi.", "materi": ["Literasi dan Etika Digital", "Keamanan siber dasar", "Perangkat lunak perkantoran"]}]
        },
        "Seni Musik": {
            "Mengalami": [{"cp": "Mengenali dan menerapkan unsur-unsur musik berupa nada, irama, dan melodi, dengan alat musik berbasis teknologi yang sesuai dengan kondisi setempat serta mengidentifikasi karakteristik musik dari berbagai genre dan era.", "materi": ["Musik berbasis teknologi", "Karakteristik genre dan era"]}],
            "Merefleksikan": [{"cp": "Melakukan umpan balik kemampuan bermain musik, karya musik diri sendiri atau orang lain sesuai dengan genre menggunakan istilah musik yang tepat.", "materi": ["Analisis musikal genre spesifik"]}],
            "Berpikir dan Bekerja Artistik": [{"cp": "Menerapkan seluruh proses berpraktik musik untuk perbaikan keterampilan; menyajikan musik sederhana dari daerah setempat, Nusantara, dan karya musik modern Indonesia dengan interpretasi yang tepat.", "materi": ["Interpretasi musik Nusantara", "Penampilan musik Ansambel"]}],
            "Menciptakan": [{"cp": "Mengenali dan menghasilkan lagu sederhana dengan mengembangkan irama dan melodi menggunakan berbagai alat musik.", "materi": ["Komposisi lagu/musik sederhana"]}],
            "Berdampak": [{"cp": "Menunjukkan minat, empati, dan kepedulian terhadap isu-isu di lingkungan sekitar melalui kegiatan bermusik.", "materi": ["Musik untuk kepedulian sosial"]}]
        },
        "Seni Rupa": {
            "Mengalami": [{"cp": "Menganalisis unsur rupa dan prinsip desain dalam benda-benda di sekitar/karya seni rupa.", "materi": ["Analisis unsur dan prinsip seni rupa"]}],
            "Merefleksikan": [{"cp": "Merefleksikan dan mengapresiasi karya diri sendiri dan teman sekelas; membandingkan unsur rupa dan prinsip yang ada pada karya.", "materi": ["Apresiasi seni komparatif"]}],
            "Berpikir dan Bekerja Artistik": [{"cp": "Mengeksplorasi pembuatan rencana/konsep untuk berkarya seni rupa.", "materi": ["Konsep dan perencanaan karya (sketsa)"]}],
            "Menciptakan": [{"cp": "Membuat karya seni rupa dengan mengeksplorasi teknik penggunaan alat dan bahan yang tersedia berdasarkan pengalaman dan hasil pengamatannya.", "materi": ["Eksplorasi teknik dan medium (mixed media)"]}],
            "Berdampak": [{"cp": "Menghasilkan karya seni rupa yang memberikan inspirasi bagi diri sendiri dan/atau orang lain.", "materi": ["Pameran karya inspiratif"]}]
        },
        "Muatan Lokal (Opsional)": {
            "Muatan Lokal": [{"cp": "Capaian Pembelajaran disesuaikan dengan kebijakan satuan pendidikan tingkat SMP.", "materi": ["Materi Muatan Lokal"]}]
        }
    }
}
