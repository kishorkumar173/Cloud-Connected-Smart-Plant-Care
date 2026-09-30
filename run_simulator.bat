@echo off
title Smart Plant Cloud - Virtual IoT Sensor Simulator
echo ========================================================
echo Starting Python Virtual IoT Sensor Simulator...
echo Target Endpoint: http://localhost:8000/api/sensors/data
echo Node: PLANT-001 (Roma Tomato)
echo ========================================================
python -m sensor_simulator.simulator
pause
