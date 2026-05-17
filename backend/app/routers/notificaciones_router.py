"""
API Router para Notificaciones por Email
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import Optional

from ..database import get_db
from ..auth.dependencies import oauth2_scheme
from ..services.email_integration import enviar_notificacion_post_consulta, verificar_configuracion_email
from ..services.email_service import EmailNotificationService
from ..models import HistorialConsulta, CDAEmpresa

router = APIRouter(prefix="/notificaciones", tags=["Notificaciones"])


class EmailTestRequest(BaseModel):
    """Request para enviar email de prueba"""
    to_email: EmailStr
    message: Optional[str] = "Este es un email de prueba del sistema SARLAFT 4.0"


class SMTPConfigUpdate(BaseModel):
    """Request para actualizar configuración SMTP"""
    smtp_host: Optional[str] = None
    smtp_port: Optional[int] = None
    smtp_user: Optional[str] = None
    smtp_password: Optional[str] = None
    from_email: Optional[str] = None
    from_name: Optional[str] = None


async def get_current_cda_id(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> int:
    """Obtiene el cda_id del token JWT"""
    from ..auth.security import decode_token

    payload = decode_token(token)
    if not payload or "id" not in payload:
        raise HTTPException(
            status_code=401,
            detail="Token inválido"
        )

    return payload["id"]


@router.get("/config/status")
async def verificar_configuracion():
    """
    Verifica el estado de la configuración de email

    Returns:
        Estado de configuración SMTP
    """
    return verificar_configuracion_email()


@router.post("/test")
async def enviar_email_prueba(
    request: EmailTestRequest,
    cda_id: int = Depends(get_current_cda_id),
    db: Session = Depends(get_db)
):
    """
    Envía un email de prueba para verificar la configuración SMTP

    Args:
        request: Email de destino y mensaje personalizado
        cda_id: ID del CDA autenticado
        db: Sesión de base de datos

    Returns:
        Confirmación de envío
    """
    # Obtener CDA
    cda = db.query(CDAEmpresa).filter(CDAEmpresa.id == cda_id).first()
    if not cda:
        raise HTTPException(status_code=404, detail="CDA no encontrado")

    # Crear email de prueba simple
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    import smtplib
    import os

    try:
        # Verificar configuración
        smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
        smtp_port = int(os.getenv("SMTP_PORT", "587"))
        smtp_user = os.getenv("SMTP_USER", "")
        smtp_password = os.getenv("SMTP_PASSWORD", "")
        from_email = os.getenv("FROM_EMAIL", "noreply@sarlaf.agentesia.cloud")
        from_name = os.getenv("FROM_NAME", "SARLAFT 4.0")

        if not smtp_user or not smtp_password:
            raise HTTPException(
                status_code=400,
                detail="Servicio de email no configurado. Configure SMTP_USER y SMTP_PASSWORD"
            )

        # Crear mensaje
        msg = MIMEMultipart('alternative')
        msg['Subject'] = '🧪 Email de Prueba - SARLAFT 4.0'
        msg['From'] = f"{from_name} <{from_email}>"
        msg['To'] = request.to_email

        # HTML content
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f9fafb; padding: 30px; border: 1px solid #e5e7eb; }}
                .success {{ background: #d1fae5; padding: 15px; border-left: 4px solid #10b981; margin: 20px 0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🧪 Email de Prueba</h1>
                    <p>SARLAFT 4.0 - Sistema de Debida Diligencia</p>
                </div>
                <div class="content">
                    <h2>✅ Configuración SMTP Correcta</h2>

                    <p>Estimado(a) <strong>{cda.razon_social}</strong>,</p>

                    <p>Este email confirma que la configuración SMTP del sistema SARLAFT 4.0 está funcionando correctamente.</p>

                    <div class="success">
                        <strong>✅ Servicio de Notificaciones Activado</strong>
                        <p>El sistema podrá enviar notificaciones automáticas después de cada consulta.</p>
                    </div>

                    <p><strong>Mensaje personalizado:</strong></p>
                    <p>{request.message}</p>

                    <p>Fecha y hora de prueba: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>

                    <p>Atentamente,</p>
                    <p><strong>Equipo SARLAFT 4.0</strong></p>
                </div>
            </div>
        </body>
        </html>
        """

        html_part = MIMEText(html_content, 'html')
        msg.attach(html_part)

        # Enviar email
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.send_message(msg)

        return {
            "status": "exitoso",
            "mensaje": "Email de prueba enviado correctamente",
            "destino": request.to_email,
            "fecha_hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error enviando email de prueba: {str(e)}"
        )


@router.post("/reenviar/{consulta_id}")
async def reenviar_notificacion_consulta(
    consulta_id: int,
    cda_id: int = Depends(get_current_cda_id),
    db: Session = Depends(get_db)
):
    """
    Reenvía el email de notificación de una consulta específica

    Args:
        consulta_id: ID de la consulta
        cda_id: ID del CDA autenticado
        db: Sesión de base de datos

    Returns:
        Confirmación de envío
    """
    # Verificar que la consulta pertenezca al CDA
    consulta = db.query(HistorialConsulta).filter(
        HistorialConsulta.id == consulta_id,
        HistorialConsulta.cda_id == cda_id
    ).first()

    if not consulta:
        raise HTTPException(
            status_code=404,
            detail="Consulta no encontrada"
        )

    # Verificar si tiene PDF
    pdf_path = None
    if consulta.pdf_generado and consulta.pdf_path:
        # La ruta del PDF es relativa a la URL, convertir a ruta del sistema
        pdf_path = consulta.pdf_path.replace("/api/v1/download/", "")
        pdf_path = f"/app/app/services/{pdf_path}"

    # Enviar notificación
    exitoso = await enviar_notificacion_post_consulta(db, consulta, pdf_path)

    if exitoso:
        return {
            "status": "exitoso",
            "mensaje": "Notificación reenviada correctamente",
            "consulta_id": consulta_id
        }
    else:
        raise HTTPException(
            status_code=500,
            detail="Error reenviando notificación"
        )


@router.get("/historial")
async def listar_historial_notificaciones(
    limite: int = 20,
    cda_id: int = Depends(get_current_cda_id),
    db: Session = Depends(get_db)
):
    """
    Lista el historial de notificaciones enviadas (basado en historial de consultas)

    Args:
        limite: Cantidad máxima de registros
        cda_id: ID del CDA autenticado
        db: Sesión de base de datos

    Returns:
        Lista de consultas con notificaciones enviadas
    """
    from sqlalchemy import desc

    # Obtener consultas recientes del CDA
    consultas = db.query(HistorialConsulta).filter(
        HistorialConsulta.cda_id == cda_id
    ).order_by(desc(HistorialConsulta.fecha_consulta)).limit(limite).all()

    # Convertir a lista de diccionarios
    resultados = []
    for consulta in consultas:
        # Verificar si se habría enviado email (tiene PDF o consulta reciente)
        notificacion_enviada = consulta.pdf_generado

        resultados.append({
            "consulta_id": consulta.id,
            "fecha_consulta": consulta.fecha_consulta,
            "nombre_contraparte": consulta.nombre_contraparte,
            "documento": consulta.numero_documento,
            "nivel_riesgo": consulta.nivel_riesgo,
            "decision": consulta.decision,
            "notificacion_enviada": notificacion_enviada,
            "pdf_generado": consulta.pdf_generado
        })

    return {
        "total": len(resultados),
        "items": resultados
    }
