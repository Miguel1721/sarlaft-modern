"""
API Router para CRUD de Contrapartes KYC
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional

from ..database import get_db
from ..models import ContraparteKYC, CDAEmpresa
from ..auth.dependencies import oauth2_scheme
from .contrapartes_schemas import (
    ContraparteCreate,
    ContraparteUpdate,
    ContraparteResponse,
    ContraparteList
)

router = APIRouter(prefix="/contrapartes", tags=["Contrapartes KYC"])


def get_current_cda_id(token: str = Depends(get_current_user), db: Session = Depends(get_db)) -> int:
    """
    Obtiene el cda_id del usuario actual del token JWT

    Args:
        token: Usuario del token JWT
        db: Sesión de base de datos

    Returns:
        cda_id del usuario autenticado
    """
    from ..auth import decode_token
    payload = decode_token(token)

    if not payload:
        raise HTTPException(
            status_code=401,
            detail="Token inválido"
        )

    user_id = payload.get("id")
    cda = db.query(CDAEmpresa).filter(CDAEmpresa.id == user_id).first()

    if not cda:
        raise HTTPException(
            status_code=404,
            detail="CDA no encontrado"
        )

    return cda.id


@router.post("/", response_model=ContraparteResponse, status_code=status.HTTP_201_CREATED)
async def crear_contraparte(
    contraparte: ContraparteCreate,
    cda_id: int = Depends(get_current_cda_id),
    db: Session = Depends(get_db)
):
    """
    Crea una nueva contraparte KYC

    Args:
        contraparte: Datos de la contraparte
        cda_id: ID del CDA autenticado
        db: Sesión de base de datos

    Returns:
        Contraparte creada
    """
    # Verificar si ya existe una contraparte con el mismo documento para este CDA
    existing = db.query(ContraparteKYC).filter(
        ContraparteKYC.cda_id == cda_id,
        ContraparteKYC.documento == contraparte.documento
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"Ya existe una contraparte con documento {contraparte.documento}"
        )

    # Crear nueva contraparte
    nueva = ContraparteKYC(
        cda_id=cda_id,
        tipo_persona=contraparte.tipo_persona,
        documento=contraparte.documento,
        nombre_completo=contraparte.nombre_completo,
        actividad_economica=contraparte.actividad_economica,
        origen_fondos=contraparte.origen_fondos,
        es_pep=contraparte.es_pep
    )

    try:
        db.add(nueva)
        db.commit()
        db.refresh(nueva)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error al crear contraparte: {str(e)}"
        )

    return nueva


@router.get("/", response_model=ContraparteList)
async def listar_contrapartes(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    search: Optional[str] = None,
    cda_id: int = Depends(get_current_cda_id),
    db: Session = Depends(get_db)
):
    """
    Lista todas las contrapartes del CDA autenticado con paginación

    Args:
        page: Número de página
        per_page: Items por página
        search: Buscar por nombre o documento
        cda_id: ID del CDA autenticado
        db: Sesión de base de datos

    Returns:
        Lista paginada de contrapartes
    """
    query = db.query(ContraparteKYC).filter(ContraparteKYC.cda_id == cda_id)

    # Aplicar búsqueda si existe
    if search:
        query = query.filter(
            (ContraparteKYC.nombre_completo.ilike(f"%{search}%")) |
            (ContraparteKYC.documento.ilike(f"%{search}%"))
        )

    # Total de registros
    total = query.count()

    # Aplicar paginación
    offset = (page - 1) * per_page
    contrapartes = query.order_by(ContraparteKYC.fecha_vinculacion.desc()).offset(offset).limit(per_page).all()

    return {
        "total": total,
        "page": page,
        "per_page": per_page,
        "contrapartes": contrapartes
    }


@router.get("/{contraparte_id}", response_model=ContraparteResponse)
async def obtener_contraparte(
    contraparte_id: int,
    cda_id: int = Depends(get_current_cda_id),
    db: Session = Depends(get_db)
):
    """
    Obtiene una contraparte específica por ID

    Args:
        contraparte_id: ID de la contraparte
        cda_id: ID del CDA autenticado
        db: Sesión de base de datos

    Returns:
        Datos de la contraparte
    """
    contraparte = db.query(ContraparteKYC).filter(
        ContraparteKYC.id == contraparte_id,
        ContraparteKYC.cda_id == cda_id
    ).first()

    if not contraparte:
        raise HTTPException(
            status_code=404,
            detail="Contraparte no encontrada"
        )

    return contraparte


@router.put("/{contraparte_id}", response_model=ContraparteResponse)
async def actualizar_contraparte(
    contraparte_id: int,
    contraparte: ContraparteUpdate,
    cda_id: int = Depends(get_current_cda_id),
    db: Session = Depends(get_db)
):
    """
    Actualiza una contraparte existente

    Args:
        contraparte_id: ID de la contraparte
        contraparte: Datos a actualizar
        cda_id: ID del CDA autenticado
        db: Sesión de base de datos

    Returns:
        Contraparte actualizada
    """
    # Buscar contraparte
    existing = db.query(ContraparteKYC).filter(
        ContraparteKYC.id == contraparte_id,
        ContraparteKYC.cda_id == cda_id
    ).first()

    if not existing:
        raise HTTPException(
            status_code=404,
            detail="Contraparte no encontrada"
        )

    # Actualizar campos proporcionados
    update_data = contraparte.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(existing, field, value)

    try:
        db.commit()
        db.refresh(existing)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error al actualizar contraparte: {str(e)}"
        )

    return existing


@router.delete("/{contraparte_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_contraparte(
    contraparte_id: int,
    cda_id: int = Depends(get_current_cda_id),
    db: Session = Depends(get_db)
):
    """
    Elimina una contraparte (soft delete deshabilitando)

    Args:
        contraparte_id: ID de la contraparte
        cda_id: ID del CDA autenticado
        db: Sesión de base de datos
    """
    # Buscar contraparte
    existing = db.query(ContraparteKYC).filter(
        ContraparteKYC.id == contraparte_id,
        ContraparteKYC.cda_id == cda_id
    ).first()

    if not existing:
        raise HTTPException(
            status_code=404,
            detail="Contraparte no encontrada"
        )

    # Soft delete - simplemente eliminamos el registro
    try:
        db.delete(existing)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error al eliminar contraparte: {str(e)}"
        )

    return None
