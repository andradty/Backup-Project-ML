"""Image preprocessing and feature extraction module for Rice Leaf Disease Classification.

Extracts 100 interpretable visual features from a single RGB image resized to 128x128:
1. HSV Color Histogram (16 + 8 + 8 = 32 features)
2. RGB Color Histogram (8 + 8 + 8 = 24 features)
3. Color Moments (Mean, Std, Skewness) across R, G, B, H, S, V (18 features)
4. GLCM Texture Features (contrast, dissimilarity, homogeneity, energy, correlation, ASM)
   at distances=[1] and angles=[0, pi/4, pi/2, 3*pi/4], summarized by Mean & Std (12 features)
5. Spatial Lesion / Color Ratios & Shape Proxies (14 features):
   - Green healthy ratio, Yellow/Orange ratio (Tungro indicator), Brown/Dark necrotic ratio,
     Bright/White lesion ratio (Blast/Blight center indicator)
   - Center-crop vs Border color ratios (4 features)
   - Edge density & gradient statistics via Sobel filter (6 features)
"""

from pathlib import Path
from typing import Union
import numpy as np
import pandas as pd
from PIL import Image
from scipy.stats import skew
from skimage.color import rgb2hsv, rgb2gray
from skimage.feature import graycomatrix, graycoprops
from skimage.filters import sobel

IMAGE_SIZE = (128, 128)


def get_feature_names() -> list[str]:
    """Return the exact ordered list of 100 feature names."""
    names = []
    # 1. HSV Histogram (32)
    for i in range(16):
        names.append(f"hsv_h_bin_{i:02d}")
    for i in range(8):
        names.append(f"hsv_s_bin_{i:02d}")
    for i in range(8):
        names.append(f"hsv_v_bin_{i:02d}")

    # 2. RGB Histogram (24)
    for ch in ["r", "g", "b"]:
        for i in range(8):
            names.append(f"rgb_{ch}_bin_{i:02d}")

    # 3. Color Moments (18)
    for ch in ["r", "g", "b", "h", "s", "v"]:
        for stat in ["mean", "std", "skew"]:
            names.append(f"moment_{ch}_{stat}")

    # 4. GLCM Texture (12)
    props = ["contrast", "dissimilarity", "homogeneity", "energy", "correlation", "ASM"]
    for p in props:
        names.append(f"glcm_{p}_mean")
        names.append(f"glcm_{p}_std")

    # 5. Lesion ratios & edge/spatial statistics (14)
    names.extend(
        [
            "ratio_healthy_green",
            "ratio_yellow_orange_tungro",
            "ratio_brown_necrotic",
            "ratio_white_pale_lesion",
            "ratio_background_white_black",
            "exg_excess_green_mean",
            "exg_excess_green_std",
            "exr_excess_red_mean",
            "center_green_ratio",
            "center_lesion_ratio",
            "sobel_edge_mean",
            "sobel_edge_std",
            "sobel_edge_p90",
            "sobel_high_edge_ratio",
        ]
    )
    assert len(names) == 100, f"Expected 100 features, got {len(names)}"
    return names


def load_and_preprocess_image(
    image_input: Union[str, Path, Image.Image], target_size: tuple[int, int] = IMAGE_SIZE
) -> np.ndarray:
    """
    Load an image from file path or PIL Image, convert RGBA/P to RGB on a white background,
    resize to target_size using bilinear interpolation, and return uint8 array of shape (H, W, 3).
    """
    if isinstance(image_input, (str, Path)):
        img = Image.open(image_input)
    elif isinstance(image_input, Image.Image):
        img = image_input
    else:
        raise ValueError(f"Unsupported image input type: {type(image_input)}")

    if img.mode == "RGBA":
        background = Image.new("RGB", img.size, (255, 255, 255))
        background.paste(img, mask=img.split()[3])
        img = background
    elif img.mode != "RGB":
        img = img.convert("RGB")

    img_resized = img.resize(target_size, Image.Resampling.BILINEAR)
    arr = np.asarray(img_resized, dtype=np.uint8)
    return arr


def extract_features_from_array(rgb_uint8: np.ndarray) -> np.ndarray:
    """Extract 100 numerical features from an RGB uint8 numpy array of shape (H, W, 3)."""
    rgb_float = rgb_uint8.astype(np.float32) / 255.0
    hsv = rgb2hsv(rgb_float)  # values in [0, 1]

    r, g, b = rgb_float[:, :, 0], rgb_float[:, :, 1], rgb_float[:, :, 2]
    h, s, v = hsv[:, :, 0], hsv[:, :, 1], hsv[:, :, 2]

    feats = []

    # 1. HSV Color Histogram (16 + 8 + 8 = 32)
    h_hist, _ = np.histogram(h, bins=16, range=(0.0, 1.0), density=False)
    s_hist, _ = np.histogram(s, bins=8, range=(0.0, 1.0), density=False)
    v_hist, _ = np.histogram(v, bins=8, range=(0.0, 1.0), density=False)
    total_px = float(rgb_uint8.shape[0] * rgb_uint8.shape[1])
    feats.extend(h_hist / total_px)
    feats.extend(s_hist / total_px)
    feats.extend(v_hist / total_px)

    # 2. RGB Color Histogram (8 + 8 + 8 = 24)
    for ch in (r, g, b):
        c_hist, _ = np.histogram(ch, bins=8, range=(0.0, 1.0), density=False)
        feats.extend(c_hist / total_px)

    # 3. Color Moments (Mean, Std, Skew) across R, G, B, H, S, V (18)
    for ch in (r, g, b, h, s, v):
        flat = ch.ravel()
        mean_val = float(np.mean(flat))
        std_val = float(np.std(flat))
        if std_val < 1e-6:
            skew_val = 0.0
        else:
            skew_val = float(skew(flat))
            if np.isnan(skew_val) or np.isinf(skew_val):
                skew_val = 0.0
        feats.extend([mean_val, std_val, skew_val])

    # 4. GLCM Texture Features (12)
    gray_float = rgb2gray(rgb_float)
    # Quantize to 32 levels (0..31) for fast & stable GLCM
    gray_q = np.clip((gray_float * 31).astype(np.uint8), 0, 31)
    glcm = graycomatrix(
        gray_q,
        distances=[1, 2],
        angles=[0, np.pi / 4, np.pi / 2, 3 * np.pi / 4],
        levels=32,
        symmetric=True,
        normed=True,
    )
    props = ["contrast", "dissimilarity", "homogeneity", "energy", "correlation", "ASM"]
    for p in props:
        val = graycoprops(glcm, p)
        feats.append(float(np.mean(val)))
        feats.append(float(np.std(val)))

    # 5. Spatial Lesion / Color Ratios & Shape Proxies (14)
    # Healthy green: Hue roughly 65..165 deg (0.18..0.46), S > 0.2, V > 0.2
    healthy_mask = (h >= 0.18) & (h <= 0.46) & (s >= 0.20) & (v >= 0.20)
    # Yellow/Orange (Tungro / chlorosis): Hue roughly 25..65 deg (0.07..0.18), S > 0.25, V > 0.3
    yellow_mask = (h >= 0.07) & (h < 0.18) & (s >= 0.25) & (v >= 0.30)
    # Brown / dark necrotic (Brownspot / Blast border): Hue < 0.12 or low V with medium S
    brown_mask = ((h < 0.12) & (s >= 0.20) & (v >= 0.15) & (v <= 0.75)) | (
        (v >= 0.10) & (v < 0.40) & (s >= 0.15)
    )
    # Pale / gray-white lesion center (Blast / Bacterial blight dry streak)
    pale_lesion_mask = (s < 0.25) & (v >= 0.45) & (v < 0.92)
    # Pure white or pure black background
    bg_mask = ((s < 0.08) & (v >= 0.92)) | (v < 0.08)

    exg = 2.0 * g - r - b  # Excess Green Index
    exr = 1.4 * r - g  # Excess Red Index

    H_sz, W_sz = rgb_uint8.shape[:2]
    h4, w4 = H_sz // 4, W_sz // 4
    center_green = float(np.mean(healthy_mask[h4 : 3 * h4, w4 : 3 * w4]))
    center_lesion = float(
        np.mean((yellow_mask | brown_mask | pale_lesion_mask)[h4 : 3 * h4, w4 : 3 * w4])
    )

    edges = sobel(gray_float)
    edge_mean = float(np.mean(edges))
    edge_std = float(np.std(edges))
    edge_p90 = float(np.percentile(edges, 90))
    high_edge_ratio = float(np.mean(edges > 0.08))

    feats.extend(
        [
            float(np.mean(healthy_mask)),
            float(np.mean(yellow_mask)),
            float(np.mean(brown_mask)),
            float(np.mean(pale_lesion_mask)),
            float(np.mean(bg_mask)),
            float(np.mean(exg)),
            float(np.std(exg)),
            float(np.mean(exr)),
            center_green,
            center_lesion,
            edge_mean,
            edge_std,
            edge_p90,
            high_edge_ratio,
        ]
    )

    feat_arr = np.asarray(feats, dtype=np.float32)
    feat_arr = np.nan_to_num(feat_arr, nan=0.0, posinf=0.0, neginf=0.0)
    return feat_arr


def extract_features_from_image(
    image_input: Union[str, Path, Image.Image], target_size: tuple[int, int] = IMAGE_SIZE
) -> np.ndarray:
    """Load, preprocess, and extract 100 features from a single image."""
    arr = load_and_preprocess_image(image_input, target_size=target_size)
    return extract_features_from_array(arr)


def validate_uploaded_image(image_input: Union[str, Path, Image.Image]) -> tuple[bool, str, dict]:
    """
    Validate an uploaded image for the Streamlit app (FR-02).
    Checks readability, minimum dimensions (>= 32x32), non-blank variance, and returns image diagnostics.
    """
    try:
        if isinstance(image_input, (str, Path)):
            img = Image.open(image_input)
        elif isinstance(image_input, Image.Image):
            img = image_input
        else:
            return False, "Format input gambar tidak dikenali.", {}

        width, height = img.size
        mode = img.mode
        if width < 32 or height < 32:
            return (
                False,
                f"Resolusi gambar terlalu kecil ({width}x{height} px). Minimal 32x32 piksel.",
                {"width": width, "height": height, "mode": mode},
            )

        arr = load_and_preprocess_image(img)
        std_val = float(np.std(arr))
        if std_val < 3.0:
            return (
                False,
                "Gambar tampak kosong atau hanya satu warna polos (variansi piksel terlalu rendah).",
                {"width": width, "height": height, "mode": mode, "pixel_std": round(std_val, 2)},
            )

        feats = extract_features_from_array(arr)
        feat_names = get_feature_names()
        feat_dict = dict(zip(feat_names, feats))

        info = {
            "width": width,
            "height": height,
            "mode": mode,
            "pixel_std": round(float(std_val), 2),
            "ratio_healthy_green": round(100.0 * float(feat_dict["ratio_healthy_green"]), 1),
            "ratio_yellow_orange": round(100.0 * float(feat_dict["ratio_yellow_orange_tungro"]), 1),
            "ratio_brown_necrotic": round(100.0 * float(feat_dict["ratio_brown_necrotic"]), 1),
            "ratio_pale_lesion": round(100.0 * float(feat_dict["ratio_white_pale_lesion"]), 1),
            "glcm_contrast": round(float(feat_dict["glcm_contrast_mean"]), 2),
            "glcm_homogeneity": round(float(feat_dict["glcm_homogeneity_mean"]), 3),
        }
        return True, "Gambar valid dan siap diprediksi.", info
    except Exception as e:
        return False, f"Gagal membaca file gambar: {e}", {}
