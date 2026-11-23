"""Model training, group-aware cross-validation, tuning, and artifact generation for Rice Leaf Disease Classification."""

import json
import time
import warnings
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import joblib
import numpy as np
import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import StratifiedGroupKFold, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from xgboost import XGBClassifier

from src import (
    CLASSES,
    DATA_PROCESSED_DIR,
    MODELS_DIR,
    REPORTS_DIR,
)
from src.data_loader import extract_leaf_group_id, get_dataset_summary, scan_dataset
from src.preprocessing import extract_features_from_image, get_feature_names

warnings.filterwarnings("ignore", category=FutureWarning)


def build_feature_dataset(force_rebuild: bool = False) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Scan dataset, extract 100 features for all 5,932 images (reusing cached features if present),
    and return (df_meta, df_all).
    """
    DATA_PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    meta_path = DATA_PROCESSED_DIR / "metadata_audit.csv"
    all_csv_path = DATA_PROCESSED_DIR / "features_all.csv"
    uniq_csv_path = DATA_PROCESSED_DIR / "features_unique.csv"

    df_meta = scan_dataset()
    df_meta.to_csv(meta_path, index=False)

    if not force_rebuild and all_csv_path.exists():
        df_all = pd.read_csv(all_csv_path)
        if "leaf_group" not in df_all.columns:
            df_all["leaf_group"] = [
                extract_leaf_group_id(c, f)
                for c, f in zip(df_all["class_name"], df_all["filename"])
            ]
            df_all.to_csv(all_csv_path, index=False)
            df_unique = df_all[~df_all["is_duplicate"]].reset_index(drop=True)
            df_unique.to_csv(uniq_csv_path, index=False)
        return df_meta, df_all

    print(f"[1/4] Extracting 100 color & GLCM texture features from {len(df_meta)} images...")
    t0 = time.time()
    filepaths = df_meta["filepath"].tolist()

    with ThreadPoolExecutor(max_workers=8) as ex:
        feats_list = list(ex.map(extract_features_from_image, filepaths))

    feat_names = get_feature_names()
    df_feats = pd.DataFrame(np.vstack(feats_list), columns=feat_names)
    df_all = pd.concat(
        [
            df_meta[
                [
                    "filepath",
                    "relpath",
                    "filename",
                    "class_name",
                    "label",
                    "leaf_group",
                    "is_duplicate",
                    "md5_hash",
                ]
            ],
            df_feats,
        ],
        axis=1,
    )
    df_all.to_csv(all_csv_path, index=False)
    df_unique = df_all[~df_all["is_duplicate"]].reset_index(drop=True)
    df_unique.to_csv(uniq_csv_path, index=False)
    print(f"      Feature extraction finished in {time.time() - t0:.1f}s.")
    return df_meta, df_all


def evaluate_predictions(y_true: np.ndarray, y_pred: np.ndarray, y_proba: np.ndarray) -> dict:
    """Compute multi-class evaluation metrics."""
    acc = float(accuracy_score(y_true, y_pred))
    prec_macro = float(precision_score(y_true, y_pred, average="macro", zero_division=0))
    rec_macro = float(recall_score(y_true, y_pred, average="macro", zero_division=0))
    f1_macro = float(f1_score(y_true, y_pred, average="macro", zero_division=0))
    f1_weighted = float(f1_score(y_true, y_pred, average="weighted", zero_division=0))
    roc_auc = float(roc_auc_score(y_true, y_proba, multi_class="ovr", average="macro"))
    return {
        "accuracy": round(acc, 4),
        "precision_macro": round(prec_macro, 4),
        "recall_macro": round(rec_macro, 4),
        "f1_macro": round(f1_macro, 4),
        "f1_weighted": round(f1_weighted, 4),
        "roc_auc_ovr": round(roc_auc, 4),
    }


def run_group_cv_evaluation(
    pipeline: Pipeline, X: pd.DataFrame, y: np.ndarray, groups: np.ndarray, n_splits: int = 5
) -> dict:
    """Run StratifiedGroupKFold CV on training data and return out-of-fold metrics."""
    sgkf = StratifiedGroupKFold(n_splits=n_splits, shuffle=True, random_state=42)
    oof_proba = np.zeros((len(y), len(CLASSES)), dtype=np.float64)
    oof_pred = np.zeros(len(y), dtype=np.int64)

    for train_idx, val_idx in sgkf.split(X, y, groups):
        X_tr, y_tr = X.iloc[train_idx], y[train_idx]
        X_va = X.iloc[val_idx]
        pipeline.fit(X_tr, y_tr)
        oof_proba[val_idx] = pipeline.predict_proba(X_va)
        oof_pred[val_idx] = pipeline.predict(X_va)

    return evaluate_predictions(y, oof_pred, oof_proba)


def train_and_evaluate_all(force_rebuild: bool = False) -> dict:
    """Execute full M4-M6 pipeline: leakage ablation, group-aware split, baseline CV, tuned models, test evaluation."""
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    df_meta, df_all = build_feature_dataset(force_rebuild=force_rebuild)
    feat_names = get_feature_names()

    # --- 1. Leakage & Duplicate Ablation Check ---
    print("[2/4] Running duplicate & augmentation leakage analysis...")
    # A) Naive split WITH exact MD5 duplicates (5,932 images)
    X_raw = df_all[feat_names]
    y_raw = df_all["label"].to_numpy()
    X_tr_raw, X_te_raw, y_tr_raw, y_te_raw = train_test_split(
        X_raw, y_raw, test_size=0.20, stratify=y_raw, random_state=42
    )
    rf_naive = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    rf_naive.fit(X_tr_raw, y_tr_raw)
    acc_with_dup = float(accuracy_score(y_te_raw, rf_naive.predict(X_te_raw)))
    f1_with_dup = float(f1_score(y_te_raw, rf_naive.predict(X_te_raw), average="macro"))

    # B) Deduplicated by MD5 (4,794 unique images), but naive random split (augmentation leakage across split)
    df_unique = df_all[~df_all["is_duplicate"]].reset_index(drop=True)
    X_uniq = df_unique[feat_names]
    y_uniq = df_unique["label"].to_numpy()
    groups_uniq = df_unique["leaf_group"].to_numpy()

    X_tr_u, X_te_u, y_tr_u, y_te_u = train_test_split(
        X_uniq, y_uniq, test_size=0.20, stratify=y_uniq, random_state=42
    )
    rf_naive_u = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    rf_naive_u.fit(X_tr_u, y_tr_u)
    acc_naive_uniq = float(accuracy_score(y_te_u, rf_naive_u.predict(X_te_u)))
    f1_naive_uniq = float(f1_score(y_te_u, rf_naive_u.predict(X_te_u), average="macro"))

    # C) Strict Group-Aware Split (StratifiedGroupKFold 80:20 by physical leaf specimen ID)
    print("[3/4] Performing strict StratifiedGroupKFold 80:20 split by leaf_group (zero specimen leakage)...")
    sgkf_split = StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=42)
    train_idx, test_idx = next(sgkf_split.split(X_uniq, y_uniq, groups_uniq))

    X_train, y_train, groups_train = (
        X_uniq.iloc[train_idx].reset_index(drop=True),
        y_uniq[train_idx],
        groups_uniq[train_idx],
    )
    X_test, y_test, groups_test = (
        X_uniq.iloc[test_idx].reset_index(drop=True),
        y_uniq[test_idx],
        groups_uniq[test_idx],
    )
    df_test_meta = (
        df_unique.iloc[test_idx][
            ["filepath", "relpath", "filename", "class_name", "label", "leaf_group"]
        ]
        .reset_index(drop=True)
    )

    assert len(set(groups_train).intersection(set(groups_test))) == 0, "Group overlap detected!"
    print(
        f"      Train: {len(X_train)} images ({len(set(groups_train))} unique leaf specimens) | "
        f"Test: {len(X_test)} images ({len(set(groups_test))} unique leaf specimens)"
    )

    df_unique.iloc[train_idx].to_csv(DATA_PROCESSED_DIR / "train_features.csv", index=False)
    df_unique.iloc[test_idx].to_csv(DATA_PROCESSED_DIR / "test_features.csv", index=False)

    # --- 2. Baseline Models (M5: 5-fold StratifiedGroupKFold CV on Train Set) ---
    print("[4/4] Training & evaluating Baseline (M5) and Tuned (M6) models...")
    baseline_models = {
        "Dummy (Stratified)": Pipeline(
            [
                ("scaler", StandardScaler()),
                ("clf", DummyClassifier(strategy="stratified", random_state=42)),
            ]
        ),
        "SVM (RBF Baseline)": Pipeline(
            [
                ("scaler", StandardScaler()),
                ("clf", SVC(C=1.0, kernel="rbf", probability=True, random_state=42)),
            ]
        ),
        "Random Forest (Baseline)": Pipeline(
            [
                ("scaler", StandardScaler()),
                ("clf", RandomForestClassifier(n_estimators=100, max_depth=8, random_state=42, n_jobs=-1)),
            ]
        ),
        "XGBoost (Baseline)": Pipeline(
            [
                ("scaler", StandardScaler()),
                (
                    "clf",
                    XGBClassifier(
                        n_estimators=100,
                        max_depth=4,
                        learning_rate=0.1,
                        random_state=42,
                        n_jobs=-1,
                        eval_metric="mlogloss",
                    ),
                ),
            ]
        ),
    }

    baseline_cv_results = {}
    for name, pipe in baseline_models.items():
        t_start = time.time()
        metrics = run_group_cv_evaluation(pipe, X_train, y_train, groups_train, n_splits=5)
        metrics["time_sec"] = round(time.time() - t_start, 2)
        baseline_cv_results[name] = metrics
        print(
            f"  [Baseline 5-Fold Group-CV] {name}: Acc={metrics['accuracy']:.4f}, "
            f"F1-Macro={metrics['f1_macro']:.4f}, ROC-AUC={metrics['roc_auc_ovr']:.4f}"
        )

    # --- 3. Tuned Models (M6: Hyperparameter Tuning via 5-Fold Group-CV & Hold-out Test Evaluation) ---
    tuned_models = {
        "SVM (RBF)": Pipeline(
            [
                ("scaler", StandardScaler()),
                (
                    "clf",
                    SVC(
                        C=10.0,
                        kernel="rbf",
                        gamma="scale",
                        class_weight="balanced",
                        probability=True,
                        random_state=42,
                    ),
                ),
            ]
        ),
        "Random Forest": Pipeline(
            [
                ("scaler", StandardScaler()),
                (
                    "clf",
                    RandomForestClassifier(
                        n_estimators=300,
                        max_depth=16,
                        min_samples_split=4,
                        min_samples_leaf=2,
                        max_features="sqrt",
                        class_weight="balanced_subsample",
                        random_state=42,
                        n_jobs=-1,
                    ),
                ),
            ]
        ),
        "XGBoost": Pipeline(
            [
                ("scaler", StandardScaler()),
                (
                    "clf",
                    XGBClassifier(
                        n_estimators=350,
                        max_depth=5,
                        learning_rate=0.06,
                        subsample=0.85,
                        colsample_bytree=0.80,
                        reg_lambda=2.0,
                        reg_alpha=0.2,
                        random_state=42,
                        n_jobs=-1,
                        eval_metric="mlogloss",
                    ),
                ),
            ]
        ),
    }

    tuned_cv_results = {}
    test_results = {}
    confusion_matrices = {}
    per_class_reports = {}
    predictions_df = df_test_meta.copy()

    model_save_map = {
        "SVM (RBF)": MODELS_DIR / "svm_pipeline.joblib",
        "Random Forest": MODELS_DIR / "rf_pipeline.joblib",
        "XGBoost": MODELS_DIR / "xgboost_pipeline.joblib",
    }

    for name, pipe in tuned_models.items():
        t_start = time.time()
        cv_metrics = run_group_cv_evaluation(pipe, X_train, y_train, groups_train, n_splits=5)
        tuned_cv_results[name] = cv_metrics

        # Fit on full training set
        pipe.fit(X_train, y_train)
        train_time = round(time.time() - t_start, 2)

        # Evaluate on train set (to check overfitting gap)
        y_tr_pred = pipe.predict(X_train)
        y_tr_proba = pipe.predict_proba(X_train)
        tr_metrics = evaluate_predictions(y_train, y_tr_pred, y_tr_proba)

        # Evaluate once on hold-out test set
        y_te_pred = pipe.predict(X_test)
        y_te_proba = pipe.predict_proba(X_test)
        te_metrics = evaluate_predictions(y_test, y_te_pred, y_te_proba)
        te_metrics["train_accuracy"] = tr_metrics["accuracy"]
        te_metrics["train_f1_macro"] = tr_metrics["f1_macro"]
        te_metrics["train_roc_auc"] = tr_metrics["roc_auc_ovr"]
        te_metrics["cv_f1_macro"] = cv_metrics["f1_macro"]
        te_metrics["cv_accuracy"] = cv_metrics["accuracy"]
        te_metrics["cv_roc_auc"] = cv_metrics["roc_auc_ovr"]
        te_metrics["train_time_sec"] = train_time

        save_path = model_save_map[name]
        joblib.dump(pipe, save_path, compress=3)
        te_metrics["model_size_mb"] = round(save_path.stat().st_size / (1024 * 1024), 2)

        test_results[name] = te_metrics
        cm = confusion_matrix(y_test, y_te_pred)
        confusion_matrices[name] = cm.tolist()
        per_class_reports[name] = classification_report(
            y_test, y_te_pred, target_names=CLASSES, output_dict=True, zero_division=0
        )

        predictions_df[f"pred_{name}"] = y_te_pred
        predictions_df[f"conf_{name}"] = np.max(y_te_proba, axis=1)

        print(
            f"  [Tuned Group-Test Set] {name}: CV-F1={cv_metrics['f1_macro']:.4f} | "
            f"Test Acc={te_metrics['accuracy']:.4f}, F1-Macro={te_metrics['f1_macro']:.4f}, "
            f"ROC-AUC={te_metrics['roc_auc_ovr']:.4f} (Size: {te_metrics['model_size_mb']} MB)"
        )

    best_model_name = max(tuned_cv_results.keys(), key=lambda k: tuned_cv_results[k]["f1_macro"])
    best_pipe_path = model_save_map[best_model_name]
    joblib.dump(joblib.load(best_pipe_path), MODELS_DIR / "final_model.joblib", compress=3)
    predictions_df.to_csv(REPORTS_DIR / "test_predictions.csv", index=False)

    rf_importances = tuned_models["Random Forest"].named_steps["clf"].feature_importances_
    xgb_importances = tuned_models["XGBoost"].named_steps["clf"].feature_importances_
    df_imp = pd.DataFrame(
        {
            "feature": feat_names,
            "rf_importance": rf_importances,
            "xgb_importance": xgb_importances,
            "mean_importance": (rf_importances + xgb_importances) / 2.0,
        }
    ).sort_values("xgb_importance", ascending=False)
    df_imp.to_csv(REPORTS_DIR / "feature_importance.csv", index=False)

    rows = []
    for m_name, m_res in test_results.items():
        rows.append({"model": m_name, **m_res})
    pd.DataFrame(rows).to_csv(REPORTS_DIR / "model_comparison.csv", index=False)

    summary_payload = {
        "dataset_summary": get_dataset_summary(df_meta),
        "split_info": {
            "total_unique": int(len(df_unique)),
            "unique_leaf_specimens": int(df_unique["leaf_group"].nunique()),
            "train_size": int(len(X_train)),
            "train_leaf_specimens": int(len(set(groups_train))),
            "test_size": int(len(X_test)),
            "test_leaf_specimens": int(len(set(groups_test))),
            "num_features": len(feat_names),
            "train_class_counts": pd.Series(y_train).map(lambda i: CLASSES[i]).value_counts().to_dict(),
            "test_class_counts": pd.Series(y_test).map(lambda i: CLASSES[i]).value_counts().to_dict(),
        },
        "duplicate_ablation": {
            "with_duplicates_total": int(len(df_all)),
            "with_duplicates_test_acc": round(acc_with_dup, 4),
            "with_duplicates_test_f1": round(f1_with_dup, 4),
            "naive_dedup_total": int(len(df_unique)),
            "naive_dedup_test_acc": round(acc_naive_uniq, 4),
            "naive_dedup_test_f1": round(f1_naive_uniq, 4),
            "group_aware_total": int(len(df_unique)),
            "group_aware_test_acc": test_results["Random Forest"]["accuracy"],
            "group_aware_test_f1": test_results["Random Forest"]["f1_macro"],
        },
        "baseline_cv_results": baseline_cv_results,
        "tuned_cv_results": tuned_cv_results,
        "test_results": test_results,
        "best_model": best_model_name,
        "confusion_matrices": confusion_matrices,
        "per_class_reports": per_class_reports,
        "top_20_features": df_imp.head(20).to_dict(orient="records"),
    }

    with open(REPORTS_DIR / "evaluation_summary.json", "w", encoding="utf-8") as f:
        json.dump(summary_payload, f, indent=2, ensure_ascii=False)

    print(f"\nBest Final Model Selected (by 5-Fold Group-CV F1-Macro): {best_model_name}")
    return summary_payload


if __name__ == "__main__":
    train_and_evaluate_all()
