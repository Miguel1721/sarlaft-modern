
import os
import jinja2
from playwright.async_api import async_playwright

from jinja2 import Environment, FileSystemLoader, StrictUndefined
TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "..", "templates", "sarlaft_docs")
template_loader = FileSystemLoader(searchpath=TEMPLATE_DIR)
template_env = Environment(loader=template_loader, undefined=StrictUndefined)

async def generar_documento_pdf(nombre_template: str, datos_cda: dict, output_filename: str):
    """
    Toma un HTML estático, inyecta los datos del CDA y lo convierte a PDF.
    """
    try:
        # 1. Cargar el HTML que tú diseñaste
        template = template_env.get_template(nombre_template)
        
        # 2. Inyectar los datos (render)
        html_renderizado = template.render(**datos_cda)
        
        # 3. Usar Playwright para convertir el HTML inyectado a PDF
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True, args=['--no-sandbox'])
            page = await browser.new_page()
            
            # Cargar el HTML en memoria con robustez
            await page.set_content(html_renderizado, wait_until="networkidle")
            await page.wait_for_load_state("domcontentloaded")
            
            # Generar el PDF con formato profesional
            output_path = os.path.join('/app/app/services', output_filename)
            await page.pdf(
                path=output_path, 
                format="A4", 
                print_background=True,
                margin={"top": "2cm", "bottom": "2cm", "left": "2cm", "right": "2cm"}
            )
            
            await browser.close()
            return output_path

    except Exception as e:
        print(f"Error generando {nombre_template}: {str(e)}")
        return None

async def fabrica_docs_onboarding(datos_cda: dict):
    """
    Orquesta la generación de los 7 documentos normativos de un solo golpe.
    """
    documentos = [
        ("1_manual_politica.html", f"Manual_SARLAFT_{datos_cda['nit']}.pdf"),
        ("2_matriz_riesgos.html", f"Matriz_Riesgos_{datos_cda['nit']}.pdf"),
        ("3_formato_kyc.html", f"Formato_KYC_{datos_cda['nit']}.pdf"),
        ("4_procedimiento_dd.html", f"Procedimiento_DD_{datos_cda['nit']}.pdf"),
        ("5_acta_nombramiento.html", f"Acta_OC_{datos_cda['nit']}.pdf"),
        ("6_plan_capacitacion.html", f"Plan_Capacitacion_{datos_cda['nit']}.pdf"),
        ("7_formato_ros.html", f"Formato_ROS_{datos_cda['nit']}.pdf")
    ]
    
    rutas_generadas = []
    for template, output_name in documentos:
        ruta = await generar_documento_pdf(template, datos_cda, output_name)
        if ruta:
            rutas_generadas.append(f"/api/v1/download/{output_name}")
            
    return rutas_generadas
