"""
Integración del servicio de email con el orquestador
Envía notificaciones automáticamente después de cada consulta
"""

from sqlalchemy.orm import Session
from typing import Dict, Any, Optional
from datetime import datetime
import os

from .email_service import EmailNotificationService
from ..models import HistorialConsulta, CDAEmpresa


async def enviar_notificacion_post_consulta(
    db: Session,
    consulta: HistorialConsulta,
    pdf_path: Optional[str] = None
) -> bool:
    """
    Envía notificación por email después de completar una consulta

    Args:
        db: Sesión de base de datos
        consulta: Objeto HistorialConsulta con los datos
        pdf_path: Ruta del PDF (opcional)

    Returns:
        True si se envió correctamente
    """

    # Obtener datos del CDA
    cda = db.query(CDAEmpresa).filter(CDAEmpresa.id == consulta.cda_id).first()
    if not cda:
        print(f"Error: CDA con ID {consulta.cda_id} no encontrado")
        return False

    # Verificar si el CDA tiene email configurado
    if not cda.email:
        print(f"CDA {cda.razon_social} no tiene email configurado")
        return False

    # Inicializar servicio de email
    email_service = EmailNotificationService()

    # Determinar si enviar alerta de riesgo o notificación normal
    if consulta.nivel_riesgo in ["ALTO", "CRITICO"] or consulta.en_lista_restrictiva:
        # Preparar hallazgos para alerta
        hallazgos = []

        if consulta.en_lista_restrictiva:
            hallazgos.append(f"Aparece en listas restrictivas: {', '.join(consulta.listas_restrictivas_encontradas)}")

        # Extraer alertas de los resultados
        if consulta.resultados_json and "details" in consulta.resultados_json:
            details = consulta.resultados_json["details"]

            # Alertas legales
            for connector in ["policia", "procuraduria", "contraloria"]:
                if connector in details:
                    connector_data = details[connector]
                    if isinstance(connector_data, dict) and connector_data.get("status") != "LIMPIO":
                        hallazgos.append(f"Alerta en {connector}: {connector_data.get('mensaje', 'Antecedentes encontrados')}")

            # RUNT alertas
            if "runt" in details:
                runt_data = details["runt"]
                if isinstance(runt_data, dict):
                    if runt_data.get("siniestros"):
                        hallazgos.append(f"Vehículo con siniestros reportados")
                    if runt_data.get("gravamenes"):
                        hallazgos.append(f"Vehículo con gravámenes")

        # Enviar alerta de riesgo
        return await email_service.notificar_alerta_riesgo(
            to_email=cda.email,
            nombre_cda=cda.razon_social,
            documento=consulta.numero_documento,
            nombre_contraparte=consulta.nombre_contraparte,
            score_riesgo=consulta.score_riesgo,
            hallazgos=hallazgos,
            listas_encontradas=consulta.listas_restrictivas_encontradas,
            pdf_path=pdf_path
        )
    else:
        # Enviar notificación normal de consulta completada
        return await email_service.notificar_consulta_completada(
            to_email=cda.email,
            nombre_cda=cda.razon_social,
            consulta_id=consulta.id,
            fecha_hora=consulta.fecha_consulta.strftime("%Y-%m-%d %H:%M:%S"),
            tipo_consulta=consulta.tipo_consulta,
            documento=consulta.numero_documento,
            tipo_documento=consulta.tipo_documento,
            nombre_contraparte=consulta.nombre_contraparte,
            nivel_riesgo=consulta.nivel_riesgo,
            decision=consulta.decision,
            en_lista_restrictiva=consulta.en_lista_restrictiva,
            listas_encontradas=consulta.listas_restrictivas_encontradas or [],
            conectores_ejecutados=consulta.conectores_ejecutados or [],
            tiempo_segundos=consulta.tiempo_ejecucion_segundos or 0,
            pdf_path=pdf_path
        )


def verificar_configuracion_email() -> Dict[str, Any]:
    """
    Verifica si el servicio de email está configurado correctamente

    Returns:
        Diccionario con estado de configuración
    """
    smtp_user = os.getenv("SMTP_USER", "")
    smtp_password = os.getenv("SMTP_PASSWORD", "")
    smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")

    config_valid = bool(smtp_user and smtp_password)

    return {
        "configurado": config_valid,
        "smtp_host": smtp_host,
        "smtp_user_configurado": bool(smtp_user),
        "smtp_password_configurado": bool(smtp_password),
        "recomendacion": "Configure SMTP_USER y SMTP_PASSWORD en variables de entorno" if not config_valid else "Servicio listo para usar"
    }
