"""PadiGuard — Animated Web Application with Top Burger Menu & Long-Scroll About Landing Page."""

import json
from pathlib import Path
import pandas as pd
import streamlit as st
from PIL import Image

import importlib
import src.ui_icons as _ui_icons_mod
importlib.reload(_ui_icons_mod)
from src import CLASSES, CLASS_INFO, DATA_PROCESSED_DIR, DATASET_DIR, FIGURES_DIR, REPORTS_DIR
from src.predict import MODEL_FILES, predict_image
from src.ui_icons import HERO_SCANNER_SVG, ICONS, inject_css, scroll_section_banner, section_header, sub_header

st.set_page_config(
    page_title="PadiGuard — Klasifikasi Penyakit Daun Padi",
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_css()


@st.cache_data
def get_eval_summary() -> dict:
    with open(REPORTS_DIR / "evaluation_summary.json", "r", encoding="utf-8") as f:
        return json.load(f)


@st.cache_data
def get_sample_test_images() -> dict:
    """Return one representative test image path per disease class from the hold-out test set."""
    test_csv = DATA_PROCESSED_DIR / "test_features.csv"
    samples = {}
    if test_csv.exists():
        df_te = pd.read_csv(test_csv)
        for cls_name in CLASSES:
            sub = df_te[df_te["class_name"] == cls_name]
            if not sub.empty:
                p = Path(sub.iloc[0]["filepath"])
                if p.exists():
                    samples[cls_name] = p
    for cls_name in CLASSES:
        if cls_name not in samples:
            cdir = DATASET_DIR / cls_name
            if cdir.exists():
                files = sorted(list(cdir.glob("*.jpg")))
                if files:
                    samples[cls_name] = files[0]
    return samples


# Initialize active page in session_state (Default: "about" as requested by user)
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "about"
if "selected_model" not in st.session_state:
    st.session_state["selected_model"] = list(MODEL_FILES.keys())[0]
if "active_sample_class" not in st.session_state:
    st.session_state["active_sample_class"] = "Bacterialblight"


def set_page(page_key: str):
    st.session_state["current_page"] = page_key


# ==============================================================================
# TOP NAVIGATION BAR WITH COMPACT BURGER MENU (POJOK KANAN ATAS)
# ==============================================================================
PAGE_LABELS = {
    "about": "Tentang Proyek",
    "scanner": "Deteksi Daun Padi",
    "evaluation": "Evaluasi 3 Model",
}

nav_left, nav_spacer, nav_right = st.columns([2.2, 3.2, 1.3], vertical_alignment="center")

with nav_left:
    st.markdown(
        f"""
        <div class="top-nav-brand">
            <div class="brand-logo-box">{ICONS["leaf"]}</div>
            <div>
                <div class="brand-title">PadiGuard ML</div>
                <div class="brand-subtitle">Rice Leaf Disease Intelligence</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with nav_spacer:
    st.markdown(
        f"<div style='text-align:right;font-size:0.84rem;color:#94a3b8;padding-right:0.5rem;'>"
        f"Halaman Aktif: <b style='color:#4ade80;'>{PAGE_LABELS[st.session_state['current_page']]}</b> &bull; "
        f"Model: <b style='color:#e2e8f0;'>{st.session_state['selected_model'].split('—')[0].strip()}</b>"
        f"</div>",
        unsafe_allow_html=True,
    )

with nav_right:
    with st.popover("☰  MENU", use_container_width=True):
        st.markdown("##### Navigasi Halaman")
        curr = st.session_state["current_page"]
        if st.button(
            "01 — Tentang Proyek (Landing)",
            type="primary" if curr == "about" else "secondary",
            use_container_width=True,
        ):
            set_page("about")
            st.rerun()
        if st.button(
            "02 — Deteksi & Diagnosis Daun",
            type="primary" if curr == "scanner" else "secondary",
            use_container_width=True,
        ):
            set_page("scanner")
            st.rerun()
        if st.button(
            "03 — Evaluasi Model & Audit",
            type="primary" if curr == "evaluation" else "secondary",
            use_container_width=True,
        ):
            set_page("evaluation")
            st.rerun()

        st.divider()
        st.markdown("##### Pilih Algoritma Model")
        chosen_m = st.selectbox(
            "Model Klasifikasi Aktif:",
            list(MODEL_FILES.keys()),
            index=list(MODEL_FILES.keys()).index(st.session_state["selected_model"]),
            help="SVM (RBF) adalah model final terpilih (CV F1: 0,9761 | Test Acc: 98,75%).",
        )
        st.session_state["selected_model"] = chosen_m
        st.caption(
            "Akurasi Data Uji (962 Citra Unik):\n"
            "- **SVM (RBF):** 98,75% (F1 0,9867)\n"
            "- **XGBoost:** 98,75% (F1 0,9865)\n"
            "- **Random Forest:** 97,51% (F1 0,9733)"
        )

st.markdown("<hr style='margin: 0.45rem 0 1.2rem 0; opacity: 0.16;'/>", unsafe_allow_html=True)


# ==============================================================================
# VIEW 1: LONG-SCROLL ABOUT PROJECT LANDING PAGE (DEFAULT INITIAL VIEW)
# ==============================================================================
def render_about_landing_page():
    summary = get_eval_summary()
    ds = summary["dataset_summary"]
    sp = summary["split_info"]

    st.markdown('<div class="page-anim-wrap">', unsafe_allow_html=True)

    # --- SECTION 1: 2-COLUMN SPLIT HERO BANNER (TALL & PROPORTIONAL) ---
    st.markdown(
        f"""
        <div class="hero-split">
            <div>
                <div class="hero-badge-pill">{ICONS["leaf"]}<span>TEK1302 Pembelajaran Mesin &bull; Computer Vision</span></div>
                <div class="hero-main-title">
                    Klasifikasi Penyakit Daun Padi dengan <span class="hero-highlight">Fitur Citra &amp; Machine Learning</span>
                </div>
                <div class="hero-desc">
                    <b>PadiGuard ML</b> mengidentifikasi 4 penyakit utama tanaman padi — <i>Bacterial Blight</i>, <i>Blast</i>,
                    <i>Brown Spot</i>, dan <i>Tungro</i> — secara cepat dan akurat melalui ekstraksi <b>100 fitur visual</b>
                    (Histogram Warna HSV/RGB, Color Moments, Tekstur GLCM, dan Gradien Tepi Sobel) yang dievaluasi secara ketat
                    dengan <b>StratifiedGroupKFold</b> bebas <i>data leakage</i>.
                </div>
                <div class="hero-mini-tags">
                    <span class="hero-tag-chip">SVM (RBF) &bull; Random Forest &bull; XGBoost</span>
                    <span class="hero-tag-chip">Zero Specimen Leakage</span>
                    <span class="hero-tag-chip">Inferensi &lt; 0,2 Detik</span>
                </div>
            </div>
            <div class="hero-visual-panel">
                <div class="visual-svg-box">{HERO_SCANNER_SVG}</div>
                <div class="visual-kpi-grid">
                    <div class="visual-kpi-box">
                        <div class="visual-kpi-val">4.794 Citra</div>
                        <div class="visual-kpi-lbl">Unik Bersih (-1.138 Duplikat MD5)</div>
                    </div>
                    <div class="visual-kpi-box">
                        <div class="visual-kpi-val">100 Fitur</div>
                        <div class="visual-kpi-lbl">Warna HSV/RGB, GLCM &amp; Sobel</div>
                    </div>
                    <div class="visual-kpi-box">
                        <div class="visual-kpi-val">858 Daun</div>
                        <div class="visual-kpi-lbl">Group-Split 80:20 Bebas Leakage</div>
                    </div>
                    <div class="visual-kpi-box">
                        <div class="visual-kpi-val">98,75%</div>
                        <div class="visual-kpi-lbl">Test Accuracy (F1: 0,9867)</div>
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    _, cta_left, cta_right, _ = st.columns([0.8, 1.4, 1.4, 0.8])
    with cta_left:
        if st.button("Mulai Deteksi Foto Daun →", type="primary", use_container_width=True):
            set_page("scanner")
            st.rerun()
    with cta_right:
        if st.button("Lihat Evaluasi 3 Model →", type="secondary", use_container_width=True):
            set_page("evaluation")
            st.rerun()

    st.markdown(
        f'<div class="scroll-cue">{ICONS["arrow_down"]}<span>Gulir ke Bawah untuk Membaca Keseluruhan Tentang Proyek</span>{ICONS["arrow_down"]}</div>',
        unsafe_allow_html=True,
    )

    # --- SECTION 2: LATAR BELAKANG & PERMASALAHAN ---
    scroll_section_banner(
        "Bagian 01 • Latar Belakang & Urgensi",
        "Mengapa Deteksi Dini Penyakit Daun Padi Sangat Krusial?",
        "Serangan patogen bakteri, jamur, dan virus pada daun padi sering kali terlambat dikenali atau tertukar satu sama lain ketika hanya diamati secara kasat mata di sawah.",
    )

    bg_c1, bg_c2, bg_c3 = st.columns(3)
    with bg_c1:
        st.markdown(
            f"""
            <div class="anim-card anim-card-accent">
                <div class="anim-card-header">
                    <div class="icon-box">{ICONS["alert"]}</div>
                    <div class="anim-card-title">Ancaman Gagal Panen (Puso)</div>
                </div>
                <div class="anim-card-body">
                    Empat penyakit utama daun padi — <b>Bacterial Blight</b>, <b>Blast</b>, <b>Brown Spot</b>, dan <b>Tungro</b> —
                    merusak jaringan klorofil daun, menghambat pengisian bulir gabah, dan dapat menurunkan hasil panen hingga 50–80%
                    apabila tidak ditangani sejak fase vegetatif awal.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with bg_c2:
        st.markdown(
            f"""
            <div class="anim-card anim-card-accent">
                <div class="anim-card-header">
                    <div class="icon-box">{ICONS["scan"]}</div>
                    <div class="anim-card-title">Gejala Visual yang Mirip</div>
                </div>
                <div class="anim-card-body">
                    Pengamatan manual sering kali keliru membedakan bercak nekrotik memanjang pada <i>Bacterial Blight</i>
                    dengan bercak belah ketupat pada <i>Blast</i>. Kesalahan diagnosis menyebabkan petani salah menyemprotkan
                    fungisida pada penyakit yang disebabkan oleh bakteri atau virus.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with bg_c3:
        st.markdown(
            f"""
            <div class="anim-card anim-card-accent">
                <div class="anim-card-header">
                    <div class="icon-box">{ICONS["cpu"]}</div>
                    <div class="anim-card-title">Solusi ML Ringan &amp; Terinterpretasi</div>
                </div>
                <div class="anim-card-body">
                    Tanpa membutuhkan server GPU mahal untuk model <i>Deep Learning</i> raksasa, kami membuktikan bahwa
                    rekayasa <b>100 fitur warna &amp; tekstur GLCM</b> yang dipadukan dengan <b>SVM (RBF)</b> dan <b>XGBoost</b>
                    mampu mencapai akurasi <b>98,75%</b> dengan waktu prediksi <b>&lt; 0,2 detik</b> di CPU biasa.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # --- SECTION 3: ENSIKLOPEDIA 4 PENYAKIT DAUN PADI ---
    scroll_section_banner(
        "Bagian 02 • Target Klasifikasi (4 Kelas)",
        "Ensiklopedia 4 Penyakit Utama Daun Padi pada Dataset",
        "Setiap kelas memiliki karakteristik patogen, pola warna spektrum HSV, dan struktur kekasaran tekstur permukaan daun (GLCM) yang khas.",
    )

    d_cols = st.columns(2)
    for idx, (cls_key, info) in enumerate(CLASS_INFO.items()):
        raw_cnt = ds["per_class_raw"].get(cls_key, 0)
        uniq_cnt = ds["per_class_unique"].get(cls_key, 0)
        spec_cnt = ds["per_class_leaf_specimens"].get(cls_key, 0)
        with d_cols[idx % 2]:
            st.markdown(
                f"""
                <div class="disease-card" style="border-top: 4px solid {info['warna_badge']};">
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.5rem;">
                        <span style="font-size:1.15rem;font-weight:800;">{info['nama_id']}</span>
                        <span style="font-size:0.78rem;font-weight:700;padding:3px 10px;border-radius:999px;background:rgba(34,197,94,0.14);color:#22c55e;">
                            {uniq_cnt:,} Citra Unik ({spec_cnt} Daun)
                        </span>
                    </div>
                    <div style="font-size:0.88rem;line-height:1.6;opacity:0.9;">
                        <b>&bull; Patogen Penyebab:</b> {info['penyebab']}<br/>
                        <b>&bull; Gejala Visual Khas:</b> {info['gejala']}<br/>
                        <b>&bull; Dampak Pertanian:</b> {info['dampak']}<br/>
                        <b>&bull; Rekomendasi Pengendalian:</b> {info['penanganan']}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    if (FIGURES_DIR / "02_sample_images_grid.png").exists():
        st.image(
            str(FIGURES_DIR / "02_sample_images_grid.png"),
            caption="Sampel Citra Daun Padi dari Keempat Kelas Penyakit pada Dataset (Setelah Normalisasi RGB 128x128)",
            use_container_width=True,
        )

    # --- SECTION 4: ARSITEKTUR PIPELINE & 100 FITUR VISUAL ---
    scroll_section_banner(
        "Bagian 03 • Metodologi & Rekayasa Fitur",
        "Arsitektur Pipeline Machine Learning & Ekstraksi 100 Fitur Citra",
        "Seluruh tahapan dari pembacaan citra mentah, pembersihan duplikat MD5, ekstraksi 100 fitur, hingga pelatihan 3 algoritma dirancang bebas dari kebocoran data (Data Leakage).",
    )

    p_left, p_right = st.columns([1.05, 1.0], gap="large")
    with p_left:
        steps_data = [
            (
                "Tahap 01 • Audit Dataset & Deduplikasi MD5",
                f"Memindai <b>{ds['total_files']:,} citra mentah</b> di folder <code>penyakit padi/</code>. Menemukan dan menghapus <b>{ds['duplicate_count']:,} duplikat identik ({ds['duplicate_pct']}%)</b> berdasarkan <i>MD5 hash</i> sehingga diperoleh <b>{ds['unique_count']:,} citra unik</b>.",
            ),
            (
                "Tahap 02 • Normalisasi Warna RGBA & Dimensi 128×128",
                "Mengonversi 156 citra berformat <code>RGBA</code> (4 kanal) menjadi <code>RGB</code> 3 kanal di atas latar putih serta menyeragamkan ukuran resolusi ke <b>128×128 piksel</b> menggunakan interpolasi bilinear.",
            ),
            (
                "Tahap 03 • Ekstraksi 100 Fitur Visual Terinterpretasi",
                "Mengubah matriks piksel menjadi 100 fitur numerik: <b>32 HSV Histogram</b>, <b>24 RGB Histogram</b>, <b>18 Color Moments</b>, <b>12 Tekstur GLCM</b>, serta <b>14 Rasio Lesi &amp; Gradien Tepi Sobel</b>.",
            ),
            (
                "Tahap 04 • Pemisahan Data StratifiedGroupKFold (80:20)",
                f"Mengelompokkan 4.794 citra berdasarkan <b>{ds['unique_leaf_specimens']} spesimen daun fisik</b> (<code>leaf_group</code>) agar rotasi dari daun yang sama tidak bocor lintas Train (<b>{sp['train_size']:,} citra</b>) dan Test (<b>{sp['test_size']:,} citra</b>).",
            ),
            (
                "Tahap 05 • Pipeline StandardScaler + 3 Algoritma Klasifikasi",
                "Melatih dan men-tuning <b>SVM (RBF)</b>, <b>Random Forest</b>, dan <b>XGBoost</b> menggunakan <i>5-Fold StratifiedGroupKFold Cross-Validation</i> pada data latih, lalu mengevaluasi satu kali pada 962 citra uji.",
            ),
        ]
        for s_num, s_desc in steps_data:
            st.markdown(
                f"""
                <div class="pipe-step">
                    <div class="pipe-num">{s_num}</div>
                    <div style="font-size:0.9rem;line-height:1.55;">{s_desc}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    with p_right:
        st.markdown(
            f"""
            <div class="anim-card anim-card-accent" style="margin-bottom:1rem;">
                <div class="anim-card-header">
                    <div class="icon-box">{ICONS["sliders"]}</div>
                    <div class="anim-card-title">Rincian 100 Fitur Citra yang Diekstraksi</div>
                </div>
                <div class="anim-card-body">
                    <b>1. HSV Color Histogram (32 Fitur):</b><br/>
                    16 bin <i>Hue</i> (spektrum warna), 8 bin <i>Saturation</i>, 8 bin <i>Value</i>. Sangat kuat memisahkan perubahan warna kuning-oranye pada <i>Tungro</i>.<br/><br/>
                    <b>2. RGB Color Histogram (24 Fitur):</b><br/>
                    Masing-masing 8 bin untuk distribusi intensitas kanal <i>Red, Green, Blue</i>.<br/><br/>
                    <b>3. Color Moments (18 Fitur):</b><br/>
                    Nilai rata-rata (<i>Mean</i>), simpangan baku (<i>Std</i>), dan kemencengan (<i>Skewness</i>) pada 6 kanal (R, G, B, H, S, V).<br/><br/>
                    <b>4. Tekstur GLCM — Gray-Level Co-occurrence Matrix (12 Fitur):</b><br/>
                    <i>Contrast, Dissimilarity, Homogeneity, Energy, Correlation,</i> dan <i>ASM</i> (Mean &amp; Std) pada 32 tingkat keabuan, jarak <i>d</i>=[1,2], sudut 0&deg;, 45&deg;, 90&deg;, 135&deg;.<br/><br/>
                    <b>5. Rasio Lesi Spesifik &amp; Tepi Sobel (14 Fitur):</b><br/>
                    Proporsi hijau sehat, kuning klorosis, cokelat nekrotik, lesi pucat, indeks <i>Excess Green/Red</i>, rasio lesi tengah daun, serta statistik ketajaman tepi bercak (<i>Sobel Edge Filter</i>).
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # --- SECTION 5: RINGKASAN PERBANDINGAN 3 MODEL ---
    scroll_section_banner(
        "Bagian 04 • Ringkasan Eksperimen ML",
        "Perbandingan 3 Algoritma Klasifikasi & Alasan Pemilihan Model Terbaik",
        "Ketiga algoritma diuji secara adil pada 962 citra Hold-Out Test Set (172 spesimen daun fisik yang belum pernah dilihat saat training).",
    )

    m_col1, m_col2, m_col3 = st.columns(3)
    with m_col1:
        st.markdown(
            f"""
            <div class="anim-card" style="border-top: 4px solid #22c55e;">
                <div style="font-size:0.76rem;font-weight:800;color:#22c55e;text-transform:uppercase;letter-spacing:1px;">
                    Model Final Terpilih
                </div>
                <div style="font-size:1.35rem;font-weight:800;margin:0.2rem 0 0.6rem 0;">SVM (RBF Kernel)</div>
                <div style="font-size:0.9rem;line-height:1.65;">
                    &bull; <b>5-Fold Group-CV F1:</b> <code>0,9761</code> (Tertinggi)<br/>
                    &bull; <b>Test Accuracy:</b> <code>98,75%</code> (950/962 benar)<br/>
                    &bull; <b>Test F1-Macro:</b> <code>0,9867</code> (Tertinggi)<br/>
                    &bull; <b>Test Recall Macro:</b> <code>0,9889</code> (Tertinggi)<br/>
                    &bull; <b>Test ROC-AUC (OvR):</b> <code>1,0000</code><br/>
                    &bull; <b>Ukuran File Model:</b> <code>0,28 MB</code> (Paling Ringan)
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with m_col2:
        st.markdown(
            """
            <div class="anim-card" style="border-top: 4px solid #ea580c;">
                <div style="font-size:0.76rem;font-weight:800;color:#ea580c;text-transform:uppercase;letter-spacing:1px;">
                    Ensemble Gradient Boosting
                </div>
                <div style="font-size:1.35rem;font-weight:800;margin:0.2rem 0 0.6rem 0;">XGBoost Classifier</div>
                <div style="font-size:0.9rem;line-height:1.65;">
                    &bull; <b>5-Fold Group-CV F1:</b> <code>0,9716</code><br/>
                    &bull; <b>Test Accuracy:</b> <code>98,75%</code> (950/962 benar)<br/>
                    &bull; <b>Test F1-Macro:</b> <code>0,9865</code><br/>
                    &bull; <b>Test Precision Macro:</b> <code>0,9894</code><br/>
                    &bull; <b>Test ROC-AUC (OvR):</b> <code>0,9996</code><br/>
                    &bull; <b>Ukuran File Model:</b> <code>0,38 MB</code>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with m_col3:
        st.markdown(
            """
            <div class="anim-card" style="border-top: 4px solid #3b82f6;">
                <div style="font-size:0.76rem;font-weight:800;color:#3b82f6;text-transform:uppercase;letter-spacing:1px;">
                    Ensemble Bagging Trees
                </div>
                <div style="font-size:1.35rem;font-weight:800;margin:0.2rem 0 0.6rem 0;">Random Forest</div>
                <div style="font-size:0.9rem;line-height:1.65;">
                    &bull; <b>5-Fold Group-CV F1:</b> <code>0,9540</code><br/>
                    &bull; <b>Test Accuracy:</b> <code>97,51%</code> (938/962 benar)<br/>
                    &bull; <b>Test F1-Macro:</b> <code>0,9733</code><br/>
                    &bull; <b>Test Recall Macro:</b> <code>0,9733</code><br/>
                    &bull; <b>Test ROC-AUC (OvR):</b> <code>0,9996</code><br/>
                    &bull; <b>Ukuran File Model:</b> <code>1,43 MB</code>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # --- SECTION 6: STUDI LITERATUR 5 JURNAL ---
    scroll_section_banner(
        "Bagian 05 • Landasan Ilmiah (5 Jurnal)",
        "Tabel Studi Literatur & Perbedaan Spesifik dengan Proyek Kami",
        "Perbandingan metodologi, dataset, dan hasil penelitian kami terhadap 5 artikel jurnal ilmiah terpublikasi.",
    )

    st.markdown(
        """
        | No. | Penulis & Tahun | Permasalahan & Dataset | Metode / Algoritma | Metrik Evaluasi | Hasil Utama | Perbedaan Spesifik dengan Proyek Kami |
        |---|---|---|---|---|---|---|
        | **1** | **Sethy et al. (2020)** — *Computers and Electronics in Agriculture* | Identifikasi 4 penyakit daun padi pada **5.932 citra** (dataset yang sama) | Ekstraksi fitur CNN (ResNet50) + **SVM** | Accuracy, F1-Score | ResNet50 + SVM mencapai F1-Score **98,38%** | Sethy et al. memakai fitur CNN berat (butuh GPU) tanpa dedup/group split; proyek kami memakai **100 fitur warna HSV/RGB + GLCM + Sobel** yang cepat di CPU dengan `StratifiedGroupKFold` bebas leakage (F1-Macro **98,67%**) |
        | **2** | **Prajapati et al. (2017)** — *Intelligent Decision Technologies* | Deteksi 3 penyakit daun padi (BLB, Brown Spot, Leaf Smut) pada 120 citra | Segmentasi K-Means + **88 fitur warna, bentuk, GLCM** + **SVM** | Accuracy & 5-Fold CV | Akurasi uji **93,33%** (5-Fold CV **83,80%**) | Dataset Prajapati et al. hanya 120 citra (3 kelas); proyek kami mengevaluasi **4.794 citra unik (4 kelas termasuk Tungro & Blast)** pada 3 algoritma |
        | **3** | **Azim et al. (2021)** — *Agronomy (MDPI)* | Klasifikasi penyakit daun padi hemat komputasi pada dataset UCI (3 kelas) | Fitur **GLCM + Warna HSV** + **XGBoost** | Accuracy, Precision, Recall, F1 | **XGBoost** mencapai akurasi **86,58%** | Azim et al. hanya menguji 3 kelas; proyek kami menambahkan fitur rasio klorosis & Sobel pada 4 kelas dan mencapai akurasi **98,75%** pada XGBoost & SVM |
        | **4** | **Pothen & Pai (2020)** — *IEEE I-SMAC* | Klasifikasi penyakit daun padi berbasis tekstur pada 3 kelas penyakit | Fitur **HOG + LBP/GLCM** + **SVM** | Accuracy, Precision, Recall | SVM mencapai akurasi **94,60%** | Pothen & Pai hanya mengandalkan tekstur keabuan; proyek kami memadukan spektrum warna HSV/RGB + GLCM sehingga penyakit klorosis seperti *Tungro* terdeteksi 100% |
        | **5** | **Haruna et al. (2023)** — *IJEECS* | Perbandingan algoritma ML pada dataset Mendeley Rice Leaf Disease (4 kelas) | Fitur warna & tekstur + **Random Forest, SVM, KNN** | Accuracy, F1, Confusion Matrix | RF & SVM mencapai akurasi >95% | Studi terdahulu memakai *random split* langsung tanpa mengaudit 1.138 duplikat MD5 dan grup spesimen; proyek kami menyertakan studi ablasi leakage & aplikasi Streamlit lengkap |
        """
    )

    # --- SECTION 7: TIM PENGEMBANG, BATASAN & CTA AKHIR ---
    scroll_section_banner(
        "Bagian 06 • Tim Pengembang & Etika Penggunaan",
        "Kontribusi Tim & Batasan Sistem (Disclaimer)",
        "Proyek ini dikerjakan oleh 3 anggota kelompok dengan pembagian tanggung jawab yang jelas serta transparansi penuh atas batasan model.",
    )

    t1, t2, t3 = st.columns(3)
    with t1:
        st.markdown(
            f"""
            <div class="anim-card">
                <div class="anim-card-header">
                    <div class="icon-box">{ICONS["users"]}</div>
                    <div class="anim-card-title">Anggota 1 — Data &amp; CV</div>
                </div>
                <div class="anim-card-body">
                    Bertanggung jawab atas audit 5.932 citra, deteksi 1.138 duplikat MD5 &amp; 858 grup spesimen daun,
                    Exploratory Data Analysis (EDA), serta ekstraksi 100 fitur warna HSV/RGB, Tekstur GLCM, dan Tepi Sobel
                    (<code>src/data_loader.py</code>, <code>src/preprocessing.py</code>, Notebook 01–03).
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with t2:
        st.markdown(
            f"""
            <div class="anim-card">
                <div class="anim-card-header">
                    <div class="icon-box">{ICONS["cpu"]}</div>
                    <div class="anim-card-title">Anggota 2 — Machine Learning</div>
                </div>
                <div class="anim-card-body">
                    Bertanggung jawab atas skema validasi <i>StratifiedGroupKFold</i>, pelatihan baseline 3 model,
                    <i>hyperparameter tuning</i> (SVM, Random Forest, XGBoost), uji ablasi <i>data leakage</i>,
                    serta analisis <i>confusion matrix</i> &amp; <i>feature importance</i>
                    (<code>src/train.py</code>, <code>src/evaluate.py</code>, Notebook 04–05).
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with t3:
        st.markdown(
            f"""
            <div class="anim-card">
                <div class="anim-card-header">
                    <div class="icon-box">{ICONS["layers"]}</div>
                    <div class="anim-card-title">Anggota 3 — Web App &amp; Laporan</div>
                </div>
                <div class="anim-card-body">
                    Bertanggung jawab atas arsitektur aplikasi web interaktif Streamlit, sistem navigasi Burger Menu,
                    integrasi pipeline inferensi &amp; validasi gambar (<code>src/predict.py</code>), penyusunan studi literatur 5 jurnal,
                    PRD, PPT Laporan, dan Portofolio Project.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.write("")
    st.warning(
        "**Batasan Sistem & Etika Penggunaan (Disclaimer):** "
        "(1) **Klasifikasi Tertutup 4 Kelas:** Model dilatih khusus pada 4 kelas penyakit (*Bacterial Blight, Blast, Brown Spot, Tungro*) sesuai isi dataset Mendeley dan belum memiliki kelas 'Daun Sehat' atau penolak objek non-daun. "
        "(2) **Sensitivitas Pencahayaan:** Warna bercak daun dapat dipengaruhi oleh bayangan ekstrem atau latar belakang yang terlalu ramai. "
        "(3) **Pendukung Keputusan Awal:** Hasil prediksi ini merupakan alat bantu skrining dini dan edukasi, bukan pengganti diagnosis laboratorium maupun rekomendasi penyuluh pertanian (PPL)."
    )

    st.write("")
    b_end1, b_end2 = st.columns(2)
    with b_end1:
        if st.button("Buka Halaman Deteksi & Diagnosis Daun Padi →", type="primary", use_container_width=True):
            set_page("scanner")
            st.rerun()
    with b_end2:
        if st.button("Buka Halaman Evaluasi 3 Model & Confusion Matrix →", type="secondary", use_container_width=True):
            set_page("evaluation")
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


# ==============================================================================
# VIEW 2: DETEKSI & DIAGNOSIS CITRA DAUN PADI (SCANNER PAGE)
# ==============================================================================
def render_scanner_page():
    st.markdown('<div class="page-anim-wrap">', unsafe_allow_html=True)

    scroll_section_banner(
        "Halaman 02 • Deteksi & Diagnosis Interaktif",
        "Deteksi Penyakit Daun Padi dari Citra Visual",
        "Unggah foto helai daun padi Anda atau klik salah satu dari 4 skenario sampel uji di bawah. Anda juga dapat mengganti algoritma model melalui tombol ☰ MENU & MODEL di pojok kanan atas.",
    )

    # 3-Step Guide Cards
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            """
            <div class="anim-card anim-card-accent">
                <div class="anim-card-header">
                    <div class="icon-box">01</div>
                    <div class="anim-card-title">Unggah atau Pilih Sampel Daun</div>
                </div>
                <div class="anim-card-body">Unggah foto daun padi (JPG/PNG) atau klik salah satu dari 4 tombol contoh citra uji di bawah.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            """
            <div class="anim-card anim-card-accent">
                <div class="anim-card-header">
                    <div class="icon-box">02</div>
                    <div class="anim-card-title">Ekstraksi 100 Fitur Visual</div>
                </div>
                <div class="anim-card-body">Sistem memeriksa validitas gambar, menormalisasi ke 128×128 RGB, dan menghitung profil warna HSV &amp; tekstur GLCM.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            """
            <div class="anim-card anim-card-accent">
                <div class="anim-card-header">
                    <div class="icon-box">03</div>
                    <div class="anim-card-title">Diagnosis &amp; Saran Penanganan</div>
                </div>
                <div class="anim-card-body">Lihat kelas penyakit, distribusi probabilitas 4 kelas, indikator bercak daun, serta rekomendasi pengendalian awal.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.write("")
    samples_map = get_sample_test_images()
    selected_model = st.session_state["selected_model"]

    col_input, col_output = st.columns([1.0, 1.25], gap="large")

    with col_input:
        section_header("camera", "1. Input Citra Daun Padi")
        uploaded_file = st.file_uploader(
            "Unggah foto daun padi (.jpg, .jpeg, .png):",
            type=["jpg", "jpeg", "png"],
            help="Resolusi minimal 32×32 piksel. Jika Anda mengunggah file, sistem akan otomatis memproses file unggahan Anda.",
        )

        st.markdown("**Atau pilih Skenario Contoh Citra dari Data Uji (Hold-Out Test Set):**")
        b_col1, b_col2, b_col3, b_col4 = st.columns(4)
        with b_col1:
            if st.button("Blight", use_container_width=True, help="Contoh daun Bacterial Blight"):
                st.session_state["active_sample_class"] = "Bacterialblight"
        with b_col2:
            if st.button("Blast", use_container_width=True, help="Contoh daun Rice Blast"):
                st.session_state["active_sample_class"] = "Blast"
        with b_col3:
            if st.button("Brownspot", use_container_width=True, help="Contoh daun Brown Spot"):
                st.session_state["active_sample_class"] = "Brownspot"
        with b_col4:
            if st.button("Tungro", use_container_width=True, help="Contoh daun Tungro"):
                st.session_state["active_sample_class"] = "Tungro"

        active_image = None
        source_caption = ""
        ground_truth_label = None

        if uploaded_file is not None:
            try:
                active_image = Image.open(uploaded_file)
                source_caption = f"Citra Unggahan Pengguna: {uploaded_file.name}"
            except Exception as e:
                st.error(f"File tidak dapat dibaca sebagai gambar: {e}")
        else:
            sample_cls = st.session_state["active_sample_class"]
            sample_path = samples_map.get(sample_cls)
            if sample_path and sample_path.exists():
                active_image = Image.open(sample_path)
                ground_truth_label = sample_cls
                source_caption = f"Sampel Data Uji: {sample_path.name} (Label Aktual: {sample_cls})"

        if active_image is not None:
            st.image(active_image, caption=source_caption, use_container_width=True)

    with col_output:
        section_header("scan", f"2. Hasil Diagnosis ({selected_model})")

        if active_image is None:
            st.info("Silakan unggah foto daun padi atau pilih salah satu tombol sampel di sebelah kiri.")
        else:
            res = predict_image(active_image, model_name=selected_model)

            if not res["valid"]:
                st.error(f"Validasi Citra Gagal (FR-02): {res['message']}")
            else:
                pred_cls = res["predicted_class"]
                info = res["class_info"]
                conf_pct = res["confidence_pct"]
                badge_color = info["warna_badge"]

                gt_html = ""
                if ground_truth_label:
                    match_status = "Cocok dengan Label Aktual" if ground_truth_label == pred_cls else "Berbeda dari Label Aktual"
                    gt_html = (
                        f"<div style='font-size:0.88rem;margin-top:0.4rem;opacity:0.92;'>"
                        f"Label Sampel Uji: <b>{ground_truth_label}</b> ({match_status})</div>"
                    )

                st.markdown(
                    f"""
                    <div class="result-banner" style="background: linear-gradient(135deg, {badge_color} 0%, #0f172a 100%);">
                        <div style="font-size:0.78rem;text-transform:uppercase;letter-spacing:1.1px;opacity:0.88;font-weight:600;">
                            Hasil Prediksi &bull; {res['model_name']}
                        </div>
                        <div style="font-size:1.6rem;font-weight:800;margin-top:0.2rem;">
                            {res['nama_id']}
                        </div>
                        <div style="font-size:1.02rem;margin-top:0.25rem;">
                            Tingkat Keyakinan Model (Confidence): <b>{conf_pct:.2f}%</b>
                        </div>
                        {gt_html}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                sub_header("chart", "Distribusi Probabilitas Prediksi (4 Kelas)")
                prob_df = pd.DataFrame(
                    [
                        {
                            "Kelas Penyakit": f"{c} ({CLASS_INFO[c]['nama_id'].split('(')[0].strip()})",
                            "Probabilitas (%)": round(float(p) * 100.0, 2),
                        }
                        for c, p in res["probabilities"].items()
                    ]
                )
                for _, row in prob_df.iterrows():
                    p_val = float(row["Probabilitas (%)"])
                    st.progress(
                        min(max(int(round(p_val)), 0), 100),
                        text=f"**{row['Kelas Penyakit']}**: {p_val:.2f}%",
                    )

                diag = res["diagnostics"]
                sub_header("sliders", "Profil Visual & Tekstur Daun yang Terdeteksi")
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Hijau Sehat", f"{float(diag['ratio_healthy_green']):.1f}%", help="Proporsi piksel spektrum hijau daun sehat")
                m2.metric("Kuning / Klorosis", f"{float(diag['ratio_yellow_orange']):.1f}%", help="Proporsi spektrum kuning-oranye (tinggi pada Tungro)")
                m3.metric("Bercak Nekrotik", f"{float(diag['ratio_brown_necrotic']):.1f}%", help="Proporsi bercak cokelat/gelap nekrotik")
                m4.metric("Kontras GLCM", f"{float(diag['glcm_contrast']):.2f}", help="Tingkat kekasaran tekstur permukaan daun (GLCM Contrast)")

                with st.expander("Penjelasan Gejala, Penyebab & Rekomendasi Penanganan", expanded=True):
                    st.markdown(f"- **Patogen Penyebab:** {info['penyebab']}")
                    st.markdown(f"- **Gejala Visual Khas:** {info['gejala']}")
                    st.markdown(f"- **Dampak pada Tanaman:** {info['dampak']}")
                    st.markdown(f"- **Rekomendasi Pengendalian Awal:** {info['penanganan']}")

                st.caption(
                    "Disclaimer & Batasan Model: Nilai probabilitas di atas merupakan estimasi statistik berdasarkan 100 fitur warna & tekstur dari 4 kelas penyakit pada dataset (tanpa kelas daun sehat). Gunakan hasil ini sebagai alat bantu skrining awal dan konsultasikan dengan Penyuluh Pertanian Lapangan (PPL)."
                )

    st.markdown("</div>", unsafe_allow_html=True)


# ==============================================================================
# VIEW 3: EVALUASI MODEL & AUDIT DATASET
# ==============================================================================
def render_evaluation_page():
    summary = get_eval_summary()
    ds = summary["dataset_summary"]
    sp = summary["split_info"]
    ab = summary["duplicate_ablation"]

    st.markdown('<div class="page-anim-wrap">', unsafe_allow_html=True)

    scroll_section_banner(
        "Halaman 03 • Evaluasi & Audit Eksperimen",
        "Evaluasi 3 Algoritma, Confusion Matrix, Feature Importance & Audit Data",
        "Hasil eksperimen nyata dari tahap M2 (Data Understanding) hingga M6 (Evaluasi Hold-Out Test Set pada 962 citra unik dari 172 spesimen daun fisik).",
    )

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
            "Alasan Pemilihan Model Final: SVM (RBF) dipilih sebagai model final utama karena memperoleh skor 5-Fold Group-CV F1-Macro tertinggi pada data latih (0,9761) serta menghasilkan Test Accuracy 98,75%, Test F1-Macro 0,9867, Recall Macro tertinggi (0,9889), dan ukuran file paling ringan (0,28 MB)."
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
                - **Brownspot (240/240) & Tungro (260/260) Terklasifikasi 100% Sempurna:** Ketiga model mampu memisahkan *Brownspot* dan *Tungro* tanpa satu pun kesalahan.
                - **Letak Kesalahan Minor (Bacterial Blight vs Blast):** Dari 962 citra uji, SVM dan XGBoost hanya salah pada **12 citra (2 spesimen daun fisik, atau 1,25%)** antara kelas `Bacterialblight` dan `Blast` akibat kemiripan lesi pucat mengering pada fase lanjut.
                - **Evaluasi Overfitting:** Selisih antara F1-Macro pada data latih (`1,0000`) dan data uji (`0,9867`) hanya sebesar **`0,0133` (1,33%)**, membuktikan generalisasi yang kuat pada spesimen daun baru.
                """
            )

    with tab3:
        section_header("sliders", "Pengaruh Fitur Citra (Feature Importance) & Visualisasi EDA")
        fig_imp = FIGURES_DIR / "07_feature_importance.png"
        if fig_imp.exists():
            st.image(str(fig_imp), caption="15 Fitur Citra Paling Berpengaruh (XGBoost & Random Forest)", use_container_width=True)

        st.divider()
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

    st.markdown("</div>", unsafe_allow_html=True)


# ==============================================================================
# DISPATCH CURRENT ACTIVE VIEW
# ==============================================================================
active_view = st.session_state["current_page"]
if active_view == "about":
    render_about_landing_page()
elif active_view == "scanner":
    render_scanner_page()
elif active_view == "evaluation":
    render_evaluation_page()
else:
    render_about_landing_page()
