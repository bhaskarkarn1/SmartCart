"""
Native Streamlit landing page — no iframe, renders directly in the page.
"""

def get_landing_css():
    """Return scoped CSS for the landing sections."""
    return """
<style>
/* Landing page scoped styles */
.landing-hero {
  text-align: center;
  padding: 20px 0 40px;
  position: relative;
}
.landing-badge {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 8px 20px; background: rgba(91,76,219,0.08);
  border: 1px solid rgba(91,76,219,0.15); border-radius: 999px;
  font-size: 13px; font-weight: 600; color: #5B4CDB; margin-bottom: 24px;
}
.landing-title {
  font-size: 52px; font-weight: 900; letter-spacing: -0.04em;
  line-height: 1.1; margin-bottom: 20px; color: #1A1523;
}
.landing-gradient {
  background: linear-gradient(135deg, #5B4CDB 0%, #8B6FE8 50%, #D4896B 100%);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}
.landing-subtitle {
  max-width: 620px; margin: 0 auto 36px; font-size: 17px;
  line-height: 1.7; color: #5C5470;
}
.landing-stats {
  display: flex; align-items: center; justify-content: center; gap: 40px;
  padding: 28px 48px; background: rgba(255,255,255,0.72);
  backdrop-filter: blur(16px); border: 1px solid rgba(26,21,35,0.08);
  border-radius: 24px; box-shadow: 0 4px 16px rgba(26,21,35,0.08);
  margin: 0 auto; max-width: 700px;
}
.landing-stat { text-align: center; }
.landing-stat-val { display: block; font-size: 30px; font-weight: 900; letter-spacing: -0.03em; color: #1A1523; }
.landing-stat-lbl { font-size: 12px; font-weight: 500; color: #8E8B99; margin-top: 4px; }
.landing-stat-div { width: 1px; height: 40px; background: rgba(26,21,35,0.08); }

/* Section headers */
.landing-sh { text-align: center; margin-bottom: 40px; }
.landing-tag {
  display: inline-flex; align-items: center; gap: 6px;
  padding: 6px 16px; background: rgba(91,76,219,0.08); color: #5B4CDB;
  font-size: 11px; font-weight: 700; text-transform: uppercase;
  letter-spacing: 0.08em; border-radius: 999px; margin-bottom: 14px;
}
.landing-h2 {
  font-size: 36px; font-weight: 900; letter-spacing: -0.04em;
  line-height: 1.15; margin-bottom: 14px; color: #1A1523;
}
.landing-desc { max-width: 560px; margin: 0 auto; font-size: 16px; color: #5C5470; line-height: 1.7; }

/* Feature cards */
.landing-grid { display: grid; grid-template-columns: repeat(3,1fr); gap: 20px; }
.landing-fcard {
  background: #fff; border: 1px solid rgba(26,21,35,0.08); border-radius: 16px;
  padding: 28px 24px; transition: all 0.35s cubic-bezier(0.4,0,0.2,1);
}
.landing-fcard:hover {
  border-color: rgba(91,76,219,0.25); box-shadow: 0 12px 40px rgba(26,21,35,0.12), 0 8px 30px rgba(91,76,219,0.12);
  transform: translateY(-6px);
}
.landing-ficon {
  width: 44px; height: 44px; border-radius: 10px;
  display: flex; align-items: center; justify-content: center;
  margin-bottom: 16px; font-size: 20px;
}
.ic-indigo { background: rgba(91,76,219,0.1); color: #5B4CDB; }
.ic-violet { background: rgba(139,111,232,0.1); color: #8B6FE8; }
.ic-rose { background: rgba(232,93,117,0.1); color: #E85D75; }
.ic-amber { background: rgba(212,148,10,0.1); color: #D4940A; }
.ic-emerald { background: rgba(45,159,111,0.1); color: #2D9F6F; }
.ic-cyan { background: rgba(27,154,170,0.1); color: #1B9AAA; }
.landing-fcard h4 { font-size: 17px; font-weight: 700; margin-bottom: 8px; letter-spacing: -0.02em; color: #1A1523; }
.landing-fcard p { font-size: 13.5px; color: #5C5470; line-height: 1.65; }

/* Steps */
.landing-scard {
  position: relative; background: #fff; border: 1px solid rgba(26,21,35,0.08);
  border-radius: 16px; padding: 32px 24px 24px; text-align: center;
  transition: all 0.35s cubic-bezier(0.4,0,0.2,1);
}
.landing-scard:hover { border-color: rgba(91,76,219,0.25); box-shadow: 0 12px 40px rgba(26,21,35,0.12); transform: translateY(-6px); }
.landing-snum { position: absolute; top: 12px; left: 16px; font-size: 12px; font-weight: 800; color: #5B4CDB; opacity: 0.5; }
.landing-sicon {
  width: 52px; height: 52px; background: rgba(91,76,219,0.08); color: #5B4CDB;
  border-radius: 50%; display: flex; align-items: center; justify-content: center;
  margin: 0 auto 16px; font-size: 22px;
  transition: all 0.3s cubic-bezier(0.34,1.56,0.64,1);
}
.landing-scard:hover .landing-sicon { background: #5B4CDB; color: #fff; transform: scale(1.1); box-shadow: 0 4px 20px rgba(91,76,219,0.18); }
.landing-scard h4 { font-size: 16px; font-weight: 700; margin-bottom: 8px; color: #1A1523; }
.landing-scard p { font-size: 13px; color: #5C5470; line-height: 1.6; }

/* Performance bars */
.landing-mcard {
  background: #fff; border: 1px solid rgba(26,21,35,0.08); border-radius: 16px;
  padding: 24px; transition: all 0.35s cubic-bezier(0.4,0,0.2,1);
}
.landing-mcard:hover { border-color: rgba(91,76,219,0.25); box-shadow: 0 12px 40px rgba(26,21,35,0.12); transform: translateY(-4px); }
.landing-mhdr { display: flex; align-items: center; gap: 10px; margin-bottom: 20px; font-size: 15px; font-weight: 700; color: #1A1523; }
.landing-mhdr span.mi { color: #5B4CDB; font-size: 18px; }
.landing-bgrp { margin-bottom: 12px; }
.landing-blbl { font-size: 11px; font-weight: 600; color: #8E8B99; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 4px; }
.landing-btrack { height: 28px; background: #F3EDE4; border-radius: 8px; overflow: hidden; }
.landing-bfill {
  height: 100%; border-radius: 8px; display: flex; align-items: center;
  justify-content: flex-end; padding-right: 10px; font-size: 12px; font-weight: 700;
}
.landing-bbase { background: #F3EDE4; border: 1px solid rgba(26,21,35,0.08); color: #5C5470; }
.landing-bsmart { background: linear-gradient(135deg, #5B4CDB 0%, #8B6FE8 50%, #D4896B 100%); color: #fff; }
.landing-mbadge {
  display: inline-flex; align-items: center; padding: 5px 14px;
  background: rgba(45,159,111,0.1); color: #2D9F6F;
  font-size: 14px; font-weight: 800; border-radius: 999px; margin-top: 12px;
}

/* Tech stack */
.landing-tgrid { display: grid; grid-template-columns: repeat(6,1fr); gap: 16px; }
.landing-tcard {
  background: #fff; border: 1px solid rgba(26,21,35,0.08); border-radius: 16px;
  padding: 24px 12px; text-align: center; transition: all 0.35s cubic-bezier(0.4,0,0.2,1);
}
.landing-tcard:hover { border-color: rgba(91,76,219,0.25); box-shadow: 0 4px 16px rgba(26,21,35,0.08); transform: translateY(-4px); }
.landing-ticon {
  width: 44px; height: 44px; background: rgba(91,76,219,0.08); color: #5B4CDB;
  border-radius: 10px; display: flex; align-items: center; justify-content: center;
  margin: 0 auto 12px; font-size: 20px;
}
.landing-tcard h5 { font-size: 14px; font-weight: 700; margin-bottom: 2px; color: #1A1523; }
.landing-tcard p { font-size: 11px; color: #8E8B99; font-weight: 500; }

/* Team */
.landing-team { display: grid; grid-template-columns: repeat(3,1fr); gap: 28px; max-width: 850px; margin: 0 auto; }
.landing-tmcard {
  background: #fff; border: 1px solid rgba(26,21,35,0.08); border-radius: 24px;
  padding: 32px 24px; text-align: center; transition: all 0.4s cubic-bezier(0.4,0,0.2,1);
}
.landing-tmcard:hover { border-color: rgba(91,76,219,0.25); box-shadow: 0 12px 40px rgba(26,21,35,0.12); transform: translateY(-6px); }
.landing-tmavatar {
  width: 88px; height: 88px; border-radius: 50%; margin: 0 auto 16px;
  overflow: hidden; border: 3px solid #F3EDE4; box-shadow: 0 4px 16px rgba(26,21,35,0.08);
  transition: all 0.3s cubic-bezier(0.4,0,0.2,1); background: #F3EDE4;
  display: flex; align-items: center; justify-content: center; font-size: 32px; color: #5B4CDB;
}
.landing-tmcard:hover .landing-tmavatar { border-color: #5B4CDB; box-shadow: 0 0 0 4px rgba(91,76,219,0.08), 0 12px 40px rgba(26,21,35,0.12); }
.landing-tmcard h4 { font-size: 16px; font-weight: 700; margin-bottom: 10px; color: #1A1523; }
.landing-tmlink {
  display: inline-flex; align-items: center; gap: 6px;
  padding: 8px 18px; background: #0a66c2; color: #fff;
  font-size: 12px; font-weight: 600; border-radius: 999px;
  text-decoration: none; transition: all 0.3s cubic-bezier(0.4,0,0.2,1);
}
.landing-tmlink:hover { background: #004182; transform: translateY(-2px); box-shadow: 0 4px 12px rgba(10,102,194,0.3); }

/* Divider */
.landing-divider { border: none; height: 1px; background: linear-gradient(90deg, transparent, rgba(26,21,35,0.08), transparent); margin: 48px 0; }

/* Section alt bg */
.landing-alt { background: #F3EDE4; border-radius: 24px; padding: 48px 32px; margin: 0 -1rem; }

/* Responsive */
@media (max-width: 1024px) {
  .landing-title { font-size: 40px; }
  .landing-h2 { font-size: 30px; }
  .landing-grid { grid-template-columns: repeat(2,1fr); }
  .landing-tgrid { grid-template-columns: repeat(3,1fr); }
  .landing-stats { gap: 24px; padding: 20px 28px; }
  .landing-stat-val { font-size: 24px; }
}
@media (max-width: 768px) {
  .landing-title { font-size: 30px; }
  .landing-h2 { font-size: 24px; }
  .landing-grid { grid-template-columns: 1fr; }
  .landing-tgrid { grid-template-columns: repeat(2,1fr); }
  .landing-team { grid-template-columns: 1fr; max-width: 340px; }
  .landing-stats { flex-direction: column; gap: 16px; padding: 20px; }
  .landing-stat-div { width: 60px; height: 1px; }
  .landing-alt { padding: 32px 16px; margin: 0 -0.5rem; }
}
@media (max-width: 480px) {
  .landing-title { font-size: 26px; }
  .landing-h2 { font-size: 20px; }
  .landing-stat-val { font-size: 20px; }
}
</style>
"""


def get_landing_sections():
    """Return a list of HTML section strings to render via st.markdown."""
    hero = """
<div class="landing-hero">
  <div class="landing-badge">🏆 WWT Unravel 2025 — Team JaiMataDi</div>
  <h1 class="landing-title">Turn Static Menus into<br><span class="landing-gradient">Smart Recommendations</span></h1>
  <p class="landing-subtitle">SmartCart is a personalized, data-driven recommendation engine that transforms upsells across apps, web, and kiosks — improving key metrics by <strong>150%</strong> over baseline.</p>
  <div class="landing-stats">
    <div class="landing-stat"><span class="landing-stat-val">1,414,410</span><span class="landing-stat-lbl">Orders Analyzed</span></div>
    <div class="landing-stat-div"></div>
    <div class="landing-stat"><span class="landing-stat-val">563,346</span><span class="landing-stat-lbl">Customers</span></div>
    <div class="landing-stat-div"></div>
    <div class="landing-stat"><span class="landing-stat-val">138</span><span class="landing-stat-lbl">Menu Items</span></div>
    <div class="landing-stat-div"></div>
    <div class="landing-stat"><span class="landing-stat-val">150%</span><span class="landing-stat-lbl">Recall Improvement</span></div>
  </div>
</div>
"""

    features = """
<div class="landing-sh">
  <div class="landing-tag">✨ Capabilities</div>
  <h2 class="landing-h2">Everything you need for<br><span class="landing-gradient">intelligent upselling</span></h2>
  <p class="landing-desc">From real-time suggestions to bulk predictions, SmartCart covers the full recommendation pipeline.</p>
</div>
<div class="landing-grid">
  <div class="landing-fcard"><div class="landing-ficon ic-indigo">🖱️</div><h4>Interactive Recommendations</h4><p>Select up to 3 menu items and instantly receive top-3 personalized suggestions powered by co-occurrence intelligence.</p></div>
  <div class="landing-fcard"><div class="landing-ficon ic-violet">🔲</div><h4>Co-occurrence Engine</h4><p>Normalized co-occurrence matrix with type-aware scoring built from 1.4M real transaction records.</p></div>
  <div class="landing-fcard"><div class="landing-ficon ic-rose">🎯</div><h4>Smart Scoring</h4><p>Weighted co-scores combined with soft category bias and spicy-aware logic for diverse, relevant picks.</p></div>
  <div class="landing-fcard"><div class="landing-ficon ic-amber">📊</div><h4>Batch Predict</h4><p>Bulk CSV predictions for 1,000+ test cases in seconds — perfect for offline evaluation and QA.</p></div>
  <div class="landing-fcard"><div class="landing-ficon ic-emerald">📈</div><h4>Metrics Dashboard</h4><p>Item distribution charts, top items by category, and deep-dive analytics at your fingertips.</p></div>
  <div class="landing-fcard"><div class="landing-ficon ic-cyan">⚙️</div><h4>Architecture View</h4><p>Interactive Mermaid flowchart of the entire recommendation pipeline for full transparency.</p></div>
</div>
"""

    how_it_works = """
<div class="landing-alt">
<div class="landing-sh">
  <div class="landing-tag">🔗 Pipeline</div>
  <h2 class="landing-h2">How SmartCart <span class="landing-gradient">thinks</span></h2>
  <p class="landing-desc">Six intelligent stages from raw data to personalized top-3 recommendations.</p>
</div>
<div class="landing-grid">
  <div class="landing-scard"><div class="landing-snum">01</div><div class="landing-sicon">🗄️</div><h4>Data Ingestion</h4><p>Parses 1.4M order records with JSON-embedded item details from real transaction data.</p></div>
  <div class="landing-scard"><div class="landing-snum">02</div><div class="landing-sicon">🏷️</div><h4>Item Tagging</h4><p>Classifies 138 items into main, side, dip, drink, and other categories automatically.</p></div>
  <div class="landing-scard"><div class="landing-snum">03</div><div class="landing-sicon">🧮</div><h4>Co-occurrence Matrix</h4><p>Computes conditional probability P(j|i) for all item pairs using normalized frequencies.</p></div>
  <div class="landing-scard"><div class="landing-snum">04</div><div class="landing-sicon">⚙️</div><h4>Scoring Engine</h4><p>Aggregates co-scores with soft bias for underrepresented categories and spicy-aware bonuses.</p></div>
  <div class="landing-scard"><div class="landing-snum">05</div><div class="landing-sicon">🔍</div><h4>Diversity Filter</h4><p>Ensures max 1 recommendation per type — no duplicate categories in your suggestions.</p></div>
  <div class="landing-scard"><div class="landing-snum">06</div><div class="landing-sicon">🏆</div><h4>Top-3 Output</h4><p>Final ranked suggestions using global popularity fallback when co-occurrence data is sparse.</p></div>
</div>
</div>
"""

    performance = """
<div class="landing-sh">
  <div class="landing-tag">📈 Results</div>
  <h2 class="landing-h2">Proven <span class="landing-gradient">performance gains</span></h2>
  <p class="landing-desc">Head-to-head comparison against the static baseline upsell strategy.</p>
</div>
<div class="landing-grid">
  <div class="landing-mcard">
    <div class="landing-mhdr"><span class="mi">🎯</span> Recall@3</div>
    <div class="landing-bgrp"><div class="landing-blbl">Baseline</div><div class="landing-btrack"><div class="landing-bfill landing-bbase" style="width:40%"><span>~0.20</span></div></div></div>
    <div class="landing-bgrp"><div class="landing-blbl">SmartCart</div><div class="landing-btrack"><div class="landing-bfill landing-bsmart" style="width:100%"><span>~0.50</span></div></div></div>
    <div class="landing-mbadge">+150%</div>
  </div>
  <div class="landing-mcard">
    <div class="landing-mhdr"><span class="mi">🎯</span> Precision@3</div>
    <div class="landing-bgrp"><div class="landing-blbl">Baseline</div><div class="landing-btrack"><div class="landing-bfill landing-bbase" style="width:39%"><span>~0.15</span></div></div></div>
    <div class="landing-bgrp"><div class="landing-blbl">SmartCart</div><div class="landing-btrack"><div class="landing-bfill landing-bsmart" style="width:100%"><span>~0.38</span></div></div></div>
    <div class="landing-mbadge">+153%</div>
  </div>
  <div class="landing-mcard">
    <div class="landing-mhdr"><span class="mi">✅</span> Top-1 Accuracy</div>
    <div class="landing-bgrp"><div class="landing-blbl">Baseline</div><div class="landing-btrack"><div class="landing-bfill landing-bbase" style="width:58%"><span>~0.30</span></div></div></div>
    <div class="landing-bgrp"><div class="landing-blbl">SmartCart</div><div class="landing-btrack"><div class="landing-bfill landing-bsmart" style="width:100%"><span>~0.52</span></div></div></div>
    <div class="landing-mbadge">+73%</div>
  </div>
</div>
"""

    tech = """
<div class="landing-alt">
<div class="landing-sh">
  <div class="landing-tag">🔧 Stack</div>
  <h2 class="landing-h2">Built with <span class="landing-gradient">modern tools</span></h2>
</div>
<div class="landing-tgrid">
  <div class="landing-tcard"><div class="landing-ticon">📊</div><h5>Streamlit</h5><p>Frontend</p></div>
  <div class="landing-tcard"><div class="landing-ticon">🐍</div><h5>Python</h5><p>Backend</p></div>
  <div class="landing-tcard"><div class="landing-ticon">🗃️</div><h5>Pandas</h5><p>Data Processing</p></div>
  <div class="landing-tcard"><div class="landing-ticon">🔢</div><h5>NumPy</h5><p>Computation</p></div>
  <div class="landing-tcard"><div class="landing-ticon">☁️</div><h5>Render</h5><p>Deployment</p></div>
  <div class="landing-tcard"><div class="landing-ticon">🔤</div><h5>Inter</h5><p>Typography</p></div>
</div>
</div>
"""

    team = """
<div class="landing-sh">
  <div class="landing-tag">👥 Team</div>
  <h2 class="landing-h2">Meet <span class="landing-gradient">Team JaiMataDi</span></h2>
  <p class="landing-desc">The builders behind SmartCart.</p>
</div>
<div class="landing-team">
  <div class="landing-tmcard">
    <div class="landing-tmavatar">👨‍💻</div>
    <h4>Bhaskar Ranjan Karn</h4>
    <a href="https://linkedin.com/in/bhaskar-ranjan-karn/" target="_blank" class="landing-tmlink">🔗 LinkedIn</a>
  </div>
  <div class="landing-tmcard">
    <div class="landing-tmavatar">👨‍💻</div>
    <h4>Astitva</h4>
    <a href="https://linkedin.com/in/astitva-07a338229/" target="_blank" class="landing-tmlink">🔗 LinkedIn</a>
  </div>
  <div class="landing-tmcard">
    <div class="landing-tmavatar">👨‍💻</div>
    <h4>Sanjay Kumar</h4>
    <a href="https://linkedin.com/in/sanjay-kumar-39b73a239/" target="_blank" class="landing-tmlink">🔗 LinkedIn</a>
  </div>
</div>
"""

    return [hero, features, how_it_works, performance, tech, team]
