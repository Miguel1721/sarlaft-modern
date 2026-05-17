from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, EmailStr

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

# Pydantic Models
class Token(BaseModel):
    access_token: str
    token_type: str

class LoginRequest(BaseModel):
    email: str  # Changed from EmailStr to str
    password: str

class RegisterRequest(BaseModel):
    nit: str
    razon_social: str
    email: str  # Changed from EmailStr to str
    password: str
    representante_legal: str
