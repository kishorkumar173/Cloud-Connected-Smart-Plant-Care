# Project Demonstration Screenshots & Proof Checklist

This folder documents the 26 verified proof artifacts required for academic evaluation, GitHub portfolio demonstration, and technical interviews.

---

## Proof Checklist Matrix

| # | Artifact Filename | View / Component | Proof Objective |
|---|---|---|---|
| 01 | `01_project_folder_structure.png` | Terminal / IDE File Explorer | Demonstrates modular folder architecture and separation of concerns. |
| 02 | `02_cloud_architecture_diagram.png` | Architecture Diagram | Explains IoT Perception, Cloud Ingestion, Automation, and UI layers. |
| 03 | `03_sensor_simulator_running.png` | Terminal Console | Shows Python IoT simulator emitting realistic diurnal telemetry ticks. |
| 04 | `04_sensor_api_ingest_request.png` | Postman / Swagger UI | Displays `POST /api/sensors/data` HTTP 201 response with pump decision. |
| 05 | `05_database_records_view.png` | Database Viewer / SQLite | Proves database tables (`devices`, `sensor_readings`, `watering_events`). |
| 06 | `06_dashboard_overview.png` | Web Dashboard | Full view of dark-mode web dashboard showing node PLANT-001. |
| 07 | `07_soil_moisture_kpi_card.png` | KPI Grid Card | Shows real-time soil moisture gauge (e.g., 32.5%) and target threshold. |
| 08 | `08_climate_telemetry_cards.png` | KPI Grid Cards | Displays ambient temperature (29.4°C), humidity (61%), and light (72%). |
| 09 | `09_historical_moisture_graph.png` | Chart.js Graph | Visualizes continuous moisture curve against red dashed threshold line. |
| 10 | `10_healthy_plant_status.png` | Header Badge | Shows green `Healthy` plant status badge with node online indicator. |
| 11 | `11_soil_moisture_dropping.png` | Terminal + Dashboard | Proves gradual soil drying physics down to 29.0%. |
| 12 | `12_low_moisture_alert_trigger.png`| Alert Banner | Shows yellow/red alert: "Soil moisture dropped below threshold". |
| 13 | `13_automatic_watering_triggered.png`| Terminal Log | Shows Cloud Decision Engine actuating pump (`pump_command: ON`). |
| 14 | `14_virtual_pump_active_state.png` | Dashboard KPI Card | Shows blue pulsing `PUMP: ON` status and disabled manual button. |
| 15 | `15_soil_moisture_recovery.png` | Graph / Cards | Demonstrates post-irrigation moisture rising from 29% to 55%. |
| 16 | `16_virtual_pump_deactivated.png` | Dashboard KPI Card | Pump automatically reverts to `OFF` standby after cycle ends. |
| 17 | `17_watering_audit_history.png` | Audit Table | Displays immutable log row with trigger `AUTOMATIC`, before/after %, and duration. |
| 18 | `18_manual_watering_action.png` | Dashboard Action | Demonstrates user clicking "Water Plant Now" and instant pump actuation. |
| 19 | `19_threshold_configuration.png`| Control Panel | Shows slider adjusting trigger threshold (e.g. from 30% to 40%). |
| 20 | `20_device_offline_detection.png` | Alert Banner | Proves heartbeat watchdog marking node OFFLINE when simulator stops. |
| 21 | `21_automated_pytest_results.png` | Terminal Output | Shows 21/21 automated tests passing (`test_api`, `test_engine`, `test_simulator`). |
| 22 | `22_cloud_deployment_dashboard.png`| Cloud Console (Render/Vercel) | Displays deployed cloud services with live HTTPS endpoints. |
| 23 | `23_live_production_app.png` | Web Browser | Shows live deployed dashboard accessible over public internet. |
| 24 | `24_git_commit_history.png` | Git Log / GitHub Commits | Displays clean chronological commit trail from Day 1 to Day 13. |
| 25 | `25_github_repository_home.png` | GitHub Repository Page | Shows repository README badges, topics, and complete source code. |
| 26 | `26_readme_documentation_preview.png`| Markdown Viewer | Displays comprehensive professional README with diagrams and guide. |
