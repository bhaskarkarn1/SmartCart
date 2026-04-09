from __future__ import annotations
import json
import os
import pickle
from collections import Counter, defaultdict
from typing import Optional

import pandas as pd
import streamlit as st

# =====================
#  PATH SETUP
# =====================
from pathlib import Path as _Path

_THIS_DIR = _Path(__file__).resolve().parent          # app/
BASE_DIR = str(_THIS_DIR.parent)                       # project root
DATA_DIR = os.path.join(BASE_DIR, "data")
ART_DIR = os.path.join(BASE_DIR, "artifacts")


# =====================
#  UTILITY HELPERS
# =====================
def ensure_dirs() -> None:
    """Create the artifacts directory if missing."""
    os.makedirs(ART_DIR, exist_ok=True)


# =====================
#  LOAD CSV DATASETS
# =====================
@st.cache_data(show_spinner=False)
def load_csvs() -> dict[str, pd.DataFrame]:
    """Load lightweight CSVs. order_data.csv is loaded only if present."""
    dfs: dict[str, pd.DataFrame] = {}

    paths = {
        "customer": os.path.join(DATA_DIR, "customer_data.csv"),
        "store": os.path.join(DATA_DIR, "store_data.csv"),
        "test": os.path.join(DATA_DIR, "test_data_question.csv"),
    }

    for name, path in paths.items():
        if not os.path.exists(path):
            raise FileNotFoundError(f"Missing required CSV: {path}")
        dfs[name] = pd.read_csv(path)

    # Heavy CSV — only load when it exists (not on every page)
    temp_csv = os.path.join(DATA_DIR, "order_data.csv")
    if os.path.exists(temp_csv):
        dfs["order"] = pd.read_csv(temp_csv)
    else:
        dfs["order"] = pd.DataFrame()

    return dfs


def download_order_csv():
    """Download large CSV from Google Drive."""
    import gdown

    drive_url = "https://drive.google.com/uc?id=1KS3Umzo-sEpi15JLqhfli_F4YRT1JhXN"
    temp_csv = os.path.join(DATA_DIR, "order_data.csv")
    gdown.download(drive_url, temp_csv, quiet=False)
    # Clear the cached CSVs so next load picks up the new file
    load_csvs.clear()
    return temp_csv




# =====================
#  ITEM PARSING & CLEANING
# =====================
NON_ITEMS = ["memo", "blankline", "asap", "order"]


def extract_item_names(order_str: str) -> list[str]:
    """Extract item names from JSON string field in order_data."""
    try:
        data = json.loads(order_str)
        items = []
        for order in data.get("orders", []):
            for it in order.get("item_details", []):
                nm = it.get("item_name")
                if nm:
                    items.append(nm)
        return items
    except Exception:
        return []


def clean_item_list(item_list: list[str]) -> list[str]:
    """Remove non-food placeholders like 'memo' or 'blankline'."""
    return [
        it for it in item_list
        if not any(sw in it.lower() for sw in NON_ITEMS)
    ]


# =====================
#  TAGGING FUNCTIONS
# =====================
def tag_item_type(name: str) -> str:
    """Roughly classify each item into main/side/dip/drink/other."""
    n = name.lower()
    if any(k in n for k in
           ["combo", "feast", "meal", "wings", "strips", "flavor platter", "sub", "box", "lunch", "crispy"]):
        return "main"
    if "dip" in n or "sauce" in n:
        return "dip"
    if any(k in n for k in ["fries", "corn", "sticks", "cake"]):
        return "side"
    if any(k in n for k in ["soda", "tea", "lemonade", "drink", "lager", "punch", "root beer", "water"]):
        return "drink"
    return "other"


def extract_item_features(name: str) -> set[str]:
    """Assign lightweight tags such as veg/non-veg, spicy, combo, dessert, etc."""
    n = name.lower()
    tags = set()
    veg_keywords = ["veggie", "veg", "corn", "celery", "sticks", "salad", "carrot"]
    non_veg_keywords = ["chicken", "wings", "strips", "grilled", "crispy", "buffalo"]

    if any(k in n for k in ["plastic", "fork", "knife", "spoon", "napkin", "packaging", "fee", "delivery"]):
        tags.add("non-food")
        return tags

    if any(k in n for k in veg_keywords):
        tags.add("veg")
    elif any(k in n for k in non_veg_keywords):
        tags.add("non-veg")

    if "spicy" in n:
        tags.add("spicy")
    if any(k in n for k in ["combo", "feast", "bundle", "lunch", "box", "platter"]):
        tags.add("combo")
    if any(k in n for k in ["cake", "dessert"]):
        tags.add("dessert")
    if any(k in n for k in ["soda", "fruit punch", "root beer", "drink", "lemonade", "tea"]):
        tags.add("cold_drink")

    return tags


# =====================
#  BUILD ITEM DICTIONARIES
# =====================
def build_items_and_tags(order_df: pd.DataFrame) -> tuple[dict, dict, dict, list[str]]:
    """
    From order data:
      - Parse each row into item list
      - Generate type and feature mappings
      - Count frequency and top items by type
    """
    order_df = order_df.copy()
    order_df["ITEM_LIST"] = (
        order_df["ORDERS"]
        .apply(extract_item_names)
        .apply(clean_item_list)
    )

    # Unique items
    all_items = sorted({it for items in order_df["ITEM_LIST"] for it in items})

    item_type = {it: tag_item_type(it) for it in all_items}
    item_features = {it: extract_item_features(it) for it in all_items}

    # Count item frequency and find top items by type
    counts = Counter([it for items in order_df["ITEM_LIST"] for it in items])
    top_by_type = defaultdict(list)

    for item, c in counts.items():
        t = item_type.get(item, "other")
        if t in ["main", "side", "dip", "drink"]:
            top_by_type[t].append((item, c))

    for t in top_by_type:
        top_by_type[t].sort(key=lambda x: -x[1])

    return item_type, item_features, top_by_type, all_items


# =====================
#  BUILD NORMALIZED CO-MATRIX
# =====================
def build_normalized_comatrix(order_df: pd.DataFrame, sample_n: Optional[int] = None) -> dict:
    """
    Build normalized co-occurrence matrix:
      P(j|i) ≈ count(i→j) / count(i)
    """
    if sample_n:
        order_df = order_df.sample(n=min(sample_n, len(order_df)), random_state=42)

    lists = order_df["ITEM_LIST"]
    item_count = defaultdict(int)
    pair_count = defaultdict(lambda: defaultdict(int))

    for items in lists:
        uniq = list(set(items))
        for i in uniq:
            item_count[i] += 1
        for i in uniq:
            for j in uniq:
                if i != j:
                    pair_count[i][j] += 1

    norm = defaultdict(dict)
    for a, b_dict in pair_count.items():
        denom = item_count[a] or 1
        for b, c in b_dict.items():
            norm[a][b] = c / denom

    return norm


# =====================
#  ARTIFACT I/O
# =====================
def save_artifact(name: str, obj) -> str:
    """Serialize and save an artifact to disk."""
    ensure_dirs()
    path = os.path.join(ART_DIR, name)
    with open(path, "wb") as f:
        pickle.dump(obj, f)
    return path


def load_artifact(name: str):
    """Load an artifact from disk if it exists."""
    path = os.path.join(ART_DIR, name)
    if os.path.exists(path):
        with open(path, "rb") as f:
            return pickle.load(f)
    return None

