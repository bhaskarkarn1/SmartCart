import streamlit as st

# =========================================
# ICON & TYPE MAPPING
# =========================================
TYPE_EMOJI = {
    "main": "🍱",
    "side": "🍟",
    "dip": "🥣",
    "drink": "🥤",
    "other": "🍽️",
}

def icon_for_item(name: str) -> str:
    """Return an emoji icon for the given item name."""
    n = name.lower()
    if "wing" in n:
        return "🍗"
    if "fries" in n or "fry" in n:
        return "🍟"
    if "dip" in n or "sauce" in n or "ranch" in n:
        return "🥣"
    if "burger" in n or "sandwich" in n:
        return "🍔"
    if "corn" in n:
        return "🌽"
    if "drink" in n or "cola" in n or "juice" in n:
        return "🥤"
    return "🍽️"


# =========================================
# HEADERS & BADGES
# =========================================
def header(text: str, emoji: str = ""):
    """Renders a small section header with emoji."""
    st.markdown(
        f"<h4 class='section-title'>{emoji} {text}</h4>",
        unsafe_allow_html=True
    )


def topbar_badges(items, limit=3):
    """Displays up to `limit` item badges horizontally."""
    shown = items[:limit]
    if not shown:
        return

    st.markdown("<div class='badge-bar'>", unsafe_allow_html=True)
    for it in shown:
        st.markdown(
            f"<span class='badge'>{icon_for_item(it)} {it}</span>",
            unsafe_allow_html=True
        )
    st.markdown("</div>", unsafe_allow_html=True)


# =========================================
# RECOMMENDATION CARD
# =========================================
def reco_card(rank, item_name, score, typ):
    """Displays a clean recommendation card with emoji, item name, and confidence."""
    emoji = icon_for_item(item_name)
    typ_emoji = TYPE_EMOJI.get(typ, "🍽️")
    rank_class = f"reco-rank reco-rank-{rank}" if rank <= 3 else "reco-rank"

    st.markdown(
        f"""
        <div class="reco-card">
            <div class="{rank_class}">{'🥇' if rank==1 else '🥈' if rank==2 else '🥉'}</div>
            <div class="reco-title">#{rank} {emoji} <b>{item_name}</b></div>
            <div class="reco-desc">{typ_emoji} {typ.title()} • Confidence {score:.2f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

