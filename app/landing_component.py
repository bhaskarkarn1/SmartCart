"""
Landing page HTML component for Streamlit.
Renders the full landing page inside st.components.v1.html,
keeping everything under one URL.
"""
import os

_DIR = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_DIR)


def get_landing_html() -> str:
    """Read landing.css and index.html, inline the CSS, strip the navbar
    (Streamlit sidebar replaces it) and return a self-contained HTML string."""

    css_path = os.path.join(_ROOT, "landing.css")
    html_path = os.path.join(_ROOT, "index.html")

    with open(css_path, "r") as f:
        css = f.read()
    with open(html_path, "r") as f:
        html = f.read()

    # We need to build a self-contained HTML page that works inside
    # st.components.v1.html (an iframe). We inline the CSS and keep the JS.

    # The "Launch App" buttons should navigate to the sidebar pages
    # instead of opening a new tab — but since we're in an iframe,
    # we keep them pointing to "#" sections within the landing page.

    # Replace external CSS link with inline
    html = html.replace(
        '<link rel="stylesheet" href="landing.css" />',
        f"<style>{css}</style>",
    )

    # The navbar "Launch App" CTA should scroll to features since
    # we are already IN the app. Replace with in-page anchor.
    html = html.replace(
        'href="https://smartcart-hqzl.onrender.com" target="_blank" class="nav-cta"',
        'href="#features" class="nav-cta"',
    )

    # Hero "Launch App" button — make it navigate parent (Streamlit) to
    # the sidebar page. We use JS to communicate with the parent.
    html = html.replace(
        '<a href="https://smartcart-hqzl.onrender.com" target="_blank" class="btn btn-primary">',
        '<a href="#features" class="btn btn-primary" onclick="event.preventDefault();document.getElementById(\'features\').scrollIntoView({behavior:\'smooth\'});">',
    )

    # Team photos: use absolute GitHub raw URLs since Streamlit can't serve local assets
    html = html.replace(
        'src="assets/team/bhaskar.jpg"',
        'src="https://raw.githubusercontent.com/bhaskarkarn1/SmartCart/main/assets/team/bhaskar.jpg"',
    )
    html = html.replace(
        'src="assets/team/astitva.jpg"',
        'src="https://raw.githubusercontent.com/bhaskarkarn1/SmartCart/main/assets/team/astitva.jpg"',
    )
    html = html.replace(
        'src="assets/team/sanjay.jpg"',
        'src="https://raw.githubusercontent.com/bhaskarkarn1/SmartCart/main/assets/team/sanjay.jpg"',
    )

    return html
