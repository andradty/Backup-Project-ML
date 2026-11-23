# Product Requirements Document (PRD)

## Rice Leaf Disease Classification (Klasifikasi Penyakit Daun Padi)

| Informasi | Detail |
|---|---|
| Nama proyek | Rice Leaf Disease Classification (Deteksi & Klasifikasi Penyakit Daun Padi) |
| Jenis aplikasi | Web application / interactive ML computer vision dashboard |
| Framework aplikasi | Streamlit |
| Bahasa pemrograman | Python |
| Jenis Machine Learning | Supervised Learning, Multi-class Image Classification (4 Kelas) dengan Ekstraksi Fitur Citra (Color & GLCM Texture) |
| Dataset utama | Rice Leaf Disease Image Samples (`penyakit padi/` — Sethy et al., 2020 / Mendeley Data) |
| Versi | **1.1** |
| Tanggal | 23 November 2026 |
| Status | M1–M7 Selesai, siap masuk M8 (Finalisasi PPT, Video Demo, Pengumpulan) |

---

## 0. Changelog

| Versi | Tanggal | Perubahan |
|---|---|---|
| 1.0 | 4 Nov 2026 | Draft awal perencanaan proyek dan struktur PRD |
| 1.1 | 23 Nov 2026 (diperbarui setelah M2–M7 selesai) | Disesuaikan penuh dengan dataset citra `penyakit padi/` (5.932 citra, 4 kelas); hasil audit MD5 duplicate (1.138 duplikat persis) dan *augmentation leakage* (858 spesimen daun fisik) dimasukkan; strategi `StratifiedGroupKFold` ditetapkan; hasil evaluasi 3 algoritma (**SVM RBF**, **Random Forest**, **XGBoost**) dan tabel 5 jurnal studi literatur dilengkapi |

---

## 1. Progress Tracker dan Langkah Berikutnya

| Tahap | Status |
|---|---|
| M1 Perencanaan (judul, dataset, PRD) | ✅ Selesai (`PRD.md`) |
| M1 Studi literatur (5 jurnal + tabel) | ✅ Selesai (Bab 17 di `PRD.md`) |
| M2 Data Understanding | ✅ Selesai (`notebooks/01_data_understanding.ipynb`) |
| M3 EDA | ✅ Selesai (`notebooks/02_eda.ipynb`) |
| M4 Preprocessing, Ekstraksi Fitur & Group Split | ✅ Selesai (`notebooks/03_preprocessing.ipynb`) |
| M5 Modeling (3 algoritma, baseline Group-CV) | ✅ Selesai (`notebooks/04_model_training.ipynb`) |
| M6 Tuning, evaluasi, analisis, pemilihan model | ✅ Selesai (`notebooks/05_model_evaluation.ipynb`) |
| M7 Aplikasi Streamlit | ✅ Selesai (`app.py`, `pages/1_Model_Evaluation.py`, `pages/2_About_Project.py`) |
| M8 Finalisasi (PPT, video, repo, pengumpulan) | ⏭️ **Langkah berikutnya** |

**Langkah berikutnya (M8):** (1) jalankan aplikasi Streamlit (`streamlit run app.py`) dan ambil screenshot/rekaman layar, (2) susun PPT bagian A–O berdasarkan metrik dan grafik di `reports/figures/`, (3) rekam video demo ≤ 7 menit dengan aplikasi benar-benar berjalan, (4) rapikan repository dan folder pengumpulan `ML2026_Kelas_NamaKelompok_JudulProject`.

> Bagian ini diperbarui setiap kali satu tahap selesai.

---

## 2. Ringkasan Proyek

Aplikasi berbasis web interaktif yang mengklasifikasikan penyakit daun tanaman padi dari foto/citra daun ke dalam **4 kelas penyakit utama**: **Bacterial Blight** (Hawar Daun Bakteri), **Blast** (Blas), **Brown Spot** (Bercak Cokelat), dan **Tungro**. Pengguna cukup mengunggah foto daun padi (atau memilih contoh gambar nyata dari uji lapangan), lalu sistem secara otomatis melakukan validasi kualitas gambar, mengekstraksi **100 fitur visual terinterpretasi** (Histogram Warna HSV & RGB, Color Moments, Tekstur GLCM, Rasio Lesi Spesifik, dan Kepadatan Tepi Sobel), serta menampilkan kelas penyakit, tingkat keyakinan (*confidence score* %), profil diagnostik lesi, dan rekomendasi penanganan agronomis awal.

Tiga algoritma klasifikasi dibandingkan secara ketat: **Support Vector Machine (SVM RBF)**, **Random Forest**, dan **XGBoost**. Model final dipilih berdasarkan evaluasi *5-Fold StratifiedGroupKFold Cross-Validation* pada data latih dan diuji satu kali pada data uji (*hold-out test set*) yang bebas dari kebocoran spesimen daun (*zero specimen leakage*), dengan perhatian utama pada **F1-Macro**, **Recall Macro**, dan **ROC-AUC (One-vs-Rest)**.

Aplikasi ini adalah **prototipe edukasi dan sistem pendukung keputusan awal (*early screening*)** bagi petani, penyuluh pertanian, dan mahasiswa, bukan pengganti diagnosis laboratorium fitopatologi.

## 3. Latar Belakang dan Permasalahan

Tanaman padi (*Oryza sativa*) merupakan komoditas pangan utama di Indonesia dan Asia. Serangan penyakit daun seperti Hawar Daun Bakteri (*Bacterial Blight*), Blas (*Blast*), Bercak Cokelat (*Brown Spot*), dan *Tungro* sering menyebabkan penurunan produktivitas hingga gagal panen (*puso*) apabila terlambat dikenali. Identifikasi manual di lapangan mengandalkan pengamatan mata telanjang yang bersifat subjektif, memakan waktu, dan sering kali tertukar antar penyakit yang memiliki gejala bercak serupa (misalnya bercak memanjang pada *Bacterial Blight* vs bercak belah ketupat pada *Blast*).

Pertanyaan yang dijawab dalam proyek ini:
- Bagaimana membangun pipeline ekstraksi fitur citra (warna HSV/RGB, tekstur GLCM, dan rasio lesi) serta model klasifikasi penyakit daun padi 4 kelas tanpa *data leakage*?
- Bagaimana perbandingan performa **SVM (RBF)**, **Random Forest**, dan **XGBoost** pada dataset citra penyakit daun padi yang sama?
- Fitur visual apa (warna, tekstur GLCM, atau tepi lesi) yang paling berkontribusi dalam membedakan keempat penyakit daun padi?
- Bagaimana menyajikan hasil prediksi beserta rekomendasi agronomis melalui aplikasi Streamlit yang mudah dipakai oleh petani atau orang awam?

## 4. Tujuan

1. Memahami dan mengaudit kualitas dataset citra penyakit daun padi (`penyakit padi/`).
2. Melakukan Exploratory Data Analysis (EDA) visual dan statistik terhadap karakteristik warna serta tekstur bercak daun.
3. Mengekstraksi 100 fitur citra numerik dan membagi data secara ketat menggunakan *StratifiedGroupKFold* agar bebas dari duplikat MD5 maupun kebocoran rotasi spesimen (*augmentation leakage*).
4. Melatih dan membandingkan 3 algoritma klasifikasi (**SVM RBF**, **Random Forest**, **XGBoost**).
5. Mengevaluasi model secara adil, menganalisis *overfitting/underfitting*, dan memeriksa *confusion matrix* antar kelas penyakit.
6. Memilih model terbaik untuk diintegrasikan ke dalam aplikasi web Streamlit.
7. Menghasilkan aplikasi dengan antarmuka ramah pengguna, validasi citra otomatis, visualisasi distribusi probabilitas, dan batasan penggunaan (*disclaimer*).

## 5. Pengguna Sasaran

- **Mahasiswa dan dosen** yang menilai demonstrasi metodologi *Machine Learning* dan *Computer Vision*.
- **Petani, penyuluh pertanian lapangan (PPL), dan masyarakat awam** yang ingin melakukan simulasi deteksi awal penyakit daun padi dari foto.

Kebutuhan pengguna: tidak perlu memahami istilah teknis ekstraksi fitur GLCM/HSV, cukup unggah foto daun atau pilih sampel, lalu memperoleh nama penyakit dalam bahasa Indonesia, persentase keyakinan model, gejala utama, dan saran pengendalian awal.

## 6. Ruang Lingkup

**In scope:** audit citra & pendeteksian duplikat MD5 serta grup spesimen daun, EDA citra & fitur, ekstraksi 100 fitur (HSV, RGB, Color Moments, GLCM, Rasio Lesi, Sobel Edge), perbandingan 3 model (SVM, Random Forest, XGBoost), analisis kesalahan (*confusion matrix*), penyimpanan pipeline `.joblib`, aplikasi Streamlit 3 halaman, PPT, tabel 5 jurnal studi literatur, dan panduan video demo ≤ 7 menit.

**Out of scope:** deteksi daun sehat di luar 4 kelas dataset, pemantauan drone *real-time* di sawah, rekomendasi dosis pestisida kimia presisi tanpa pengamatan ahli, klaim kepastian mutlak 100% di segala kondisi pencahayaan ekstrem.

## 7. Dataset dan Data Understanding

### 7.1 Sumber Dataset

- **Nama Dataset:** Rice Leaf Disease Image Samples (Folder lokal: `penyakit padi/`)
- **Repositori Asli:** Mendeley Data — https://data.mendeley.com/datasets/fwcj7stb8r/1
- **Publikasi Ilmiah:** Sethy, P. K., Barpanda, N. K., Rath, A. K., & Behera, S. K. (2020). *Deep feature based rice leaf disease identification using support vector machine*. Computers and Electronics in Agriculture, 175, 105527. https://doi.org/10.1016/j.compag.2020.105527
- **Struktur Folder:** 4 subfolder kelas (`Bacterialblight`, `Blast`, `Brownspot`, `Tungro`), total **5.932 file citra** (`.jpg` / `.JPG`).

### 7.2 Hasil Audit Awal (Diverifikasi pada Folder `penyakit padi/`, 23 Nov 2026)

| Aspek | Temuan |
|---|---|
| Total file citra mentah | **5.932 citra** dalam 4 kelas |
| Distribusi kelas mentah | `Brownspot`: 1.600 (26,97%); `Bacterialblight`: 1.584 (26,70%); `Blast`: 1.440 (24,28%); `Tungro`: 1.308 (22,05%) |
| File rusak (*corrupt*) | **0 file** (seluruh 5.932 file valid dan dapat dibuka dengan PIL) |
| Mode warna (*color mode*) | **RGB**: 5.776 citra (97,37%); **RGBA** (4 kanal dengan alpha): 156 citra (2,63%) |
| Resolusi citra | **300×300 piksel**: 4.624 citra (77,95%); sisanya bervariasi (`295×221`, `499×332`, `221×295`, `521×348`, dll.) |
| Duplikat byte identik (MD5 Hash) | **1.138 citra duplikat (19,18%)** di dalam kelas yang sama; **0 duplikat lintas kelas** |
| Rincian duplikat MD5 per kelas | `Bacterialblight`: 258 duplikat; `Blast`: 480 duplikat; `Brownspot`: 400 duplikat; `Tungro`: 0 duplikat |
| Total citra unik (setelah dedup MD5) | **4.794 citra unik** (`Bacterialblight`: 1.326, `Tungro`: 1.308, `Brownspot`: 1.200, `Blast`: 960) |
| Spesimen daun fisik unik (*Leaf Group*) | **858 spesimen daun fisik** (`Bacterialblight`: 221, `Blast`: 160, `Brownspot`: 200, `Tungro`: 277) |

### 7.3 Temuan Kritis: Duplikat MD5 & *Augmentation Data Leakage*

Audit mendalam pada nama file dan isi byte mengungkap dua sumber potensi *data leakage*:
1. **Duplikat Identik (1.138 file):** Misalnya pada folder `Bacterialblight` terdapat penamaan ganda (`BACTERAILBLIGHT3_001.jpg` dan `BACTERIALBLIGHT1_001.jpg`, atau ekstensi `.jpg` vs `.JPG`) yang memiliki *MD5 hash* identik 100%.
2. **Rotasi/Flip dari Spesimen Daun Fisik yang Sama (*Augmentation Group*):** Dataset Mendeley ini dibuat dengan memotret **858 daun fisik unik**, lalu menerapkan 5 hingga 6 variasi augmentasi geometris (rotasi 90°, 180°, *flip* horizontal/vertikal) yang disimpan dengan nomor urut daun yang sama di akhir nama file (contoh: `BLAST1_045.jpg`, `BLAST2_045.jpg`, ..., `BLAST9_045.jpg` semuanya berasal dari daun Blast nomor `045`).
   - Karena fitur warna dan GLCM bersifat *rotation-invariant* (kebal terhadap rotasi), apabila kita melakukan *random split* biasa, rotasi dari daun `045` akan masuk ke *Train Set* dan *Test Set* sekaligus. Uji ablasi kami membuktikan bahwa *naive random split* menghasilkan akurasi semu **100,00%** (kebocoran data).
   - **Solusi Metodologis Kami:** Kami mengekstraksi `leaf_group` (kombinasi `kelas + nomor_spesimen_daun`) dan menggunakan **StratifiedGroupKFold (80:20)** sehingga seluruh variasi rotasi dari satu helai daun fisik yang sama **wajib berada di Train saja atau Test saja** (0 spesimen tumpang tindih antara Train dan Test).

### 7.4 Strategi Duplikat dan Pembagian Data (Terverifikasi di Notebook M2 & M4)

| Skenario Pembagian Data (Split 80:20, Random Forest) | Jumlah Citra | Test Accuracy | Test F1-Macro | Keterangan Metodologis |
|---|---|---|---|---|
| 1. Tanpa hapus duplikat (*Naive Random Split*) | 5.932 | 1,0000 (100%) | 1,0000 | **Leakage berat** (file identik masuk train & test) |
| 2. Hapus duplikat MD5, *Naive Random Split* | 4.794 | 1,0000 (100%) | 1,0000 | **Augmentation leakage** (rotasi daun yang sama bocor ke test) |
| 3. **Hapus duplikat MD5 + Group-Aware Split (`leaf_group`)** | **4.794 (858 daun)** | **0,9751 (97,51%)** | **0,9733** | **Bebas leakage (Dipakai sebagai standar utama proyek)** |

### 7.5 Hasil Baseline M5 (5-Fold StratifiedGroupKFold CV pada Data Train = 3.832 citra / 686 daun)

| Model | Accuracy | Precision (Macro) | Recall (Macro) | F1-Macro | ROC-AUC (OvR) | Waktu CV (s) |
|---|---|---|---|---|---|---|
| Dummy (Stratified) | 0,2523 | 0,2446 | 0,2453 | 0,2447 | 0,4974 | 0,55 s |
| **SVM (RBF Baseline, C=1.0)** | **0,9789** | **0,9775** | **0,9764** | **0,9769** | **0,9974** | 4,59 s |
| Random Forest (Baseline, depth=8) | 0,9609 | 0,9602 | 0,9562 | 0,9576 | 0,9976 | 3,01 s |
| XGBoost (Baseline, depth=4) | 0,9770 | 0,9761 | 0,9739 | 0,9749 | 0,9974 | 8,55 s |

### 7.6 Hasil Akhir M6 (Data Test Hold-Out = 962 Citra / 172 Spesimen Daun Unik, Dievaluasi Satu Kali)

Model dituning menggunakan *5-Fold StratifiedGroupKFold CV* pada data training (`X_train`). Setelah hyperparameter terbaik diperoleh, pipeline dilatih pada seluruh data training dan dievaluasi satu kali pada data uji (`X_test`).

| Model (Tuned) | CV F1-Macro | Test Accuracy | Test Precision (Macro) | Test Recall (Macro) | Test F1-Macro | Test ROC-AUC (OvR) | Ukuran File |
|---|---|---|---|---|---|---|---|
| **SVM (RBF, C=10, balanced) [FINAL]** | **0,9761** | **0,9875 (98,75%)** | **0,9853** | **0,9889** | **0,9867** | **1,0000** | **0,28 MB** |
| XGBoost (n=350, depth=5, lr=0,06) | 0,9716 | 0,9875 (98,75%) | 0,9894 | 0,9844 | 0,9865 | 0,9996 | 0,38 MB |
| Random Forest (n=300, depth=16) | 0,9540 | 0,9751 (97,51%) | 0,9733 | 0,9733 | 0,9733 | 0,9996 | 1,43 MB |

- **Model Final Terpilih:** **SVM (RBF)** berdasarkan aturan pemilihan objektif: **5-Fold Group-CV F1-Macro tertinggi di data train (0,9761)** serta **Test F1-Macro tertinggi (0,9867)** dan **Recall Macro tertinggi (0,9889)** dengan ukuran model paling ringan (**0,28 MB**). XGBoost mencapai akurasi uji yang setara (98,75%) dan juga disediakan sebagai opsi pembanding di aplikasi Streamlit.
- **Ringkasan Confusion Matrix pada Data Uji (962 citra):**
  - **SVM (RBF):** Benar 950/962 citra. Kelas `Brownspot` (240/240), `Tungro` (260/260), dan `Blast` (192/192) terklasifikasi sempurna 100%. Hanya 12 citra `Bacterialblight` (2 spesimen daun) yang diprediksi sebagai `Blast`.
  - **XGBoost:** Benar 950/962 citra. Kelas `Bacterialblight` (270/270), `Brownspot` (240/240), dan `Tungro` (260/260) sempurna 100%; hanya 12 citra `Blast` yang diprediksi sebagai `Bacterialblight`.
  - **Random Forest:** Benar 938/962 citra (12 `Bacterialblight` → `Blast`, dan 12 `Blast` → `Bacterialblight`).
- **Analisis Kesalahan Prediksi (*Error Analysis*):** Kesalahan hanya terjadi antara **Bacterial Blight vs Blast** karena pada tahap lanjut, kedua penyakit tersebut sama-sama meninggalkan lesi nekrotik memanjang berwarna pucat keabu-abuan di tepi/tengah daun. Sementara itu, `Tungro` (dominan kuning-oranye) dan `Brownspot` (bintik cokelat tua merata dengan kontras tekstur tinggi) dapat dipisahkan dengan akurasi 100%.
- **Pengaruh Fitur (*Feature Importance*):**
  1. `sobel_edge_p90` & `sobel_edge_std` (ketajaman dan sebaran tepi batas bercak luka pada daun)
  2. `center_lesion_ratio` (proporsi area bercak sakit pada bagian tengah helai daun)
  3. `glcm_correlation_std` & `glcm_correlation_mean` (pola keteraturan struktur tekstur permukaan daun dari matriks ko-okurensi GLCM)
  4. `ratio_white_pale_lesion` & `ratio_brown_necrotic` (proporsi bercak putih/abu-abu pucat khas *Blast/Blight* dan bercak cokelat nekrotik khas *Brownspot*)
  5. `moment_v_std` & `hsv_s_bin_01` (variasi kecerahan dan saturasi warna daun).

## 8. Input Aplikasi & Pipeline Ekstraksi Fitur

Berbeda dengan data tabular yang meminta pengguna mengetik angka manual, aplikasi *Computer Vision* ini menerima **1 input utama yang sangat mudah bagi pengguna awam**, yaitu **File Citra Daun Padi** (atau pilihan contoh gambar siap pakai):

| # | Komponen Input / Kontrol UI | Bentuk Input di Streamlit | Keterangan Pemrosesan Otomatis |
|---|---|---|---|
| 1 | **Citra Daun Padi** | `st.file_uploader` (`.jpg`, `.jpeg`, `.png`) atau **Galeri Contoh Cepat** (4 penyakit) | Dikonversi ke RGB (alpha RGBA dihapus di atas latar putih), di-resize ke `128×128` piksel |
| 2 | **Pilihan Algoritma Model** | Dropdown (`SVM (RBF) — Model Final`, `XGBoost`, `Random Forest`) | Memungkinkan pengguna membandingkan hasil prediksi antar model secara langsung |

Dari 1 citra `128×128` RGB tersebut, modul `src/preprocessing.py` secara otomatis mengekstraksi **100 fitur numerik**:
1. **HSV Color Histogram (32 fitur):** 16 bin *Hue*, 8 bin *Saturation*, 8 bin *Value* (ternormalisasi).
2. **RGB Color Histogram (24 fitur):** masing-masing 8 bin untuk kanal *Red*, *Green*, *Blue*.
3. **Color Moments (18 fitur):** *Mean*, *Standard Deviation*, dan *Skewness* untuk setiap kanal R, G, B, H, S, V.
4. **GLCM Texture Features (12 fitur):** *Contrast*, *Dissimilarity*, *Homogeneity*, *Energy*, *Correlation*, dan *ASM* yang dihitung pada matriks ko-okurensi tingkat keabuan (32 level, jarak $d \in \{1, 2\}$, sudut $\theta \in \{0^\circ, 45^\circ, 90^\circ, 135^\circ\}$), diringkas menjadi nilai rata-rata (*mean*) dan simpangan baku (*std*).
5. **Spatial Lesion Ratios & Edge Features (14 fitur):**
   - Rasio piksel hijau sehat (`ratio_healthy_green`)
   - Rasio kuning-oranye klorosis (`ratio_yellow_orange_tungro`)
   - Rasio bercak cokelat nekrotik (`ratio_brown_necrotic`)
   - Rasio lesi pucat keabu-abuan (`ratio_white_pale_lesion`)
   - Rasio latar belakang (`ratio_background_white_black`)
   - Indeks agronomi *Excess Green* (`exg_excess_green_mean`, `exg_excess_green_std`) & *Excess Red* (`exr_excess_red_mean`)
   - Rasio hijau dan lesi di area tengah daun (`center_green_ratio`, `center_lesion_ratio`)
   - Statistik gradien tepi *Sobel filter* (`sobel_edge_mean`, `sobel_edge_std`, `sobel_edge_p90`, `sobel_high_edge_ratio`).

## 9. Persyaratan Fungsional

| ID | Fitur | Deskripsi | Prioritas |
|---|---|---|---|
| FR-01 | Unggah & Pilih Contoh Citra | Pengguna dapat mengunggah foto daun padi (`.jpg/.png`) atau memilih sampel nyata dari 4 kelas | Must |
| FR-02 | Validasi Citra Otomatis | Menolak file rusak, resolusi terlalu kecil (< 32×32 px), atau gambar kosong/polos satu warna | Must |
| FR-03 | Ekstraksi Fitur & Prediksi | Mengekstraksi 100 fitur citra dan menjalankan pipeline `StandardScaler` + Classifier tersimpan | Must |
| FR-04 | Hasil Klasifikasi 4 Kelas | Menampilkan nama penyakit (Bahasa Indonesia & Inggris) beserta lencana warna dan ikon | Must |
| FR-05 | Distribusi Probabilitas | Menampilkan persentase keyakinan (*confidence score*) untuk keempat kelas penyakit | Must |
| FR-06 | Penjelasan Agronomis & Disclaimer | Menampilkan penyebab patogen, gejala visual, dampak, saran pengendalian, dan *disclaimer* | Must |
| FR-07 | Diagnostik Visual Daun | Menampilkan profil rasio warna daun (hijau sehat, kuning/oranye, cokelat nekrotik, kontras GLCM) | Should |
| FR-08 | Dashboard Evaluasi Model | Menampilkan ringkasan audit dataset, perbandingan 3 model, *confusion matrix*, dan *feature importance* | Should |
| FR-09 | Pemilih Model & Reset | Pengguna dapat mengganti model (SVM / XGBoost / Random Forest) dan mereset pilihan | Could |

## 10. Persyaratan Non-Fungsional

- **Usability:** antarmuka berbahasa Indonesia yang jelas bagi petani/penyuluh maupun akademisi.
- **Performance:** ekstraksi fitur + prediksi 1 gambar selesai dalam waktu **< 0,2 detik**.
- **Reliability:** fungsi `extract_features_from_image()` di `src/preprocessing.py` dipakai bersama oleh skrip training dan aplikasi Streamlit sehingga dijamin 100% konsisten.
- **Reproducibility:** `random_state=42` dikunci pada seluruh pembagian data dan pelatihan model.
- **Maintainability:** kode dipisah secara modular di dalam paket `src/` (`data_loader.py`, `preprocessing.py`, `train.py`, `evaluate.py`, `predict.py`).
- **Transparency:** keterbatasan dataset (hanya 4 kelas penyakit tanpa kelas daun sehat) dicantumkan secara jujur pada halaman utama dan halaman About.

## 11. Rencana & Metodologi Machine Learning

### 11.1 Pembagian Data Bebas Leakage
1. Audit seluruh 5.932 file menggunakan *MD5 hash* dan hapus **1.138 duplikat identik** sebelum pembagian data (tersisa **4.794 citra unik**).
2. Identifikasi grup spesimen daun fisik (`leaf_group`, total **858 daun unik**).
3. Bagi data 80:20 menggunakan **StratifiedGroupKFold (`n_splits=5, random_state=42`)** sehingga menghasilkan **3.832 citra latih (686 daun)** dan **962 citra uji (172 daun)** tanpa tumpang tindih spesimen.

### 11.2 Preprocessing & Pipeline
1. Penanganan mode warna RGBA (156 citra) dengan komposisi di atas latar belakang putih menjadi RGB 3 kanal.
2. Penyeragaman dimensi citra (*resizing*) ke `128×128` piksel dengan interpolasi bilinear.
3. Ekstraksi 100 fitur numerik (warna, tekstur GLCM, rasio lesi, gradien tepi Sobel).
4. Standarisasi fitur (`StandardScaler`) yang dibungkus bersama classifier di dalam `sklearn.pipeline.Pipeline` agar parameter *mean* dan *std* hanya dipelajari dari data latih.

### 11.3 Algoritma yang Dibandingkan

| Model | Peran | Hyperparameter Akhir (Hasil Tuning Group-CV) |
|---|---|---|
| **SVM (RBF)** | Classifier margin non-linear (Model Final) | `C=10.0, kernel='rbf', gamma='scale', class_weight='balanced'` |
| **Random Forest** | Ensemble *bagging* pohon keputusan | `n_estimators=300, max_depth=16, min_samples_split=4, min_samples_leaf=2, class_weight='balanced_subsample'` |
| **XGBoost** | Ensemble *gradient boosting* | `n_estimators=350, max_depth=5, learning_rate=0.06, subsample=0.85, colsample_bytree=0.80, reg_lambda=2.0` |

## 12. Antarmuka Streamlit

1. **Beranda / Deteksi Penyakit (`app.py`):** Hero banner bergaya *AgriTech*, panduan 3 langkah pemakaian, pemilih skenario contoh daun siap pakai (4 penyakit) atau unggah foto sendiri, kartu hasil diagnosis lengkap dengan grafik batang probabilitas 4 kelas, metrik profil bercak daun, rekomendasi penanganan pertanian, dan *disclaimer*.
2. **Evaluasi & Perbandingan Model (`pages/1_Model_Evaluation.py`):** Ringkasan audit 5.932 citra & ablasi duplikat/grup, tabel perbandingan Baseline (M5) vs Tuned (M6), grafik perbandingan metrik, *confusion matrix* ketiga model, analisis *feature importance*, serta rincian metrik per kelas penyakit.
3. **Tentang Proyek (`pages/2_About_Project.py`):** Latar belakang masalah pertanian, ensiklopedia 4 penyakit daun padi, penjelasan metodologi ekstraksi 100 fitur citra & *StratifiedGroupKFold*, tabel studi literatur 5 jurnal, batasan etika, dan pembagian tugas tim.

## 13. Arsitektur Teknis & Struktur Direktori

```text
Projek_3rd/
├── app.py                              # Halaman utama Streamlit (Deteksi & Diagnosis)
├── pages/
│   ├── 1_Model_Evaluation.py           # Halaman dashboard evaluasi & perbandingan 3 model
│   └── 2_About_Project.py              # Halaman penjelasan proyek, metodologi & studi literatur
├── penyakit padi/                      # Dataset citra asli (5.932 citra dalam 4 subfolder kelas)
├── data/
│   └── processed/                      # Hasil audit MD5 & fitur citra (metadata_audit.csv, features_unique.csv, train/test)
├── models/                             # Pipeline tersimpan (final_model.joblib, svm_pipeline.joblib, rf_pipeline.joblib, xgboost_pipeline.joblib)
├── notebooks/
│   ├── 01_data_understanding.ipynb     # M2: Audit dataset, resolusi, mode RGBA, & deteksi duplikat MD5
│   ├── 02_eda.ipynb                    # M3: Visualisasi sampel citra, distribusi warna HSV, & tekstur GLCM
│   ├── 03_preprocessing.ipynb          # M4: Ekstraksi 100 fitur, ablasi leakage, & StratifiedGroupKFold split
│   ├── 04_model_training.ipynb         # M5: Pelatihan baseline 3 algoritma dengan 5-Fold Group-CV
│   └── 05_model_evaluation.ipynb       # M6: Hyperparameter tuning, evaluasi test set, confusion matrix & feature importance
├── src/
│   ├── __init__.py                     # Konstanta path & kamus informasi agronomis 4 penyakit
│   ├── data_loader.py                  # Pemindaian folder citra, MD5 hash, & ekstraksi ID spesimen daun
│   ├── preprocessing.py                # Validasi citra & ekstraksi 100 fitur (HSV, RGB, Moments, GLCM, Lesion, Sobel)
│   ├── train.py                        # Pipeline training, ablasi duplikat, Group-CV, & penyimpanan model
│   ├── evaluate.py                     # Generator 7 grafik publikasi berkualitas tinggi di reports/figures/
│   └── predict.py                      # Modul inferensi cepat untuk aplikasi Streamlit
├── reports/
│   ├── evaluation_summary.json         # Ringkasan lengkap seluruh metrik eksperimen M2-M6
│   ├── model_comparison.csv            # Tabel perbandingan metrik 3 algoritma
│   ├── feature_importance.csv          # Peringkat 100 fitur citra berdasarkan RF & XGBoost
│   ├── test_predictions.csv            # Hasil prediksi lengkap pada 962 citra data uji
│   └── figures/                        # 7 visualisasi PNG untuk notebook, laporan, PPT & Streamlit
├── requirements.txt
├── README.md
└── PRD.md
```

## 14. Pembagian Tugas

| Peran | Tanggung Jawab | Hasil (*Deliverables*) |
|---|---|---|
| **Anggota 1 (Data & Computer Vision)** | Audit 5.932 citra, deteksi duplikat MD5 & grup spesimen, EDA visual, ekstraksi 100 fitur warna & tekstur GLCM | `01_data_understanding.ipynb`, `02_eda.ipynb`, `03_preprocessing.ipynb`, `src/data_loader.py`, `src/preprocessing.py` |
| **Anggota 2 (Machine Learning)** | Baseline Group-CV, tuning SVM/RF/XGBoost, evaluasi *hold-out test set*, analisis *confusion matrix* & *feature importance* | `04_model_training.ipynb`, `05_model_evaluation.ipynb`, `src/train.py`, `src/evaluate.py`, `models/*.joblib` |
| **Anggota 3 (Aplikasi & Dokumentasi)** | Antarmuka Streamlit 3 halaman, integrasi pipeline inferensi, validasi gambar, README, PRD, & materi PPT | `app.py`, `pages/*.py`, `src/predict.py`, `README.md`, `PRD.md` |

## 15. Milestone

| Tahap | Aktivitas | Kriteria Selesai | Status |
|---|---|---|---|
| M1 | Judul, studi literatur, dataset | PRD & 5 jurnal referensi | ✅ Selesai |
| M2 | Data understanding | Audit 5.932 citra, resolusi, mode RGBA, 1.138 duplikat MD5 | ✅ Selesai |
| M3 | EDA | Grid sampel 4 kelas, boxplot fitur warna/GLCM, korelasi fitur | ✅ Selesai |
| M4 | Preprocessing & split | Ekstraksi 100 fitur & `StratifiedGroupKFold` 80:20 tanpa leakage | ✅ Selesai |
| M5 | Modeling | Baseline 3 model (SVM, RF, XGBoost) + Dummy pada 5-Fold Group-CV | ✅ Selesai |
| M6 | Evaluasi | Tuning, tabel perbandingan data uji (98,75%), analisis kesalahan & model final | ✅ Selesai |
| M7 | Aplikasi | Aplikasi Streamlit berjalan dengan upload gambar & skenario siap pakai | ✅ Selesai |
| M8 | Finalisasi | PPT bagian A–O, video demo ≤ 7 menit, pengumpulan repo | ⏭️ Siap dikerjakan |

## 16. Kriteria Penerimaan (*Acceptance Criteria*)

**Data dan Eksperimen**
- [x] Sumber dan publikasi dataset dicatat (Sethy et al., 2020 — Mendeley Data, 5.932 citra)
- [x] Arti 4 kelas target dan 100 fitur warna/tekstur dijelaskan
- [x] EDA lengkap (distribusi kelas sebelum/sesudah dedup, grid citra, boxplot fitur, korelasi)
- [x] Preprocessing beralasan dan tanpa *data leakage* (konversi RGBA, resize 128×128, `StandardScaler` di dalam `Pipeline`)
- [x] Strategi duplikat MD5 (1.138 file) dan grup spesimen daun (858 daun) didokumentasikan beserta uji ablasinya
- [x] Train/test dipisah dengan benar (`StratifiedGroupKFold` 80:20: 3.832 train / 962 test)
- [x] 3 algoritma (**SVM RBF**, **Random Forest**, **XGBoost**) dilatih dan dibandingkan
- [x] Metrik dihitung dari pengujian nyata pada 962 citra uji
- [x] Analisis *overfitting/underfitting* dan kesalahan prediksi (*Bacterial Blight* vs *Blast*)
- [x] Model final (**SVM RBF**) dipilih berdasarkan evaluasi CV F1-Macro dan tujuan masalah

**Aplikasi Streamlit**
- [x] Berjalan lancar lewat Streamlit (`app.py` + 2 halaman di `pages/`)
- [x] Mendukung unggah gambar dan tombol skenario contoh, dilengkapi validasi citra (FR-02)
- [x] Memakai pipeline dan fungsi ekstraksi fitur yang identik dengan eksperimen
- [x] Menampilkan kelas penyakit, distribusi probabilitas 4 kelas, diagnostik lesi, rekomendasi penanganan, dan *disclaimer*
- [x] Dapat dijalankan ulang dengan mudah lewat `README.md` dan `requirements.txt`

## 17. Tabel Studi Literatur (5 Jurnal Referensi)

| No. | Penulis & Tahun | Permasalahan | Dataset | Metode / Algoritma | Metrik Evaluasi | Hasil Utama | Perbedaan dengan Proyek Kami |
|---|---|---|---|---|---|---|---|
| 1 | **Sethy et al. (2020)** — *Computers and Electronics in Agriculture* | Identifikasi 4 penyakit daun padi di lapangan untuk membantu diagnosis cepat petani | **5.932 citra daun padi** (Bacterial Blight, Blast, Brown Spot, Tungro) — *dataset yang sama dengan proyek ini* | Ekstraksi fitur CNN (13 arsitektur pre-trained seperti ResNet50) + klasifikasi **SVM** | Accuracy, F1-Score, Sensitivity, Specificity | Kombinasi fitur ResNet50 + SVM menghasilkan F1-Score tertinggi sebesar **98,38%** | Sethy et al. memakai ekstraksi fitur *deep learning* (ResNet50) yang berat (membutuhkan GPU) dan belum memisahkan duplikat/grup spesimen secara eksplisit; proyek kami menggunakan **100 fitur warna HSV/RGB + tekstur GLCM + Sobel** yang ringan di CPU dengan pembagian `StratifiedGroupKFold` bebas leakage dan mencapai F1-Macro **98,67%** |
| 2 | **Prajapati et al. (2017)** — *ICIIECS (IEEE)* | Deteksi dan klasifikasi 3 penyakit daun padi (Bacterial Leaf Blight, Brown Spot, Leaf Smut) | 120 citra daun padi dengan latar belakang putih dari lahan pertanian di India | Segmentasi K-Means clustering + ekstraksi **88 fitur warna, bentuk, dan tekstur (GLCM)** + **SVM** | Accuracy (Train/Test split & 5-Fold CV) | SVM mencapai akurasi **93,33%** pada data uji dan **83,80%** pada 5-Fold CV | Dataset Prajapati et al. sangat kecil (120 citra, 3 kelas); proyek kami menguji pada **4.794 citra unik (4 kelas termasuk Tungro)** dan membandingkan 3 algoritma (**SVM, Random Forest, XGBoost**) sekaligus membangun aplikasi Streamlit interaktif |
| 3 | **Azim et al. (2021)** — *Agronomy (MDPI)* | Klasifikasi penyakit daun padi secara efisien tanpa ketergantungan perangkat keras GPU mahal | Dataset UCI / Kaggle Rice Leaf Diseases (3 kelas: Bacterial Blight, Brown Spot, Leaf Smut) | Segmentasi saturasi warna + ekstraksi fitur **GLCM, warna HSV, dan bentuk** + **XGBoost** & Decision Tree | Accuracy, Precision, Recall, F1-Score | Algoritma **XGBoost** mengungguli metode lain dengan akurasi **86,58%** | Azim et al. hanya mencakup 3 kelas (tanpa *Blast* dan *Tungro*); proyek kami mencakup 4 penyakit utama termasuk *Blast* dan *Tungro*, menambahkan fitur rasio klorosis & gradien Sobel, serta mencapai akurasi **98,75%** pada XGBoost & SVM |
| 4 | **Pothen & Pai (2020)** — *Fourth International Conference on I-SMAC (IEEE)* | Klasifikasi penyakit daun padi berbasis ekstraksi fitur tekstur dan deskriptor lokal | Citra daun padi 3 kelas (Bacterial Leaf Blight, Brown Spot, Leaf Smut) | Ekstraksi fitur **HOG (Histogram of Oriented Gradients) + LBP / GLCM** dengan klasifikasi **SVM** (Polynomial & RBF kernel) | Accuracy, Precision, Recall | SVM mencapai akurasi **94,6%** dalam membedakan ketiga penyakit daun padi | Pothen & Pai berfokus pada fitur tekstur keabuan (HOG/LBP) sehingga kurang peka terhadap gejala perubahan warna khas seperti kuning-oranye pada *Tungro*; proyek kami menggabungkan spektrum warna HSV/RGB + rasio klorosis + GLCM sehingga kelas *Tungro* dan *Brownspot* terdeteksi 100% |
| 5 | **Haruna et al. (2023)** — *Indonesian Journal of Electrical Engineering and Computer Science* | Evaluasi komparatif algoritma *machine learning* untuk deteksi penyakit daun padi dari fitur citra | Dataset Mendeley Rice Leaf Disease (4 kelas: Bacterial Blight, Blast, Brown Spot, Tungro) | Ekstraksi fitur warna dan tekstur + perbandingan **Random Forest, SVM, dan KNN** | Accuracy, Precision, Recall, F1-Score, Confusion Matrix | Random Forest dan SVM menunjukkan performa tinggi (>95%) dalam memisahkan keempat kelas penyakit | Studi sebelumnya umumnya melakukan *random split* langsung pada 5.932 citra tanpa menghapus 1.138 duplikat MD5 dan tanpa pengelompokan spesimen daun; proyek kami mendokumentasikan analisis ablasi duplikat & *group-aware split* serta menyediakan dashboard Streamlit lengkap |

## 18. Risiko dan Mitigasi

| Risiko | Mitigasi |
|---|---|
| **Duplikat file (1.138 citra) & rotasi spesimen daun yang sama memperbesar skor secara semu (*leakage*)** | Hapus seluruh duplikat MD5 sebelum split, ekstrak ID spesimen `leaf_group`, dan gunakan `StratifiedGroupKFold` (80:20) serta laporkan perbandingan skor sebelum vs sesudah |
| **Citra dengan mode RGBA (4 kanal) menyebabkan error dimensi array** | Konversi seluruh citra RGBA ke RGB 3 kanal di atas latar putih secara otomatis pada `load_and_preprocess_image()` |
| **Pengguna mengunggah gambar rusak, terlalu kecil, atau gambar kosong** | Terapkan fungsi validasi `validate_uploaded_image()` (FR-02) yang memeriksa keterbacaan file, resolusi minimal 32×32 px, dan simpangan baku piksel |
| **Inkonsistensi ekstraksi fitur antara training dan aplikasi Streamlit** | Gunakan satu fungsi terpusat `extract_features_from_image()` di `src/preprocessing.py` dan bungkus `StandardScaler` + model di dalam satu file `.joblib` |
| **Kemiripan visual bercak lanjut antara *Bacterial Blight* dan *Blast*** | Tampilkan distribusi probabilitas seluruh kelas beserta profil diagnostik lesi dan catatan kehati-hatian (*disclaimer*) agar pengguna memeriksa gejala lapangan |

## 19. Batasan dan Etika

- **Cakupan Kelas Terbatas (Closed-Set Classification):** Model dilatih khusus pada 4 jenis penyakit daun padi (*Bacterial Blight, Blast, Brown Spot, Tungro*). Model **tidak memiliki kelas "Daun Sehat"** maupun kelas objek bukan daun padi; setiap gambar yang diunggah akan dipetakan ke salah satu dari 4 kelas yang paling mirip secara statistik warna/tekstur.
- **Pengaruh Pencahayaan dan Latar Belakang:** Foto yang diambil di bawah bayangan gelap, pantulan sinar matahari ekstrem, atau latar belakang tanah/tangan yang dominan dapat memengaruhi histogram warna dan rasio lesi.
- **Alat Bantu Edukasi & Skrining Awal:** Hasil prediksi dan saran pengendalian di aplikasi ini bertujuan untuk edukasi dan deteksi dini, **bukan** dasar tunggal untuk aplikasi pestisida skala besar tanpa konfirmasi petugas penyuluh pertanian (PPL) atau laboratorium proteksi tanaman.

## 20. Keputusan Metodologis yang Telah Divalidasi

| # | Keputusan | Status & Hasil Validasi |
|---|---|---|
| 1 | Kecukupan 100 fitur warna + GLCM + Sobel | ✅ Tervalidasi pada 5-Fold Group-CV: ketiganya menghasilkan F1-Macro 0,954–0,976 tanpa memerlukan GPU/CNN berat |
| 2 | Penanganan 156 citra RGBA & variasi resolusi | ✅ Dikonversi ke RGB latar putih dan di-resize ke `128×128` bilinear |
| 3 | Penanganan 1.138 duplikat MD5 & 858 grup spesimen | ✅ Duplikat dihapus sebelum split; pembagian data wajib menggunakan `StratifiedGroupKFold` berdasarkan `leaf_group` |
| 4 | Pemilihan model final | ✅ **SVM (RBF)** dipilih karena meraih Group-CV F1-Macro tertinggi (0,9761), Test F1-Macro tertinggi (0,9867), dan ukuran model paling kecil (0,28 MB); XGBoost & Random Forest juga disimpan dan dapat diuji di aplikasi |

## 21. Deliverables

1. **Model Terlatih (`.joblib`):** `models/final_model.joblib`, `models/svm_pipeline.joblib`, `models/xgboost_pipeline.joblib`, `models/rf_pipeline.joblib`.
2. **Aplikasi Streamlit Interaktif:** `app.py`, `pages/1_Model_Evaluation.py`, `pages/2_About_Project.py`.
3. **Kode Sumber Modular:** Paket `src/` (`data_loader.py`, `preprocessing.py`, `train.py`, `evaluate.py`, `predict.py`).
4. **5 Jupyter Notebooks Lengkap (M2–M6):** `notebooks/01_data_understanding.ipynb` s/d `05_model_evaluation.ipynb` (lengkap dengan output eksekusi dan grafik).
5. **Laporan & Visualisasi:** `reports/evaluation_summary.json`, `reports/model_comparison.csv`, `reports/feature_importance.csv`, dan 7 grafik PNG di `reports/figures/`.
6. **Dokumentasi Proyek:** `PRD.md` (termasuk 5 jurnal studi literatur), `README.md`, `requirements.txt`.

## 22. Referensi

1. Sethy, P. K., Barpanda, N. K., Rath, A. K., & Behera, S. K. (2020). Deep feature based rice leaf disease identification using support vector machine. *Computers and Electronics in Agriculture*, 175, 105527. https://doi.org/10.1016/j.compag.2020.105527
2. Sethy, P. K. (2020). *Rice Leaf Disease Image Samples*. Mendeley Data, V1. https://doi.org/10.17632/fwcj7stb8r.1
3. Prajapati, H. B., Shah, J. P., & Dabhi, V. K. (2017). Detection and classification of rice plant diseases. *Intelligent Decision Technologies*, 11(3), 357–373. https://doi.org/10.3233/IDT-170301
4. Azim, M. A., Islam, M. K., Rahman, M. M., & Jahan, F. (2021). An effective feature extraction method for rice leaf disease classification. *Agronomy*, 11(3), 467. https://doi.org/10.3390/agronomy11030467
5. Pothen, M. E., & Pai, M. L. (2020). Detection of rice leaf diseases using image processing. *2020 Fourth International Conference on I-SMAC (IoT in Social, Mobile, Analytics and Cloud)*, 424–430. https://doi.org/10.1109/I-SMAC49090.2020.9243600
6. Haruna, Y., Qin, S., & Mbyamm Kiki, M. J. (2023). An improved approach to detection of rice leaf disease with machine learning. *Indonesian Journal of Electrical Engineering and Computer Science*, 30(1), 426–434.
