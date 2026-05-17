"""
Funciones de seguridad para autenticación
"""

from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError
from typing import Optional, Dict

# Importar desde dependencies
SECRET_KEY = "sarlaft-secret-key-change-in-production-2024"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica si el password plain coincide con el hash"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hashea un password usando bcrypt"""
    return pwd_context.hash(password)


def create_access_token(data: Dict, expires_delta: timedelta = None) -> str:
    """Crea un token JWT de acceso"""
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=60*24)  # 24 horas

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> Optional[Dict]:
    """
    Decodifica y valida un token JWT

    Args:
        token: Token JWT a decodificar

    Returns:
        Payload del token o None si es inválido
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
