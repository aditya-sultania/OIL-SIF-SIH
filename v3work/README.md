# OIL-SIF — React Port

This is a React + FastAPI port of the OIL-SIF Streamlit project. It currently
covers **`app.py`** — the live, git-tracked entry point of the original repo
(multilingual UI, role-based dashboards, AI hazard scanner, multilingual
chatbot).

`app1.py`, `app2.py`, `app3.py`, `app4.py` and `"app copy.py"` are a different,
larger multi-page design (sidebar navigation, no multilingual layer) and are
**not yet ported** — see "What's left" below.

Nothing in the original Python project was changed, added to, or deleted.
The entire original repo is preserved untouched inside `backend/app_core/`.
The FastAPI layer in `backend/main.py` only *calls* that existing code
(the same `.joblib` models, the same `chatbot/assistant.py`, the same CSVs)
and exposes it over HTTP so React can render what Streamlit used to render.

## Project layout

```
oil-sif-react/
├── backend/
│   ├── main.py            # FastAPI wrapper — calls app_core/ code as-is
│   ├── requirements.txt
│   └── app_core/          # untouched copy of the original repo
│       ├── app.py                          (ported)
│       ├── app1.py / app2.py / app3.py     (not yet ported)
│       ├── app4.py / "app copy.py"         (not yet ported)
│       ├── chatbot/
│       ├── *.joblib, *.csv
│       └── ...
└── frontend/
    ├── package.json
    ├── vite.config.js
    └── src/
        ├── api.js                # HTTP client for the FastAPI backend
        ├── components/UI.jsx     # shared building blocks
        ├── styles/global.css     # ported 1:1 from app.py's <style> block
        └── pages/app/            # the app.py port
            ├── App.jsx
            ├── LoginScreen.jsx
            ├── DashboardShell.jsx
            ├── EmployeeDashboard.jsx
            ├── HseDashboard.jsx
            ├── ManagementDashboard.jsx
            └── translations.js   # TRANSLATIONS dict, copied verbatim
```

## Running it

### 1. Backend (FastAPI)

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

The chatbot needs a Gemini API key exactly like the original Streamlit app did.
Put it in `backend/app_core/.env`:

```
GEMINI_API_KEY=your_key_here
```

If it's missing, `/api/chat` automatically falls back to the same canned
response the original `app.py` fell back to on error — no crash.

Then run the server:

```bash
uvicorn main:app --reload --port 8000
```

### 2. Frontend (React + Vite)

```bash
cd frontend
npm install
npm run dev
```

Open the URL Vite prints (usually `http://localhost:5173`). The dev server
proxies `/api/*` to `http://localhost:8000` (see `vite.config.js`), so just
run both servers side by side.

### 3. Production build

```bash
cd frontend
npm run build     # outputs static files to frontend/dist
```
Serve `frontend/dist` with any static host, and point it at your deployed
FastAPI backend (set `VITE`-style proxy/base URL as needed for your host).

## What was ported from app.py

- Multilingual UI (English / Hindi / Assamese) — `TRANSLATIONS` dict copied
  verbatim, not retyped or reworded.
- Login screen: quick 1-click role portals, sign-in form, registration form,
  the "Global Fleet Barrier Health Telemetry" radar chart.
- Field Worker (Employee) view: shift alert banner, hazard presets, the AI
  Guard scanner (calls the real `SIF_Model_v4_DomainAware.joblib` and
  `IOGP_Life_Saving_Rule_Classifier_v2.joblib` models via the backend), the
  Life-Saving Rules card, and the shift safety gauge.
- HSE Officer view: KPI metrics, the SIF review queue table (reads
  `SIF_HSE_Review_Queue_v2.csv` via the backend, with the same dummy fallback
  rows as the original when the CSV is empty), the barrier/activity charts,
  and the multilingual chatbot (calls `chatbot/assistant.py` → Gemini,
  unchanged).
- Management view: the three site-risk cards, the 6-month trend chart, and
  the root-cause drill-down funnel.

Chart library note: the original used Plotly; this port uses Recharts (a
React-native charting library) for the same visualizations, since embedding
Plotly's Python figures directly isn't meaningful once rendering moves to the
browser. Layouts, colors, and data are matched as closely as possible.

## What's left

`app1.py`, `app2.py`, `app3.py`, `app4.py`, and `"app copy.py"` are each
their own large (1,100–1,600 line) Streamlit app with a different design
(sidebar `st.sidebar.radio` navigation, dark-mode toggle, no multilingual
layer). Porting each to the same standard as `app.py` above is the next
phase — say the word and I'll continue with the next one.


### Management geographic heatmap

The Management dashboard now has an animated, accessible geographic safety heatmap as its primary visual:
- Uses the supplied **January 2015–November 2025** dataset (the project copy is verified against the uploaded dataset).
- Uses `State`, `Latitude`, `Longitude`, `FederalState`, incident dates, and derived operational activity groups.
- Shows a U.S. state-level geographic view with animated density bubbles, state selection, hotspot ranking, activity filtering, and a 2015–2025 playback timeline.
- Country scope is explicitly shown as **United States** because the source dataset does not contain a `Country` column. U.S. territories/outlying areas present in `State` remain visible as inset points rather than being silently discarded.
- Heat intensity means **report volume/density only**. It is deliberately not presented as an SIF probability or model confidence.
- The map is backed by `GET /api/management/geography`; the older `/api/management/heatmap` endpoint remains available for compatibility.
- `frontend/public/us-states-outline.svg` is a local vector outline used as the map layer, so the frontend does not depend on an external map service at runtime.
- Motion automatically respects `prefers-reduced-motion` for accessibility.

The rest of the Management workflow is preserved: site risk cards, site drill-down, activity → hazard → barrier investigation, evidence reports, printing, role controls, and existing backend/ML workflows.
