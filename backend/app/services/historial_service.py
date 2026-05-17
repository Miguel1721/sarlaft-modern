"""
Servicio para guardar consultas en el historial
"""

from sqlalchemy.orm import Session
from datetime import datetime
from typing import Dict, Any, List
from ..models import HistorialConsulta


async def guardar_consulta_en_historial(
    db: Session,
    cda_id: int,
    tipo_documento: str,
    numero_documento: str,
    nombre_contraparte: str,
    tipo_consulta: str,
    cliente_id: str,
    resultados_json: Dict[str, Any],
    ip_origen: str = None,
    user_agent: str = None,
    tiempo_ejecucion_segundos: int = None
) -> HistorialConsulta:
    """
    Guarda una consulta en el historial

    Args:
        db: Sesión de base de datos
        cda_id: ID del CDA que realizó la consulta
        tipo_documento: Tipo de documento (CC, CE, NIT, etc.)
        numero_documento: Número de documento consultado
        nombre_contraparte: Nombre de la contraparte
        tipo_consulta: Tipo de consulta (SARLAFT_CDA, SARLAFT_COMPLETO, etc.)
        cliente_id: ID interno del cliente
        resultados_json: Resultados completos de la consulta
        ip_origen: IP desde donde se hizo la consulta
        user_agent: User agent del navegador
        tiempo_ejecucion_segundos: Tiempo que tomó la consulta

    Returns:
        Instancia de HistorialConsulta guardada
    """

    # Extraer información del resultado
    summary = resultados_json.get("summary", {})
    details = resultados_json.get("details", {})

    # Determinar nivel de riesgo y decisión
    status = summary.get("status", "VERDE")
    if status == "VERDE":
        nivel_riesgo = "BAJO"
        decision = "APROBADO"
    elif status == "AMARILLO":
        nivel_riesgo = "MEDIO"
        decision = "REVISION_MANUAL"
    else:  # ROJO
        nivel_riesgo = "ALTO"
        decision = "RECHAZADO"

    # Verificar si está en listas restrictivas
    listas_encontradas = []
    en_lista_restrictiva = False

    # Revisar internacionales (OFAC, ONU, UE)
    for lista_key in ["ofac", "onu", "ue"]:
        if lista_key in details:
            lista_data = details[lista_key]
            if isinstance(lista_data, dict) and lista_data.get("en_lista"):
                en_lista_restrictiva = True
                nombre_lista = lista_data.get("nombre_lista", lista_key.upper())
                listas_encontradas.append(nombre_lista)

    # Revisar alertas legales
    for connector in ["policia", "procuraduria", "contraloria"]:
        if connector in details:
            connector_data = details[connector]
            if isinstance(connector_data, dict) and connector_data.get("status") != "LIMPIO":
                listas_encontradas.append(f"Alerta legal: {connector}")

    # Contar conectores exitosos y fallidos
    conectores_ejecutados = []
    conectores_exitosos = 0
    conectores_fallidos = 0

    for nombre, resultado in details.items():
        if nombre == "concepto_ia":
            continue
        conectores_ejecutados.append(nombre)
        if isinstance(resultado, dict):
            if resultado.get("status") == "ERROR":
                conectores_fallidos += 1
            else:
                conectores_exitosos += 1

    # Verificar si se generó PDF
    pdf_generado = "pdf_url" in resultados_json
    pdf_path = resultados_json.get("pdf_url", "")

    # Crear registro de historial
    historial = HistorialConsulta(
        cda_id=cda_id,
        tipo_documento=tipo_documento,
        numero_documento=numero_documento,
        nombre_contraparte=nombre_contraparte,
        tipo_consulta=tipo_consulta,
        cliente_id=cliente_id,
        resultados_json=resultados_json,
        score_riesgo=_calcular_score_riesgo(nivel_riesgo, listas_encontradas),
        nivel_riesgo=nivel_riesgo,
        decision=decision,
        conectores_ejecutados=conectores_ejecutados,
        conectores_exitosos=conectores_exitosos,
        conectores_fallidos=conectores_fallidos,
        listas_restrictivas_encontradas=listas_encontradas,
        en_lista_restrictiva=en_lista_restrictiva,
        ip_origen=ip_origen,
        user_agent=user_agent,
        tiempo_ejecucion_segundos=tiempo_ejecucion_segundos,
        pdf_generado=pdf_generado,
        pdf_path=pdf_path
    )

    db.add(historial)
    db.commit()
    db.refresh(historial)

    return historial


def _calcular_score_riesgo(nivel_riesgo: str, listas_restrictivas: List[str]) -> int:
    """
    Calcula un score de riesgo (0-100) basado en el nivel y listas restrictivas

    Args:
        nivel_riesgo: Nivel de riesgo (BAJO, MEDIO, ALTO, CRITICO)
        listas_restrictivas: Lista de listas restrictivas encontradas

    Returns:
        Score de 0 a 100
    """
    base_score = {
        "BAJO": 20,
        "MEDIO": 50,
        "ALTO": 75,
        "CRITICO": 90
    }.get(nivel_riesgo, 20)

    # Aumentar score si está en listas restrictivas
    if listas_restrictivas:
        # Por cada lista restrictiva, sumar 10 puntos (máximo +30)
        bonus = min(len(listas_restrictivas) * 10, 30)
        base_score = min(base_score + bonus, 100)

    return base_score
