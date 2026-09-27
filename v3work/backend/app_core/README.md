# OIL SIF Precursor Intelligence Platform

AI-assisted safety intelligence dashboard for Oil India Limited (OIL), built for the
Smart India Hackathon prototype. Identifies Serious Injury / Fatality (SIF) precursor
patterns from Unsafe Act / Unsafe Condition / Near Miss / Incident reports, with a
human-in-the-loop HSE review workflow.

## 1. Where these files go

Your existing project lives at:

```
C:\Users\parvathy\OneDrive\Desktop\oil-sif
```

Copy/extract everything from this delivered package **into that folder**, merging with
what's already there. This package does not touch or delete any existing files —
it only adds:

```
oil-sif/
├── app.py                          # entry point — streamlit run app.py
├── requirements.txt
├── README.md
└── src/
    ├── __init__.py
    └── frontend/
        ├── __init__.py
        ├── mock_data.py            # synthetic OIL-style report dataset (clearly marked as mock)
        ├── data_api.py             # BACKEND INTEGRATION SEAM — swap mock calls for real DB/ML here
        ├── styles.py                # design system / CSS (industrial dark theme, risk-semantic colors)
        ├── charts.py                # Plotly chart builders
        ├── components.py            # reusable UI building blocks (KPI cards, badges, reasoning flow, etc.)
        └── pages_/
            ├── __init__.py
            ├── overview.py
            ├── report_analysis.py
            ├── sif_risk.py
            ├── precursor_intelligence.py
            ├── barrier_analysis.py
            ├── life_saving_rules.py
            ├── sites_activities.py
            ├── reports.py
            └── hse_review.py
```

If your existing repo already had a `src/` or `app.py`, review for conflicts before
copying over — but this structure was designed to be additive and self-contained.

## 2. Install & run

From inside `C:\Users\parvathy\OneDrive\Desktop\oil-sif`, using your existing `venv`:

```powershell
# activate your existing virtual environment
venv\Scripts\activate

# install the (small) dependency set — safe even if already partially installed
pip install -r requirements.txt

# run the app
streamlit run app.py
```

The app will open at `http://localhost:8501`.

## 3. What's real vs. mock right now

- **Mock (clearly marked):** `src/frontend/mock_data.py` generates a synthetic but
  internally-consistent dataset of ~400 safety reports (sites, hazards, activities,
  Life-Saving Rules, barriers, failures, consequences all map to each other logically,
  not randomly).
- **Integration seam:** `src/frontend/data_api.py` is the contract the UI depends on
  (`analyze_report`, `get_reports`, `get_site_risk`, `get_precursor_patterns`,
  `get_barrier_failures`, `get_lsr_statistics`, `get_pending_reviews`,
  `submit_review_decision`). Every function has a `BACKEND INTEGRATION POINT` comment
  showing exactly what to replace when your MySQL database and NLP/ML pipeline are ready.
  Function signatures are designed not to change, so the UI won't need rework.
- The UI already frames all AI outputs as **"AI-assessed"** / **"suggested"**, never as
  a final safety determination — this framing must be preserved when you wire in the
  real model.

## 4. Human-in-the-loop workflow

The **HSE Review** page implements: AI flags → HSE officer reviews → Confirm / Reject /
Correct. Corrections are written back to the (currently in-memory) dataset via
`submit_review_decision()` — replace this with a write to your `review_decisions` table
and a feedback record for model retraining.

## 5. Notes

- Built and tested against Streamlit 1.32+, Plotly 5.18+, Pandas 2.x — matches what's
  already in your `venv` per your environment description.
- No new heavyweight frontend frameworks were introduced, per your constraints.
- Every page (`Overview`, `Report Analysis`, `SIF Risk`, `Precursor Intelligence`,
  `Barrier Analysis`, `Life-Saving Rules`, `Sites & Activities`, `Reports`, `HSE Review`)
  was smoke-tested end-to-end with no import errors, broken charts, or broken navigation.
