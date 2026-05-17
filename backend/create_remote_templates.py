
import os

base_dir = "/app/app/templates/sarlaft_docs"
os.makedirs(base_dir, exist_ok=True)

templates = [
    '1_manual_politica.html', '2_matriz_riesgos.html', '3_formato_kyc.html',
    '4_procedimiento_dd.html', '5_acta_nombramiento.html', '6_plan_capacitacion.html',
    '7_formato_ros.html'
]

html_template = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <style>
        body {{ font-family: Arial, sans-serif; padding: 40px; }}
        h1 {{ color: #1F4E79; }}
        h2 {{ color: #2E75B6; }}
        .header {{ border-bottom: 4px solid #1F4E79; padding-bottom: 10px; margin-bottom: 20px; }}
        .info {{ margin-bottom: 20px; color: #333; }}
        .footer {{ border-top: 1px solid #ccc; padding-top: 10px; margin-top: 40px; font-size: 12px; color: #666; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
        th, td {{ border: 1px solid #ccc; padding: 8px; text-align: left; }}
        th {{ background-color: #1F4E79; color: white; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>{title_display}</h1>
    </div>
    
    <div class="info">
        <p><strong>Razón Social:</strong> {{{{ razon_social }}}}</p>
        <p><strong>NIT:</strong> {{{{ nit }}}}</p>
        <p><strong>Ciudad:</strong> {{{{ ciudad }}}}</p>
        <p><strong>Departamento:</strong> {{{{ departamento }}}}</p>
        <p><strong>Dirección:</strong> {{{{ direccion }}}}</p>
        <p><strong>Teléfono:</strong> {{{{ telefono }}}}</p>
        <p><strong>Correo Electrónico:</strong> {{{{ correo }}}}</p>
    </div>
    
    <div class="content">
        <h2>Representante Legal</h2>
        <p><strong>Nombre:</strong> {{{{ representante_legal }}}}</p>
        <p><strong>Cédula:</strong> {{{{ rep_cedula }}}}</p>
        
        <h2>Oficial de Cumplimiento</h2>
        <p><strong>Nombre:</strong> {{{{ nombre_oc }}}}</p>
        <p><strong>Cédula:</strong> {{{{ oc_cedula }}}}</p>
        <p><strong>Correo:</strong> {{{{ oc_correo }}}}</p>

        <h2>Datos de Operación</h2>
        <p><strong>Empleados:</strong> {{{{ empleados }}}}</p>
        <p><strong>Zonas de Operación:</strong> {{{{ zonas_operacion }}}}</p>
        <p><strong>Servicios:</strong> {{{{ servicios }}}}</p>
        <p><strong>Ingresos Anuales COP:</strong> {{{{ ingresos_anuales }}}}</p>
        <p><strong>Régimen:</strong> {{{{ regimen }}}}</p>
        <p><strong>Fecha de Implementación:</strong> {{{{ fecha_implementacion }}}}</p>
        
        <!-- Otras variables para ROS, KYC, Capacitación y Matriz -->
        <p style="display:none;">
            {{{{ numero_acta }}}} {{{{ oc_formacion }}}} {{{{ oc_horas }}}} {{{{ oc_institucion }}}} {{{{ oc_experiencia_meses }}}}
            {{{{ oc_suplente_nombre }}}} {{{{ oc_suplente_cedula }}}} {{{{ oc_suplente_correo }}}}
            {{{{ fecha_vinculacion }}}} {{{{ numero_registro }}}} {{{{ tipo_contraparte }}}}
            {{{{ nombre_cliente }}}} {{{{ cedula_cliente }}}} {{{{ rep_legal_cliente }}}} {{{{ cedula_rep_cliente }}}}
            {{{{ anio_ros }}}} {{{{ consecutivo_ros }}}} {{{{ fecha_reporte }}}} {{{{ fecha_deteccion }}}}
            {{{{ nombre_reportado }}}} {{{{ documento_reportado }}}} {{{{ direccion_reportado }}}} {{{{ telefono_reportado }}}}
            {{{{ actividad_reportado }}}} {{{{ monto }}}} {{{{ descripcion_operacion }}}} {{{{ senales_alerta }}}}
            {{{{ justificacion }}}} {{{{ accion_tomada }}}} {{{{ otra_tipologia }}}} {{{{ otra_evidencia }}}}
            {{{{ anio_plan }}}} {{{{ costo_asesor }}}} {{{{ costo_material }}}} {{{{ total_presupuesto }}}}
            {{{{ periodo_inicio }}}} {{{{ periodo_fin }}}} {{{{ fecha_informe }}}} {{{{ version_informe }}}}
            {{{{ resumen_ejecutivo }}}} {{{{ contrapartes_nuevas }}}} {{{{ verificaciones_listas }}}}
            {{{{ coincidencias_positivas }}}} {{{{ casos_rechazados }}}} {{{{ op_inusuales }}}} {{{{ ros_enviados }}}}
            {{{{ ausencia_ros }}}} {{{{ empleados_capacitados }}}} {{{{ alertas_gestionadas }}}}
            {{{{ descripcion_casos_relevantes }}}} {{{{ deficiencia_1 }}}} {{{{ plan_1 }}}} {{{{ fecha_1 }}}}
            {{{{ deficiencia_2 }}}} {{{{ plan_2 }}}} {{{{ fecha_2 }}}} {{{{ deficiencia_3 }}}} {{{{ plan_3 }}}} {{{{ fecha_3 }}}}
            {{{{ cambios_normativos }}}} {{{{ recomendaciones }}}} {{{{ nombre_receptor }}}} {{{{ cargo_receptor }}}} {{{{ cedula_receptor }}}}
        </p>
    </div>

    <div class="footer">
        <p>Generado automáticamente por SARLAFT Modern AI - {{{{ fecha_implementacion }}}}</p>
        <p>Versión 1.0</p>
    </div>
</body>
</html>
"""

for t in templates:
    title_display = t.replace('_', ' ').replace('.html', '').upper()
    content = html_template.format(title=t, title_display=title_display)
    with open(os.path.join(base_dir, t), 'w', encoding='utf-8') as f:
        f.write(content)

print(f"Creados 7 templates HTML en {base_dir}")
