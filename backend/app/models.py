from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class CDAEmpresa(Base):
    __tablename__ = "cda_empresas"
    id = Column(Integer, primary_key=True, index=True)
    nit = Column(String, unique=True, index=True)
    razon_social = Column(String)
    email = Column(String, unique=True, index=True)  # Agregado para auth
    password_hash = Column(String)  # Agregado para auth
    representante_legal = Column(String)
    oficial_cumplimiento_id = Column(String)
    nivel_riesgo_aceptado = Column(String, default="BAJO")
    fecha_registro = Column(DateTime(timezone=True), server_default=func.now())
    activo = Column(Boolean, default=True)

    contrapartes = relationship("ContraparteKYC", back_populates="cda")

class ContraparteKYC(Base):
    __tablename__ = "contrapartes_kyc"
    id = Column(Integer, primary_key=True, index=True)
    cda_id = Column(Integer, ForeignKey("cda_empresas.id"))
    tipo_persona = Column(String)
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
    decision_tomada = Column(String)
    usuario_auditor = Column(String)

    contraparte = relationship("ContraparteKYC", back_populates="evidencias")

class ListaRestrictivaCache(Base):
    __tablename__ = "lista_restrictiva_cache"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    documento = Column(String, index=True, nullable=True)
    lista_origen = Column(String, index=True)
    fecha_actualizacion = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class HistorialConsulta(Base):
    """Historial completo de todas las consultas SARLAFT realizadas"""
    __tablename__ = "historial_consultas"

    id = Column(Integer, primary_key=True, index=True)
    cda_id = Column(Integer, ForeignKey("cda_empresas.id"), index=True)

    # Información de la contraparte consultada
    tipo_documento = Column(String, index=True)  # CC, CE, NIT, PASAPORTE, etc.
    numero_documento = Column(String, index=True)
    nombre_contraparte = Column(String)

    # Tipo de consulta
    tipo_consulta = Column(String, index=True)  # SARLAFT_CDA, SARLAFT_COMPLETO, KYC_BASICO
    cliente_id = Column(String)  # ID interno del cliente

    # Resultados de la consulta
    resultados_json = Column(JSON)  # Todos los resultados de los conectores
    score_riesgo = Column(Integer, default=0)  # 0-100
    nivel_riesgo = Column(String)  # BAJO, MEDIO, ALTO, CRITICO
    decision = Column(String)  # APROBADO, RECHAZADO, REVISION_MANUAL

    # Detalles de conectores
    conectores_ejecutados = Column(JSON)  # Lista de conectores ejecutados
    conectores_exitosos = Column(Integer, default=0)
    conectores_fallidos = Column(Integer, default=0)

    # Listas restrictivas
    listas_restrictivas_encontradas = Column(JSON)  # Listas donde apareció
    en_lista_restrictiva = Column(Boolean, default=False, index=True)

    # Metadatos
    fecha_consulta = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    ip_origen = Column(String)
    user_agent = Column(String)
    tiempo_ejecucion_segundos = Column(Integer)  # Tiempo que tomó la consulta

    # Archivos generados
    pdf_generado = Column(Boolean, default=False)
    pdf_path = Column(String)

    cda = relationship("CDAEmpresa")
