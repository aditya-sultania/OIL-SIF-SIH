import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import App from './pages/app/App.jsx'
import './styles/global.css'

// NOTE ON SCOPE
// This React project ports the OIL-SIF Streamlit apps one at a time.
// Route "/" (App.jsx) is the full port of the original app.py — the
// live/tracked entry point of the Streamlit project (multilingual UI,
// role-based dashboards, AI hazard scanner, multilingual chatbot).
// Routes for app1.py, app2.py, app3.py, app4.py and "app copy.py" are
// added as /app1, /app2, /app3, /app4, /app-copy as they are ported.

ReactDOM.createRoot(document.getElementById('root')).render(
  <BrowserRouter>
    <Routes>
      <Route path="/" element={<App />} />
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  </BrowserRouter>,
)
