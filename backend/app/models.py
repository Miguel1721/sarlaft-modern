
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class CDAEmpresa(Base):
    __tablename__ = "cda_empresas"
    id = Column(Integer, primary_key=True, index=True)
    nit = Column(String, unique=True, index=True)
    razon_social = Column(String)
    representante_legal = Column(String)
    oficial_cumplimiento_id = Column(String)
    nivel_riesgo_aceptado = Column(String, default="BAJO")
    
    contrapartes = relationship("ContraparteKYC", back_populates="cda")

class ContraparteKYC(Base):
    __tablename__ = "contrapartes_kyc"
    id = Column(Integer, primary_key=True, index=True)
    cda_id = Column(Integer, ForeignKey("cda_empresas.id"))
    tipo_persona = Column(String) # Natural / Juridica
    documento = Column(String, index=True)
    nombre_completo = Column(String)
    actividad_economica = Column(String)
    origen_fondos = Column(String)
    es_pep = Column(Boolean, default=False)
    fecha_vinculacion = Column(DateTime(timezone=True), server_default=func.now())

    cda = relationship("CDAEmpresa", back_populates="contrapartes")
    evidencias = relationship("EvidenciaLog", back_populates="contraparte")

class EvidenciaLog(Base):
    __tablename__ = "evidencias_log"
    id = Column(Integer, primary_key=True, index=True)
    cda_id = Column(Integer, ForeignKey("cda_empresas.id"))
    contraparte_id = Column(Integer, ForeignKey("contrapartes_kyc.id"))
    fecha_consulta = Column(DateTime(timezone=True), server_default=func.now())
    orquestador_json_raw = Column(JSON)
    score_riesgo = Column(Integer)
    decision_tomada = Column(String) # Aprobado / Rechazado / Escalado
    usuario_auditor = Column(String)

    contraparte = relationship("ContraparteKYC", back_populates="evidencias")

class ListaRestrictivaCache(Base):
    __tablename__ = "lista_restrictiva_cache"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    documento = Column(String, index=True, nullable=True)
    lista_origen = Column(String, index=True)
    fecha_actualizacion = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
