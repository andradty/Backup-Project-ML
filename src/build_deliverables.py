"""Generate Final Submission Deliverables for TEK1302 M15 Project Akhir:
1. PowerPoint Presentation (.pptx) covering Sections A to O (16 slides with embedded charts & tables)
2. Word Document (.docx) for CLASS-IPB 'Portofolio Project' (KELAS_KELOMPOK_Portofolio_Project.docx)
"""

import json
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
from docx import Document
from docx.shared import Inches as DocxInches, Pt as DocxPt, RGBColor as DocxRGB

from src import BASE_DIR, FIGURES_DIR, REPORTS_DIR

SUBMISSION_DIR = BASE_DIR / "deliverables_M8"

# Color palette (Clean AgriTech Forest Green & Slate)
C_DARK_BG = RGBColor(15, 23, 42)       # #0f172a
C_FOREST = RGBColor(20, 83, 45)        # #14532d
C_GREEN = RGBColor(22, 163, 74)        # #16a34a
C_LIGHT_BG = RGBColor(248, 250, 252)   # #f8fafc
C_WHITE = RGBColor(255, 255, 255)
C_TEXT_DARK = RGBColor(30, 41, 59)     # #1e293b
C_TEXT_MUTED = RGBColor(100, 116, 139) # #64748b
C_BORDER = RGBColor(203, 213, 225)     # #cbd5e1


def add_header_banner(slide, section_code: str, title_text: str, subtitle_text: str = ""):
    """Add a consistent top banner with Section Badge (A-O) and slide title."""
    # Top bar background
    banner = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.15)
    )
    banner.fill.solid()
    banner.fill.fore_color.rgb = C_FOREST
    banner.line.fill.background()

    # Section code badge (e.g., "A", "B", ...)
    badge = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.45), Inches(0.22), Inches(0.72), Inches(0.72)
    )
    badge.fill.solid()
    badge.fill.fore_color.rgb = C_GREEN
    badge.line.color.rgb = C_WHITE
    badge.line.width = Pt(1.5)
    tf_b = badge.text_frame
    tf_b.word_wrap = False
    p_b = tf_b.paragraphs[0]
    p_b.text = section_code
    p_b.alignment = PP_ALIGN.CENTER
    p_b.font.size = Pt(22)
    p_b.font.bold = True
    p_b.font.color.rgb = C_WHITE
    p_b.font.name = "Calibri"

    # Title & Subtitle
    tb = slide.shapes.add_textbox(Inches(1.35), Inches(0.16), Inches(11.5), Inches(0.85))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = C_WHITE
    p.font.name = "Calibri"

    if subtitle_text:
        p2 = tf.add_paragraph()
        p2.text = subtitle_text
        p2.font.size = Pt(12)
        p2.font.color.rgb = RGBColor(220, 252, 231)
        p2.font.name = "Calibri"

    # Footer bar
    footer = slide.shapes.add_textbox(Inches(0.45), Inches(7.1), Inches(12.4), Inches(0.35))
    tf_f = footer.text_frame
    p_f = tf_f.paragraphs[0]
    p_f.text = "TEK1302 Pembelajaran Mesin (M15)  |  Sekolah Vokasi IPB — Teknologi Rekayasa Komputer  |  PadiGuard: Klasifikasi Penyakit Daun Padi"
    p_f.font.size = Pt(9.5)
    p_f.font.color.rgb = C_TEXT_MUTED
    p_f.font.name = "Calibri"


def add_bullet_card(slide, left, top, width, height, heading: str, bullets: list[str], bg_color=C_LIGHT_BG):
    """Add a bordered card with a bold heading and bullet points."""
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    card.line.color.rgb = C_BORDER
    card.line.width = Pt(1)

    tb = slide.shapes.add_textbox(left + Inches(0.18), top + Inches(0.12), width - Inches(0.36), height - Inches(0.24))
    tf = tb.text_frame
    tf.word_wrap = True

    p_h = tf.paragraphs[0]
    p_h.text = heading
    p_h.font.size = Pt(15)
    p_h.font.bold = True
    p_h.font.color.rgb = C_FOREST
    p_h.font.name = "Calibri"
    p_h.space_after = Pt(6)

    for b_text in bullets:
        p = tf.add_paragraph()
        p.text = f"•  {b_text}"
        p.font.size = Pt(12.5)
        p.font.color.rgb = C_TEXT_DARK
        p.font.name = "Calibri"
        p.space_after = Pt(4)


def add_styled_table(slide, left, top, width, height, headers: list[str], rows: list[list[str]], font_size=10.5):
    """Add a clean formatted table to a slide."""
    table_shape = slide.shapes.add_table(len(rows) + 1, len(headers), left, top, width, height)
    table = table_shape.table

    for col_idx, h_text in enumerate(headers):
        cell = table.cell(0, col_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_FOREST
        p = cell.text_frame.paragraphs[0]
        p.text = h_text
        p.font.size = Pt(font_size)
        p.font.bold = True
        p.font.color.rgb = C_WHITE
        p.font.name = "Calibri"

    for row_idx, r_data in enumerate(rows):
        bg = C_WHITE if row_idx % 2 == 0 else C_LIGHT_BG
        for col_idx, val in enumerate(r_data):
            cell = table.cell(row_idx + 1, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = bg
            p = cell.text_frame.paragraphs[0]
            p.text = str(val)
            p.font.size = Pt(font_size)
            p.font.color.rgb = C_TEXT_DARK
            p.font.name = "Calibri"
            if col_idx == 0:
                p.font.bold = True
    return table


def build_pptx():
    SUBMISSION_DIR.mkdir(parents=True, exist_ok=True)
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # --- SLIDE 1: Bagian A - Judul Project ---
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = C_DARK_BG
    bg1.line.fill.background()

    accent = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(0.35), Inches(7.5))
    accent.fill.solid()
    accent.fill.fore_color.rgb = C_GREEN
    accent.line.fill.background()

    tb1 = s1.shapes.add_textbox(Inches(1.0), Inches(0.8), Inches(11.3), Inches(5.8))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p_tag = tf1.paragraphs[0]
    p_tag.text = "BAGIAN A  |  PROJECT AKHIR PEMBELAJARAN MESIN (TEK1302 — M15)"
    p_tag.font.size = Pt(13)
    p_tag.font.bold = True
    p_tag.font.color.rgb = RGBColor(74, 222, 128)
    p_tag.space_after = Pt(14)

    p_title = tf1.add_paragraph()
    p_title.text = "Klasifikasi Penyakit Daun Padi Berbasis Ekstraksi Fitur Citra (HSV, RGB, GLCM, Sobel) & Supervised Machine Learning"
    p_title.font.size = Pt(32)
    p_title.font.bold = True
    p_title.font.color.rgb = C_WHITE
    p_title.space_after = Pt(12)

    p_sub = tf1.add_paragraph()
    p_sub.text = "Perbandingan Support Vector Machine (SVM RBF), Random Forest, dan XGBoost dengan Evaluasi StratifiedGroupKFold Bebas Data Leakage serta Implementasi Aplikasi Web Streamlit (PadiGuard)"
    p_sub.font.size = Pt(15)
    p_sub.font.color.rgb = RGBColor(203, 213, 225)
    p_sub.space_after = Pt(28)

    members = [
        "1. [Nama Anggota 1]  —  NIM: [Isi NIM 1]  (Fokus: Dataset, Audit MD5, EDA Visual, Ekstraksi 100 Fitur Citra)",
        "2. [Nama Anggota 2]  —  NIM: [Isi NIM 2]  (Fokus: Baseline Group-CV, Tuning SVM/RF/XGBoost, Evaluasi & Error Analysis)",
        "3. [Nama Anggota 3]  —  NIM: [Isi NIM 3]  (Fokus: Implementasi Aplikasi Web Streamlit 3 Halaman, Validasi & Dokumentasi)",
        "Kelas: [Isi Kelas, misal: TRK-A / B]   |   Program Studi Teknologi Rekayasa Komputer — Sekolah Vokasi IPB",
    ]
    for m_line in members:
        pm = tf1.add_paragraph()
        pm.text = m_line
        pm.font.size = Pt(14)
        pm.font.bold = True if "Kelas:" in m_line else False
        pm.font.color.rgb = RGBColor(240, 253, 244)
        pm.space_after = Pt(6)

    # --- SLIDE 2: Bagian B - Latar Belakang & Masalah ---
    s2 = prs.slides.add_slide(blank_layout)
    add_header_banner(s2, "B", "Latar Belakang & Rumusan Masalah", "Kondisi lapangan, urgensi deteksi penyakit padi, dan pertanyaan penelitian")
    add_bullet_card(
        s2, Inches(0.45), Inches(1.4), Inches(6.05), Inches(5.45),
        "Kondisi & Urgensi Masalah di Lapangan",
        [
            "Tanaman padi (Oryza sativa) adalah komoditas pangan strategis utama, namun rentan terserang 4 penyakit daun mematikan: Bacterial Blight (Hawar Daun Bakteri), Blast (Blas), Brown Spot (Bercak Cokelat), dan Tungro.",
            "Pengamatan manual oleh petani dengan mata telanjang bersifat subjektif, lambat, dan sering tertukar antar penyakit yang memiliki bercak serupa (misal bercak pucat Bacterial Blight vs Blast).",
            "Kesalahan diagnosis awal mengakibatkan salah pilih tindakan (misal menyemprot fungisida pada penyakit bakteri/virus) dan berujung gagal panen (puso).",
            "Pendekatan Deep Learning (CNN besar) membutuhkan GPU mahal, sehingga diperlukan metode ekstraksi fitur citra + Machine Learning klasik yang akurat, ringan di CPU, dan mudah diinterpretasikan."
        ]
    )
    add_bullet_card(
        s2, Inches(6.8), Inches(1.4), Inches(6.05), Inches(5.45),
        "Rumusan Masalah yang Dijawab",
        [
            "1. Bagaimana mengekstraksi fitur visual yang komprehensif (warna HSV/RGB, Color Moments, tekstur GLCM, rasio lesi, dan tepi Sobel) dari citra daun padi?",
            "2. Bagaimana membersihkan duplikat identik (MD5) dan mencegah kebocoran rotasi spesimen daun (augmentation leakage) menggunakan StratifiedGroupKFold?",
            "3. Bagaimana perbandingan performa SVM (RBF), Random Forest, dan XGBoost pada dataset citra penyakit daun padi yang sama?",
            "4. Fitur visual apa yang paling berpengaruh dalam membedakan keempat kelas penyakit daun padi?",
            "5. Bagaimana mengimplementasikan model terbaik ke dalam aplikasi Streamlit interaktif untuk pengguna awam?"
        ]
    )

    # --- SLIDE 3: Bagian C - Tujuan Project ---
    s3 = prs.slides.add_slide(blank_layout)
    add_header_banner(s3, "C", "Tujuan Project & Sasaran Pengguna", "Target terukur yang ingin dicapai dari eksperimen Machine Learning hingga aplikasi")
    add_bullet_card(
        s3, Inches(0.45), Inches(1.4), Inches(7.5), Inches(5.45),
        "7 Tujuan Utama Project",
        [
            "1. Mengaudit kualitas 5.932 citra dataset penyakit daun padi (resolusi, mode warna RGBA, duplikat MD5, dan struktur spesimen daun fisik).",
            "2. Melakukan Exploratory Data Analysis (EDA) disertai interpretasi agronomis atas perbedaan warna HSV dan tekstur GLCM antar penyakit.",
            "3. Mengekstraksi 100 fitur citra numerik dan membagi data 80:20 dengan StratifiedGroupKFold (bebas data leakage).",
            "4. Melatih dan membandingkan 3 algoritma klasifikasi: SVM (RBF), Random Forest, dan XGBoost.",
            "5. Mengevaluasi model pada hold-out test set (Accuracy, Precision, Recall, F1-Macro, ROC-AUC, Confusion Matrix) dan menganalisis overfitting.",
            "6. Memilih satu model final berdasarkan analisis menyeluruh (bukan hanya akurasi).",
            "7. Membangun aplikasi web Streamlit 3 halaman lengkap dengan validasi gambar, profil bercak daun, rekomendasi penanganan, dan disclaimer."
        ]
    )
    add_bullet_card(
        s3, Inches(8.25), Inches(1.4), Inches(4.6), Inches(5.45),
        "Sasaran Pengguna & Manfaat",
        [
            "Petani & Penyuluh Pertanian (PPL): Alat bantu skrining dini penyakit daun padi langsung dari foto daun beserta saran pengendalian awal.",
            "Mahasiswa & Akademisi: Referensi metodologi Computer Vision + Machine Learning yang bebas dari jebakan duplicate/augmentation data leakage.",
            "Target Performa: F1-Score Macro > 95% pada hold-out test set dengan waktu inferensi < 0,2 detik per gambar di CPU."
        ]
    )

    # --- SLIDE 4: Bagian D - Studi Literatur (5 Jurnal) ---
    s4 = prs.slides.add_slide(blank_layout)
    add_header_banner(s4, "D", "Studi Literatur (5 Artikel Jurnal Ilmiah Relevan)", "Perbandingan metode, dataset, metrik, hasil utama, dan posisi/perbedaan project kami")
    lit_headers = ["No", "Penulis & Tahun", "Dataset & Masalah", "Algoritma & Metrik", "Hasil Utama", "Perbedaan Spesifik dengan Project Kami"]
    lit_rows = [
        ["1", "Sethy et al. (2020)\nComp. & Electron. in Agric.", "5.932 citra daun padi (4 kelas: Blight, Blast, Brownspot, Tungro)", "Fitur CNN ResNet50 + SVM\n(Accuracy, F1-Score)", "F1-Score tertinggi 98,38% dengan ResNet50+SVM", "Sethy memakai CNN berat (butuh GPU) tanpa dedup/group split; kami memakai 100 fitur HSV/GLCM/Sobel ringan di CPU + StratifiedGroupKFold (F1: 98,67%)."],
        ["2", "Prajapati et al. (2017)\nIntell. Decision Tech.", "120 citra daun padi India (3 kelas: BLB, Brown Spot, Leaf Smut)", "K-Means + 88 fitur warna/bentuk/GLCM + SVM", "Akurasi uji 93,33%; 5-Fold CV 83,80%", "Dataset Prajapati sangat kecil (120 citra, 3 kelas); kami menguji 4.794 citra unik (4 kelas termasuk Blast & Tungro) pada 3 algoritma + aplikasi Streamlit."],
        ["3", "Azim et al. (2021)\nAgronomy (MDPI)", "Dataset UCI Rice Leaf (3 kelas penyakit daun padi)", "Fitur GLCM + Warna HSV + XGBoost & Decision Tree", "XGBoost unggul dengan akurasi 86,58%", "Azim hanya 3 kelas (tanpa Blast & Tungro); kami menambahkan fitur rasio klorosis & Sobel pada 4 kelas dan mencapai akurasi 98,75% pada XGBoost & SVM."],
        ["4", "Pothen & Pai (2020)\nIEEE I-SMAC", "Citra daun padi 3 kelas penyakit", "Fitur tekstur HOG + LBP/GLCM + SVM (RBF)", "SVM mencapai akurasi 94,60%", "Pothen hanya memakai tekstur keabuan sehingga kurang peka warna; kami menggabungkan spektrum HSV/RGB + GLCM sehingga Tungro & Brownspot akurat 100%."],
        ["5", "Haruna et al. (2023)\nIJEECS", "Mendeley Rice Leaf Disease (4 kelas penyakit)", "Fitur warna & tekstur + Random Forest, SVM, KNN", "RF & SVM mencapai akurasi >95%", "Studi sebelumnya memakai random split langsung tanpa menghapus 1.138 duplikat MD5 & grup spesimen; kami menyajikan ablasi leakage & web app lengkap."]
    ]
    add_styled_table(s4, Inches(0.45), Inches(1.35), Inches(12.43), Inches(5.55), lit_headers, lit_rows, font_size=9.5)

    # --- SLIDE 5: Bagian E - Dataset ---
    s5 = prs.slides.add_slide(blank_layout)
    add_header_banner(s5, "E", "Dataset & Audit Kualitas Data (M2)", "Sumber dataset, distribusi 4 kelas target, audit resolusi/mode warna, dan temuan duplikat MD5")
    ds_headers = ["Kelas Penyakit (Target)", "Citra Mentah", "Duplikat MD5", "Citra Unik Bersih", "Spesimen Daun Fisik", "Ciri Visual Utama"]
    ds_rows = [
        ["0 - Bacterialblight", "1.584 (26,70%)", "258 (16,29%)", "1.326 (27,66%)", "221 daun", "Lesi memanjang kuning-putih pucat mengering di tepi daun"],
        ["1 - Blast", "1.440 (24,28%)", "480 (33,33%)", "960 (20,03%)", "160 daun", "Bercak belah ketupat (diamond) tengah abu-abu pucat, tepi cokelat"],
        ["2 - Brownspot", "1.600 (26,97%)", "400 (25,00%)", "1.200 (25,03%)", "200 daun", "Bintik-bintik bulat/oval cokelat tua tersebar merata di daun"],
        ["3 - Tungro", "1.308 (22,05%)", "0 (0,00%)", "1.308 (27,28%)", "277 daun", "Perubahan warna daun menjadi kuning-oranye terang (klorosis)"],
        ["TOTAL DATASET", "5.932 Citra", "1.138 (19,18%)", "4.794 Citra Unik", "858 Spesimen Daun", "0 File Corrupt | 5.776 RGB & 156 RGBA | 77,95% ukuran 300x300 px"]
    ]
    add_styled_table(s5, Inches(0.45), Inches(1.35), Inches(12.43), Inches(2.9), ds_headers, ds_rows, font_size=10.5)
    add_bullet_card(
        s5, Inches(0.45), Inches(4.45), Inches(12.43), Inches(2.45),
        "Sumber Dataset & Temuan Audit Penting",
        [
            "Sumber Resmi: Mendeley Data (Sethy et al., 2020 — DOI: 10.17632/fwcj7stb8r.1), folder lokal `penyakit padi/`.",
            "Temuan 1 (Duplikat Identik): Terdapat 1.138 file duplikat byte identik (MD5 hash sama persis, misal perbedaan nama/ekstensi .jpg vs .JPG). Wajib dihapus sebelum split.",
            "Temuan 2 (Grup Spesimen Daun): 4.794 citra unik berasal dari 858 daun fisik yang mengalami rotasi/flip (misal BLAST1_045.jpg s/d BLAST9_045.jpg adalah daun #045). Oleh karena itu, pemisahan data wajib dikelompokkan berdasarkan `leaf_group`."
        ]
    )

    # --- SLIDE 6: Bagian F - Exploratory Data Analysis (EDA) ---
    s6 = prs.slides.add_slide(blank_layout)
    add_header_banner(s6, "F", "Exploratory Data Analysis (EDA) & Interpretasi Visual", "Setiap visualisasi menjelaskan karakteristik data dan pengaruhnya terhadap preprocessing & model")
    if (FIGURES_DIR / "01_class_distribution.png").exists():
        s6.shapes.add_picture(str(FIGURES_DIR / "01_class_distribution.png"), Inches(0.45), Inches(1.35), width=Inches(6.1))
    if (FIGURES_DIR / "03_feature_distributions.png").exists():
        s6.shapes.add_picture(str(FIGURES_DIR / "03_feature_distributions.png"), Inches(6.75), Inches(1.35), width=Inches(6.1))
    add_bullet_card(
        s6, Inches(0.45), Inches(4.95), Inches(12.43), Inches(1.95),
        "Interpretasi Hasil Visualisasi EDA & Dampaknya pada Pemodelan",
        [
            "1. Distribusi Kelas (Kiri): Setelah 1.138 duplikat MD5 dihapus, kelas Blast memiliki jumlah paling sedikit (960 citra) dibanding Bacterialblight (1.326). Ketidakseimbangan ringan ini ditangani dengan `class_weight='balanced'` dan pembagian Stratified.",
            "2. Boxplot Fitur Kunci (Kanan): Tungro memiliki `ratio_yellow_orange_tungro` tertinggi (rata-rata 23,14% vs <10% pada kelas lain); Brownspot memiliki `glcm_contrast_mean` tertinggi (19,87) dan `sobel_edge_mean` tertinggi akibat bintik nekrotik kasar; sedangkan Blast & Blight tinggi pada `ratio_white_pale_lesion`."
        ]
    )

    # --- SLIDE 7: Bagian G - Preprocessing & Ekstraksi Fitur ---
    s7 = prs.slides.add_slide(blank_layout)
    add_header_banner(s7, "G", "Preprocessing Citra, Ekstraksi 100 Fitur & Pencegahan Leakage", "Alasan pemilihan setiap tahapan preprocessing dan bukti uji ablasi data leakage")
    add_bullet_card(
        s7, Inches(0.45), Inches(1.35), Inches(6.2), Inches(5.5),
        "Tahapan Preprocessing & Ekstraksi 100 Fitur",
        [
            "1. Konversi RGBA ke RGB (156 citra): Menghindari error 4 kanal dengan menempelkan kanal alpha di atas latar putih (255, 255, 255).",
            "2. Resizing 128×128 Piksel (Bilinear): Menyeragamkan resolusi citra yang beragam (300×300, 499×332, 295×221) agar matriks GLCM & gradien tepi konsisten.",
            "3. Ekstraksi 100 Fitur Visual Terinterpretasi:",
            "   • HSV Histogram (32 fitur) & RGB Histogram (24 fitur)",
            "   • Color Moments: Mean, Std, Skewness pada 6 kanal R,G,B,H,S,V (18 fitur)",
            "   • Tekstur GLCM: Contrast, Dissimilarity, Homogeneity, Energy, Correlation, ASM pada 32 level keabuan, d=[1,2], 4 sudut (12 fitur)",
            "   • Rasio Lesi Spesifik & Gradien Sobel Edge: Hijau sehat, kuning klorosis, cokelat nekrotik, lesi pucat, Excess Green/Red, lesi tengah, Sobel (14 fitur)",
            "4. StandardScaler di dalam Pipeline: Dipasang hanya pada data training (X_train) agar bebas dari kebocoran statistik mean/std."
        ]
    )
    ab_headers = ["Skenario Split (80:20, Random Forest)", "Jml Citra", "Test Acc", "Test F1", "Status Metodologis"]
    ab_rows = [
        ["1. Tanpa Hapus Duplikat (Random Split)", "5.932", "100,00%", "1,0000", "LEAKAGE BERAT (File identik bocor ke test)"],
        ["2. Dedup MD5, Naive Random Split", "4.794", "100,00%", "1,0000", "AUGMENTATION LEAKAGE (Rotasi daun bocor)"],
        ["3. Dedup MD5 + StratifiedGroupKFold", "4.794", "97,51%", "0,9733", "BEBAS LEAKAGE (Standar utama project)"]
    ]
    add_styled_table(s7, Inches(6.85), Inches(1.35), Inches(6.03), Inches(2.5), ab_headers, ab_rows, font_size=9.5)
    if (FIGURES_DIR / "02_sample_images_grid.png").exists():
        s7.shapes.add_picture(str(FIGURES_DIR / "02_sample_images_grid.png"), Inches(8.1), Inches(3.95), height=Inches(2.9))

    # --- SLIDE 8: Bagian H - Pengembangan Model ---
    s8 = prs.slides.add_slide(blank_layout)
    add_header_banner(s8, "H", "Pengembangan Model Machine Learning (M5 & M6)", "Alasan pemilihan 3 algoritma, skema pembagian data 80:20, dan parameter hasil tuning")
    add_bullet_card(
        s8, Inches(0.45), Inches(1.35), Inches(5.8), Inches(5.5),
        "Skema Pembagian Data & Validasi Silang",
        [
            "Total Data Bersih: 4.794 citra unik (858 spesimen daun fisik).",
            "Metode Split (80:20): StratifiedGroupKFold (random_state=42) berdasarkan `leaf_group`:",
            "   • Data Training: 3.832 citra (686 spesimen daun fisik)",
            "   • Data Testing (Hold-Out): 962 citra (172 spesimen daun fisik)",
            "   • Irisan Spesimen Train vs Test: 0 spesimen (100% terpisah).",
            "Proses Tuning: Seluruh hyperparameter dipilih menggunakan 5-Fold StratifiedGroupKFold CV hanya pada Data Training (3.832 citra).",
            "Data Testing (962 citra) dikunci dan hanya dievaluasi satu kali di tahap akhir (M6)."
        ]
    )
    m_headers = ["Algoritma", "Alasan Pemilihan", "Hyperparameter Akhir (Tuned via 5-Fold Group-CV)"]
    m_rows = [
        ["1. SVM (RBF)", "Sangat efektif pada ruang fitur numerik dimensi menengah (100 fitur) dengan batas keputusan non-linear yang halus.", "C=10.0, kernel='rbf', gamma='scale', class_weight='balanced', random_state=42"],
        ["2. Random Forest", "Ensemble bagging pohon keputusan yang tahan terhadap outlier dan mampu menangkap interaksi fitur warna & tekstur.", "n_estimators=300, max_depth=16, min_samples_split=4, min_samples_leaf=2, max_features='sqrt', class_weight='balanced_subsample'"],
        ["3. XGBoost", "Ensemble gradient boosting modern dengan regularisasi L1/L2 yang kuat untuk meminimalkan kesalahan klasifikasi bertahap.", "n_estimators=350, max_depth=5, learning_rate=0.06, subsample=0.85, colsample_bytree=0.80, reg_lambda=2.0, reg_alpha=0.2"]
    ]
    add_styled_table(s8, Inches(6.45), Inches(1.35), Inches(6.43), Inches(5.5), m_headers, m_rows, font_size=10)

    # --- SLIDE 9: Bagian I - Evaluasi & Perbandingan Model ---
    s9 = prs.slides.add_slide(blank_layout)
    add_header_banner(s9, "I", "Evaluasi & Perbandingan Performa Model (M5 & M6)", "Perbandingan adil ketiga algoritma pada 5-Fold Group-CV (Train) dan Hold-Out Test Set (962 Citra)")
    ev_headers = ["Algoritma Model", "Baseline CV F1", "Tuned CV F1 (Train)", "Test Accuracy", "Test Precision", "Test Recall", "Test F1-Macro", "Test ROC-AUC", "Ukuran"]
    ev_rows = [
        ["Dummy (Stratified)", "0,2447", "—", "25,23%", "0,2446", "0,2453", "0,2447", "0,4974", "—"],
        ["SVM (RBF) [MODEL FINAL]", "0,9769", "0,9761", "98,75%", "0,9853", "0,9889", "0,9867", "1,0000", "0,28 MB"],
        ["XGBoost", "0,9749", "0,9716", "98,75%", "0,9894", "0,9844", "0,9865", "0,9996", "0,38 MB"],
        ["Random Forest", "0,9576", "0,9540", "97,51%", "0,9733", "0,9733", "0,9733", "0,9996", "1,43 MB"]
    ]
    add_styled_table(s9, Inches(0.45), Inches(1.35), Inches(12.43), Inches(2.25), ev_headers, ev_rows, font_size=10)
    if (FIGURES_DIR / "05_model_comparison.png").exists():
        s9.shapes.add_picture(str(FIGURES_DIR / "05_model_comparison.png"), Inches(0.45), Inches(3.75), height=Inches(3.2))
    if (FIGURES_DIR / "06_confusion_matrices.png").exists():
        s9.shapes.add_picture(str(FIGURES_DIR / "06_confusion_matrices.png"), Inches(6.35), Inches(3.75), width=Inches(6.5))

    # --- SLIDE 10: Bagian J - Pemilihan Model Terbaik & Analisis Mendalam ---
    s10 = prs.slides.add_slide(blank_layout)
    add_header_banner(s10, "J", "Pemilihan Model Terbaik & Analisis Mengapa (Bab 10 Panduan)", "Analisis model terbaik, model terendah, overfitting, kesalahan prediksi, dan pengaruh fitur")
    add_bullet_card(
        s10, Inches(0.45), Inches(1.35), Inches(6.5), Inches(5.5),
        "5 Analisis Kritis Hasil Eksperimen",
        [
            "1. Mengapa SVM (RBF) Dipilih sebagai Model Final (Bukan Sekadar Accuracy): Walaupun SVM dan XGBoost sama-sama meraih Test Accuracy 98,75%, SVM dipilih karena memiliki 5-Fold Group-CV F1-Macro tertinggi di data latih (0,9761), Test F1-Macro tertinggi (0,9867), Test Recall Macro tertinggi (0,9889), ROC-AUC sempurna (1,0000), waktu training tercepat (4,27s), dan ukuran file paling ringan (0,28 MB).",
            "2. Mengapa Random Forest Performanya Paling Rendah (97,51%): Pembagian pohon keputusan bersifat axis-aligned (tegak lurus sumbu fitur tunggal), sehingga sedikit kurang presisi dibanding kernel RBF atau boosting saat memisahkan batas kontinu antara fitur warna/tekstur Bacterial Blight dan Blast.",
            "3. Analisis Overfitting / Underfitting: Selisih (gap) F1-Macro antara Train (1,0000) dan Test (0,9867) pada SVM hanya 0,0133 (1,33%), membuktikan model tidak mengalami overfitting berat dan mampu menggeneralisasi pada 172 spesimen daun baru.",
            "4. Analisis Kesalahan Prediksi (Confusion Matrix): Kelas Brownspot (240/240) dan Tungro (260/260) terprediksi 100% benar. Kesalahan 12 citra (1,25%) hanya terjadi antara Bacterial Blight dan Blast karena lesi stadium lanjut keduanya sama-sama berupa bercak pucat keabu-abuan."
        ]
    )
    if (FIGURES_DIR / "07_feature_importance.png").exists():
        s10.shapes.add_picture(str(FIGURES_DIR / "07_feature_importance.png"), Inches(7.15), Inches(1.45), width=Inches(5.7))
    add_bullet_card(
        s10, Inches(7.15), Inches(5.25), Inches(5.7), Inches(1.6),
        "5. Pengaruh Fitur (Feature Importance)",
        [
            "Fitur paling menentukan adalah ketajaman tepi bercak (`sobel_edge_p90`, `sobel_edge_std`), rasio bercak di tengah daun (`center_lesion_ratio`), keteraturan tekstur (`glcm_correlation_std`), serta rasio bercak pucat & cokelat nekrotik."
        ]
    )

    # --- SLIDE 11: Bagian K - Implementasi Aplikasi ---
    s11 = prs.slides.add_slide(blank_layout)
    add_header_banner(s11, "K", "Implementasi Aplikasi Web Berbasis Streamlit (M7)", "Arsitektur end-to-end, teknologi, dan alur Input -> Process -> Output yang konsisten")
    add_bullet_card(
        s11, Inches(0.45), Inches(1.35), Inches(4.0), Inches(5.5),
        "1. INPUT (Pengguna)",
        [
            "Unggah file citra daun padi (.jpg, .jpeg, .png) melalui `st.file_uploader`.",
            "Atau klik salah satu dari 4 tombol Skenario Contoh Citra Uji (Blight, Blast, Brownspot, Tungro) dari hold-out test set.",
            "Pilih algoritma model pada sidebar: SVM (RBF) [Model Final], XGBoost, atau Random Forest."
        ]
    )
    add_bullet_card(
        s11, Inches(4.65), Inches(1.35), Inches(4.0), Inches(5.5),
        "2. PROCESS (Validasi & Pipeline)",
        [
            "Validasi Otomatis (FR-02): Menolak file rusak, resolusi < 32×32 px, atau gambar kosong/polos satu warna (pixel std < 3,0).",
            "Preprocessing Konsisten: Memanggil fungsi `extract_features_from_image()` di `src/preprocessing.py` yang identik 100% dengan saat training.",
            "Menjalankan pipeline `.joblib` (`StandardScaler` + Classifier) dalam waktu < 0,2 detik."
        ]
    )
    add_bullet_card(
        s11, Inches(8.85), Inches(1.35), Inches(4.0), Inches(5.5),
        "3. OUTPUT (Diagnosis & Edukasi)",
        [
            "Nama penyakit (Bahasa Indonesia & Inggris) + persentase keyakinan (Confidence Score %).",
            "Grafik distribusi probabilitas untuk keempat kelas penyakit.",
            "Profil Visual & Tekstur Daun (% Hijau Sehat, % Kuning Klorosis, % Bercak Nekrotik, Kontras GLCM).",
            "Penjelasan penyebab patogen, gejala, saran pengendalian pertanian, & disclaimer."
        ]
    )

    # --- SLIDE 12: Bagian L - Demo Project ---
    s12 = prs.slides.add_slide(blank_layout)
    add_header_banner(s12, "L", "Demonstrasi Aplikasi PadiGuard (3 Halaman Interaktif)", "Skenario pengujian langsung pada aplikasi Streamlit lokal (http://localhost:8501)")
    demo_headers = ["Halaman Aplikasi", "File Kode Sumber", "Fitur yang Didemonstrasikan secara Langsung"]
    demo_rows = [
        ["1. Beranda & Deteksi Penyakit", "app.py", "Unggah foto daun padi / klik 4 tombol sampel uji (Blight, Blast, Brownspot, Tungro), ganti algoritma model di sidebar, lihat perubahan probabilitas 4 kelas, metrik profil bercak daun, & rekomendasi penanganan."],
        ["2. Dashboard Evaluasi Model", "pages/1_Model_Evaluation.py", "Kartu KPI audit 5.932 citra, 4 tab interaktif: Tabel & grafik perbandingan 3 model, Confusion Matrix & metrik per kelas, Feature Importance & EDA, serta tabel uji ablasi data leakage."],
        ["3. Tentang Proyek & Literatur", "pages/2_About_Project.py", "Ensiklopedia 4 penyakit daun padi, penjelasan arsitektur ekstraksi 100 fitur & StratifiedGroupKFold, tabel studi literatur 5 jurnal, serta batasan sistem & etika penggunaan."]
    ]
    add_styled_table(s12, Inches(0.45), Inches(1.35), Inches(12.43), Inches(2.85), demo_headers, demo_rows, font_size=10.5)
    add_bullet_card(
        s12, Inches(0.45), Inches(4.4), Inches(12.43), Inches(2.45),
        "Hasil Pengujian Skenario Sampel Data Uji pada Aplikasi (Model Final: SVM RBF)",
        [
            "• Sampel Uji 1 (`BACTERAILBLIGHT3_006.jpg`)  →  Prediksi: Hawar Daun Bakteri (Bacterial Blight)  |  Confidence: 99,77%  (Cocok dengan Label Aktual)",
            "• Sampel Uji 2 (`BLAST1_003.jpg`)            →  Prediksi: Penyakit Blas (Rice Blast)             |  Confidence: 99,51%  (Cocok dengan Label Aktual)",
            "• Sampel Uji 3 (`BROWNSPOT1_004.jpg`)        →  Prediksi: Bercak Cokelat (Brown Spot)            |  Confidence: 99,60%  (Cocok dengan Label Aktual)",
            "• Sampel Uji 4 (`TUNGRO1_004.jpg`)           →  Prediksi: Penyakit Tungro                        |  Confidence: 99,66%  (Cocok dengan Label Aktual)"
        ]
    )

    # --- SLIDE 13: Bagian M - Kesimpulan ---
    s13 = prs.slides.add_slide(blank_layout)
    add_header_banner(s13, "M", "Kesimpulan Utama Project", "Intisari pencapaian eksperimen data, pemodelan Machine Learning, dan implementasi aplikasi")
    add_bullet_card(
        s13, Inches(0.45), Inches(1.35), Inches(12.43), Inches(5.5),
        "Intisari Hasil Project Klasifikasi Penyakit Daun Padi",
        [
            "1. Keberhasilan Ekstraksi Fitur Citra Ringan: Kombinasi 100 fitur visual (Histogram HSV/RGB, Color Moments, Tekstur GLCM, Rasio Lesi, dan Gradien Tepi Sobel) terbukti mampu membedakan 4 penyakit daun padi dengan sangat akurat tanpa memerlukan pelatihan CNN berat di GPU.",
            "2. Pentingnya Audit Duplikat & Group-Aware Split: Audit menemukan 1.138 duplikat MD5 (19,18%) dan struktur 858 spesimen daun fisik dari 5.932 citra. Penggunaan StratifiedGroupKFold (80:20) berhasil menghilangkan ilusi akurasi 100% akibat augmentation leakage dan memberikan evaluasi yang jujur.",
            "3. Perbandingan 3 Algoritma & Model Terbaik: Dari perbandingan SVM (RBF), Random Forest, dan XGBoost pada 962 citra uji (172 spesimen daun), SVM (RBF) terpilih sebagai model final dengan 5-Fold Group-CV F1-Macro tertinggi (0,9761), Test Accuracy 98,75%, Test F1-Macro 0,9867, Test Recall 0,9889, ROC-AUC 1,0000, dan ukuran file hanya 0,28 MB.",
            "4. Karakteristik Prediksi: Kelas Brownspot dan Tungro teridentifikasi 100% sempurna oleh ketiga algoritma, sedangkan kemiripan visual bercak pucat memanjang antara Bacterial Blight dan Blast hanya menyisakan error 1,25% (12 dari 962 citra).",
            "5. Aplikasi Berfungsi Penuh: Seluruh pipeline telah diintegrasikan ke dalam aplikasi web Streamlit 3 halaman (PadiGuard) yang cepat, bebas emoji berlebihan, responsif di Dark/Light mode, dan siap digunakan."
        ]
    )

    # --- SLIDE 14: Bagian N - Keterbatasan & Pengembangan ---
    s14 = prs.slides.add_slide(blank_layout)
    add_header_banner(s14, "N", "Keterbatasan Sistem & Rencana Pengembangan Lanjutan", "Evaluasi jujur terhadap batasan dataset, model, dan aplikasi beserta solusi ke depan")
    add_bullet_card(
        s14, Inches(0.45), Inches(1.35), Inches(6.05), Inches(5.5),
        "Keterbatasan Saat Ini (Dataset, Model & Aplikasi)",
        [
            "1. Klasifikasi Tertutup 4 Kelas (Closed-Set): Dataset Mendeley (Sethy et al., 2020) hanya berisi 4 kelas daun sakit dan tidak memiliki kelas 'Daun Padi Sehat' maupun kelas objek bukan daun.",
            "2. Sensitivitas Latar Belakang & Pencahayaan: Karena fitur warna dan GLCM dihitung pada keseluruhan citra 128×128, latar belakang yang terlalu ramai (tanah/tangan) atau bayangan ekstrem di lapangan dapat memengaruhi nilai histogram.",
            "3. Kemiripan Bercak Lanjut Blight vs Blast: Pada stadium lanjut, lesi nekrotik pucat kedua penyakit ini memiliki tekstur global yang berdekatan sehingga masih terdapat 1,25% kesalahan silang."
        ]
    )
    add_bullet_card(
        s14, Inches(6.8), Inches(1.35), Inches(6.05), Inches(5.5),
        "Rencana Pengembangan Lanjutan",
        [
            "1. Penambahan Kelas Daun Sehat & Out-of-Distribution (OOD) Detector: Menambahkan kelas 'Healthy Leaf' serta ambang batas entropi/jarak fitur untuk menolak gambar non-daun padi secara otomatis.",
            "2. Segmentasi Daun Otomatis (Background Removal): Menambahkan tahap segmentasi U-Net ringan atau GrabCut sebelum ekstraksi fitur agar histogram warna 100% hanya dihitung pada area helai daun.",
            "3. Ekstraksi Fitur Lokal Berbasis Grid/ROI: Membagi citra daun menjadi 3×3 zona lokal (ujung, tengah, pangkal daun) untuk membedakan pola rambatan tepi Bacterial Blight dari bercak belah ketupat Blast."
        ]
    )

    # --- SLIDE 15: Bagian O - Pembagian Tugas ---
    s15 = prs.slides.add_slide(blank_layout)
    add_header_banner(s15, "O", "Pembagian Tugas & Kontribusi Anggota Kelompok", "Setiap anggota memiliki kontribusi nyata dan memahami keseluruhan alur project")
    t_headers = ["Anggota Kelompok", "Peran Utama", "Tanggung Jawab & Kontribusi Nyata", "File & Deliverable yang Dihasilkan"]
    t_rows = [
        ["Mahasiswa 1\n[Nama Anggota 1]\nNIM: [Isi NIM 1]", "Data Engineering, Computer Vision & Preprocessing", "• Mengaudit 5.932 citra, mendeteksi 1.138 duplikat MD5 & 858 grup spesimen daun.\n• Merancang ekstraksi 100 fitur visual (HSV, RGB, Moments, GLCM, Rasio Lesi, Sobel).\n• Menyusun EDA visual & pembagian StratifiedGroupKFold 80:20.", "• src/data_loader.py\n• src/preprocessing.py\n• notebooks/01_data_understanding.ipynb\n• notebooks/02_eda.ipynb\n• notebooks/03_preprocessing.ipynb"],
        ["Mahasiswa 2\n[Nama Anggota 2]\nNIM: [Isi NIM 2]", "Machine Learning Modeling, Tuning & Evaluation", "• Melatih baseline 3 algoritma (SVM, RF, XGBoost) + Dummy dengan 5-Fold Group-CV.\n• Melakukan hyperparameter tuning, uji ablasi leakage, & evaluasi hold-out test set.\n• Menganalisis confusion matrix, overfitting, & feature importance.", "• src/train.py\n• src/evaluate.py\n• models/*.joblib\n• reports/figures/*.png\n• notebooks/04_model_training.ipynb\n• notebooks/05_model_evaluation.ipynb"],
        ["Mahasiswa 3\n[Nama Anggota 3]\nNIM: [Isi NIM 3]", "Streamlit Web Application, Literatur & Dokumentasi", "• Membangun aplikasi Streamlit 3 halaman dengan ikon SVG & validasi input (FR-02).\n• Mengintegrasikan modul inferensi cepat (`src/predict.py`).\n• Menyusun tabel 5 jurnal studi literatur, PRD, README, PPT, & skrip video demo.", "• app.py\n• pages/1_Model_Evaluation.py\n• pages/2_About_Project.py\n• src/predict.py & src/ui_icons.py\n• PRD.md, README.md & PPT"]
    ]
    add_styled_table(s15, Inches(0.45), Inches(1.35), Inches(12.43), Inches(5.5), t_headers, t_rows, font_size=10.5)

    pptx_path = SUBMISSION_DIR / "PPT_Laporan_Project_TEK1302_Klasifikasi_Penyakit_Daun_Padi.pptx"
    prs.save(pptx_path)
    print(f"Saved PPTX (15 slides, Sections A-O) to: {pptx_path}")
    return pptx_path


def build_portfolio_docx():
    """Generate the CLASS-IPB Portofolio Project Word document (Bab 17 of PDF guide)."""
    SUBMISSION_DIR.mkdir(parents=True, exist_ok=True)
    doc = Document()

    title = doc.add_heading("PORTOFOLIO PROJECT AKHIR PEMBELAJARAN MESIN (TEK1302)", level=0)
    title.alignment = 1

    p_sub = doc.add_paragraph("Program Studi Teknologi Rekayasa Komputer — Sekolah Vokasi IPB University")
    p_sub.alignment = 1

    # 1. Identitas Kelompok & Judul Project
    doc.add_heading("1. Identitas Kelompok, Judul Project, dan Referensi Utama", level=1)
    t_id = doc.add_table(rows=7, cols=2)
    t_id.style = "Table Grid"
    id_rows = [
        ("Judul Project", "Klasifikasi Penyakit Daun Padi Berbasis Ekstraksi Fitur Citra (HSV, RGB, GLCM, Sobel) dan Supervised Machine Learning (PadiGuard)"),
        ("Kelas / Kelompok", "[Isi Kelas, misal: A] / [Isi Nama Kelompok, misal: Kelompok 03]"),
        ("Anggota 1 (Data & Preprocessing)", "[Nama Anggota 1] — NIM: [Isi NIM 1]"),
        ("Anggota 2 (Modeling & Evaluasi)", "[Nama Anggota 2] — NIM: [Isi NIM 2]"),
        ("Anggota 3 (Aplikasi & Dokumentasi)", "[Nama Anggota 3] — NIM: [Isi NIM 3]"),
        ("Jurnal Referensi Utama", "Sethy, P. K., Barpanda, N. K., Rath, A. K., & Behera, S. K. (2020). Deep feature based rice leaf disease identification using support vector machine. Computers and Electronics in Agriculture, 175, 105527. https://doi.org/10.1016/j.compag.2020.105527"),
        ("5 Jurnal Studi Literatur", "1. Sethy et al. (2020) — Computers and Electronics in Agriculture\n2. Prajapati et al. (2017) — Intelligent Decision Technologies\n3. Azim et al. (2021) — Agronomy (MDPI)\n4. Pothen & Pai (2020) — IEEE I-SMAC\n5. Haruna et al. (2023) — Indonesian Journal of Electrical Engineering and Computer Science"),
    ]
    for idx, (k, v) in enumerate(id_rows):
        t_id.cell(idx, 0).text = k
        t_id.cell(idx, 1).text = v

    # 2. Tautan Dataset, Source Code, dan Aplikasi
    doc.add_heading("2. Tautan Dataset, Source Code, Video Demo, dan Aplikasi", level=1)
    t_links = doc.add_table(rows=5, cols=2)
    t_links.style = "Table Grid"
    link_rows = [
        ("Tautan Sumber Dataset Resmi", "Mendeley Data (Rice Leaf Disease Image Samples — 5.932 citra, 4 kelas): https://data.mendeley.com/datasets/fwcj7stb8r/1 (DOI: 10.17632/fwcj7stb8r.1)"),
        ("Tautan Repository / Source Code", "[Masukkan Link GitHub / Google Drive Folder ML2026_Kelas_NamaKelompok_JudulProject]"),
        ("Tautan Web / Aplikasi Streamlit", "Lokal: http://localhost:8501 (`streamlit run app.py`) | Cloud (jika di-deploy): [Masukkan Link Streamlit Cloud jika ada]"),
        ("Tautan Video Demo (Maks 7 Menit)", "[Masukkan Link YouTube / Google Drive Video Demo]"),
        ("Nama Folder Pengumpulan", "ML2026_[Kelas]_[NamaKelompok]_KlasifikasiPenyakitDaunPadi"),
    ]
    for idx, (k, v) in enumerate(link_rows):
        t_links.cell(idx, 0).text = k
        t_links.cell(idx, 1).text = v

    # 3. Penjelasan Implementasi Machine Learning
    doc.add_heading("3. Penjelasan Implementasi Machine Learning", level=1)

    doc.add_heading("3.1 Audit Dataset & Preprocessing Citra", level=2)
    doc.add_paragraph(
        "Dataset terdiri dari 5.932 citra daun padi yang terbagi ke dalam 4 kelas penyakit: Bacterial Blight (1.584 citra), "
        "Blast (1.440 citra), Brown Spot (1.600 citra), dan Tungro (1.308 citra). Audit kualitas data menemukan 0 file rusak, "
        "156 citra berformat RGBA (4 kanal), variasi ukuran resolusi (77,95% berukuran 300x300 piksel), serta 1.138 citra duplikat "
        "byte identik berdasarkan MD5 hash (19,18%). Seluruh 1.138 duplikat MD5 dihapus sebelum pemodelan sehingga diperoleh 4.794 citra unik."
    )
    doc.add_paragraph(
        "Setiap citra dikonversi ke RGB 3 kanal di atas latar putih, di-resize ke 128x128 piksel, lalu diekstraksi menjadi 100 fitur numerik: "
        "(1) 32 fitur Histogram Warna HSV, (2) 24 fitur Histogram Warna RGB, (3) 18 fitur Color Moments (Mean, Std, Skewness pada R,G,B,H,S,V), "
        "(4) 12 fitur Tekstur GLCM (Contrast, Dissimilarity, Homogeneity, Energy, Correlation, ASM — Mean & Std), serta "
        "(5) 14 fitur Rasio Lesi Spesifik (hijau sehat, kuning-oranye klorosis, cokelat nekrotik, lesi pucat, indeks Excess Green/Red, rasio lesi tengah) "
        "dan statistik gradien tepi Sobel. Seluruh fitur distandarisasi menggunakan StandardScaler di dalam sklearn.pipeline.Pipeline."
    )

    doc.add_heading("3.2 Pembagian Data Training & Testing (80:20 StratifiedGroupKFold)", level=2)
    doc.add_paragraph(
        "Ke-4.794 citra unik berasal dari 858 spesimen daun fisik unik yang mengalami augmentasi rotasi/flip. "
        "Untuk mencegah augmentation data leakage antara data latih dan data uji, pemisahan 80:20 dilakukan menggunakan StratifiedGroupKFold "
        "(random_state=42) berdasarkan ID spesimen daun (leaf_group), menghasilkan:\n"
        "• Data Training: 3.832 citra unik (686 spesimen daun fisik) — digunakan untuk training dan hyperparameter tuning via 5-Fold StratifiedGroupKFold CV.\n"
        "• Data Testing (Hold-Out): 962 citra unik (172 spesimen daun fisik) — tidak pernah dilihat selama training/tuning dan hanya dievaluasi satu kali di akhir."
    )

    doc.add_heading("3.3 Perbandingan 3 Algoritma Klasifikasi pada Hold-Out Test Set (962 Citra)", level=2)
    t_ev = doc.add_table(rows=5, cols=7)
    t_ev.style = "Table Grid"
    ev_h = ["Algoritma Model", "5-Fold CV F1 (Train)", "Test Accuracy", "Test Precision", "Test Recall", "Test F1-Macro", "Test ROC-AUC"]
    for c_i, h_str in enumerate(ev_h):
        t_ev.cell(0, c_i).text = h_str
    ev_data = [
        ["Dummy (Stratified)", "0,2447", "25,23%", "0,2446", "0,2453", "0,2447", "0,4974"],
        ["SVM (RBF, C=10, balanced) [FINAL]", "0,9761", "98,75%", "0,9853", "0,9889", "0,9867", "1,0000"],
        ["XGBoost (n=350, depth=5, lr=0,06)", "0,9716", "98,75%", "0,9894", "0,9844", "0,9865", "0,9996"],
        ["Random Forest (n=300, depth=16)", "0,9540", "97,51%", "0,9733", "0,9733", "0,9733", "0,9996"],
    ]
    for r_i, r_vals in enumerate(ev_data):
        for c_i, val in enumerate(r_vals):
            t_ev.cell(r_i + 1, c_i).text = val

    # 4. Analisis Mendalam
    doc.add_heading("4. Analisis Mendalam: Ablasi Data Leakage, Pemilihan Model & Error Analysis", level=1)
    doc.add_paragraph(
        "1. Analisis Mendalam Dampak Duplikat & Augmentation Leakage: Uji ablasi membuktikan bahwa apabila model Random Forest dilatih "
        "tanpa menghapus 1.138 duplikat MD5 atau dibagi dengan random split biasa tanpa pengelompokan spesimen daun (leaf_group), "
        "skor Test Accuracy mencapai 100,00% (F1-Macro 1,0000) secara semu karena variasi rotasi dari helai daun fisik yang sama bocor ke data uji. "
        "Dengan menerapkan deduplikasi MD5 diikuti StratifiedGroupKFold berdasarkan 858 spesimen daun fisik, evaluasi menjadi murni bebas leakage (Test Accuracy 97,51% pada RF dan 98,75% pada SVM/XGBoost)."
    )
    doc.add_paragraph(
        "2. Alasan Pemilihan Model Terbaik (Bukan Sekadar Accuracy): SVM (RBF) dan XGBoost sama-sama memperoleh Test Accuracy 98,75% (950/962 citra benar). "
        "Namun, SVM (RBF) dipilih sebagai model final karena meraih skor 5-Fold Group-CV F1-Macro tertinggi pada data training (0,9761), "
        "Test F1-Macro tertinggi (0,9867), Test Recall Macro tertinggi (0,9889 — sangat penting agar tanaman sakit tidak lolos dari deteksi), "
        "ROC-AUC sempurna (1,0000), serta ukuran model paling ringan (0,28 MB vs 0,38 MB pada XGBoost dan 1,43 MB pada Random Forest)."
    )
    doc.add_paragraph(
        "3. Error Analysis & Feature Importance: Berdasarkan Confusion Matrix pada 962 citra uji, kelas Brownspot (240/240) dan Tungro (260/260) "
        "terklasifikasi 100% sempurna oleh ketiga model karena profil warnanya sangat khas (Tungro dominan spektrum kuning-oranye klorosis; "
        "Brownspot memiliki kontras tekstur GLCM dan bintik cokelat nekrotik tertinggi). Kesalahan minor sebanyak 12 citra (2 spesimen daun fisik, atau 1,25%) "
        "hanya terjadi antara Bacterial Blight dan Blast karena pada stadium lanjut kedua penyakit tersebut sama-sama meninggalkan lesi nekrotik pucat keabu-abuan. "
        "Analisis Feature Importance menunjukkan bahwa 5 fitur terpenting adalah sobel_edge_p90, center_lesion_ratio, glcm_correlation_std, sobel_edge_std, dan glcm_correlation_mean."
    )

    if (FIGURES_DIR / "05_model_comparison.png").exists():
        doc.add_picture(str(FIGURES_DIR / "05_model_comparison.png"), width=DocxInches(5.8))
    if (FIGURES_DIR / "06_confusion_matrices.png").exists():
        doc.add_picture(str(FIGURES_DIR / "06_confusion_matrices.png"), width=DocxInches(6.0))

    docx_path = SUBMISSION_DIR / "KELAS_KELOMPOK_Portofolio_Project.docx"
    doc.save(docx_path)
    print(f"Saved Word Portfolio Document to: {docx_path}")
    return docx_path


if __name__ == "__main__":
    build_pptx()
    build_portfolio_docx()
