"""Schemas Pydantic para Historial de Consultas"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class HistorialItemResponse(BaseModel):
    """Respuesta simplificada para listado de historial"""
    id: int
    fecha_consulta: datetime
    tipo_documento: str
    numero_documento: str
    nombre_contraparte: str
    tipo_consulta: str
    score_riesgo: int
    nivel_riesgo: str
    decision: str
    en_lista_restrictiva: bool
    conectores_exitosos: int
    conectores_fallidos: int

    class Config:
        from_attributes = True


class HistorialDetalleResponse(HistorialItemResponse):
    """Respuesta completa con todos los detalles de una consulta"""
    cliente_id: str
    resultados_json: Dict[str, Any]
    conectores_ejecutados: List[str]
    listas_restrictivas_encontradas: List[str]
    ip_origen: Optional[str]
    tiempo_ejecucion_segundos: Optional[int]
    pdf_generado: bool
    pdf_path: Optional[str]


class HistorialListResponse(BaseModel):
    """Respuesta paginada de historial"""
    total: int
    pagina: int
    por_pagina: int
    total_paginas: int
    items: List[HistorialItemResponse]


class HistorialFiltros(BaseModel):
    """Filtros para búsqueda de historial"""
    fecha_desde: Optional[datetime] = None
    fecha_hasta: Optional[datetime] = None
    tipo_documento: Optional[str] = None
    numero_documento: Optional[str] = None
    nombre_contraparte: Optional[str] = None
    tipo_consulta: Optional[str] = None
    nivel_riesgo: Optional[str] = None
    decision: Optional[str] = None
    en_lista_restrictiva: Optional[bool] = None
    pagina: int = Field(default=1, ge=1)
    por_pagina: int = Field(default=20, ge=1, le=100)
