# OIL-SIF V4 — Management Command Center + Employee HSE Mail Notice

## What changed

### Employee reporting
- Added a clear notice at the top of the employee "Report a safety concern" flow:
  "A copy of your report will be mailed to HSE."
- Explains that the report is saved securely and copied to HSE for review/follow-up.
- Existing email workflow remains intact: the backend sends an HSE email for every submitted employee safety report when SMTP is configured.

### Management heatmap
- Reworked the management geographic view into a dark geospatial risk-surface presentation inspired by facility heatmaps.
- Uses the actual supplied U.S. state outline and state-level report-density data.
- Added glowing/pulsing concentration hotspots, state labels, selected-state focus, hotspot ranking, legend, historical timeline, activity lens, search, and "Why this signal?" explanation.
- Keeps the important distinction: intensity is report concentration, not model-derived SIF probability.

### Management command center
Visible improvements include:
- Management Command Center hero
- Animated KPI cards
- Management attention alert
- State/activity search
- Historical concentration trend
- Quick management actions
- Safety Assistant entry point
- Executive Safety Briefing / Story Mode
- State intelligence / explainability panel
- Site risk overview
- Activity → hazard → barrier → report evidence trail
- Management priorities

### Accessibility
- Added Enhanced readability mode in Settings.
- It increases readability and reduces/softens non-essential animation.
- Existing dark/light mode, voice help, keyboard interaction, and reduced-motion behavior remain.

### Navigation
- Management users can now open the AI Safety Assistant from the main navigation.

## Run

Backend:
```powershell
cd "PROJECT_FOLDER\backend"
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m uvicorn main:app --reload --port 8000
```

Frontend:
```powershell
cd "PROJECT_FOLDER\frontend"
npm install
npm run dev
```

Open http://localhost:5173
