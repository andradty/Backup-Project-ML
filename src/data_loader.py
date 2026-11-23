"""Data loading and dataset auditing module for Rice Leaf Disease Classification."""

import hashlib
import re
from pathlib import Path
import pandas as pd
from PIL import Image
from src import DATASET_DIR, CLASSES, DATA_PROCESSED_DIR


def extract_leaf_group_id(class_name: str, filename: str) -> str:
    """
    Extract the base leaf specimen ID from Sethy et al. (2020) Mendeley dataset filenames.
    For example, BLAST1_045.jpg, BLAST2_045.jpg, ..., BLAST9_045.jpg are augmented
    views (rotations/flips) of the same physical leaf specimen #045 in class Blast.
    Grouping by (class_name, leaf_num) prevents data leakage across train and test sets!
    """
    nums = re.findall(r"\d+", filename)
    leaf_num = int(nums[-1]) if nums else 0
    return f"{class_name}_{leaf_num:04d}"


def scan_dataset(dataset_dir: Path = DATASET_DIR) -> pd.DataFrame:
    """
    Scan all image files in dataset_dir, computing MD5 hash, dimensions, color mode,
    file size, duplicate hash flags, and physical leaf specimen group ID.
    """
    records = []
    seen_hashes = {}

    for label_idx, class_name in enumerate(CLASSES):
        class_dir = dataset_dir / class_name
        if not class_dir.exists():
            continue
        files = sorted([f for f in class_dir.iterdir() if f.is_file()])
        for file_path in files:
            raw_bytes = file_path.read_bytes()
            md5_hash = hashlib.md5(raw_bytes).hexdigest()
            file_size_kb = len(raw_bytes) / 1024.0

            is_duplicate = md5_hash in seen_hashes
            duplicate_of = seen_hashes.get(md5_hash, None)
            if not is_duplicate:
                seen_hashes[md5_hash] = str(file_path.relative_to(dataset_dir))

            width, height, mode = 0, 0, "INVALID"
            is_corrupt = False
            try:
                with Image.open(file_path) as img:
                    width, height = img.size
                    mode = img.mode
            except Exception:
                is_corrupt = True

            leaf_group = extract_leaf_group_id(class_name, file_path.name)

            records.append(
                {
                    "filepath": str(file_path),
                    "relpath": str(file_path.relative_to(dataset_dir)),
                    "filename": file_path.name,
                    "class_name": class_name,
                    "label": label_idx,
                    "leaf_group": leaf_group,
                    "width": width,
                    "height": height,
                    "aspect_ratio": round(width / height, 4) if height > 0 else 0.0,
                    "mode": mode,
                    "file_size_kb": round(file_size_kb, 2),
                    "md5_hash": md5_hash,
                    "is_duplicate": is_duplicate,
                    "duplicate_of": duplicate_of,
                    "is_corrupt": is_corrupt,
                }
            )

    df = pd.DataFrame(records)
    return df


def get_dataset_summary(df: pd.DataFrame) -> dict:
    """Return high-level audit statistics from the scanned dataset DataFrame."""
    total_files = len(df)
    corrupt_count = int(df["is_corrupt"].sum())
    dup_count = int(df["is_duplicate"].sum())
    unique_count = total_files - dup_count

    per_class_raw = df.groupby("class_name").size().to_dict()
    per_class_unique = df[~df["is_duplicate"]].groupby("class_name").size().to_dict()
    per_class_dup = df[df["is_duplicate"]].groupby("class_name").size().to_dict()
    per_class_groups = df[~df["is_duplicate"]].groupby("class_name")["leaf_group"].nunique().to_dict()

    modes = df["mode"].value_counts().to_dict()
    resolutions = (
        df.assign(res=df["width"].astype(str) + "x" + df["height"].astype(str))["res"]
        .value_counts()
        .head(10)
        .to_dict()
    )

    return {
        "total_files": total_files,
        "corrupt_count": corrupt_count,
        "duplicate_count": dup_count,
        "duplicate_pct": round(100.0 * dup_count / total_files, 2) if total_files else 0.0,
        "unique_count": unique_count,
        "unique_leaf_specimens": int(df[~df["is_duplicate"]]["leaf_group"].nunique()),
        "per_class_raw": per_class_raw,
        "per_class_unique": per_class_unique,
        "per_class_dup": per_class_dup,
        "per_class_leaf_specimens": per_class_groups,
        "modes": modes,
        "top_resolutions": resolutions,
    }


if __name__ == "__main__":
    DATA_PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    df_meta = scan_dataset()
    meta_path = DATA_PROCESSED_DIR / "metadata_audit.csv"
    df_meta.to_csv(meta_path, index=False)
    summary = get_dataset_summary(df_meta)
    print("Dataset Audit Summary:")
    for k, v in summary.items():
        print(f"  {k}: {v}")
