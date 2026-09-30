@echo off
title Smart Plant Cloud - React Vite Frontend
echo ========================================================
echo Starting React Vite Frontend Development Server...
echo Dev Server: http://localhost:5173
echo ========================================================
cd frontend
if not exist node_modules (
    echo Installing node dependencies...
    npm install
)
npm run dev
pause
