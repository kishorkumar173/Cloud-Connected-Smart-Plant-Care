@echo off
title Smart Plant Cloud - Master Launcher
echo ========================================================
echo Launching Complete Smart Plant Cloud System...
echo 1. Starting Backend API Server (Port 8000)...
echo 2. Starting Virtual IoT Sensor Simulator...
echo ========================================================

start "Backend Server (FastAPI)" cmd /k "python -m uvicorn backend.app:app --host 0.0.0.0 --port 8000 --reload"
timeout /t 3 /nobreak > nul

start "Virtual IoT Simulator" cmd /k "python -m sensor_simulator.simulator"

echo.
echo Both components launched!
echo Open your browser to view the live dashboard:
echo    http://localhost:8000/
echo.
pause
