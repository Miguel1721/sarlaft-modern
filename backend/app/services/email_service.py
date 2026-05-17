"""
Servicio de Notificaciones por Email
Envía emails con PDFs adjuntos y alertas de hallazgos
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from typing import Optional, List
from jinja2 import Template
from datetime import datetime


class EmailService:
    """Servicio para enviar emails usando SMTP"""

    def __init__(self):
        self.smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.smtp_user = os.getenv("SMTP_USER", "")
        self.smtp_password = os.getenv("SMTP_PASSWORD", "")
        self.from_email = os.getenv("FROM_EMAIL", "noreply@sarlaf.agentesia.cloud")
        self.from_name = os.getenv("FROM_NAME", "SARLAFT 4.0 - Sistema de Debida Diligencia")

    def enviar_email(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        attachments: Optional[List[tuple]] = None
    ) -> bool:
        """
        Envía un email usando SMTP

        Args:
            to_email: Email del destinatario
            subject: Asunto del email
            html_content: Contenido HTML del email
            attachments: Lista de tuplas (filename, content_bytes)

        Returns:
            True si se envió correctamente, False si falló
        """
        try:
            # Crear mensaje
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = f"{self.from_name} <{self.from_email}>"
            msg['To'] = to_email

            # Agregar contenido HTML
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)

            # Agregar adjuntos si existen
            if attachments:
                for filename, content in attachments:
                    part = MIMEApplication(content)
                    part.add_header(
                        'Content-Disposition',
                        'attachment',
                        filename=filename
                    )
                    msg.attach(part)

            # Conectar al servidor SMTP
            if self.smtp_user and self.smtp_password:
                with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                    server.starttls()
                    server.login(self.smtp_user, self.smtp_password)
                    server.send_message(msg)
            else:
                # Sin autenticación (para desarrollo)
                with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                    server.send_message(msg)

            return True

        except Exception as e:
            print(f"Error enviando email: {e}")
            return False


# Templates HTML para emails

TEMPLATE_CONFIRMACION_CONSULTA = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }
        .content { background: #f9fafb; padding: 30px; border: 1px solid #e5e7eb; }
        .footer { background: #1f2937; color: white; padding: 20px; text-align: center; border-radius: 0 0 10px 10px; font-size: 12px; }
        .highlight { background: #fef3c7; padding: 15px; border-left: 4px solid #f59e0b; margin: 20px 0; }
        .success { background: #d1fae5; padding: 15px; border-left: 4px solid #10b981; margin: 20px 0; }
        .alert { background: #fee2e2; padding: 15px; border-left: 4px solid #ef4444; margin: 20px 0; }
        .details-table { width: 100%; margin: 20px 0; border-collapse: collapse; }
        .details-table th { background: #1e3a8a; color: white; padding: 12px; text-align: left; }
        .details-table td { padding: 10px; border-bottom: 1px solid #e5e7eb; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🛡️ SARLAFT 4.0</h1>
            <p>Sistema de Debida Diligencia Automotriz</p>
        </div>

        <div class="content">
            <h2>✅ Consulta Completada Exitosamente</h2>

            <p>Estimado(a) <strong>{{ nombre_cda }}</strong>,</p>

            <p>Le informamos que se ha completado exitosamente la consulta de debida diligencia en el marco de la Resolución 2328 de 2025.</p>

            <table class="details-table">
                <tr>
                    <th colspan="2">📋 Detalles de la Consulta</th>
                </tr>
                <tr>
                    <td><strong>Número de Consulta:</strong></td>
                    <td>{{ consulta_id }}</td>
                </tr>
                <tr>
                    <td><strong>Fecha y Hora:</strong></td>
                    <td>{{ fecha_hora }}</td>
                </tr>
                <tr>
                    <td><strong>Tipo de Consulta:</strong></td>
                    <td>{{ tipo_consulta }}</td>
                </tr>
                <tr>
                    <td><strong>Documento Consultado:</strong></td>
                    <td>{{ documento }} ({{ tipo_documento }})</td>
                </tr>
                <tr>
                    <td><strong>Nombre Contraparte:</strong></td>
                    <td>{{ nombre_contraparte }}</td>
                </tr>
                <tr>
                    <td><strong>Nivel de Riesgo:</strong></td>
                    <td>
                        {% if nivel_riesgo == 'BAJO' %}
                            <span style="color: #10b981; font-weight: bold;">✅ BAJO</span>
                        {% elif nivel_riesgo == 'MEDIO' %}
                            <span style="color: #f59e0b; font-weight: bold;">⚠️ MEDIO</span>
                        {% else %}
                            <span style="color: #ef4444; font-weight: bold;">🚨 ALTO</span>
                        {% endif %}
                    </td>
                </tr>
                <tr>
                    <td><strong>Decisión:</strong></td>
                    <td>
                        {% if decision == 'APROBADO' %}
                            <span style="color: #10b981; font-weight: bold;">✅ APROBADO</span>
                        {% elif decision == 'REVISION_MANUAL' %}
                            <span style="color: #f59e0b; font-weight: bold;">🔍 REVISIÓN MANUAL</span>
                        {% else %}
                            <span style="color: #ef4444; font-weight: bold;">❌ RECHAZADO</span>
                        {% endif %}
                    </td>
                </tr>
            </table>

            {% if en_lista_restrictiva %}
            <div class="alert">
                <strong>⚠️ ALERTA:</strong> La contraparte aparece en listas restrictivas: {{ listas_encontradas }}
            </div>
            {% endif %}

            {% if pdf_adjunto %}
            <div class="success">
                <strong>📎 Adjunto:</strong> Encontrará el reporte completo en PDF adjunto a este email.
            </div>
            {% endif %}

            <p><strong>Conectores Ejecutados:</strong> {{ conectores_ejecutados | join(', ') }}</p>
            <p><strong>Tiempo de Ejecución:</strong> {{ tiempo_segundos }} segundos</p>

            <hr style="margin: 30px 0; border: none; border-top: 1px solid #e5e7eb;">

            <p><em>Este reporte ha sido generado automáticamente por el sistema SARLAFT 4.0 y cumple con los requisitos de la Resolución 2328 de 2025 del Ministerio de Transporte.</em></p>

            <p>Para cualquier consulta o aclaración, no dude en contactarnos.</p>

            <p>Atentamente,</p>

            <p><strong>Equipo SARLAFT 4.0</strong><br>
            <a href="mailto:soporte@sarlaf.agentesia.cloud">soporte@sarlaf.agentesia.cloud</a></p>
        </div>

        <div class="footer">
            <p>© 2026 SARLAFT 4.0 - Sistema de Debida Diligencia Automotriz</p>
            <p>Este mensaje es automático, por favor no responda directamente.</p>
        </div>
    </div>
</body>
</html>
"""


TEMPLATE_ALERTA_RIESGO = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .alert-header { background: #dc2626; color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }
        .content { background: #fef2f2; padding: 30px; border: 1px solid #fecaca; }
        .hallazgos { background: #fee2e2; padding: 20px; border-left: 4px solid #ef4444; margin: 20px 0; }
    </style>
</head>
<body>
    <div class="container">
        <div class="alert-header">
            <h1>🚨 ALERTA DE RIESGO</h1>
            <p>Hallazgos Importantes Detectados</p>
        </div>

        <div class="content">
            <h2>⚠️ Consulta con Alertas</h2>

            <p>Estimado(a) <strong>{{ nombre_cda }}</strong>,</p>

            <p>Le informamos que la consulta realizada ha generado alertas importantes que requieren su atención inmediata.</p>

            <div class="hallazgos">
                <h3>🔍 Hallazgos Detectados:</h3>
                <ul>
                    {% for hallazgo in hallazgos %}
                    <li>{{ hallazgo }}</li>
                    {% endfor %}
                </ul>
            </div>

            <table style="width: 100%; margin: 20px 0; border-collapse: collapse;">
                <tr>
                    <td><strong>Documento:</strong></td>
                    <td>{{ documento }}</td>
                </tr>
                <tr>
                    <td><strong>Nombre:</strong></td>
                    <td>{{ nombre_contraparte }}</td>
                </tr>
                <tr>
                    <td><strong>Score de Riesgo:</strong></td>
                    <td><strong style="color: #dc2626;">{{ score_riesgo }}/100</strong></td>
                </tr>
                <tr>
                    <td><strong>Listas Restrictivas:</strong></td>
                    <td>{{ listas_encontradas | join(', ') }}</td>
                </tr>
            </table>

            <p><strong>⚠️ Recomendación:</strong> Se sugiere revisar manualmente esta contraparte antes de proceder con cualquier vinculación comercial.</p>

            <p>El reporte completo en PDF se adjunta a este email.</p>

            <p>Atentamente,</p>
            <p><strong>Equipo SARLAFT 4.0</strong></p>
        </div>
    </div>
</body>
</html>
"""


class EmailNotificationService:
    """Servicio de notificaciones por email para SARLAFT"""

    def __init__(self):
        self.email_service = EmailService()

    async def notificar_consulta_completada(
        self,
        to_email: str,
        nombre_cda: str,
        consulta_id: int,
        fecha_hora: str,
        tipo_consulta: str,
        documento: str,
        tipo_documento: str,
        nombre_contraparte: str,
        nivel_riesgo: str,
        decision: str,
        en_lista_restrictiva: bool,
        listas_encontradas: List[str],
        conectores_ejecutados: List[str],
        tiempo_segundos: int,
        pdf_path: Optional[str] = None
    ) -> bool:
        """
        Envía email de notificación de consulta completada

        Args:
            to_email: Email del CDA
            nombre_cda: Nombre del CDA (razón social)
            consulta_id: ID de la consulta
            fecha_hora: Fecha y hora de la consulta
            tipo_consulta: Tipo de consulta
            documento: Número de documento
            tipo_documento: Tipo de documento
            nombre_contraparte: Nombre de la contraparte
            nivel_riesgo: Nivel de riesgo (BAJO, MEDIO, ALTO)
            decision: Decisión tomada
            en_lista_restrictiva: Si aparece en listas restrictivas
            listas_encontradas: Lista de listas donde apareció
            conectores_ejecutados: Lista de conectores ejecutados
            tiempo_segundos: Tiempo de ejecución
            pdf_path: Ruta del PDF para adjuntar

        Returns:
            True si se envió correctamente
        """

        # Renderizar template
        template = Template(TEMPLATE_CONFIRMACION_CONSULTA)
        html_content = template.render(
            nombre_cda=nombre_cda,
            consulta_id=consulta_id,
            fecha_hora=fecha_hora,
            tipo_consulta=tipo_consulta,
            documento=documento,
            tipo_documento=tipo_documento,
            nombre_contraparte=nombre_contraparte,
            nivel_riesgo=nivel_riesgo,
            decision=decision,
            en_lista_restrictiva=en_lista_restrictiva,
            listas_encontradas=", ".join(listas_encontradas),
            conectores_ejecutados=conectores_ejecutados,
            tiempo_segundos=tiempo_segundos,
            pdf_adjunto=pdf_path is not None
        )

        # Preparar adjuntos
        attachments = []
        if pdf_path and os.path.exists(pdf_path):
            with open(pdf_path, 'rb') as f:
                pdf_content = f.read()
            filename = os.path.basename(pdf_path)
            attachments.append((filename, pdf_content))

        # Enviar email
        subject = f"✅ Consulta SARLAFT Completada - {nombre_contraparte} ({consulta_id})"
        return self.email_service.enviar_email(to_email, subject, html_content, attachments)

    async def notificar_alerta_riesgo(
        self,
        to_email: str,
        nombre_cda: str,
        documento: str,
        nombre_contraparte: str,
        score_riesgo: int,
        hallazgos: List[str],
        listas_encontradas: List[str],
        pdf_path: Optional[str] = None
    ) -> bool:
        """
        Envía email de alerta de riesgo

        Args:
            to_email: Email del CDA
            nombre_cda: Nombre del CDA
            documento: Número de documento
            nombre_contraparte: Nombre de la contraparte
            score_riesgo: Score de riesgo (0-100)
            hallazgos: Lista de hallazgos detectados
            listas_encontradas: Lista de listas donde apareció
            pdf_path: Ruta del PDF

        Returns:
            True si se envió correctamente
        """

        # Renderizar template
        template = Template(TEMPLATE_ALERTA_RIESGO)
        html_content = template.render(
            nombre_cda=nombre_cda,
            documento=documento,
            nombre_contraparte=nombre_contraparte,
            score_riesgo=score_riesgo,
            hallazgos=hallazgos,
            listas_encontradas=listas_encontradas
        )

        # Preparar adjuntos
        attachments = []
        if pdf_path and os.path.exists(pdf_path):
            with open(pdf_path, 'rb') as f:
                pdf_content = f.read()
            filename = os.path.basename(pdf_path)
            attachments.append((filename, pdf_content))

        # Enviar email
        subject = f"🚨 ALERTA DE RIESGO - {nombre_contraparte}"
        return self.email_service.enviar_email(to_email, subject, html_content, attachments)
