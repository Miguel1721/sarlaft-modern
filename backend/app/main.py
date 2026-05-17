import os
from typing import Optional
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
from .database import engine, Base, get_db
from .routers import api_kyc, onboarding_router, admin_router
# from .routers import contrapartes_router  # Temporarily disabled - needs get_current_user import
from .routers import historial_router
from .auth import router as auth_router
from .auth.dependencies import oauth2_scheme
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
app.include_router(auth_router.router, prefix="/api/v1")
app.include_router(historial_router.router, prefix="/api/v1")
app.include_router(api_kyc.router)
app.include_router(onboarding_router.router)
app.include_router(admin_router.router)
# app.include_router(contrapartes_router.router, prefix="/api/v1")  # Temporarily disabled

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
async def ejecutar_auditoria(
    req: AuditoriaRequest,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    """
    Ejecuta auditoría SARLAFT y guarda en historial

    Args:
        req: Datos de la auditoría
        db: Sesión de base de datos
        token: Token JWT del CDA autenticado

    Returns:
        Resultados de la auditoría
    """
    from .services.historial_service import guardar_consulta_en_historial
    from .auth.security import decode_token
    import time

    # Obtener cda_id del token
    payload = decode_token(token)
    if not payload or "id" not in payload:
        raise HTTPException(status_code=401, detail="Token inválido")

    cda_id = payload["id"]

    # Medir tiempo de ejecución
    inicio = time.time()

    # Ejecutar auditoría
    resultado = await run_full_audit(req.placa, req.cedula, req.client_id, req.tipo_consulta)

    fin = time.time()
    tiempo_ejecucion = int(fin - inicio)

    # Determinar tipo de documento
    tipo_documento = "CEDULA"
    if req.placa:
        tipo_documento = "PLACA"

    # Guardar en historial (async, no bloquea la respuesta)
    try:
        await guardar_consulta_en_historial(
            db=db,
            cda_id=cda_id,
            tipo_documento=tipo_documento,
            numero_documento=req.placa if req.placa else req.cedula,
            nombre_contraparte=req.cedula,  # Podría mejorarse obteniendo el nombre real
            tipo_consulta=req.tipo_consulta,
            cliente_id=req.client_id,
            resultados_json=resultado,
            tiempo_ejecucion_segundos=tiempo_ejecucion
        )
    except Exception as e:
        # No fallar la consulta si hay error guardando historial
        print(f"Error guardando en historial: {e}")

    return resultado

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
