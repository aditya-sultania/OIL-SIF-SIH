@echo off
setlocal
cd /d "%~dp0"

echo ==========================================
echo OIL-SIF Safety Intelligence Platform
echo ==========================================
echo.

echo Starting FastAPI backend on port 8000...
start "OIL-SIF Backend" cmd /k "cd /d "%~dp0backend" && python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload"

timeout /t 2 /nobreak >nul

echo Starting React frontend on port 5173...
start "OIL-SIF Frontend" cmd /k "cd /d "%~dp0frontend" && npm run dev"

timeout /t 3 /nobreak >nul
start "" http://localhost:5173

echo.
echo OIL-SIF is starting. Keep both terminal windows open.
