"""
SmartCart — Menu Recommender
Streamlit Community Cloud entry-point.

This file is the single entry-point that Streamlit Cloud will execute.
All heavy logic lives in the `app/` package; we import from there.
"""

import os
import sys
from pathlib import Path
from collections import Counter
from typing import Optional

import pandas as pd
import streamlit as st

# ---------------------------------------------------------------------------
# Ensure project root is on sys.path so `app.*` imports work everywhere.
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# ---------------------------------------------------------------------------
# Page config (MUST be the first Streamlit command)
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="SmartCart — Menu Recommender",
    page_icon="🍗",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Mobile sidebar toggle (injected HTML/JS)
# ---------------------------------------------------------------------------
sidebar_toggle_html = """
<style>
[data-testid="collapsedControl"] {display: none !important;}
[data-testid="stSidebar"] {transition: all 0.4s ease-in-out;}
[data-testid="stSidebar"][aria-expanded="false"] {transform: translateX(-100%);}
[data-testid="stSidebar"][aria-expanded="true"] {transform: translateX(0%);}
.open-sidebar-button {
    position: fixed;
    top: 60px;
    left: 15px;
    background-color: rgba(91, 76, 219, 0.9);
    color: white;
    border: none;
    border-radius: 6px;
    padding: 6px 12px;
    font-size: 22px;
    font-weight: bold;
    cursor: pointer;
    z-index: 10000;
}
@media (min-width: 768px) {.open-sidebar-button {display: none;}}
</style>

<script>
function toggleSidebar() {
    const sidebar = window.parent.document.querySelector('[data-testid="stSidebar"]');
    const expanded = sidebar.getAttribute("aria-expanded");
    sidebar.setAttribute("aria-expanded", expanded === "true" ? "false" : "true");
}
</script>

<button class="open-sidebar-button" onclick="toggleSidebar()">☰</button>
"""

st.markdown(sidebar_toggle_html, unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# App-package imports (now safe because PROJECT_ROOT is on sys.path)
# ---------------------------------------------------------------------------
from app.data_loader import (
    clean_item_list,
    extract_item_names,
    load_csvs,
    build_items_and_tags,
    build_normalized_comatrix,
    save_artifact,
    load_artifact,
    download_order_csv,
)
from app.recommender import enhanced_recommend, batch_predict, normalize_user_items
from app.ui_components import icon_for_item, TYPE_EMOJI, topbar_badges, reco_card

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE_DIR = str(PROJECT_ROOT)
APP_DIR = os.path.join(BASE_DIR, "app")
DATA_DIR = os.path.join(BASE_DIR, "data")
ART_DIR = os.path.join(BASE_DIR, "artifacts")
ASSET_DIR = os.path.join(BASE_DIR, "assets")
LOGO_PATH = os.path.join(ASSET_DIR, "logo.png")

# ---------------------------------------------------------------------------
# Brand copy
# ---------------------------------------------------------------------------
APP_BRAND_LINE = (
    "We are **Team JaiMataDi**.\n\n"
    "We built **SmartCart** — a lightweight recommendation engine that turns static upsells "
    "into personalized suggestions across apps, web, and kiosks.\n\n"
    "In our tests, SmartCart improved **Recall@3** and **Precision@3** by **150%** over the baseline."
)

TEAM = [
    {
        "name": "Bhaskar Ranjan Karn",
        "linkedin": "https://www.linkedin.com/in/bhaskar-ranjan-karn/",
        "photo": Path(BASE_DIR) / "assets" / "team" / "bhaskar.jpg",
    },
    {
        "name": "Astitva",
        "linkedin": "https://www.linkedin.com/in/astitva-07a338229/",
        "photo": Path(BASE_DIR) / "assets" / "team" / "astitva.jpg",
    },
    {
        "name": "Sanjay Kumar",
        "linkedin": "https://www.linkedin.com/in/sanjay-kumar-39b73a239/",
        "photo": Path(BASE_DIR) / "assets" / "team" / "sanjay.jpg",
    },
]

# ---------------------------------------------------------------------------
# Inject Google Fonts + viewport meta + Load CSS
# ---------------------------------------------------------------------------
st.markdown(
    '<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">'
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
    '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">',
    unsafe_allow_html=True,
)

css_path = os.path.join(APP_DIR, "styles.css")
if os.path.exists(css_path):
    with open(css_path, "r") as f:
        css = f.read()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Sidebar navigation
# ---------------------------------------------------------------------------
st.sidebar.markdown(
    """
    <div class="brand-side">
      <span class="brand-blue">🍗 SmartCart</span>
    </div>
    """,
    unsafe_allow_html=True,
)

if os.path.exists(LOGO_PATH):
    st.sidebar.image(LOGO_PATH, use_column_width=True)

page = st.sidebar.radio(
    "Navigation",
    [
        "🏁 Start",
        "🧱 Build Model (First Run)",
        "🛒 Menu & Recommendations",
        "📦 Batch Predict (CSV)",
        "📊 Metrics & Explore",
        "🧩 Architecture & Workflow",
        "ℹ️ About",
    ],
    label_visibility="collapsed",
)


# ===================================================================
#  CACHED HELPERS
# ===================================================================
@st.cache_data(show_spinner=False)
def load_all_csvs():
    return load_csvs()


@st.cache_data(show_spinner=True)
def prepare_artifacts(sample_n: Optional[int]):
    dfs = load_all_csvs()
    order = dfs["order"].copy()
    if order.empty:
        raise ValueError("order_data.csv is required to build artifacts.")

    order["ITEM_LIST"] = order["ORDERS"].apply(extract_item_names).apply(clean_item_list)
    item_type, item_feat, top_by_type, all_items = build_items_and_tags(order)
    co_norm = build_normalized_comatrix(order, sample_n=sample_n)

    known_lower = {itm.lower(): itm for itm in all_items}
    art = {
        "item_type": item_type,
        "item_feat": item_feat,
        "top_by_type": top_by_type,
        "co_norm": co_norm,
        "known_items_lower": list(known_lower.keys()),
        "lower_to_orig": known_lower,
    }
    save_artifact("artifacts.pkl", art)
    return art


def load_or_build_artifacts():
    art = load_artifact("artifacts.pkl")
    if art is None:
        st.warning("Artifacts not found. Go to **Build Model (First Run)**.")
        return None
    return art


def app_brand_title():
    st.markdown(
        """
        <h1 class="brand-center">
          <span class="brand-blue">SmartCart</span>
        </h1>
        """,
        unsafe_allow_html=True,
    )


# ===================================================================
#  PAGES
# ===================================================================
def start_page():
    """Render the landing page natively inside Streamlit — no iframe."""
    from app.landing_component import get_landing_css, get_landing_sections

    # Inject scoped CSS
    st.markdown(get_landing_css(), unsafe_allow_html=True)

    # Render each section natively
    for section_html in get_landing_sections():
        st.markdown(section_html, unsafe_allow_html=True)
        st.markdown("<hr class='landing-divider'>", unsafe_allow_html=True)



def build_model_page():
    app_brand_title()
    st.markdown("<h2 class='page-h2'>Build Model (First Run)</h2>", unsafe_allow_html=True)
    st.markdown(
        "<p style='text-align:center; color:#8b8fa3; font-size:15px;'>"
        "Downloads order data and builds the recommendation engine."
        "</p>",
        unsafe_allow_html=True,
    )

    temp_csv = os.path.join(DATA_DIR, "order_data.csv")

    # Step 1: Download if missing
    if not os.path.exists(temp_csv):
        st.markdown("### Step 1: Download Order Data")
        st.warning("⚠ `order_data.csv` is missing. Download it first (~50MB compressed).")
        if st.button("📥 Download order_data.csv"):
            with st.spinner("⏳ Downloading from Google Drive... please wait."):
                download_order_csv()
            st.success("✅ Download complete!")
            st.rerun()
        st.stop()  # Don't show build UI until file exists

    # Step 2: Build artifacts
    st.markdown("### Step 2: Build Recommendation Model")
    st.success("✅ `order_data.csv` found!")

    # Check if artifacts already exist
    existing_art = load_artifact("artifacts.pkl")
    if existing_art:
        st.info("ℹ️ Artifacts already exist. Rebuild only if you want to change the sample size.")

    sample = st.slider("Sample N Orders", 100_000, 1_400_000, 250_000, 50_000)
    if st.button("🚀 Build Now"):
        with st.spinner("🔨 Building co-occurrence matrix... this takes ~30 seconds."):
            _ = prepare_artifacts(sample_n=sample)
        st.success("✅ Model built! Head to **🛒 Menu & Recommendations** to start.")
        st.balloons()


def menu_reco_page():
    app_brand_title()
    st.markdown("<h2 class='page-h2'>Menu & Recommendations</h2>", unsafe_allow_html=True)

    art = load_or_build_artifacts()
    if art is None:
        return

    all_items = list(art["lower_to_orig"].values())
    selected = st.multiselect("Select up to 3 items", options=all_items, default=[])
    if len(selected) > 3:
        st.error("You selected more than 3 items. Only first 3 will be used.")
        selected = selected[:3]

    topbar_badges(selected, limit=3)
    if st.button("🍽️ Recommend", disabled=len(selected) == 0):
        cart = normalize_user_items(selected, art["known_items_lower"], art["lower_to_orig"])
        recs = enhanced_recommend(cart, art["co_norm"], art["item_type"], art["top_by_type"], art["item_feat"])
        if not recs:
            st.warning("No recommendations found. Try other items or rebuild model.")
            return
        st.markdown("<h3 class='page-h3'>Top 3 Recommendations</h3>", unsafe_allow_html=True)
        cols = st.columns(3)
        for idx, (it, score) in enumerate(recs, start=1):
            t = art["item_type"].get(it, "other")
            with cols[idx - 1]:
                reco_card(idx, it, score, t)


def batch_page():
    app_brand_title()
    st.markdown("<h2 class='page-h2'>📦 Batch Predict (CSV)</h2>", unsafe_allow_html=True)

    art = load_or_build_artifacts()
    if art is None:
        return

    st.markdown("<p style='text-align:center;'>Runs predictions for test_data_question.csv.</p>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Run Batch"):
            try:
                test_path = os.path.join(DATA_DIR, "test_data_question.csv")
                test_df = pd.read_csv(test_path)
            except Exception as e:
                st.error(f"Error loading CSV: {e}")
                return

            out = batch_predict(
                test_df,
                art["co_norm"],
                art["item_type"],
                art["top_by_type"],
                art["item_feat"],
                art["known_items_lower"],
                art["lower_to_orig"],
            )
            out_path = os.path.join(ART_DIR, "SmartCart_Recommendation_Output.csv")
            out.to_csv(out_path, index=False)
            st.success(f"Saved: {out_path}")
            st.dataframe(out.head(20))
            with open(out_path, "rb") as f:
                st.download_button("📥 Download CSV", f, file_name="SmartCart_Recommendation_Output.csv")


def metrics_page():
    app_brand_title()
    st.markdown("<h2 class='page-h2'>Metrics & Explore</h2>", unsafe_allow_html=True)
    art = load_or_build_artifacts()
    if art is None:
        return

    counts = Counter(art["item_type"].values())
    st.bar_chart(pd.DataFrame.from_dict(counts, orient="index", columns=["Count"]))
    st.markdown("<h4 class='page-h4'>Top Items by Type</h4>", unsafe_allow_html=True)
    cols = st.columns(4)
    for t, col in zip(["main", "side", "dip", "drink"], cols):
        with col:
            st.markdown(f"**{t.title()}** {TYPE_EMOJI.get(t, '')}")
            for it, cnt in art["top_by_type"].get(t, [])[:10]:
                st.write(f"{icon_for_item(it)} {it} — {cnt}")


def workflow_page():
    mermaid_code = """
     graph TD
         A["📦 <b>Raw Data</b><br><i>(Orders, Customers, Stores)</i>"]
         B["🧹 <b>Data Cleaning & Tagging</b><br><i>Parse JSON, remove noise, label items</i>"]
         C["🧮 <b>Co-occurrence Matrix</b><br><i>Pair frequency normalization</i>"]
         D["⚙️ <b>Scoring Engine</b><br><i>Weighted co-scores + soft bias</i>"]
         E["🎯 <b>Top-3 Recommendations</b><br><i>Final ranked suggestions</i>"]
         F["📊 <b>Evaluation Metrics</b><br><i>Recall@3, Precision@3, Accuracy</i>"]

         %% connections
         A --> B --> C --> D --> E --> F

         %% styling
         classDef start fill:#e3f2fd,stroke:#1f77ff,stroke-width:2px,color:#0b0b0c,font-weight:bold;
         classDef process fill:#f3e5f5,stroke:#8e24aa,stroke-width:2px,color:#111;
         classDef calc fill:#fff8e1,stroke:#fbc02d,stroke-width:2px,color:#111;
         classDef output fill:#e8f5e9,stroke:#43a047,stroke-width:2px,color:#111,font-weight:bold;
         classDef eval fill:#ede7f6,stroke:#5e35b1,stroke-width:2px,color:#111;

         class A start;
         class B,C process;
         class D calc;
         class E output;
         class F eval;
     """

    html = f"""
     <div style="display:flex;justify-content:center;align-items:center;">
         <div class="mermaid" style="max-width:95%;overflow-x:auto;text-align:center;">
             {mermaid_code}
         </div>
     </div>
     <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
     <script>
       mermaid.initialize({{
         startOnLoad:true,
         theme:'default',
         securityLevel:'loose',
         flowchart:{{curve:'basis'}},
       }});
     </script>
     """
    st.components.v1.html(html, height=650, scrolling=False)


def about_page():
    app_brand_title()
    st.markdown("<h2 class='page-h2'>About</h2>", unsafe_allow_html=True)

    st.markdown(
        "<p style='text-align:center; max-width:700px; margin:0 auto 24px; "
        "color:#64687a; font-size:15px; line-height:1.7;'>"
        + APP_BRAND_LINE.replace('\n\n', '<br><br>').replace('**', '<b>').replace('**', '</b>')
        + "</p>",
        unsafe_allow_html=True,
    )

    st.markdown("<hr class='rule'/>", unsafe_allow_html=True)
    st.markdown("<h3 class='page-h3'>Team JaiMataDi</h3>", unsafe_allow_html=True)
    st.write("")  # spacer

    cols = st.columns(len(TEAM))
    for member, col in zip(TEAM, cols):
        with col:
            photo_path = Path(member["photo"])
            if photo_path.exists():
                st.image(str(photo_path), use_column_width=True)
            else:
                st.markdown(
                    f'<div class="team-placeholder">Add photo: {photo_path.name}</div>',
                    unsafe_allow_html=True,
                )
            st.markdown(
                f"<p style='text-align:center; font-weight:700; font-size:15px; margin:8px 0 4px;'>"
                f"{member['name']}</p>",
                unsafe_allow_html=True,
            )
            st.markdown(
                f'<p style="text-align:center;">'
                f'<a href="{member["linkedin"]}" target="_blank" '
                f'style="display:inline-block; padding:6px 18px; background:#0a66c2; '
                f'color:white; border-radius:6px; text-decoration:none; font-size:13px; '
                f'font-weight:600;">🔗 LinkedIn</a></p>',
                unsafe_allow_html=True,
            )


# ===================================================================
#  PAGE ROUTER
# ===================================================================
if page.startswith("🏁"):
    start_page()
elif page.startswith("🧱"):
    build_model_page()
elif page.startswith("🛒"):
    menu_reco_page()
elif page.startswith("📦"):
    batch_page()
elif page.startswith("📊"):
    metrics_page()
elif page.startswith("🧩"):
    workflow_page()
else:
    about_page()
