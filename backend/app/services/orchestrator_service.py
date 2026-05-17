
import asyncio
import inspect
import os
from . import (
    runt_connector, simit_connector, policia_connector, 
    procuraduria_connector, contraloria_connector, sisben_connector, 
    libreta_militar_connector, internacionales_connector, pdf_generator
)
from .llm_evaluator import generar_concepto_juridico

MATRIZ_CONECTORES = {
    "runt": runt_connector.consultar_vehiculo,
    "simit": simit_connector.consultar_async,
    "policia": policia_connector.consultar_judicial,
    "procuraduria": procuraduria_connector.consultar_async,
    "contraloria": contraloria_connector.consultar_async,
    "sisben": sisben_connector.consultar_async,
    "libreta_militar": libreta_militar_connector.consultar_async,
    "internacionales": internacionales_connector.consultar_listas_internacionales
}

async def run_full_audit(placa: str = None, cedula: str = None, client_id: str = None, tipo_consulta: str = "SARLAFT_CDA"):
    reporte_final = {
        "documento": cedula,
        "placa": placa,
        "client_id": client_id,
        "tipo_consulta": tipo_consulta,
        "summary": {"status": "VERDE", "alerts": []},
        "details": {}
    }

    tasks = []
    
    # Filter connectors based on tipo_consulta
    conectores_activos = dict(MATRIZ_CONECTORES)
    if tipo_consulta == "SARLAFT_CDA":
        conectores_activos.pop("sisben", None)
    elif tipo_consulta == "SARLAFT_B2B":
        conectores_activos.pop("sisben", None)
        conectores_activos.pop("runt", None)
        conectores_activos.pop("simit", None)
    
    for nombre, func in conectores_activos.items():
        sig = inspect.signature(func)
        
        # Smart Routing: Skip vehicle-only connectors if no plate is provided
        if 'placa' in sig.parameters and not placa:
            if nombre in ["runt", "simit"]:
                reporte_final['details'][nombre] = {"status": "NO_APLICA", "mensaje": "Búsqueda omitida (solo identidad)"}
            continue

        params = {}
        if 'placa' in sig.parameters: params['placa'] = placa
        if 'cedula' in sig.parameters: params['cedula'] = cedula
        tasks.append((nombre, func(**params)))

    resultados = await asyncio.gather(*(t[1] for t in tasks), return_exceptions=True)

    for (nombre, _), resultado in zip(tasks, resultados):
        if isinstance(resultado, Exception):
            reporte_final['details'][nombre] = {"status": "ERROR", "error": str(resultado)}
        else:
            if nombre == 'internacionales':
                reporte_final['details'].update(resultado)
            else:
                reporte_final['details'][nombre] = resultado
            
            if nombre in ['policia', 'procuraduria', 'contraloria'] and resultado.get('status') != 'LIMPIO':
                reporte_final['summary']['status'] = 'ROJO'
                reporte_final['summary']['alerts'].append(f'Alerta Legal en {nombre}')
            if nombre == 'runt' and (resultado.get('siniestros') or resultado.get('gravamenes')):
                reporte_final['summary']['status'] = 'ROJO'
                reporte_final['summary']['alerts'].append('Embargo o Siniestro detectado')

    # AI Legal Concept
    try:
        reporte_final['concepto_ia'] = await generar_concepto_juridico(reporte_final)
    except Exception as e:
        reporte_final['concepto_ia'] = "Error generando concepto: " + str(e)
        
    if tipo_consulta == "RRHH":
        reporte_final['disclaimer_rrhh'] = "NOTA LEGAL: Este reporte ha sido generado bajo el perfil de Recursos Humanos (RRHH). Incluye información extraída del Sisbén y otras bases de datos aplicables, procesada en estricto cumplimiento de la Ley 1581 de 2012 (Ley de Protección de Datos Personales / Habeas Data) exclusivamente para fines de selección, contratación o vinculación laboral."

    # PDF Generation - Handle optional placa in filename
    suffix = f"_{placa}" if placa else ""
    pdf_filename = f'reporte_{cedula}{suffix}.pdf'
    pdf_path = os.path.join('/app/app/services', pdf_filename)
    try:
        await pdf_generator.generate_report_pdf(reporte_final, pdf_path)
        reporte_final['pdf_url'] = f'/api/v1/download/{pdf_filename}'
    except Exception as e:
        reporte_final['pdf_error'] = str(e)

    return reporte_final
