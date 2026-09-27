# OIL-SIF — Final SIH Full-Stack Build

## What is included

- React/Vite frontend
- FastAPI backend
- SIF ML model: `SIF_Model_v4_DomainAware.joblib`
- IOGP Life-Saving Rule ML model: `IOGP_Life_Saving_Rule_Classifier_v2.joblib`
- HSE review workflow
- Facility-aware live report scope
- Multilingual interface with stable source-text restoration
- Gemini 3.6 Flash for AI assistant and runtime translation
- Dark/light appearance toggle
- Profile dropdown and settings
- Collapsible desktop sidebar
- Voice input with language-aware browser speech recognition
- Read-aloud support
- Management safety overview

## Run on Windows

1. Install Python 3.10+ and Node.js.
2. Open a terminal in `backend` and run:

```powershell
pip install -r requirements.txt
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

3. In a second terminal:

```powershell
cd frontend
npm install
npm run dev
```

4. Open `http://localhost:5173`.

Or double-click `START-OIL-SIF.bat` after installing dependencies.

## Gemini 3.6

Set `GEMINI_API_KEY` in `backend/app_core/.env` when Gemini features are required. The active Gemini model is `gemini-3.6-flash`.

## Demo accounts

- Employee: `employee` / `employee123`
- HSE: `hse` / `hse123`
- Management: `management` / `management123`

## Facility scope

The historical OIL-SIF master dataset in this project does not contain a facility/site column. Therefore the facility selector scopes live submitted reports, HSE review items and management period metrics. Historical enterprise analytics remain clearly labelled as enterprise-wide rather than pretending they are facility-specific.
