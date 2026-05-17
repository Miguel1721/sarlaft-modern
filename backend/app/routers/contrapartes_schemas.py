"""
Schemas para el CRUD de Contrapartes KYC
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ContraparteCreate(BaseModel):
    """Schema para crear contraparte"""
    tipo_persona: str = Field(..., description="NATURAL o JURIDICA")
    documento: str = Field(..., min_length=5, max_length=20)
    nombre_completo: str = Field(..., min_length=3, max_length=200)
    actividad_economica: str = Field(..., max_length=100)
    origen_fondos: str = Field(..., max_length=100)
    es_pep: bool = False


class ContraparteUpdate(BaseModel):
    """Schema para actualizar contraparte"""
    nombre_completo: Optional[str] = Field(None, min_length=3, max_length=200)
    actividad_economica: Optional[str] = Field(None, max_length=100)
    origen_fondos: Optional[str] = Field(None, max_length=100)
    es_pep: Optional[bool] = None


class ContraparteResponse(BaseModel):
    """Schema para respuesta de contraparte"""
    id: int
    cda_id: int
    tipo_persona: str
    documento: str
    nombre_completo: str
    actividad_economica: str
    origen_fondos: str
    es_pep: bool
    fecha_vinculacion: datetime

    class Config:
        from_attributes = True


class ContraparteList(BaseModel):
    """Schema para lista paginada"""
    total: int
    page: int
    per_page: int
    contrapartes: list[ContraparteResponse]
