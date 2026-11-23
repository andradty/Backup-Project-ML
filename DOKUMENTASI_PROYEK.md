# 📌 Dokumentasi Teknis & Panduan Proyek — PadiGuard AI

Dokumen ini memuat catatan teknis mulai dari **Ringkasan Proyek & Hasil Eksperimen**, **Struktur Direktori**, hingga **Cara Menjalankan Aplikasi & Eksperimen** untuk proyek **PadiGuard AI**.

---

## 📌 Ringkasan Proyek & Hasil Eksperimen

- **Dataset:** *Rice Leaf Disease Image Samples* (`penyakit padi/` — Sethy et al., 2020 / Mendeley Data)
- **4 Kelas Penyakit:**
  1. `Bacterialblight` — Hawar Daun Bakteri (*Xanthomonas oryzae*)
  2. `Blast` — Penyakit Blas (*Pyricularia oryzae*)
  3. `Brownspot` — Bercak Cokelat (*Bipolaris oryzae*)
  4. `Tungro` — Virus Tungro (*RTBV & RTSV*)
- **Audit Kualitas Data & Pencegahan Data Leakage:**
  - Total citra mentah: **5.932 citra** (0 file rusak, 5.776 RGB, 156 RGBA).
  - Ditemukan dan dihapus **1.138 duplikat identik (MD5 Hash — 19,18%)** → tersisa **4.794 citra unik**.
  - Ditemukan bahwa 4.794 citra tersebut berasal dari **858 spesimen daun fisik** yang mengalami rotasi/flip. Untuk mencegah *augmentation data leakage*, pembagian Train/Test (80:20) dilakukan dengan **StratifiedGroupKFold** berdasarkan `leaf_group` (**3.832 citra latih [686 daun]** dan **962 citra uji [172 daun]**).

### 🏆 Tabel Perbandingan 3 Algoritma pada Hold-Out Test Set (962 Citra / 172 Daun Unik)

| Algoritma Model | 5-Fold Group-CV F1 (Train) | Test Accuracy | Test Precision (Macro) | Test Recall (Macro) | Test F1-Macro | Test ROC-AUC (OvR) | Ukuran File |
|---|---|---|---|---|---|---|---|
| **SVM (RBF, C=10, balanced) [Model Final]** | **0,9761** | **98,75% (0,9875)** | **0,9853** | **0,9889** | **0,9867** | **1,0000** | **0,28 MB** |
| **XGBoost** (n=350, depth=5, lr=0,06) | 0,9716 | **98,75% (0,9875)** | 0,9894 | 0,9844 | 0,9865 | 0,9996 | 0,38 MB |
| **Random Forest** (n=300, depth=16) | 0,9540 | 97,51% (0,9751) | 0,9733 | 0,9733 | 0,9733 | 0,9996 | 1,43 MB |

---

## 🗂️ Struktur Direktori

```text
Backup-Project-ML/
├── app.py                              # Halaman utama Streamlit (Deteksi & Diagnosis Citra Daun)
├── pages/
│   ├── 1_Model_Evaluation.py           # Dashboard evaluasi model, confusion matrix & feature importance
│   └── 2_About_Project.py              # Penjelasan penyakit, metodologi, 5 jurnal literatur & disclaimer
├── penyakit padi/                      # Dataset citra asli (5.932 citra dalam 4 subfolder kelas)
├── data/
│   └── processed/                      # Hasil audit MD5 & ekstraksi 100 fitur (metadata_audit.csv, features_unique.csv, train/test)
├── models/                             # Pipeline tersimpan (final_model.joblib, svm_pipeline.joblib, xgboost_pipeline.joblib, rf_pipeline.joblib)
├── notebooks/
│   ├── 01_data_understanding.ipynb     # M2: Audit dataset, resolusi, mode RGBA & duplikat MD5
│   ├── 02_eda.ipynb                    # M3: Visualisasi sampel citra, distribusi warna HSV & tekstur GLCM
│   ├── 03_preprocessing.ipynb          # M4: Ekstraksi 100 fitur, uji ablasi leakage & StratifiedGroupKFold
│   ├── 04_model_training.ipynb         # M5: Pelatihan baseline 3 algoritma dengan 5-Fold Group-CV
│   └── 05_model_evaluation.ipynb       # M6: Hyperparameter tuning, evaluasi test set & pemilihan model final
├── src/
│   ├── __init__.py                     # Konstanta path & informasi agronomis 4 penyakit daun padi
│   ├── data_loader.py                  # Pemindaian folder citra, MD5 hash & ekstraksi ID spesimen daun
│   ├── preprocessing.py                # Validasi citra & ekstraksi 100 fitur (HSV, RGB, Moments, GLCM, Lesion, Sobel)
│   ├── train.py                        # Pipeline training, ablasi duplikat, Group-CV & penyimpanan model
│   ├── evaluate.py                     # Pembuatan 7 visualisasi PNG di reports/figures/
│   └── predict.py                      # Modul inferensi untuk aplikasi Streamlit
├── reports/
│   ├── evaluation_summary.json         # Ringkasan lengkap seluruh metrik eksperimen
│   ├── model_comparison.csv            # Tabel perbandingan metrik 3 algoritma
│   ├── feature_importance.csv          # Peringkat 100 fitur citra
│   ├── test_predictions.csv            # Hasil prediksi pada 962 citra data uji
│   └── figures/                        # 7 visualisasi PNG (distribusi kelas, sampel, boxplot, korelasi, perbandingan, CM, feature importance)
├── PRD.md                              # Product Requirements Document (Versi 1.1 lengkap dengan 5 jurnal studi literatur)
├── DOKUMENTASI_PROYEK.md               # Catatan eksperimen, struktur direktori & panduan instalasi/menjalankan aplikasi
├── requirements.txt
└── README.md                           # Profil & penjelasan utama aplikasi web PadiGuard AI
```

---

## 🚀 Cara Menjalankan Aplikasi & Eksperimen

### 1. Persiapan Environment
Pastikan Anda menggunakan Python (misalnya dari Anaconda) dan telah memasang dependensi pada `requirements.txt`:

```powershell
pip install -r requirements.txt
```

### 2. Menjalankan Aplikasi Web Streamlit
Dari direktori proyek, jalankan perintah berikut:

```powershell
# Jika menggunakan Anaconda di D:\Anaconda:
D:\Anaconda\Scripts\streamlit.exe run app.py

# Atau jika python sudah ada di PATH:
python -m streamlit run app.py
```

Aplikasi akan terbuka otomatis di browser pada alamat `http://localhost:8501`.

### 3. Menjalankan Ulang Pipeline Training & Visualisasi (Opsional)
Seluruh model (`.joblib`), fitur (`.csv`), dan grafik (`.png`) sudah tersedia dan siap pakai. Jika ingin melatih ulang dari awal:

```powershell
D:\Anaconda\python.exe -m src.train
D:\Anaconda\python.exe -m src.evaluate
```
