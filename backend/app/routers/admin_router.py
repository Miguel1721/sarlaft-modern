
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import EvidenciaLog, ContraparteKYC
from pydantic import BaseModel
from typing import List

router = APIRouter(prefix="/api/v1/admin", tags=["Admin"])

class ApprovalRequest(BaseModel):
    log_id: int
    estado: str # Aprobado / Rechazado

@router.get("/logs/pendientes")
async def get_logs_pendientes(db: Session = Depends(get_db)):
    # Buscamos evidencias que no tengan decisión final o estén en un estado intermedio
    logs = db.query(EvidenciaLog).all() # Simplificado para el dashboard
    resultados = []
    for log in logs:
        contraparte = db.query(ContraparteKYC).filter(ContraparteKYC.id == log.contraparte_id).first()
        resultados.append({
            "id": log.id,
            "documento": contraparte.documento if contraparte else "N/A",
            "nombre": contraparte.nombre_completo if contraparte else "N/A",
            "fecha": log.fecha_consulta,
            "score": log.score_riesgo,
            "decision_ia": log.decision_tomada,
            "status": "Pendiente", # Mock status para el ejercicio
            "pdf_url": log.orquestador_json_raw.get("pdf_url")
        })
    return resultados

@router.post("/logs/aprobar")
async def aprobar_log(req: ApprovalRequest, db: Session = Depends(get_db)):
    log = db.query(EvidenciaLog).filter(EvidenciaLog.id == req.log_id).first()
    if not log:
        raise HTTPException(status_code=404, detail="Log no encontrado")
    
    log.decision_tomada = req.estado
    db.commit()
    
    return {"status": "SUCCESS", "mensaje": f"Consulta {req.log_id} marcada como {req.estado}"}
