@echo off
title Smart Plant Cloud - Master Launcher
echo ========================================================
echo Launching Complete Smart Plant Cloud System...
echo 1. Starting Backend API Server (Port 8000)...
echo 2. Starting React Vite Frontend (Port 5173)...
echo 3. Starting Virtual IoT Sensor Simulator...
echo ========================================================

start "1. Backend Server (FastAPI)" cmd /k "python -m uvicorn backend.app:app --host 0.0.0.0 --port 8000 --reload"
timeout /t 3 /nobreak > nul

start "2. React Frontend (Vite)" cmd /k "cd frontend && npm run dev"
timeout /t 2 /nobreak > nul

start "3. Virtual IoT Simulator" cmd /k "python -m sensor_simulator.simulator"

echo.
echo ========================================================
echo All 3 components successfully launched!
echo.
echo Open your browser to view the dashboards:
echo    👉 React Dashboard (Vite):    http://localhost:5173/
echo    👉 Embedded Dashboard (API):  http://localhost:8000/
echo    👉 Interactive Swagger Docs:  http://localhost:8000/docs
echo ========================================================
echo.
pause
