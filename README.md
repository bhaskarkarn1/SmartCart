<div align="center">

# 🍗 SmartCart

### Personalized Menu Recommendation Engine

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

*Built by **Team JaiMataDi** for the WWT Unravel 2025 Challenge*

---

**SmartCart** transforms static menu upsells into **personalized, data-driven recommendations** across apps, web, and kiosks — improving **Recall@3** and **Precision@3** by **150%** over the baseline.

</div>

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🛒 **Interactive Recommendations** | Select up to 3 menu items → get top-3 personalized suggestions |
| 🧮 **Co-occurrence Engine** | Normalized co-occurrence matrix with type-aware scoring |
| 🎯 **Smart Scoring** | Weighted co-scores + soft category bias + spicy-aware logic |
| 📦 **Batch Predict** | Bulk CSV predictions for 1,000+ test cases |
| 📊 **Metrics Dashboard** | Item distribution charts, top items by category |
| 🧩 **Architecture View** | Interactive Mermaid flowchart of the recommendation pipeline |

---

## 🏗️ Architecture

```
User Cart (up to 3 items)
        │
        ▼
┌─────────────────────┐
│   Normalize Items    │  ← fuzzy matching to catalog
└─────────┬───────────┘
          ▼
┌─────────────────────┐
│  Co-occurrence       │  ← P(j|i) from 1.4M orders
│  Score Aggregation   │
└─────────┬───────────┘
          ▼
┌─────────────────────┐
│  Type-Aware Bias     │  ← boost underrepresented categories
│  + Spicy Awareness   │
└─────────┬───────────┘
          ▼
┌─────────────────────┐
│  Diversity Filter    │  ← max 1 per type (main/side/dip/drink)
│  + Fallback Fill     │
└─────────┬───────────┘
          ▼
    Top-3 Recommendations
```

---

## 📁 Project Structure

```
SmartCart/
├── streamlit_app.py          # Main entry point (Streamlit app)
├── app/
│   ├── data_loader.py        # CSV loading, item parsing, co-matrix builder
│   ├── recommender.py        # Scoring engine, batch predict, normalization
│   ├── ui_components.py      # Reusable UI — badges, cards, icons
│   └── styles.css            # Premium dark theme with animations
├── data/
│   ├── customer_data.csv     # 563K customer records
│   ├── store_data.csv        # 38 store records
│   └── test_data_question.csv # 1,000 test cases
├── artifacts/                # Generated model artifacts (gitignored)
├── assets/team/              # Team photos
├── notebooks/
│   └── final.ipynb           # Original hackathon notebook
├── docs/
│   └── JaiMataDi_Presentation.pdf
├── .streamlit/config.toml    # Streamlit dark theme config
├── requirements.txt
├── render.yaml               # Render deployment blueprint
├── Procfile                  # Heroku/Render process file
└── runtime.txt               # Python version spec
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- pip

### Install & Run

```bash
# Clone the repository
git clone https://github.com/bhaskarkarn1/SmartCart.git
cd SmartCart

# Install dependencies
pip install -r requirements.txt

# Start the app
streamlit run streamlit_app.py
```

### First Run
1. Navigate to **🧱 Build Model (First Run)** in the sidebar
2. If `order_data.csv` is missing, click **Download** (auto-downloads from Google Drive)
3. Set sample size and click **🚀 Build Now**
4. Head to **🛒 Menu & Recommendations** to start getting suggestions!

---

## 🌐 Deployment

### Render (Recommended)

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/bhaskarkarn1/SmartCart)

Or manually:
1. Go to [render.com](https://render.com) → **New Web Service**
2. Connect GitHub repo `bhaskarkarn1/SmartCart`
3. Render auto-detects `render.yaml` — just click **Deploy**

### Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Select repo → Main file: `streamlit_app.py`
3. Click **Deploy**

---

## 📊 Performance

| Metric | Baseline | SmartCart | Improvement |
|--------|----------|----------|-------------|
| Recall@3 | ~0.20 | ~0.50 | **+150%** |
| Precision@3 | ~0.15 | ~0.38 | **+153%** |
| Top-1 Accuracy | ~0.30 | ~0.52 | **+73%** |

---

## 🧠 How It Works

1. **Data Ingestion** — Parses 1.4M order records with JSON-embedded item details
2. **Item Tagging** — Classifies 138 items into `main`, `side`, `dip`, `drink`, `other`
3. **Co-occurrence Matrix** — Computes conditional probability P(j|i) for all item pairs
4. **Scoring Engine** — Aggregates co-scores with:
   - Soft bias for underrepresented categories (1.5× boost for drinks)
   - Spicy-aware bonuses
   - Non-food blacklist filtering
5. **Diversity Filter** — Ensures max 1 recommendation per type
6. **Fallback Fill** — Uses global popularity when co-occurrence data is sparse

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | Streamlit, Custom CSS (Dark Theme) |
| Backend | Python, Pandas, NumPy |
| Fonts | Plus Jakarta Sans (Google Fonts) |
| Deployment | Render / Streamlit Cloud |
| Data | CSV + JSON parsing |

---

## 👥 Team JaiMataDi

| | Name | LinkedIn |
|---|------|----------|
| 🧑‍💻 | **Bhaskar Ranjan Karn** | [linkedin.com/in/bhaskar-ranjan-karn](https://linkedin.com/in/bhaskar-ranjan-karn/) |
| 🧑‍💻 | **Astitva** | [linkedin.com/in/astitva-07a338229](https://linkedin.com/in/astitva-07a338229/) |
| 🧑‍💻 | **Sanjay Kumar** | [linkedin.com/in/sanjay-kumar-39b73a239](https://linkedin.com/in/sanjay-kumar-39b73a239/) |

---

## 📝 Data Notes

- `order_data.csv` (~578MB) is **not committed** due to size — downloaded at runtime via Google Drive
- `customer_data.csv`, `store_data.csv`, `test_data_question.csv` are included in `data/`
- Generated artifacts (`artifacts.pkl`) are gitignored and rebuilt on first run

---

<div align="center">

**Made with ❤️ by Team JaiMataDi**

*WWT Unravel 2025*

</div>
