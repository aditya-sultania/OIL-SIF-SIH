# OIL-SIF HSE Email Notifications

When an employee submits a safety report, the backend now sends an email notification to the configured HSE recipient(s) for **every submitted report**, not only SIF/critical reports. The report is still saved and appears in the HSE review queue if email delivery is unavailable.

## 1. Create the environment file

Copy:

`backend/app_core/.env.example`

to:

`backend/app_core/.env`

Then fill in the SMTP values.

```env
HSE_ALERT_EMAILS=hse-team@example.com
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_FROM=your-sender@gmail.com
SMTP_USERNAME=your-sender@gmail.com
SMTP_PASSWORD=your-gmail-app-password
SMTP_TLS=true

HSE_EMERGENCY_EMAIL=hse-team@example.com
HSE_EMERGENCY_PHONE=+91XXXXXXXXXX
SITE_EMERGENCY_NUMBER=
```

`HSE_ALERT_EMAILS` can contain multiple recipients separated by commas.

## 2. Gmail

For Gmail, use a Google **App Password** rather than your normal Gmail password when SMTP authentication is enabled. The sender account must have the required Google account security settings enabled.

Example:

```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_FROM=oil.safety.alerts@gmail.com
SMTP_USERNAME=oil.safety.alerts@gmail.com
SMTP_PASSWORD=xxxx xxxx xxxx xxxx
HSE_ALERT_EMAILS=hse.manager@example.com,hse.officer@example.com
```

## 3. What happens after an employee reports

1. The report is classified by the existing SIF/LSR pipeline.
2. The report is saved in the runtime report store.
3. The HSE in-app notification is created.
4. An email is sent to `HSE_ALERT_EMAILS` (or `HSE_EMERGENCY_EMAIL` as fallback).
5. The email contains the report ID, employee, site, location, immediate-danger flag, SIF probability, Life-Saving Rule, hazard, barrier, consequence and observation.
6. The employee sees whether the HSE email was sent successfully.

If SMTP is not configured, the report is **not lost**. It remains available to HSE in the review queue and the employee receives a clear message that email configuration is still required.

## 4. Start the application

Backend:

```powershell
cd "PROJECT_FOLDER\\backend"
.\\venv\\Scripts\\Activate.ps1
python -m uvicorn main:app --reload --port 8000
```

Frontend:

```powershell
cd "PROJECT_FOLDER\\frontend"
npm install
npm run dev
```

Open `http://localhost:5173`.
