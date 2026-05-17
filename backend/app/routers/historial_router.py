"""
API Router para Historial de Consultas SARLAFT
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, desc
from typing import Optional, Dict

from ..database import get_db
from ..models import HistorialConsulta, CDAEmpresa
from ..auth.dependencies import oauth2_scheme
from .historial_schemas import (
    HistorialItemResponse,
    HistorialDetalleResponse,
    HistorialListResponse,
    HistorialFiltros
)

router = APIRouter(prefix="/historial", tags=["Historial de Consultas"])


async def get_current_cda_id(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> int:
    """
    Obtiene el cda_id del usuario actual del token JWT

    Args:
        token: Token JWT del header Authorization
        db: Sesión de base de datos

    Returns:
        ID del CDA autenticado
    """
    from ..auth.security import decode_token

    payload = decode_token(token)
    if not payload:
        raise HTTPException(
            status_code=401,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )

    cda_id = payload.get("id")
    if not cda_id:
        raise HTTPException(
            status_code=401,
            detail="Token no contiene ID de CDA",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return cda_id


@router.get("", response_model=HistorialListResponse)
async def listar_historial(
    fecha_desde: Optional[str] = Query(None, description="Fecha desde (ISO 8601)"),
    fecha_hasta: Optional[str] = Query(None, description="Fecha hasta (ISO 8601)"),
    tipo_documento: Optional[str] = Query(None, description="Tipo de documento"),
    numero_documento: Optional[str] = Query(None, description="Número de documento"),
    nombre_contraparte: Optional[str] = Query(None, description="Nombre contraparte"),
    tipo_consulta: Optional[str] = Query(None, description="Tipo de consulta"),
    nivel_riesgo: Optional[str] = Query(None, description="Nivel de riesgo"),
    decision: Optional[str] = Query(None, description="Decisión tomada"),
    en_lista_restrictiva: Optional[bool] = Query(None, description="En lista restrictiva"),
    pagina: int = Query(1, ge=1, description="Número de página"),
    por_pagina: int = Query(20, ge=1, le=100, description="Items por página"),
    cda_id: int = Depends(get_current_cda_id),
    db: Session = Depends(get_db)
):
    """
    Lista el historial de consultas del CDA autenticado con filtros y paginación
    """
    # Base query - solo consultas del CDA autenticado
    query = db.query(HistorialConsulta).filter(HistorialConsulta.cda_id == cda_id)

    # Aplicar filtros
    if tipo_documento:
        query = query.filter(HistorialConsulta.tipo_documento == tipo_documento.upper())

    if numero_documento:
        query = query.filter(HistorialConsulta.numero_documento.ilike(f"%{numero_documento}%"))

    if nombre_contraparte:
        query = query.filter(HistorialConsulta.nombre_contraparte.ilike(f"%{nombre_contraparte}%"))

    if tipo_consulta:
        query = query.filter(HistorialConsulta.tipo_consulta == tipo_consulta)

    if nivel_riesgo:
        query = query.filter(HistorialConsulta.nivel_riesgo == nivel_riesgo.upper())

    if decision:
        query = query.filter(HistorialConsulta.decision == decision.upper())

    if en_lista_restrictiva is not None:
        query = query.filter(HistorialConsulta.en_lista_restrictiva == en_lista_restrictiva)

    # Ordenar por fecha descendente (más recientes primero)
    query = query.order_by(desc(HistorialConsulta.fecha_consulta))

    # Contar total
    total = query.count()

    # Aplicar paginación
    offset = (pagina - 1) * por_pagina
    items = query.offset(offset).limit(por_pagina).all()

    # Calcular total de páginas
    total_paginas = (total + por_pagina - 1) // por_pagina

    return HistorialListResponse(
        total=total,
        pagina=pagina,
        por_pagina=por_pagina,
        total_paginas=total_paginas,
        items=items
    )


@router.get("/{consulta_id}", response_model=HistorialDetalleResponse)
async def obtener_detalle_consulta(
    consulta_id: int,
    cda_id: int = Depends(get_current_cda_id),
    db: Session = Depends(get_db)
):
    """
    Obtiene el detalle completo de una consulta específica

    Args:
        consulta_id: ID de la consulta
        cda_id: ID del CDA autenticado (del token)
        db: Sesión de base de datos

    Returns:
        Detalle completo de la consulta
    """
    # Buscar la consulta
    consulta = db.query(HistorialConsulta).filter(
        and_(
            HistorialConsulta.id == consulta_id,
            HistorialConsulta.cda_id == cda_id  # Solo puede ver sus propias consultas
        )
    ).first()

    if not consulta:
        raise HTTPException(
            status_code=404,
            detail="Consulta no encontrada"
        )

    return consulta


@router.delete("/{consulta_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_consulta(
    consulta_id: int,
    cda_id: int = Depends(get_current_cda_id),
    db: Session = Depends(get_db)
):
    """
    Elimina una consulta del historial (solo si pertenece al CDA autenticado)

    Args:
        consulta_id: ID de la consulta a eliminar
        cda_id: ID del CDA autenticado (del token)
        db: Sesión de base de datos
    """
    # Buscar la consulta
    consulta = db.query(HistorialConsulta).filter(
        and_(
            HistorialConsulta.id == consulta_id,
            HistorialConsulta.cda_id == cda_id
        )
    ).first()

    if not consulta:
        raise HTTPException(
            status_code=404,
            detail="Consulta no encontrada"
        )

    # Eliminar (hard delete)
    db.delete(consulta)
    db.commit()

    return None


@router.get("/estadisticas/resumen", response_model=Dict)
async def obtener_estadisticas_resumen(
    cda_id: int = Depends(get_current_cda_id),
    db: Session = Depends(get_db)
):
    """
    Obtiene estadísticas resumidas del historial del CDA

    Returns:
        Diccionario con estadísticas:
        - total_consultas: Total de consultas realizadas
        - consultas_hoy: Consultas realizadas hoy
        - consultas_semana: Consultas realizadas en la última semana
        - aprobadas: Consultas con decisión APROBADO
        - rechazadas: Consultas con decisión RECHAZADO
        - revision_manual: Consultas en revisión manual
        - riesgo_alto: Consultas con nivel de riesgo ALTO o CRITICO
        - en_listas: Consultas que aparecen en listas restrictivas
    """
    from datetime import datetime, timedelta
    from sqlalchemy import func

    # Total de consultas
    total_consultas = db.query(func.count(HistorialConsulta.id)).filter(
        HistorialConsulta.cda_id == cda_id
    ).scalar()

    # Consultas de hoy
    hoy = datetime.now().date()
    consultas_hoy = db.query(func.count(HistorialConsulta.id)).filter(
        and_(
            HistorialConsulta.cda_id == cda_id,
            func.date(HistorialConsulta.fecha_consulta) == hoy
        )
    ).scalar()

    # Consultas de la última semana
    hace_una_semana = datetime.now() - timedelta(days=7)
    consultas_semana = db.query(func.count(HistorialConsulta.id)).filter(
        and_(
            HistorialConsulta.cda_id == cda_id,
            HistorialConsulta.fecha_consulta >= hace_una_semana
        )
    ).scalar()

    # Por decisión
    aprobadas = db.query(func.count(HistorialConsulta.id)).filter(
        and_(
            HistorialConsulta.cda_id == cda_id,
            HistorialConsulta.decision == "APROBADO"
        )
    ).scalar()

    rechazadas = db.query(func.count(HistorialConsulta.id)).filter(
        and_(
            HistorialConsulta.cda_id == cda_id,
            HistorialConsulta.decision == "RECHAZADO"
        )
    ).scalar()

    revision_manual = db.query(func.count(HistorialConsulta.id)).filter(
        and_(
            HistorialConsulta.cda_id == cda_id,
            HistorialConsulta.decision == "REVISION_MANUAL"
        )
    ).scalar()

    # Por riesgo
    riesgo_alo = db.query(func.count(HistorialConsulta.id)).filter(
        and_(
            HistorialConsulta.cda_id == cda_id,
            HistorialConsulta.nivel_riesgo.in_(["ALTO", "CRITICO"])
        )
    ).scalar()

    # En listas restrictivas
    en_listas = db.query(func.count(HistorialConsulta.id)).filter(
        and_(
            HistorialConsulta.cda_id == cda_id,
            HistorialConsulta.en_lista_restrictiva == True
        )
    ).scalar()

    return {
        "total_consultas": total_consultas or 0,
        "consultas_hoy": consultas_hoy or 0,
        "consultas_semana": consultas_semana or 0,
        "aprobadas": aprobadas or 0,
        "rechazadas": rechazadas or 0,
        "revision_manual": revision_manual or 0,
        "riesgo_alto": riesgo_alo or 0,
        "en_listas": en_listas or 0
    }
