# 🌾 PadiGuard AI — Sistem Cerdas Deteksi & Klasifikasi Penyakit Daun Padi

**PadiGuard AI** adalah aplikasi web interaktif berbasis **Streamlit** dan *Computer Vision / Machine Learning* yang dirancang untuk membantu identifikasi dini serta diagnosis visual **4 penyakit utama pada daun tanaman padi** (*Oryza sativa*).

Aplikasi ini menganalisis citra daun padi secara otomatis melalui ekstraksi **100 fitur visual citra** — meliputi *Histogram Warna HSV & RGB*, *Color Moments*, *Tekstur GLCM (Gray-Level Co-occurrence Matrix)*, *Rasio Area Lesi & Klorosis*, serta *Gradien Tepi Sobel* — untuk memberikan hasil diagnosis penyakit beserta informasi agronomis dan rekomendasi penanganan awal secara *real-time*.

---

## ✨ Fitur Utama Aplikasi Web PadiGuard AI

1. **🔍 Pemindai & Deteksi Daun Padi Interaktif (*Real-Time Scanner*)**
   - Mendukung unggah foto daun padi (`JPG`, `JPEG`, `PNG`) maupun pengujian instan menggunakan **sampel citra uji** dari 4 kelas penyakit.
   - Menampilkan hasil diagnosis penyakit utama beserta **tingkat keyakinan (*Confidence Score*)** dan grafik distribusi probabilitas untuk seluruh kelas penyakit.
   - Dilengkapi pilihan **3 model *Machine Learning*** (*SVM RBF*, *XGBoost*, dan *Random Forest*) yang dapat diganti langsung dari antarmuka web.

2. **🌿 Informasi Agronomis & Rekomendasi Penanganan**
   - Setiap hasil deteksi dilengkapi rincian **Patogen Penyebab**, **Karakteristik Gejala Visual**, **Dampak Pertanian**, serta **Saran Penanganan Awal** untuk membantu pengambilan keputusan skrining di lapangan.

3. **📊 Dashboard Evaluasi & Transparansi Model**
   - Menyajikan visualisasi interaktif performa algoritma, perbandingan metrik antar-model, *Confusion Matrix*, analisis fitur visual terpenting (*Feature Importance*), serta studi literatur dan metodologi sistem.

---

## 🦠 4 Penyakit Daun Padi yang Dideteksi

| Kelas Penyakit | Nama Indonesia | Patogen Penyebab | Karakteristik Gejala Visual Utama |
|---|---|---|---|
| **`Bacterialblight`** | Hawar Daun Bakteri (Kresek) | Bakteri *Xanthomonas oryzae* pv. *oryzae* | Garis lesi basah kekuningan hingga putih keabu-abuan memanjang di sepanjang tepi/ujung helai daun. |
| **`Blast`** | Penyakit Blas | Jamur *Pyricularia oryzae* (*Magnaporthe oryzae*) | Bercak berbentuk belah ketupat (*diamond/spindle-shaped*) dengan bagian tengah abu-abu keputihan dan tepi cokelat tua. |
| **`Brownspot`** | Bercak Cokelat | Jamur *Bipolaris oryzae* (*Cochliobolus miyabeanus*) | Bercak oval atau bulat kecil berwarna cokelat tua hingga kemerahan dengan lingkaran halo kuning di sekelilingnya. |
| **`Tungro`** | Penyakit Virus Tungro | *Rice Tungro Bacilliform Virus (RTBV)* & *Spherical Virus (RTSV)* | Perubahan warna daun (*klorosis*) menjadi kuning-oranye cerah mulai dari ujung daun disertai bercak karat kecil. |

---

## 🛠️ Teknologi yang Digunakan

- **Antarmuka Web (Frontend & UI):** Streamlit, Custom CSS & SVG Animations
- **Pemrosesan Citra (Computer Vision):** Pillow (PIL), NumPy, Scikit-Image (GLCM & Sobel Filter)
- **Machine Learning:** Scikit-Learn (SVM RBF, Random Forest), XGBoost, Joblib
- **Visualisasi Data:** Matplotlib, Seaborn, Pandas

---
