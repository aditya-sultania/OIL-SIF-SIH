# OIL-SIF — Geographic Heatmap Upgrade

## What changed

The existing React + FastAPI application remains the foundation. The upgrade adds a high-visibility geographic management experience without replacing the existing safety workflow.

### Main attraction
- Animated U.S. state hotspot map.
- State bubbles scale with report density.
- Hover/focus/click interaction for individual states.
- Historical year slider from 2015 through 2025.
- Timeline playback for an animated historical scan.
- Activity-group filter.
- Hotspot ranking and selected-state evidence card.
- Federal vs state report breakdown.
- Explicit country scope: United States.

### Accessibility / formal enterprise UX
- Controls use native buttons, selects and range input.
- Map points have keyboard focus and descriptive `aria-label` text.
- No critical information depends on color alone; counts and labels are displayed.
- `prefers-reduced-motion` disables/reduces animation automatically.
- Existing light/dark mode and high-contrast/simple-mode infrastructure remains intact.
- The language and role-based navigation layers remain unchanged.

### Data interpretation
The supplied dataset contains 105,996 records from January 2015 through November 2025, with 56 distinct values in the `State` field. It does not contain a `Country` field, so the UI does not invent country-by-country results. The country scope is explicitly derived as United States, while territories/outlying areas in the source `State` field remain represented.

The geographic heatmap measures historical report volume. It is **not** a model-derived SIF probability, risk score, or prediction.

## Files added/changed

- `frontend/src/pages/app/ManagementDashboard.jsx`
- `frontend/src/styles/global.css`
- `frontend/src/api.js`
- `frontend/public/us-states-outline.svg`
- `frontend/public/state-positions.json`
- `backend/main.py`
- `README.md`

## Existing features preserved

- React/Vite frontend
- FastAPI backend
- Authentication and role-based dashboards
- Employee reporting workflow
- HSE review queue
- SIF and Life-Saving Rule model inference
- Email alert workflow
- Multilingual UI
- Dark/light mode
- High-contrast/simple accessibility options
- Voice input/read-aloud support
- Management site drill-down
- Export/printing functionality

## Validation

- `backend/main.py` passes Python syntax compilation.
- The new geographic backend aggregation was executed successfully against the supplied dataset:
  - 105,996 total records
  - 56 state/area values
  - 11 activity groups
  - 11 annual timeline points (2015–2025)

The bundled `node_modules` in the source archive is retained as supplied. If a local environment reports missing frontend binaries, run `npm install` inside `frontend` before `npm run dev` or `npm run build`.
