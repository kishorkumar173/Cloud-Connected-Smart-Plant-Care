"""
Main FastAPI Application Entrypoint
Cloud-Connected Smart Plant Care & Watering System
Integrates REST APIs, database connections, CORS, and cloud observability.
"""

from contextlib import asynccontextmanager
import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from cloud.database_service import init_db
from backend.routes.sensors import router as sensors_router
from backend.routes.devices import router as devices_router
from backend.routes.alerts import router as alerts_router
from backend.routes.analytics import router as analytics_router
from backend.utils.logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager for startup and shutdown hooks."""
    logger.info("Starting Cloud-Connected Smart Plant Care & Watering Platform...")
    try:
        logger.info("Initializing Cloud Database and seeding demo IoT assets...")
        init_db(seed_demo=True)
        logger.info("System initialized successfully. REST APIs and Automation Engines are active.")
    except Exception as e:
        logger.error(f"Non-critical database initialization warning: {str(e)}")
    yield
    logger.info("Shutting down Cloud Smart Plant Care application.")



app = FastAPI(
    title="Cloud-Connected Smart Plant Care & Watering System",
    description=(
        "Industry-grade Cloud IoT Platform featuring telemetry ingestion, automated "
        "precision irrigation logic, species-specific botanical profiles, time-series storage, "
        "environmental anomaly alerts, heartbeat monitoring, and analytical dashboards."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Enable Cross-Origin Resource Sharing (CORS) for React / Vite / Mobile frontends
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API Route Modules
app.include_router(sensors_router)
app.include_router(devices_router)
app.include_router(alerts_router)
app.include_router(analytics_router)

# Locate static dashboard directory
STATIC_DIR = Path(__file__).resolve().parent / "static"

if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.get("/", response_class=HTMLResponse)
async def root():
    """
    Root endpoint serving the embedded web dashboard or redirecting to API docs.
    """
    index_file = STATIC_DIR / "index.html"
    if index_file.exists():
        return FileResponse(str(index_file))

    return HTMLResponse("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Cloud-Connected Smart Plant Care API</title>
        <style>
            body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
                   background: #0f172a; color: #f8fafc; display: flex; align-items: center;
                   justify-content: center; height: 100vh; margin: 0; }
            .card { background: #1e293b; padding: 2.5rem; border-radius: 1rem;
                    border: 1px solid #334155; max-width: 600px; text-align: center; box-shadow: 0 20px 25px -5px rgba(0,0,0,0.5); }
            h1 { color: #10b981; margin-top: 0; }
            p { color: #94a3b8; line-height: 1.6; }
            a { display: inline-block; background: #10b981; color: white; padding: 0.75rem 1.5rem;
                border-radius: 0.5rem; text-decoration: none; font-weight: 600; margin-top: 1rem; }
            a:hover { background: #059669; }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>🌱 Smart Plant Care Cloud API</h1>
            <p>The Cloud-Connected Smart Plant Care & Watering backend is online and accepting telemetry.</p>
            <p>Access the interactive Swagger API documentation and test endpoints directly:</p>
            <a href="/docs">Open Interactive API Docs (Swagger)</a>
        </div>
    </body>
    </html>
    """)


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    uvicorn.run("backend.app:app", host=host, port=port, reload=True)
