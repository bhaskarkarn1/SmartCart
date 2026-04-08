from __future__ import annotations
from collections import defaultdict, Counter
from difflib import get_close_matches
from typing import List, Dict, Tuple, Iterable

# =====================
#  CONSTANTS
# =====================
DEFAULT_BLACKLIST = {
    "Plastic Fork", "Plastic Knife", "Plastic Straw", "Plastic Utensils",
    "Delivery Fee", "Unavailable Item", "Ketchup Pack",
    "Seasoning Pack", "Extra Sauce"
}


# =====================
#  MAIN RECOMMENDER
# =====================
def enhanced_recommend(
    cart_items: List[str],
    co_dict: Dict[str, Dict[str, float]],
    item_type: Dict[str, str],
    top_items_by_type: Dict[str, List[Tuple[str, int]]],
    item_tags: Dict[str, set],
    blacklist: set[str] = DEFAULT_BLACKLIST,
    top_n: int = 3,
    boost_factor: float = 1.2,
    max_per_type: int = 1
) -> List[Tuple[str, float]]:
    """
    Generate top-N recommendations based on co-occurrence scores,
    soft bias for missing item categories, and fallback fill logic.

    Steps:
      1. Aggregate co-occurrence scores for all cart items.
      2. Apply type- and spice-aware biasing.
      3. Select top-N ensuring diversity across types.
      4. Fill any remaining slots using fallback items by category.
    """
    score = defaultdict(float)

    # Analyze current cart
    cart_types = Counter(item_type.get(x, "other") for x in cart_items)
    has_spicy = any("spicy" in item_tags.get(x, set()) for x in cart_items)

    # 1️⃣ Co-occurrence scoring
    for item in cart_items:
        if item not in co_dict:
            continue

        for co_item, weight in co_dict[item].items():
            if co_item in cart_items or co_item in blacklist:
                continue

            item_cat = item_type.get(co_item, "other")
            tags = item_tags.get(co_item, set())

            # Spicy-aware bonus logic
            if "spicy" in tags:
                spicy_bonus = weight * (0.3 if not has_spicy else 0.1)
            else:
                spicy_bonus = 0.0

            # Soft bias for underrepresented types
            if cart_types.get(item_cat, 0) == 0:
                bias = boost_factor * (1.5 if item_cat == "drink" else 1.0)
                score[co_item] += weight * bias + spicy_bonus
            else:
                score[co_item] += weight + spicy_bonus

    # 2️⃣ Rank and pick top-N (max one per type)
    sorted_items = sorted(score.items(), key=lambda x: x[1], reverse=True)
    reco, used_type = [], Counter()

    for it, sc in sorted_items:
        t = item_type.get(it, "other")
        if used_type[t] >= max_per_type:
            continue
        reco.append((it, round(float(sc), 4)))
        used_type[t] += 1
        if len(reco) >= top_n:
            break

    # 3️⃣ Fallback fill from top items by type
    if len(reco) < top_n:
        for t in ["main", "side", "dip", "drink"]:
            if used_type[t] >= max_per_type:
                continue
            for cand, _ in top_items_by_type.get(t, []):
                if (
                    cand in cart_items
                    or cand in [r[0] for r in reco]
                    or cand in blacklist
                ):
                    continue
                reco.append((cand, 0.0))
                used_type[t] += 1
                if len(reco) >= top_n:
                    break
            if len(reco) >= top_n:
                break

    return reco[:top_n]


# =====================
#  NORMALIZATION
# =====================
def normalize_user_items(
    raw_items: Iterable[str],
    known_items_lower: List[str],
    lower_to_orig: Dict[str, str],
    cutoff: float = 0.75
) -> List[str]:
    """
    Normalize user-entered item names to known catalog items.
    Uses fuzzy matching when exact match not found.
    """
    mapped = []
    for x in raw_items:
        if not isinstance(x, str) or not x.strip():
            continue

        lx = x.lower()
        if lx in lower_to_orig:
            mapped.append(lower_to_orig[lx])
            continue

        matches = get_close_matches(lx, known_items_lower, n=1, cutoff=cutoff)
        mapped.append(lower_to_orig[matches[0]] if matches else x)

    return mapped


# =====================
#  BATCH MODE
# =====================
def batch_predict(
    test_df: 'pd.DataFrame',
    co_dict: Dict[str, Dict[str, float]],
    item_type: Dict[str, str],
    top_items_by_type: Dict[str, List[Tuple[str, int]]],
    item_tags: Dict[str, set],
    known_items_lower: List[str],
    lower_to_orig: Dict[str, str],
    blacklist: set[str] = DEFAULT_BLACKLIST,
    top_n: int = 3
) -> 'pd.DataFrame':
    """
    Run bulk recommendations for test dataset rows.
    Each row contains up to 3 items (item1, item2, item3).
    """
    out = test_df.copy()
    for i in range(1, top_n + 1):
        out[f"RECOMMENDATION {i}"] = ""

    for idx, row in out.iterrows():
        raw = [row.get("item1", ""), row.get("item2", ""), row.get("item3", "")]
        cart = normalize_user_items(raw, known_items_lower, lower_to_orig)
        recs = enhanced_recommend(
            cart,
            co_dict,
            item_type,
            top_items_by_type,
            item_tags,
            blacklist,
            top_n=top_n,
        )

        for i, (it, _) in enumerate(recs, start=1):
            out.at[idx, f"RECOMMENDATION {i}"] = it

    return out
