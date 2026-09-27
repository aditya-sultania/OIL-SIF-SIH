# OIL-SIF Frontend Redesign

The React frontend has been redesigned for a formal, accessible and low-friction experience, with middle-aged operational users as the primary audience.

## What changed
- Replaced the dark sci-fi / HUD visual language with a clean high-contrast operational interface.
- Larger typography, clearer hierarchy, bigger click targets and plain-language navigation.
- Role-based navigation remains intact for Employee, HSE Officer and Management.
- Added **Text size** and **Contrast** controls. Preferences persist in the browser.
- Added responsive mobile navigation.
- Added clearer status, facility and user context.
- Simplified sign-in and registration screens with explicit labels and accessible form controls.
- Retained the existing API, authentication, scanning, reports, intelligence and AI Copilot functionality.
- Added reduced-motion support through `prefers-reduced-motion`.

## Faster first load
The previous frontend requested the entire `/api/data/bootstrap` payload immediately after login. The new frontend loads only the dataset required by the current screen:
- Overview -> `/api/data/overview`
- Reports -> `/api/data/queue`
- Intelligence -> precursor, barrier, activity, LSR and queue data in parallel
- HSE dashboard -> queue, barrier and activity data in parallel

This means users reach the main dashboard without waiting for every analytics dataset to be transferred.

## Run
From `frontend/`:
```bash
npm install
npm run dev
```

Production build:
```bash
npm run build
```

The existing backend and `/api` proxy setup are unchanged.
