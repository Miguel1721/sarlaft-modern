
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import CDAEmpresa, ContraparteKYC, EvidenciaLog
from ..services.orchestrator_service import run_full_audit
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(prefix="/api/v1/kyc", tags=["KYC"])

class KYCRequest(BaseModel):
    nombre_completo: str
    documento: str
    tipo_persona: str = "Natural"
    actividad_economica: str
    origen_fondos: str
    es_pep: bool = False
    client_id: str
    placa: str = "XXX000"

@router.post("/vincular")
async def vincular_contraparte(req: KYCRequest, db: Session = Depends(get_db)):
    # 1. Buscar el CDA
    cda = db.query(CDAEmpresa).filter(CDAEmpresa.nit == req.client_id).first()
    if not cda:
        # Para pruebas, si no existe el CDA lo creamos o usamos uno por defecto
        cda = CDAEmpresa(nit=req.client_id, razon_social="CDA Generico", representante_legal="Prueba")
        db.add(cda)
        db.commit()
        db.refresh(cda)

    # 2. Disparar el Orquestador
    reporte_sarlaft = await run_full_audit(req.placa, req.documento, req.client_id)
    
    # 3. Guardar Contraparte
    contraparte = db.query(ContraparteKYC).filter(ContraparteKYC.documento == req.documento).first()
    if not contraparte:
        contraparte = ContraparteKYC(
            cda_id=cda.id,
            tipo_persona=req.tipo_persona,
            documento=req.documento,
            nombre_completo=req.nombre_completo,
            actividad_economica=req.actividad_economica,
            origen_fondos=req.origen_fondos,
            es_pep=req.es_pep
        )
        db.add(contraparte)
        db.commit()
        db.refresh(contraparte)

    # 4. Guardar Evidencia
    evidencia = EvidenciaLog(
        cda_id=cda.id,
        contraparte_id=contraparte.id,
        orquestador_json_raw=reporte_sarlaft,
        score_riesgo=0 if reporte_sarlaft['summary']['status'] == 'VERDE' else 85,
        decision_tomada="Aprobado" if reporte_sarlaft['summary']['status'] == 'VERDE' else "Rechazado",
        usuario_auditor="SISTEMA_IA"
    )
    db.add(evidencia)
    db.commit()

    return {
        "status": "SUCCESS",
        "contraparte_id": contraparte.id,
        "dictamen": evidencia.decision_tomada,
        "reporte": reporte_sarlaft
    }
