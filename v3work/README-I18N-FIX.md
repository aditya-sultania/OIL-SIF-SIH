# OIL-SIF Full Interface Translation Fix

The interface language now uses the project's Gemini key for complete DOM-level UI translation, not only the labels present in the static language dictionary.

## Important
Create `backend/app_core/.env`:

```env
GEMINI_API_KEY=YOUR_ACTUAL_GEMINI_API_KEY
```

The backend explicitly loads this file at startup. Restart FastAPI after creating/changing the key.

When a language is selected, visible interface text, placeholders, titles and ARIA labels are translated in batches and cached in the browser. The translator preserves OIL-SIF, SIF, HSE, AI, IOGP, LOTO and similar safety acronyms.
