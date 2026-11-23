"""Generate all publication-quality visualizations for EDA and Model Evaluation."""

import json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from PIL import Image

from src import CLASSES, DATA_PROCESSED_DIR, FIGURES_DIR, REPORTS_DIR
from src.preprocessing import load_and_preprocess_image


def generate_all_figures():
    """Generate and save all charts for notebooks, reports, and the Streamlit dashboard."""
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    sns.set_theme(style="whitegrid", palette="muted")
    plt.rcParams["font.sans-serif"] = "DejaVu Sans"
    plt.rcParams["axes.edgecolor"] = "#cccccc"

    df_meta = pd.read_csv(DATA_PROCESSED_DIR / "metadata_audit.csv")
    df_unique = pd.read_csv(DATA_PROCESSED_DIR / "features_unique.csv")
    with open(REPORTS_DIR / "evaluation_summary.json", "r", encoding="utf-8") as f:
        eval_summary = json.load(f)

    # 1. Class distribution (Before vs After Deduplication)
    fig, ax = plt.subplots(figsize=(9, 5), dpi=150)
    raw_counts = [eval_summary["dataset_summary"]["per_class_raw"].get(c, 0) for c in CLASSES]
    uniq_counts = [eval_summary["dataset_summary"]["per_class_unique"].get(c, 0) for c in CLASSES]
    x = np.arange(len(CLASSES))
    width = 0.36
    b1 = ax.bar(x - width / 2, raw_counts, width, label="Sebelum Deduplikasi (Total: 5.932)", color="#94a3b8")
    b2 = ax.bar(x + width / 2, uniq_counts, width, label="Sesudah Deduplikasi MD5 (Unik: 4.794)", color="#16a34a")
    ax.set_xticks(x)
    ax.set_xticklabels(CLASSES, fontsize=11, fontweight="bold")
    ax.set_ylabel("Jumlah Citra Daun Padi", fontsize=11)
    ax.set_title("Distribusi Kelas Penyakit Daun Padi (Sebelum vs Sesudah Hapus Duplikat)", fontsize=13, fontweight="bold", pad=12)
    ax.legend(frameon=True, fontsize=10)
    for bar in b1:
        ax.annotate(f"{int(bar.get_height())}", (bar.get_x() + bar.get_width() / 2, bar.get_height()),
                    ha="center", va="bottom", fontsize=9, color="#475569", xytext=(0, 3), textcoords="offset points")
    for bar in b2:
        ax.annotate(f"{int(bar.get_height())}", (bar.get_x() + bar.get_width() / 2, bar.get_height()),
                    ha="center", va="bottom", fontsize=9.5, fontweight="bold", color="#15803d", xytext=(0, 3), textcoords="offset points")
    ax.set_ylim(0, max(raw_counts) * 1.15)
    plt.tight_layout()
    fig.savefig(FIGURES_DIR / "01_class_distribution.png")
    plt.close(fig)

    # 2. Sample Grid (4 classes x 4 samples)
    fig, axes = plt.subplots(4, 4, figsize=(10, 10), dpi=150)
    for row_idx, cls_name in enumerate(CLASSES):
        sub = df_unique[df_unique["class_name"] == cls_name].head(4)
        for col_idx, (_, row) in enumerate(sub.iterrows()):
            ax = axes[row_idx, col_idx]
            arr = load_and_preprocess_image(row["filepath"], target_size=(128, 128))
            ax.imshow(arr)
            ax.set_xticks([])
            ax.set_yticks([])
            if col_idx == 0:
                ax.set_ylabel(cls_name, fontsize=11, fontweight="bold", labelpad=8)
            ax.set_title(row["filename"][:18], fontsize=8, color="#334155")
    plt.suptitle("Contoh Citra Daun Padi per Kelas Penyakit (Resized 128x128 RGB)", fontsize=14, fontweight="bold", y=0.98)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    fig.savefig(FIGURES_DIR / "02_sample_images_grid.png")
    plt.close(fig)

    # 3. EDA Feature Boxplots across 4 classes
    key_feats = [
        ("ratio_healthy_green", "Rasio Piksel Hijau Sehat"),
        ("ratio_yellow_orange_tungro", "Rasio Piksel Kuning/Oranye (Indikator Tungro)"),
        ("ratio_brown_necrotic", "Rasio Bercak Cokelat Nekrotik"),
        ("glcm_contrast_mean", "Kontras Tekstur GLCM (Kasarnya Bercak)"),
        ("moment_h_mean", "Rata-rata Hue (Spektrum Warna)"),
        ("sobel_edge_mean", "Kepadatan Tepi Lesi (Sobel Edge)"),
    ]
    fig, axes = plt.subplots(2, 3, figsize=(14, 8), dpi=150)
    palette = ["#d97706", "#dc2626", "#92400e", "#16a34a"]
    for idx, (col, title) in enumerate(key_feats):
        ax = axes[idx // 3, idx % 3]
        sns.boxplot(
            data=df_unique,
            x="class_name",
            y=col,
            hue="class_name",
            order=CLASSES,
            palette=palette,
            legend=False,
            ax=ax,
            fliersize=2,
        )
        ax.set_title(title, fontsize=10.5, fontweight="bold")
        ax.set_xlabel("")
        ax.set_ylabel(col, fontsize=9)
        ax.tick_params(axis="x", rotation=15)
    plt.suptitle("Distribusi Fitur Warna & Tekstur GLCM Utama per Kelas Penyakit", fontsize=14, fontweight="bold", y=0.99)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    fig.savefig(FIGURES_DIR / "03_feature_distributions.png")
    plt.close(fig)

    # 4. Correlation Heatmap of Key Interpretable Features
    corr_cols = [
        "moment_r_mean", "moment_g_mean", "moment_b_mean",
        "moment_h_mean", "moment_s_mean", "moment_v_mean",
        "glcm_contrast_mean", "glcm_homogeneity_mean", "glcm_energy_mean", "glcm_correlation_mean",
        "ratio_healthy_green", "ratio_yellow_orange_tungro", "ratio_brown_necrotic",
        "ratio_white_pale_lesion", "exg_excess_green_mean", "sobel_edge_mean"
    ]
    fig, ax = plt.subplots(figsize=(11, 9), dpi=150)
    corr_matrix = df_unique[corr_cols].corr()
    sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="RdBu_r", center=0, ax=ax, annot_kws={"size": 7.5})
    ax.set_title("Matriks Korelasi Antar Fitur Utama (Warna, GLCM, dan Rasio Lesi)", fontsize=13, fontweight="bold", pad=12)
    plt.tight_layout()
    fig.savefig(FIGURES_DIR / "04_correlation_heatmap.png")
    plt.close(fig)

    # 5. Model Comparison Bar Chart (Test Accuracy, Precision, Recall, F1-Macro, ROC-AUC)
    test_res = eval_summary["test_results"]
    models = list(test_res.keys())
    metrics_to_plot = ["accuracy", "precision_macro", "recall_macro", "f1_macro", "roc_auc_ovr"]
    metric_labels = ["Accuracy", "Precision (Macro)", "Recall (Macro)", "F1-Score (Macro)", "ROC-AUC (OvR)"]

    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=150)
    x = np.arange(len(metrics_to_plot))
    width = 0.25
    colors = ["#2563eb", "#16a34a", "#ea580c"]
    for i, m_name in enumerate(models):
        vals = [test_res[m_name][k] for k in metrics_to_plot]
        bars = ax.bar(x + (i - 1) * width, vals, width, label=m_name, color=colors[i % len(colors)])
        for bar in bars:
            ax.annotate(
                f"{bar.get_height():.3f}",
                (bar.get_x() + bar.get_width() / 2, bar.get_height()),
                ha="center", va="bottom", fontsize=8.5, fontweight="bold", xytext=(0, 3), textcoords="offset points"
            )
    ax.set_xticks(x)
    ax.set_xticklabels(metric_labels, fontsize=10.5, fontweight="bold")
    ax.set_ylim(0.75, 1.04)
    ax.set_ylabel("Skor Evaluasi pada Data Uji (Test Set)", fontsize=11)
    ax.set_title("Perbandingan Performa 3 Algoritma Klasifikasi pada Data Uji (959 Citra Unik)", fontsize=13, fontweight="bold", pad=12)
    ax.legend(frameon=True, fontsize=10.5, loc="lower right")
    plt.tight_layout()
    fig.savefig(FIGURES_DIR / "05_model_comparison.png")
    plt.close(fig)

    # 6. Confusion Matrices for all 3 models side-by-side
    fig, axes = plt.subplots(1, 3, figsize=(16, 4.8), dpi=150)
    cmaps = ["Blues", "Greens", "Oranges"]
    for idx, m_name in enumerate(models):
        ax = axes[idx]
        cm = np.array(eval_summary["confusion_matrices"][m_name])
        sns.heatmap(
            cm,
            annot=True,
            fmt="d",
            cmap=cmaps[idx],
            xticklabels=CLASSES,
            yticklabels=CLASSES,
            cbar=False,
            ax=ax,
            annot_kws={"size": 11, "weight": "bold"},
        )
        acc_val = test_res[m_name]["accuracy"]
        f1_val = test_res[m_name]["f1_macro"]
        ax.set_title(f"{m_name}\nAcc: {acc_val*100:.2f}% | F1: {f1_val:.4f}", fontsize=11.5, fontweight="bold")
        ax.set_xlabel("Prediksi Model", fontsize=10)
        ax.set_ylabel("Kelas Sebenarnya (Aktual)" if idx == 0 else "", fontsize=10)
        ax.tick_params(axis="x", rotation=20)
        ax.tick_params(axis="y", rotation=0)
    plt.suptitle("Confusion Matrix pada Data Uji (Test Set = 959 Citra Unik)", fontsize=14, fontweight="bold", y=1.02)
    plt.tight_layout()
    fig.savefig(FIGURES_DIR / "06_confusion_matrices.png", bbox_inches="tight")
    plt.close(fig)

    # 7. Top 15 Feature Importances (XGBoost & Random Forest)
    df_imp = pd.read_csv(REPORTS_DIR / "feature_importance.csv").head(15)
    fig, ax = plt.subplots(figsize=(9.5, 5.8), dpi=150)
    y_pos = np.arange(len(df_imp))
    ax.barh(y_pos - 0.18, df_imp["xgb_importance"][::-1], height=0.35, label="XGBoost", color="#ea580c")
    ax.barh(y_pos + 0.18, df_imp["rf_importance"][::-1], height=0.35, label="Random Forest", color="#16a34a")
    ax.set_yticks(y_pos)
    ax.set_yticklabels(df_imp["feature"][::-1], fontsize=9.5, fontweight="bold")
    ax.set_xlabel("Relative Feature Importance", fontsize=10.5)
    ax.set_title("15 Fitur Citra Paling Berpengaruh terhadap Prediksi Penyakit Daun Padi", fontsize=12.5, fontweight="bold", pad=12)
    ax.legend(frameon=True, fontsize=10)
    plt.tight_layout()
    fig.savefig(FIGURES_DIR / "07_feature_importance.png")
    plt.close(fig)

    print("All 7 visualizations generated in reports/figures/.")


if __name__ == "__main__":
    generate_all_figures()
