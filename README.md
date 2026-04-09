# SmartCart

SmartCart is a Streamlit-based menu recommendation app built for the WWT Unravel 2025 challenge.
This repository now uses a single project layout instead of keeping separate notebook, prototype,
and web-app copies.

## Project Structure

```text
.
├── app/            # Streamlit app, data loading, recommender logic, UI helpers
├── artifacts/      # Generated model artifacts and sample prediction outputs
├── assets/         # Team images and other app assets
├── data/           # Small datasets kept in repo
├── docs/           # Presentation and static visuals
├── notebooks/      # Original hackathon notebook
├── .streamlit/     # Streamlit config
├── Procfile        # Deployment entrypoint
├── requirements.txt
└── runtime.txt
```

## Run Locally

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Start the app:

```bash
streamlit run streamlit_app.py
```

## Deploy

Recommended target: Streamlit Community Cloud.

Repository settings:

- Entrypoint file: `streamlit_app.py`
- Dependency file: `requirements.txt`
- Config file: `.streamlit/config.toml`
- Python version: `3.12`

## Data Notes

- `customer_data.csv`, `store_data.csv`, and `test_data_question.csv` are included in `data/`.
- `order_data.csv` is intentionally not committed because of its size.
- The app can download `order_data.csv` from Google Drive from the **Build Model (First Run)** page.

## Important Outputs

- Generated batch prediction CSVs are stored in `artifacts/SmartCart_Recommendation_Output.csv`.
- The original competition notebook is kept at `notebooks/final.ipynb`.
- Supporting presentation is in `docs/JaiMataDi_Presentation.pdf`.
