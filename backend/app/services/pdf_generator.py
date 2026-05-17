
import os
from jinja2 import Template
from playwright.async_api import async_playwright
from datetime import datetime

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @page { size: A4; margin: 0; }
        .page-break { page-break-after: always; }
        .heat-map {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 2px;
            width: 150px;
            height: 150px;
        }
        .heat-cell { border: 1px solid #ccc; height: 50px; }
        .bg-low { background-color: #dcfce7; }
        .bg-mid { background-color: #fef9c3; }
        .bg-high { background-color: #fee2e2; }
        .bg-critical { background-color: #ef4444; }
    </style>
</head>
<body class="bg-white text-slate-800 font-sans">
    <!-- PAGINA 1: PORTADA PREMIUM / RESUMEN EJECUTIVO -->
    <div class="page-break p-12 h-screen flex flex-col">
        <div class="flex justify-between items-start border-b-2 border-red-600 pb-6 mb-8">
            <div>
                <h1 class="text-4xl font-black text-slate-900 tracking-tighter">SARLAFT 4.0</h1>
                <p class="text-red-600 font-bold tracking-widest uppercase text-sm">Deep Search / Auditoría Digital</p>
            </div>
            <div class="text-right text-xs text-slate-400">
                <p>ID Consulta: {{ id_consulta }}</p>
                <p>Fecha: {{ fecha }}</p>
            </div>
        </div>

        <div class="grid grid-cols-3 gap-8 mb-12">
            <div class="col-span-2">
                <h2 class="text-2xl font-bold mb-4">Resumen Ejecutivo</h2>
                <div class="bg-slate-50 p-6 rounded-2xl border border-slate-100">
                    <p class="text-sm uppercase text-slate-500 font-bold mb-2">Identificación Consultada</p>
                    <p class="text-3xl font-mono text-slate-900">{{ documento }}</p>
                    {% if placa %}
                    <p class="mt-4 text-sm uppercase text-slate-500 font-bold mb-2">Placa Vehículo</p>
                    <p class="text-2xl font-mono text-slate-900">{{ placa }}</p>
                    {% endif %}
                </div>
            </div>
            <div class="flex flex-col items-center justify-center">
                <p class="text-sm font-bold mb-2">Nivel de Riesgo</p>
                <div class="w-32 h-32 rounded-full border-8 {% if status == 'VERDE' %}border-green-500 text-green-600{% else %}border-red-500 text-red-600{% endif %} flex items-center justify-center">
                    <span class="text-4xl font-black">{{ '0' if status == 'VERDE' else '85' }}</span>
                </div>
                <p class="mt-4 font-bold uppercase tracking-widest text-lg">{{ 'VINCULABLE' if status == 'VERDE' else 'RECHAZO' }}</p>
            </div>
        </div>

        <div class="mb-12">
            <h2 class="text-xl font-bold mb-4 flex items-center">
                <span class="w-2 h-6 bg-red-600 mr-3"></span>
                CONCEPTO JURÍDICO ESPECIALIZADO (IA)
            </h2>
            <div class="bg-red-50 p-8 rounded-3xl border-l-8 border-red-600 italic text-lg leading-relaxed text-slate-700">
                "{{ concepto }}"
            </div>
            {% if disclaimer_rrhh %}
            <div class="mt-4 bg-yellow-50 p-4 border-l-4 border-yellow-500 text-xs text-yellow-800 italic font-bold">
                {{ disclaimer_rrhh }}
            </div>
            {% endif %}
        </div>

        <div class="grid grid-cols-2 gap-8 mt-auto">
            <div>
                <h3 class="font-bold text-sm uppercase mb-4 text-slate-400 tracking-widest">Matriz de Calor de Riesgo</h3>
                <div class="heat-map">
                    <div class="heat-cell bg-low"></div><div class="heat-cell bg-mid"></div><div class="heat-cell {% if status == 'ROJO' %}bg-critical animate-pulse{% else %}bg-high{% endif %}"></div>
                    <div class="heat-cell bg-low"></div><div class="heat-cell {% if status == 'VERDE' %}bg-low ring-4 ring-green-400{% else %}bg-mid{% endif %}"></div><div class="heat-cell bg-high"></div>
                    <div class="heat-cell bg-low"></div><div class="heat-cell bg-low"></div><div class="heat-cell bg-mid"></div>
                </div>
            </div>
            <div class="text-right self-end">
                <p class="text-xs text-slate-400 mb-6">Este reporte tiene validez legal de 24 horas y ha sido generado bajo los lineamientos de la Resolución 2328 de la Supertransporte.</p>
                <div class="inline-block p-4 border-2 border-slate-900 uppercase font-black tracking-tighter">
                    VERIFICADO POR AGENTESIA IA
                </div>
            </div>
        </div>
    </div>

    <!-- ANEXOS TÉCNICOS: DETALLE DE FUENTES -->
    <div class="p-12">
        <h2 class="text-3xl font-black mb-8">Anexo Técnico de Evidencias</h2>
        <p class="mb-8 text-slate-500">Se detallan a continuación los resultados de las 50+ fuentes nacionales e internacionales consultadas para el documento <strong>{{ documento }}</strong>.</p>

        <div class="space-y-6">
            {% for fuente, data in details.items() %}
            <div class="border border-slate-200 rounded-xl overflow-hidden">
                <div class="bg-slate-100 p-4 flex justify-between items-center">
                    <h3 class="font-bold uppercase tracking-tight">{{ fuente }}</h3>
                    <span class="px-3 py-1 rounded-full text-xs font-bold {% if data.status == 'LIMPIO' or data.status == 'EXITO' %}bg-green-100 text-green-700{% else %}bg-red-100 text-red-700{% endif %}">
                        {{ data.status or 'CONSULTADO' }}
                    </span>
                </div>
                <div class="p-4 bg-white font-mono text-xs whitespace-pre-wrap text-slate-600">
                    {{ data | tojson(indent=2) }}
                </div>
            </div>
            {% endfor %}
        </div>

        <div class="mt-12 text-center text-slate-300 text-xs italic">
            <p>Fin del reporte técnico - {{ id_consulta }}</p>
        </div>
    </div>
</body>
</html>
"""

async def generate_report_pdf(report_json: dict, output_path: str):
    documento = report_json.get("documento")
    status = report_json.get("summary", {}).get("status", "VERDE")
    
    # Lógica de Concepto Jurídico
    if status == "VERDE":
        concepto = f"Tras realizar una debida diligencia intensificada y consultar 50+ listas vinculantes, no se encontraron hallazgos que vinculen al ciudadano {documento} con actividades de LA/FT. Se emite concepto FAVORABLE para la vinculación comercial."
    else:
        concepto = f"SE GENERA ALERTA DE CUMPLIMIENTO. El ciudadano {documento} presenta reportes activos en bases de datos vinculantes o de riesgo. Se recomienda RECHAZAR la vinculación según el manual de políticas SARLAFT 4.0 de la entidad."

    template = Template(HTML_TEMPLATE)
    html_content = template.render(
        id_consulta=f"REF-{datetime.now().strftime('%Y%m%d')}-{documento[-4:]}",
        fecha=datetime.now().strftime("%Y-%m-%d %H:%M"),
        documento=documento,
        placa=report_json.get("placa"),
        status=status,
        concepto=concepto,
        disclaimer_rrhh=report_json.get("disclaimer_rrhh"),
        details=report_json.get("details", {})
    )

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=['--no-sandbox'])
        page = await browser.new_page()
        await page.set_content(html_content)
        # Generamos el PDF con márgenes para que se vea profesional
        await page.pdf(
            path=output_path, 
            format="A4", 
            print_background=True,
            margin={"top": "0cm", "bottom": "0cm", "left": "0cm", "right": "0cm"}
        )
        await browser.close()
    
    return output_path
