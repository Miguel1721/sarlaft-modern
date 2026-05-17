import os
from typing import Optional
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .database import engine, Base
from .routers import api_kyc, onboarding_router, admin_router
from .services.orchestrator_service import run_full_audit
from apscheduler.schedulers.background import BackgroundScheduler
from .services.sync_service import sync_listas_restrictivas

# Initialize Database Tables
Base.metadata.create_all(bind=engine)

# Configuración del Scheduler (Cron Job)
scheduler = BackgroundScheduler()
scheduler.add_job(sync_listas_restrictivas, 'cron', hour=2, minute=0)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    scheduler.start()
    print("APScheduler iniciado. Sincronización programada a las 02:00 AM.")
    yield
    # Shutdown
    scheduler.shutdown()
    print("APScheduler detenido.")

app = FastAPI(title="Sarlaft & Seguros Deep Search API - Modern v4.0", lifespan=lifespan)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(api_kyc.router)
app.include_router(onboarding_router.router)
app.include_router(admin_router.router)

class AuditoriaRequest(BaseModel):
    placa: Optional[str] = None
    cedula: str
    client_id: str
    tipo_consulta: str = "SARLAFT_CDA"

@app.get("/")
async def health_check():
    return {"status": "online", "version": "4.0.3", "module": "KYC, Onboarding & Admin System Active"}

@app.post('/api/v1/auditar')
@app.post('/api/v1/auditar/')
async def ejecutar_auditoria(req: AuditoriaRequest):
    return await run_full_audit(req.placa, req.cedula, req.client_id, req.tipo_consulta)

@app.get('/api/v1/download/{filename}')
async def download_file(filename: str):
    from fastapi.responses import FileResponse
    path = os.path.join('/app/app/services', filename)
    if os.path.exists(path):
        is_zip = filename.endswith('.zip')
        media_type = "application/zip" if is_zip else "application/pdf"
        actual_filename = filename if (filename.endswith('.pdf') or is_zip) else filename + '.pdf'
        return FileResponse(
            path, 
            media_type=media_type,
            headers={"Content-Disposition": f"attachment; filename={actual_filename}"}
        )
    raise HTTPException(status_code=404, detail='Archivo no encontrado')
