"""Streamlit Page 2: About Project, Methodology, Literature Review & Limitations."""

import streamlit as st
from src import CLASS_INFO
from src.ui_icons import inject_css, section_header

st.set_page_config(
    page_title="Tentang Proyek — PadiGuard",
    layout="wide",
)

inject_css()

section_header("book", "Tentang Proyek: Klasifikasi Penyakit Daun Padi")
st.markdown(
    """
    **PadiGuard** adalah prototipe aplikasi berbasis web dan *Computer Vision* yang dirancang untuk membantu identifikasi dini
    4 penyakit utama pada daun tanaman padi (*Oryza sativa*) menggunakan ekstraksi **100 fitur warna & tekstur citra** serta perbandingan
    3 algoritma *Supervised Machine Learning* (**SVM RBF**, **Random Forest**, dan **XGBoost**).
    """
)

st.divider()

section_header("leaf", "1. Mengenal 4 Penyakit Utama Daun Padi pada Dataset")
cols = st.columns(2)
for idx, (cls_key, info) in enumerate(CLASS_INFO.items()):
    with cols[idx % 2]:
        with st.container(border=True):
            st.markdown(f"#### {info['nama_id']} (`{cls_key}`)")
            st.markdown(f"- **Patogen Penyebab:** {info['penyebab']}")
            st.markdown(f"- **Gejala Visual:** {info['gejala']}")
            st.markdown(f"- **Dampak Pertanian:** {info['dampak']}")
            st.markdown(f"- **Penanganan Awal:** {info['penanganan']}")

st.divider()

section_header("cpu", "2. Sumber Dataset & Arsitektur Metodologi")
c1, c2 = st.columns(2)
with c1:
    st.markdown(
        """
        **Sumber Dataset Ilmiah:**
        - **Nama Dataset:** *Rice Leaf Disease Image Samples* (`penyakit padi/`)
        - **Penulis & Publikasi:** Sethy, P. K., Barpanda, N. K., Rath, A. K., & Behera, S. K. (2020), *Computers and Electronics in Agriculture*, 175, 105527.
        - **Repositori:** [Mendeley Data (DOI: 10.17632/fwcj7stb8r.1)](https://data.mendeley.com/datasets/fwcj7stb8r/1)
        - **Komposisi:** 5.932 citra mentah → **4.794 citra unik** (setelah pembersihan 1.138 duplikat MD5) yang berasal dari **858 spesimen daun fisik**.
        """
    )
with c2:
    st.markdown(
        """
        **Alur Pipeline Machine Learning:**
        1. **Normalisasi Citra:** Konversi `RGBA` → `RGB` latar putih & resize ke `128×128` piksel.
        2. **Ekstraksi 100 Fitur Visual:**
           - Histogram Warna HSV (32 fitur) & RGB (24 fitur)
           - Color Moments Mean, Std, Skewness (18 fitur)
           - Tekstur GLCM Contrast, Dissimilarity, Homogeneity, Energy, Correlation, ASM (12 fitur)
           - Rasio Lesi Spesifik & Gradien Tepi Sobel (14 fitur)
        3. **Group-Aware Split:** `StratifiedGroupKFold` 80:20 berdasarkan ID spesimen daun (`leaf_group`).
        4. **Pemodelan:** `StandardScaler` + Classifier (`SVM RBF`, `Random Forest`, `XGBoost`).
        """
    )

st.divider()

section_header("layers", "3. Tabel Studi Literatur (5 Jurnal Referensi)")
st.markdown(
    """
    | No. | Penulis & Tahun | Permasalahan | Dataset | Metode / Algoritma | Metrik Evaluasi | Hasil Utama | Perbedaan dengan Proyek Kami |
    |---|---|---|---|---|---|---|---|
    | **1** | **Sethy et al. (2020)** — *Computers and Electronics in Agriculture* | Identifikasi 4 penyakit daun padi di lapangan | **5.932 citra daun padi** (4 kelas, dataset yang sama) | Fitur CNN (ResNet50) + **SVM** | Accuracy, F1-Score | ResNet50 + SVM mencapai F1-Score **98,38%** | Sethy et al. memakai fitur CNN berat (butuh GPU) tanpa dedup/group split; proyek kami memakai **100 fitur warna HSV/RGB + GLCM + Sobel** yang cepat di CPU dengan `StratifiedGroupKFold` bebas leakage (F1-Macro **98,67%**) |
    | **2** | **Prajapati et al. (2017)** — *Intelligent Decision Technologies* | Deteksi 3 penyakit daun padi (BLB, Brown Spot, Leaf Smut) | 120 citra daun padi berlatar putih | Segmentasi K-Means + **88 fitur warna, bentuk, GLCM** + **SVM** | Accuracy & 5-Fold CV | Akurasi uji **93,33%** (5-Fold CV **83,80%**) | Dataset Prajapati et al. hanya 120 citra (3 kelas); proyek kami mengevaluasi **4.794 citra unik (4 kelas termasuk Tungro & Blast)** pada 3 algoritma |
    | **3** | **Azim et al. (2021)** — *Agronomy (MDPI)* | Klasifikasi penyakit daun padi hemat komputasi | Dataset UCI Rice Leaf Diseases (3 kelas) | Fitur **GLCM + Warna HSV** + **XGBoost** | Accuracy, Precision, Recall, F1 | **XGBoost** mencapai akurasi **86,58%** | Azim et al. hanya menguji 3 kelas; proyek kami menambahkan fitur rasio klorosis & Sobel pada 4 kelas dan mencapai akurasi **98,75%** pada XGBoost & SVM |
    | **4** | **Pothen & Pai (2020)** — *IEEE I-SMAC* | Klasifikasi penyakit daun padi berbasis tekstur | Citra daun padi 3 kelas | Fitur **HOG + LBP/GLCM** + **SVM** | Accuracy, Precision, Recall | SVM mencapai akurasi **94,6%** | Pothen & Pai hanya mengandalkan tekstur keabuan; proyek kami memadukan spektrum warna HSV/RGB + GLCM sehingga penyakit klorosis seperti *Tungro* terdeteksi 100% |
    | **5** | **Haruna et al. (2023)** — *IJEECS* | Perbandingan algoritma ML pada penyakit daun padi | Mendeley Rice Leaf Disease (4 kelas) | Fitur warna & tekstur + **Random Forest, SVM, KNN** | Accuracy, F1, Confusion Matrix | RF & SVM mencapai akurasi >95% | Studi terdahulu memakai *random split* langsung tanpa mengaudit 1.138 duplikat MD5 dan grup spesimen; proyek kami menyertakan studi ablasi leakage & aplikasi Streamlit lengkap |
    """
)

st.divider()

section_header("alert", "4. Batasan Sistem, Etika & Disclaimer Penggunaan")
st.warning(
    """
    1. **Klasifikasi Tertutup 4 Kelas (Closed-Set Classification):** Model ini dilatih khusus pada 4 kelas penyakit (*Bacterial Blight, Blast, Brown Spot, Tungro*) sesuai isi dataset Mendeley dan **tidak memiliki kelas 'Daun Sehat'** atau penolak objek non-daun. Gambar apa pun yang lolos validasi resolusi akan diklasifikasikan ke salah satu dari 4 penyakit yang paling mendekati profil warna dan teksturnya.
    2. **Sensitivitas Pencahayaan:** Warna bercak daun dapat dipengaruhi oleh bayangan ekstrem, pantulan cahaya matahari langsung, atau latar belakang yang terlalu ramai.
    3. **Bukan Pengganti Diagnosis Laboratorium:** Aplikasi ini merupakan prototipe akademik dan alat bantu skrining awal (*decision support*). Keputusan penyemprotan fungisida/bakterisida atau eradikasi tanaman di lapangan wajib dikonsultasikan terlebih dahulu dengan **Penyuluh Pertanian Lapangan (PPL)** atau petugas POPT (Pengendali Organisme Pengganggu Tumbuhan).
    """
)
