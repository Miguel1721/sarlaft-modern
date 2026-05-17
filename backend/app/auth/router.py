"""
API Router para autenticación
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from pydantic import EmailStr

from ..database import get_db
from ..models import CDAEmpresa
from .security import verify_password, get_password_hash, create_access_token
from .dependencies import LoginRequest, RegisterRequest, Token

router = APIRouter(prefix="/auth", tags=["Autenticación"])

# Scheme para OAuth2 (token en header)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


@router.post("/register", response_model=Token)
async def register(req: RegisterRequest, db: Session = Depends(get_db)):
    """
    Registra un nuevo CDA (Centro de Diagnóstico Automotor)

    Args:
        req: Datos de registro
        db: Sesión de base de datos

    Returns:
        Token de acceso
    """
    # Verificar si ya existe el NIT
    existing_cda = db.query(CDAEmpresa).filter(CDAEmpresa.nit == req.nit).first()
    if existing_cda:
        raise HTTPException(
            status_code=400,
            detail="El NIT ya está registrado"
        )

    # Verificar si ya existe el email
    existing_email = db.query(CDAEmpresa).filter(CDAEmpresa.email == req.email).first()
    if existing_email:
        raise HTTPException(
            status_code=400,
            detail="El email ya está registrado"
        )

    # Crear nuevo CDA
    nuevo_cda = CDAEmpresa(
        nit=req.nit,
        razon_social=req.razon_social,
        email=req.email,
        password_hash=get_password_hash(req.password),
        representante_legal=req.representante_legal,
        nivel_riesgo_aceptado="BAJO"
    )

    try:
        db.add(nuevo_cda)
        db.commit()
        db.refresh(nuevo_cda)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error al crear CDA: {str(e)}"
        )

    # Crear token de acceso
    token_data = {
        "sub": nuevo_cda.nit,
        "id": nuevo_cda.id,
        "email": nuevo_cda.email
    }

    access_token = create_access_token(token_data)

    return Token(
        access_token=access_token,
        token_type="bearer"
    )


@router.post("/login", response_model=Token)
async def login(req: LoginRequest, db: Session = Depends(get_db)):
    """
    Login de CDA

    Args:
        req: Credenciales de login
        db: Sesión de base de datos

    Returns:
        Token de acceso
    """
    # Buscar CDA por email
    cda = db.query(CDAEmpresa).filter(CDAEmpresa.email == req.email).first()

    if not cda:
        raise HTTPException(
            status_code=401,
            detail="Credenciales inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Verificar password
    if not verify_password(req.password, cda.password_hash):
        raise HTTPException(
            status_code=401,
            detail="Credenciales inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Crear token de acceso
    token_data = {
        "sub": cda.nit,
        "id": cda.id,
        "email": cda.email
    }

    access_token = create_access_token(token_data)

    return Token(
        access_token=access_token,
        token_type="bearer"
    )


@router.get("/me")
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """
    Obtiene el usuario actual basado en el token

    Args:
        token: Token JWT del header Authorization
        db: Sesión de base de datos

    Returns:
        Información del usuario actual
    """
    # Decodificar token
    from .security import decode_token
    payload = decode_token(token)

    if not payload:
        raise HTTPException(
            status_code=401,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Buscar usuario
    cda = db.query(CDAEmpresa).filter(CDAEmpresa.id == payload.get("id")).first()

    if not cda:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    return {
        "id": cda.id,
        "nit": cda.nit,
        "razon_social": cda.razon_social,
        "email": cda.email,
        "representante_legal": cda.representante_legal,
        "nivel_riesgo_aceptado": cda.nivel_riesgo_aceptado
    }


@router.get("/verify")
async def verify_token(token: str = Depends(oauth2_scheme)):
    """
    Verifica si un token es válido sin devolver usuario info

    Args:
        token: Token JWT del header Authorization

    Returns:
        Confirmación de validez
    """
    from .security import decode_token
    payload = decode_token(token)

    if not payload:
        raise HTTPException(
            status_code=401,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return {"valid": True, "user_id": payload.get("id")}
