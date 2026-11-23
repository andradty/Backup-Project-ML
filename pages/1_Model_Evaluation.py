"""Streamlit Page 1: Model Evaluation & Dataset Audit Dashboard."""

import json
import pandas as pd
import streamlit as st

from src import CLASSES, FIGURES_DIR, REPORTS_DIR
from src.ui_icons import inject_css, section_header

st.set_page_config(
    page_title="Evaluasi Model — PadiGuard",
    layout="wide",
)

inject_css()

section_header("chart", "Evaluasi Model, Audit Dataset & Analisis Fitur")
st.markdown(
    "Halaman ini menyajikan hasil eksperimen nyata dari tahap **M2 (Data Understanding)** hingga **M6 (Evaluasi & Pemilihan Model Final)** pada dataset citra penyakit daun padi."
)

with open(REPORTS_DIR / "evaluation_summary.json", "r", encoding="utf-8") as f:
    summary = json.load(f)

ds = summary["dataset_summary"]
sp = summary["split_info"]
ab = summary["duplicate_ablation"]

# Top KPI Cards
k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Total Citra Mentah", f"{ds['total_files']:,}", "4 Kelas Penyakit")
k2.metric("Duplikat MD5 Dihapus", f"{ds['duplicate_count']:,}", f"-{ds['duplicate_pct']}% file identik")
k3.metric("Citra Unik Bersih", f"{ds['unique_count']:,}", f"{ds['unique_leaf_specimens']} spesimen daun")
k4.metric("Data Latih / Uji (80:20)", f"{sp['train_size']:,} / {sp['test_size']:,}", "StratifiedGroupKFold")
k5.metric("Akurasi Uji Terbaik", f"{summary['test_results']['SVM (RBF)']['accuracy']*100:.2f}%", "SVM (RBF) & XGBoost")

st.divider()

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "1. Perbandingan 3 Model (M5 & M6)",
        "2. Confusion Matrix & Error Analysis",
        "3. Feature Importance & EDA Visual",
        "4. Audit Duplikat & Pencegahan Leakage",
    ]
)

with tab1:
    section_header("layers", "Perbandingan Performa 3 Algoritma pada Hold-Out Test Set (962 Citra Unik / 172 Daun)")
    st.markdown(
        """
        Seluruh model dilatih menggunakan `Pipeline(StandardScaler + Classifier)` pada data latih (`3.832` citra dari `686` spesimen daun)
        dan dituning dengan **5-Fold StratifiedGroupKFold Cross-Validation**. Evaluasi di bawah ini dilakukan **satu kali** pada data uji (`962` citra dari `172` spesimen daun) yang belum pernah dilihat selama training.
        """
    )

    df_comp = pd.read_csv(REPORTS_DIR / "model_comparison.csv")
    display_df = df_comp[
        [
            "model",
            "cv_f1_macro",
            "accuracy",
            "precision_macro",
            "recall_macro",
            "f1_macro",
            "roc_auc_ovr",
            "train_f1_macro",
            "model_size_mb",
        ]
    ].rename(
        columns={
            "model": "Algoritma Model",
            "cv_f1_macro": "5-Fold Group-CV F1 (Train)",
            "accuracy": "Test Accuracy",
            "precision_macro": "Test Precision (Macro)",
            "recall_macro": "Test Recall (Macro)",
            "f1_macro": "Test F1-Score (Macro)",
            "roc_auc_ovr": "Test ROC-AUC (OvR)",
            "train_f1_macro": "Train F1-Macro",
            "model_size_mb": "Ukuran File (MB)",
        }
    )
    st.dataframe(display_df, use_container_width=True, hide_index=True)

    fig_comp = FIGURES_DIR / "05_model_comparison.png"
    if fig_comp.exists():
        st.image(str(fig_comp), caption="Perbandingan Metrik Evaluasi 3 Algoritma pada Data Uji", use_container_width=True)

    st.markdown("#### Hasil Baseline M5 (5-Fold StratifiedGroupKFold CV Sebelum Tuning)")
    df_base = pd.DataFrame(summary["baseline_cv_results"]).T.reset_index().rename(columns={"index": "Model Baseline"})
    st.dataframe(df_base, use_container_width=True, hide_index=True)

    st.success(
        "Alasan Pemilihan Model Final: SVM (RBF) dipilih sebagai model final utama karena memperoleh skor 5-Fold Group-CV F1-Macro tertinggi pada data latih (0,9761) serta menghasilkan Test Accuracy 98,75%, Test F1-Macro 0,9867, Recall Macro tertinggi (0,9889), dan ukuran file paling ringan (0,28 MB). XGBoost juga mencapai akurasi uji 98,75% (F1-Macro 0,9865) dan tersedia untuk dipilih pengguna di halaman utama."
    )

with tab2:
    section_header("grid", "Confusion Matrix & Analisis Kesalahan Prediksi pada Data Uji (962 Citra)")
    fig_cm = FIGURES_DIR / "06_confusion_matrices.png"
    if fig_cm.exists():
        st.image(str(fig_cm), caption="Confusion Matrix SVM (RBF), Random Forest, dan XGBoost pada Hold-Out Test Set", use_container_width=True)

    c_left, c_right = st.columns(2)
    with c_left:
        st.markdown("##### Rincian Metrik Per Kelas Penyakit — SVM (RBF) [Model Final]")
        rep_svm = summary["per_class_reports"]["SVM (RBF)"]
        rows_cls = []
        for c in CLASSES:
            rows_cls.append(
                {
                    "Kelas Penyakit": c,
                    "Precision": round(rep_svm[c]["precision"], 4),
                    "Recall": round(rep_svm[c]["recall"], 4),
                    "F1-Score": round(rep_svm[c]["f1-score"], 4),
                    "Jumlah Sampel Uji": int(rep_svm[c]["support"]),
                }
            )
        st.dataframe(pd.DataFrame(rows_cls), use_container_width=True, hide_index=True)

    with c_right:
        st.markdown("##### Analisis Overfitting & Kesalahan Prediksi (Error Analysis)")
        st.markdown(
            """
            - **Brownspot (240/240) & Tungro (260/260) Terklasifikasi 100% Sempurna:** Ketiga model mampu memisahkan *Brownspot* (bercak cokelat nekrotik dengan kontras GLCM tinggi) dan *Tungro* (perubahan warna kuning-oranye klorosis) tanpa satu pun kesalahan.
            - **Letak Kesalahan Minor (Bacterial Blight vs Blast):** Dari 962 citra uji, SVM dan XGBoost hanya salah pada **12 citra (2 spesimen daun fisik, atau 1,25%)** antara kelas `Bacterialblight` dan `Blast`. Hal ini terjadi karena lesi lanjut pada kedua penyakit tersebut sama-sama meninggalkan area pucat keabu-abuan mengering di helai daun.
            - **Evaluasi Overfitting:** Selisih antara F1-Macro pada data latih (`1,0000`) dan data uji (`0,9867`) hanya sebesar **`0,0133` (1,33%)**, menunjukkan generalisasi yang sangat kuat pada spesimen daun baru.
            """
        )

with tab3:
    section_header("sliders", "Pengaruh Fitur Citra (Feature Importance) & Visualisasi EDA")
    fig_imp = FIGURES_DIR / "07_feature_importance.png"
    if fig_imp.exists():
        st.image(str(fig_imp), caption="15 Fitur Citra Paling Berpengaruh (XGBoost & Random Forest)", use_container_width=True)

    st.markdown(
        """
        **Interpretasi Fitur Terpenting:**
        1. **`sobel_edge_p90` & `sobel_edge_std`:** Mengukur ketajaman dan variasi gradien tepi bercak luka pada permukaan daun.
        2. **`center_lesion_ratio`:** Proporsi area bercak penyakit pada bagian tengah helai daun.
        3. **`glcm_correlation_std` & `glcm_correlation_mean`:** Mengukur konsistensi pola tekstur keabuan permukaan daun dari matriks ko-okurensi GLCM.
        4. **`ratio_white_pale_lesion` & `ratio_brown_necrotic`:** Membedakan bercak putih/abu-abu pucat khas *Blast/Bacterial Blight* dari bercak cokelat tua khas *Brown Spot*.
        """
    )

    st.divider()
    st.markdown("#### Visualisasi Exploratory Data Analysis (M3)")
    g1, g2 = st.columns(2)
    with g1:
        if (FIGURES_DIR / "02_sample_images_grid.png").exists():
            st.image(str(FIGURES_DIR / "02_sample_images_grid.png"), caption="Contoh Citra per Kelas Penyakit (128x128 RGB)", use_container_width=True)
    with g2:
        if (FIGURES_DIR / "04_correlation_heatmap.png").exists():
            st.image(str(FIGURES_DIR / "04_correlation_heatmap.png"), caption="Matriks Korelasi Fitur Warna, GLCM, dan Rasio Lesi", use_container_width=True)

    if (FIGURES_DIR / "03_feature_distributions.png").exists():
        st.image(str(FIGURES_DIR / "03_feature_distributions.png"), caption="Boxplot Distribusi 6 Fitur Kunci Antar Kelas Penyakit", use_container_width=True)

with tab4:
    section_header("shield", "Audit Duplikat MD5 & Pencegahan Augmentation Data Leakage (M2 & M4)")
    if (FIGURES_DIR / "01_class_distribution.png").exists():
        st.image(str(FIGURES_DIR / "01_class_distribution.png"), caption="Distribusi Kelas Sebelum vs Sesudah Deduplikasi MD5", use_container_width=True)

    st.markdown("#### Tabel Uji Ablasi Strategi Pembagian Data (Random Forest 80:20)")
    ab_df = pd.DataFrame(
        [
            {
                "Skenario Pembagian Data": "1. Tanpa Hapus Duplikat (Naive Random Split)",
                "Jumlah Citra": ab["with_duplicates_total"],
                "Test Accuracy": f"{ab['with_duplicates_test_acc']*100:.2f}%",
                "Test F1-Macro": f"{ab['with_duplicates_test_f1']:.4f}",
                "Status Metodologi": "Leakage Berat (1.138 file identik bocor lintas train-test)",
            },
            {
                "Skenario Pembagian Data": "2. Hapus Duplikat MD5, tetapi Naive Random Split",
                "Jumlah Citra": ab["naive_dedup_total"],
                "Test Accuracy": f"{ab['naive_dedup_test_acc']*100:.2f}%",
                "Test F1-Macro": f"{ab['naive_dedup_test_f1']:.4f}",
                "Status Metodologi": "Augmentation Leakage (rotasi dari daun fisik yang sama bocor ke test)",
            },
            {
                "Skenario Pembagian Data": "3. Hapus Duplikat MD5 + StratifiedGroupKFold (by leaf_group)",
                "Jumlah Citra": ab["group_aware_total"],
                "Test Accuracy": f"{ab['group_aware_test_acc']*100:.2f}%",
                "Test F1-Macro": f"{ab['group_aware_test_f1']:.4f}",
                "Status Metodologi": "Bebas Leakage (Standar Utama Proyek — 0 spesimen daun tumpang tindih)",
            },
        ]
    )
    st.dataframe(ab_df, use_container_width=True, hide_index=True)
