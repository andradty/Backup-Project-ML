"""Utility module for Rice Leaf Disease Classification."""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATASET_DIR = BASE_DIR / "penyakit padi"
DATA_PROCESSED_DIR = BASE_DIR / "data" / "processed"
MODELS_DIR = BASE_DIR / "models"
REPORTS_DIR = BASE_DIR / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"

CLASSES = ["Bacterialblight", "Blast", "Brownspot", "Tungro"]

CLASS_INFO = {
    "Bacterialblight": {
        "nama_id": "Hawar Daun Bakteri (Bacterial Blight)",
        "penyebab": "Bakteri Xanthomonas oryzae pv. oryzae",
        "gejala": (
            "Garis-garis basah berwarna hijau keabu-abuan pada tepi daun yang meluas "
            "menjadi bercak memanjang berwarna kuning hingga putih kecokelatan dan mengering."
        ),
        "dampak": "Menurunkan kemampuan fotosintesis daun secara drastis dan menyebabkan gabah hampa (kresek).",
        "penanganan": (
            "Gunakan varietas tahan (seperti Inpari), atur jarak tanam agar tidak terlalu rapat, "
            "hindari pemupukan Nitrogen (Urea) berlebihan, dan jaga sanitasi saluran irigasi."
        ),
        "warna_badge": "#d97706",
    },
    "Blast": {
        "nama_id": "Penyakit Blas (Rice Blast)",
        "penyebab": "Jamur Pyricularia oryzae (Magnaporthe oryzae)",
        "gejala": (
            "Bercak berbentuk belah ketupat (diamond/spindle-shaped) dengan bagian tengah "
            "berwarna abu-abu keputihan dan tepi cokelat kemerahan atau kehitaman."
        ),
        "dampak": "Dapat mematahkan leher malai (blas leher) dan mematikan daun sebelum pengisian bulir.",
        "penanganan": (
            "Pemupukan berimbang (kurangi N berlebih, tambahkan Kalium & Silika), perawatan benih, "
            "pengaturan kelembapan lahan, serta aplikasi fungisida berbahan aktif trisiklazol atau isoprotiolan bila melewati ambang batas."
        ),
        "warna_badge": "#dc2626",
    },
    "Brownspot": {
        "nama_id": "Bercak Cokelat (Brown Spot)",
        "penyebab": "Jamur Bipolaris oryzae (Cochliobolus miyabeanus)",
        "gejala": (
            "Bercak bulat hingga oval kecil berwarna cokelat tua hingga kehitaman yang tersebar "
            "merata di permukaan helai daun, terkadang dikelilingi lingkaran (halo) kekuningan."
        ),
        "dampak": "Sering muncul pada tanah kurang subur/kahat hara, menurunkan bobot dan kualitas biji gabah.",
        "penanganan": (
            "Perbaiki kesuburan tanah (tambahkan pupuk Kalium, Kalsium, dan unsur mikro), gunakan benih sehat "
            "bersertifikat, dan lakukan fungisida selektif jika serangan meluas."
        ),
        "warna_badge": "#92400e",
    },
    "Tungro": {
        "nama_id": "Penyakit Tungro",
        "penyebab": "Kombinasi Rice Tungro Bacilliform Virus (RTBV) & Rice Tungro Spherical Virus (RTSV) yang ditularkan Wereng Hijau (Nephotettix virescens)",
        "gejala": (
            "Perubahan warna daun muda menjadi kuning hingga jingga-oranye dimulai dari ujung daun, "
            "disertai tanaman kerdil dan berkurangnya jumlah anakan."
        ),
        "dampak": "Menyebabkan tanaman kerdil dan gagal panen jika infeksi terjadi pada fase vegetatif awal.",
        "penanganan": (
            "Tanam serempak untuk memutus siklus wereng hijau, gunakan varietas tahan wereng/tungro, "
            "eradikasi (cabut & musnahkan) rumpun terinfeksi awal, serta kendalikan vektor wereng hijau."
        ),
        "warna_badge": "#ca8a04",
    },
}
