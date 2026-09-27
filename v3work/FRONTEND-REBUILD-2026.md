# OIL-SIF Frontend Rebuild — SIH Problem Statement Aligned

This version focuses on the SIH requirement: ingest free-text safety reports, screen SIF potential, map Life-Saving Rules, and surface recurring precursor/barrier patterns in an interactive dashboard.

## Major additions
- Employee-first guided 3-step reporting workflow
- Voice-to-text safety reporting using the browser Speech Recognition API
- Photo attachment/preview for observations
- Immediate danger / Stop Work workflow
- My Reports view with browser-local submission history
- HSE Action Centre with priority queue and clear review workflow
- Human HSE decision controls: Confirm SIF / Not SIF / Needs information
- Corrective-action and validation notes
- AI screening evidence and confidence display
- Full-dataset report search/filter integration through `/api/data/reports`
- CSV export of the current report result set
- Interactive precursor, barrier, Life-Saving Rule and activity drill-downs
- Management executive safety summary and facility focus cards
- Today's/priority-style safety communication patterns
- AI Safety Assistant with guided questions, voice input and read-aloud
- Help modal, system status, notifications, text-size controls, high contrast and Simple Mode
- Responsive layouts with mobile card-style interaction
- Print-friendly management safety brief
- No DOM mutation translation observer in the main application; React state remains the source of truth for language changes

## SIH alignment
1. SIF potential classification — existing `/api/scan` integration retained.
2. IOGP Life-Saving Rule mapping — existing classifier and dataset retained.
3. Recurring precursor patterns — precursor, barrier, activity and LSR views retained and made interactive.
4. Site/activity prioritisation — management and intelligence views highlight risk density and drill-down paths.
5. HSE focus — review queue and human-validation workflow are explicit.

## Demo credentials
- Employee: `employee` / `employee123`
- HSE: `hse` / `hse123`
- Management: `management` / `management123`

## Run
Frontend:
`cd frontend`
`npm install`
`npm run dev`

Backend:
`cd backend`
`python -m uvicorn main:app --reload --port 8000`
