# OIL-SIF Backend Enhancements

This release adds the server-side workflow needed by the SIH prototype instead of storing operational actions only in the browser.

## Added endpoints

- `POST /api/reports` — submit a safety observation / near miss, run SIF + Life-Saving Rule screening, persist the report, and optionally persist a photo.
- `GET /api/reports/my` — employee's submitted reports and current HSE status.
- `GET /api/reports/{report_id}` — report detail with HSE decision and corrective action.
- `GET /api/reports/{report_id}/photo` — retrieve an attached report photo.
- `POST /api/reports/{report_id}/review` — HSE human validation: Confirm SIF, Not SIF, or Needs More Information.
- `GET /api/notifications` and `POST /api/notifications/read` — server-side notifications.
- `GET /api/dashboard/summary?days=N` — current submitted-report operational summary.
- `GET /api/intelligence/drilldown?kind=...&value=...` — evidence drill-down for activity, LSR, barrier, precursor, or site.
- `GET /api/export/reports?...` — authenticated CSV export of filtered reports.
- `GET /api/health` — includes model availability and live submitted/pending counts.

## Persistence

Runtime workflow data is stored under `backend/app_core/runtime_data/`:

- `submitted_reports.json`
- `hse_reviews.json`
- `notifications.json`
- `uploads/`

These are intentionally separate from the large source CSV files.

## SIH alignment

The report submission path now explicitly supports the three core SIH outputs:

1. SIF-potential classification
2. IOGP Life-Saving Rule mapping
3. Recurring precursor / activity / barrier intelligence and HSE intervention

The AI result remains a screening aid. The HSE review endpoint records the human decision and corrective action.

## Environment

Optional `.env` setting:

```text
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

Run the API from `backend/` with:

```text
python -m uvicorn main:app --reload --port 8000
```
