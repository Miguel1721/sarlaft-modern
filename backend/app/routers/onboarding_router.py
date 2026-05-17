
from fastapi import APIRouter, BackgroundTasks, HTTPException, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from pydantic import BaseModel, Field, validator
from ..services.document_factory import fabrica_docs_onboarding
import zipfile
import os
import shutil
from datetime import datetime

router = APIRouter(prefix="/api/v1/onboarding", tags=["Onboarding"])

class OnboardingCDA(BaseModel):
    razon_social: str
    nit: str
    ciudad: str
    departamento: str = "N/A"
    direccion: str = "N/A"
    telefono: str = "N/A"
    correo: str = "N/A"
    representante_legal: str
    cedula_representante: str = "N/A"
    nombre_oc: str
    oc_cedula: str = "N/A"
    oc_correo: str = "N/A"
    oc_formacion: str = "N/A"
    horas_formacion_oc: str = "N/A"
    institucion_certificante_oc: str = "N/A"
    oc_experiencia_meses: int = Field(default=0, ge=0, description="Meses de experiencia en cumplimiento/SARLAFT")
    
    @validator("horas_formacion_oc", pre=True)
    def coerser_horas_formacion(cls, v):
        if isinstance(v, (int, float)):
            return str(int(v))
        return v
    
    @validator("nombre_oc")
    def debe_tener_apellido(cls, v):
        partes = v.strip().split()
        if len(partes) < 2:
            raise ValueError(
                "Ingrese nombre Y apellido completos del Oficial de Cumplimiento"
            )
        return v.strip().upper()
    ingresos_anuales: float
    empleados: int
    servicios: str
    zonas_operacion: str
    regimen: str = "N/A"
    fecha_implementacion: str
    
    # Variables adicionales opcionales para evitar errores de renderizado
    numero_acta: str = "N/A"
    fecha_aprobacion: str = "N/A"
    año_actual: str = "N/A"
    oc_suplente_nombre: str = "N/A"
    oc_suplente_cedula: str = "N/A"
    oc_suplente_correo: str = "N/A"
    fecha_vinculacion: str = "N/A"
    numero_registro: str = "N/A"
    tipo_contraparte: str = "N/A"
    nombre_cliente: str = "N/A"
    cedula_cliente: str = "N/A"
    rep_legal_cliente: str = "N/A"
    cedula_rep_cliente: str = "N/A"
    anio_ros: str = "N/A"
    consecutivo_ros: str = "N/A"
    fecha_reporte: str = "N/A"
    fecha_deteccion: str = "N/A"
    nombre_reportado: str = "N/A"
    documento_reportado: str = "N/A"
    direccion_reportado: str = "N/A"
    telefono_reportado: str = "N/A"
    actividad_reportado: str = "N/A"
    monto: str = "N/A"
    descripcion_operacion: str = "N/A"
    senales_alerta: str = "N/A"
    justificacion: str = "N/A"
    accion_tomada: str = "N/A"
    otra_tipologia: str = "N/A"
    otra_evidencia: str = "N/A"
    anio_plan: str = "N/A"
    costo_asesor: str = "N/A"
    costo_material: str = "N/A"
    total_presupuesto: str = "N/A"
    periodo_inicio: str = "N/A"
    periodo_fin: str = "N/A"
    fecha_informe: str = "N/A"
    version_informe: str = "1.0"
    resumen_ejecutivo: str = "N/A"
    contrapartes_nuevas: str = "N/A"
    verificaciones_listas: str = "N/A"
    coincidencias_positivas: str = "N/A"
    casos_rechazados: str = "N/A"
    op_inusuales: str = "N/A"
    ros_enviados: str = "N/A"
    ausencia_ros: str = "N/A"
    empleados_capacitados: str = "N/A"
    alertas_gestionadas: str = "N/A"
    descripcion_casos_relevantes: str = "N/A"
    deficiencia_1: str = "N/A"
    plan_1: str = "N/A"
    fecha_1: str = "N/A"
    deficiencia_2: str = "N/A"
    plan_2: str = "N/A"
    fecha_2: str = "N/A"
    deficiencia_3: str = "N/A"
    plan_3: str = "N/A"
    fecha_3: str = "N/A"
    cambios_normativos: str = "N/A"
    recomendaciones: str = "N/A"
    nombre_receptor: str = "N/A"
    cargo_receptor: str = "N/A"
    cedula_receptor: str = "N/A"

def generar_consecutivo_ros(db: Session, tenant_id: str) -> str:
    from datetime import datetime
    from sqlalchemy import text
    anio = datetime.now().year
    
    result = db.execute(
        text("""
        INSERT INTO ros_consecutivos (tenant_id, anio, ultimo_consecutivo)
        VALUES (:tenant_id, :anio, 1)
        ON CONFLICT (tenant_id, anio)
        DO UPDATE SET ultimo_consecutivo = ros_consecutivos.ultimo_consecutivo + 1
        RETURNING ultimo_consecutivo
        """),
        {"tenant_id": tenant_id, "anio": anio}
    )
    db.commit()
    numero = result.scalar()
    return f"ROS-{anio}-{numero:04d}"

@router.post("/generar_kit")
async def generar_kit_sarlaft(cda: OnboardingCDA, db: Session = Depends(get_db)):
    datos_cda = cda.dict()
    
    # Autogeneración de datos del sistema para modo estricto
    ahora = datetime.now()
    datos_cda["año_actual"] = str(ahora.year)
    datos_cda["anio_plan"] = str(ahora.year)
    datos_cda["anio_ros"] = str(ahora.year)
    datos_cda["consecutivo_ros"] = generar_consecutivo_ros(db, cda.nit)
    datos_cda["fecha_reporte"] = ahora.strftime("%Y-%m-%d")
    datos_cda["numero_acta"] = f"ACT-{cda.nit}-{ahora.year}-001"
    datos_cda["fecha_aprobacion"] = cda.fecha_implementacion
    
    # Asegurar que todas las variables del Manual tengan valor
    if "cedula_representante" not in datos_cda:
        datos_cda["cedula_representante"] = datos_cda.get("rep_cedula", "N/A")
    
    # 1. Generar los 7 PDFs
    rutas_pdfs_relativas = await fabrica_docs_onboarding(datos_cda)
    
    # 2. Convertir rutas relativas a rutas absolutas en el sistema de archivos
    # Nota: fabrica_docs_onboarding devuelve /api/v1/download/xxx.pdf
    # Necesitamos las rutas reales en /app/app/services/
    servicios_dir = "/app/app/services"
    archivos_reales = []
    for rel in rutas_pdfs_relativas:
        filename = rel.split("/")[-1]
        archivos_reales.append(os.path.join(servicios_dir, filename))

    # 3. Validar que se generaron archivos
    if not archivos_reales:
        raise HTTPException(status_code=500, detail="Error crítico: No se generó ningún PDF. Revisa los logs del servidor.")

    # 4. Crear el archivo ZIP
    zip_filename = f"Kit_Cumplimiento_SARLAFT_{cda.nit}.zip"
    zip_path = os.path.join(servicios_dir, zip_filename)
    
    try:
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for file in archivos_reales:
                if os.path.exists(file):
                    zipf.write(file, os.path.basename(file))
        
        # 5. Validar que el ZIP no esté vacío
        if os.path.getsize(zip_path) < 100:
             raise HTTPException(status_code=500, detail="El archivo ZIP se generó vacío. Error en la compilación de PDFs.")

        # 6. Limpiar archivos temporales
        for file in archivos_reales:
            try:
                os.remove(file)
            except:
                pass
                
        return {
            "status": "Exito",
            "mensaje": "Kit normativo SARLAFT empaquetado correctamente.",
            "zip_url": f"/api/v1/download/{zip_filename}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear ZIP: {str(e)}")
