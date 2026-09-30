@echo off
title Smart Plant Cloud - Backend Server
echo ========================================================
echo Starting Cloud-Connected Smart Plant Backend API Server...
echo Host: http://localhost:8000
echo Swagger UI Docs: http://localhost:8000/docs
echo Web Dashboard: http://localhost:8000/
echo ========================================================
python -m uvicorn backend.app:app --host 0.0.0.0 --port 8000 --reload
pause
