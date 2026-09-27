# OIL-SIF — SIH Prototype, Full Workflow Build

This version keeps the original OIL-SIF models/data while adding a real end-to-end operational workflow for the SIH problem statement.

## SIH requirements covered

- SIF-potential vs non-SIF-potential screening
- Automatic IOGP Life-Saving Rule mapping
- Recurring precursor, activity and barrier intelligence
- Site/facility and activity prioritisation
- HSE human validation and corrective-action recording
- Interactive report search and filters
- Employee voice/text/photo reporting
- Management safety brief
- Server-side notifications and report history

## Run in VS Code

### Backend terminal
```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Create `backend/app_core/.env` from `.env.example`:
```env
GEMINI_API_KEY=YOUR_ACTUAL_GEMINI_API_KEY
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

Then:
```powershell
python -m uvicorn main:app --reload --port 8000
```

### Frontend terminal
Open a second terminal:
```powershell
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`.

### Production build
```powershell
cd frontend
npm install
npm run build
```

The project retains the standard Vite React toolchain in `package.json` and `package-lock.json`. The build command requires npm to install the declared dependencies on the machine where it is run.

## Demo accounts

- employee / employee123
- hse / hse123
- management / management123

## New server-side workflow data

Runtime data is stored separately under `backend/app_core/runtime_data/`:

- `submitted_reports.json` — field submissions
- `hse_reviews.json` — HSE decisions for master-dataset reports
- `notifications.json` — user notifications
- `uploads/` — submitted report photos

These files are intentionally small and are not mixed into the source CSV datasets.

## New API capabilities

- `POST /api/reports`
- `GET /api/reports/my`
- `GET /api/reports/{report_id}`
- `GET /api/reports/{report_id}/photo`
- `POST /api/reports/{report_id}/review`
- `GET /api/notifications`
- `POST /api/notifications/read`
- `GET /api/dashboard/summary?days=N`
- `GET /api/intelligence/drilldown?kind=activity&value=...`
- `GET /api/export/reports?...`

## Important safety design

AI is used as a screening/triage aid. It does not replace qualified HSE judgement. The HSE workflow explicitly records the human decision and corrective action.

## Accessibility

The frontend includes:

- Large and extra-large text modes
- Strong high-contrast mode
- Simple-language mode
- Keyboard focus states
- Voice input for employee reports and the AI assistant
- Read-aloud support
- Mobile-friendly layouts
- Guided three-step reporting
- Large action buttons and plain-language help
- 22-language interface support with source-text-preserving runtime translation

## Latest UI refresh

The current React build includes the animated management geographic intelligence view and the HSE density matrix.

- Management: interactive U.S. state report-density map, animated historical timeline, hotspot labels, state intelligence panel, activity lens and polished site-risk/drill-down views.
- HSE: activity × Life-Saving Rule density matrix with SIF-density/report-volume toggle and clickable concentration cells.
- Accessibility: existing keyboard focus, text-size, high-contrast, simple-language and reduced-motion support are preserved.

### Latest HSE endpoint
`GET /api/hse/density` (HSE Officer role) supplies the density matrix from `SIF_HSE_Review_Queue_v2.csv`.

### Fresh ZIP startup
For a new ZIP, run `npm install` once in `frontend` if `node_modules` is not present, then use `npm run dev` for later launches.

### If Management takes a moment after login
V5 includes `backend/app_core/geography_cache.json`, so the large historical geographic CSV is no longer parsed during the first Management page load. Keep the FastAPI terminal running while the React frontend is open.
