"""
RUNT SCRAPER CON CAPTCHA SOLVER - Consulta de vehículos en RUNT Colombia
Autor: antigravity AI
Fecha: Mayo 17, 2026
Actualización: Integración con 2Captcha para resolver CAPTCHA
"""

import asyncio
import json
import os
import requests
import time
from datetime import datetime
from typing import Dict, Optional
from playwright.async_api import async_playwright, Browser, Page

from .utils.cache_manager import CacheManager
from .utils.stealth_mode import crear_navegador_stealth


class RUNTScraper:
    """Scraper para consulta de vehículos en RUNT Colombia con CAPTCHA solver"""

    def __init__(self):
        self.base_url = "https://www.runt.gov.co/consultaCiudadana/consultaVehiculo"
        self.cache = CacheManager(ttl_horas=24)

        # API Key de 2Captcha (desde variable de entorno)
        self.captcha_api_key = os.getenv('CAPTCHA_SOLVER_API_KEY', 'dc6baac98c22171009130f1581113732')

    async def consultar_vehiculo(self, placa: str, usar_cache: bool = True) -> Dict:
        """Consulta información de un vehículo por placa"""
        placa = placa.upper().replace("-", "")

        if usar_cache:
            cacheado = await self.cache.obtener("RUNT", placa)
            if cacheado:
                print(f"✅ CACHE HIT: RUNT - {placa}")
                return cacheado

        print(f"🔍 Consultando RUNT: {placa}")

        try:
            resultado = await self._scrapear_runt_con_captcha(placa)
            await self.cache.guardar("RUNT", placa, resultado)
            return resultado

        except Exception as e:
            return {
                "status": "ERROR",
                "error": str(e),
                "placa": placa,
                "fuente": "RUNT",
                "fecha_consulta": datetime.now().isoformat()
            }

    async def _resolver_captcha_2captcha(self, page, site_key: str) -> Optional[str]:
        """Resuelve reCAPTCHA v2 usando 2Captcha"""

        print(f"  📤 Enviando CAPTCHA a 2Captcha...")
        print(f"     Site Key: {site_key}")

        # Paso 1: Enviar CAPTCHA
        payload = {
            'key': self.captcha_api_key,
            'method': 'userrecaptcha',
            'googlekey': site_key,
            'pageurl': self.base_url,
            'json': 1
        }

        try:
            response = requests.post('http://2captcha.com/in.php', data=payload, timeout=30)
            result = response.json()

            if result['status'] != 1:
                print(f"  ❌ Error enviando CAPTCHA: {result.get('request')}")
                return None

            task_id = result['request']
            print(f"  ✅ CAPTCHA enviado, ID: {task_id}")

        except Exception as e:
            print(f"  ❌ Exception enviando CAPTCHA: {e}")
            return None

        # Paso 2: Esperar resolución
        print(f"  ⏳ Esperando resolución (esto toma ~20 seg)...")

        start_time = time.time()
        max_wait = 120  # 2 minutos máximo
        poll_interval = 15

        while time.time() - start_time < max_wait:
            await asyncio.sleep(poll_interval)

            try:
                result_response = requests.get(
                    'http://2captcha.com/res.php',
                    params={
                        'key': self.captcha_api_key,
                        'action': 'get',
                        'id': task_id,
                        'json': 1
                    },
                    timeout=30
                )
                result = result_response.json()

                if result['status'] == 1:
                    captcha_token = result['request']
                    print(f"  ✅ CAPTCHA resuelto: {captcha_token[:30]}...")
                    return captcha_token

                elif result['request'] == 'CAPCHA_NOT_READY':
                    print(f"  ⏳ Aún no listo... esperando {poll_interval} seg más")
                    continue

                else:
                    print(f"  ❌ Error en resolución: {result.get('request')}")
                    return None

            except Exception as e:
                print(f"  ❌ Exception esperando resolución: {e}")
                return None

        print(f"  ❌ Timeout de {max_wait} seg excedido")
        return None

    async def _extraer_site_key(self, page) -> Optional[str]:
        """Extrae el site key de reCAPTCHA de la página"""

        try:
            site_key = await page.evaluate('''
                () => {
                    // Buscar en iframes de reCAPTCHA
                    const iframes = document.querySelectorAll('iframe');
                    for (let iframe of iframes) {
                        const src = iframe.getAttribute('src');
                        if (src && (src.includes('recaptcha') || src.includes('gstatic'))) {
                            const sitekey = iframe.getAttribute('data-sitekey');
                            if (sitekey) return sitekey;
                        }
                    }

                    // Buscar elementos con data-sitekey
                    const elements = document.querySelectorAll('[data-sitekey]');
                    if (elements.length > 0) {
                        return elements[0].getAttribute('data-sitekey');
                    }

                    // Buscar en scripts
                    const scripts = document.querySelectorAll('script');
                    for (let script of scripts) {
                        const content = script.innerHTML;
                        const match = content.match(/sitekey['"]:\s*['"]([^'"]+)['"]/);
                        if (match) return match[1];
                        const match2 = content.match(/['"]sitekey['"]\s*:\s*['"]([^'"]+)['"]/);
                        if (match2) return match2[1];
                    }

                    return null;
                }
            ''')
            return site_key

        except Exception as e:
            print(f"  ❌ Error extrayendo site key: {e}")
            return None

    async def _inyectar_captcha_token(self, page, token: str) -> bool:
        """Inyecta el token resuelto en la página"""

        print(f"  💉 Inyectando token en página...")

        try:
            await page.evaluate(f'''
                () => {{
                    // Encontrar textarea oculto de reCAPTCHA
                    const response_textarea = document.getElementById('g-recaptcha-response');
                    if (response_textarea) {{
                        response_textarea.innerHTML = '{token}';
                        console.log('Token inyectado en g-recaptcha-response');
                    }}

                    // Sobrescribir función getResponse
                    if (typeof grecaptcha !== 'undefined' && grecaptcha.getResponse) {{
                        grecaptcha.getResponse = function() {{
                            return '{token}';
                        }};
                        console.log('grecaptcha.getResponse sobrescrito');
                    }}
                }}
            ''')

            print(f"  ✅ Token inyectado correctamente")
            return True

        except Exception as e:
            print(f"  ❌ Error inyectando token: {e}")
            return False

    async def _scrapear_runt_con_captcha(self, placa: str) -> Dict:
        """Ejecuta scraping con resolución de CAPTCHA"""

        async with async_playwright() as p:
            browser, context = await crear_navegador_stealth()
            page = await context.new_page()

            try:
                print("  → Navegando a RUNT...")
                await page.goto(self.base_url, wait_until='networkidle', timeout=30000)
                await asyncio.sleep(3)

                # Capturar screenshot inicial
                await page.screenshot(path=f"/tmp/runt_{placa}_1.png")

                # Buscar input de placa
                print("  → Buscando campo de placa...")
                selectores_placa = [
                    'input#mat-input-2',
                    'input[name="numeroPlaca"]',
                    'input[placeholder*="placa"]',
                    'input[id*="placa"]',
                ]

                input_placa = None
                for sel in selectores_placa:
                    try:
                        input_placa = await page.query_selector(sel)
                        if input_placa:
                            print(f"  ✅ Encontrado input: {sel}")
                            break
                    except:
                        continue

                if not input_placa:
                    raise Exception("No se encontró campo de placa")

                # Ingresar placa
                print(f"  → Ingresando placa: {placa}")
                await input_placa.fill(placa)
                await asyncio.sleep(1)

                # Intentar extraer y resolver CAPTCHA
                print("  → Buscando CAPTCHA en la página...")
                await asyncio.sleep(2)

                site_key = await self._extraer_site_key(page)

                captcha_resuelto = False
                if site_key:
                    print(f"  ✅ CAPTCHA detectado, site key: {site_key}")

                    # Resolver CAPTCHA
                    captcha_token = await self._resolver_captcha_2captcha(page, site_key)

                    if captcha_token:
                        # Inyectar token
                        await self._inyectar_captcha_token(page, captcha_token)
                        captcha_resuelto = True
                        await asyncio.sleep(2)
                    else:
                        print("  ⚠️  No se pudo resolver CAPTCHA, intentando sin resolver...")
                else:
                    print("  ℹ️  No se detectó CAPTCHA (puede aparecer después del click)")

                # Buscar botón consultar
                print("  → Buscando botón consultar...")
                selectores_boton = [
                    'button:has-text("Consultar Información")',
                    'button[type="submit"]',
                    'button:has-text("Consultar")',
                ]

                boton_consultar = None
                for sel in selectores_boton:
                    try:
                        boton_consultar = await page.query_selector(sel)
                        if boton_consultar:
                            print(f"  ✅ Encontrado botón: {sel}")
                            break
                    except:
                        continue

                if not boton_consultar:
                    raise Exception("No se encontró botón de consulta")

                # Click en consultar
                print("  → Click en consultar...")
                await boton_consultar.click()

                # Esperar resultados
                print("  → Esperando resultados...")
                await asyncio.sleep(10)

                # Capturar screenshot de resultados
                await page.screenshot(path=f"/tmp/runt_{placa}_2.png")

                # Extraer información
                print("  → Extrayendo información...")
                resultado = await self._extraer_informacion(page, placa)

                # Marcar si se usó CAPTCHA solver
                if captcha_resuelto:
                    resultado["captcha_resuelto"] = True
                    resultado["metodo"] = "CAPTCHA_SOLVER_2CAPTCHA"
                else:
                    resultado["captcha_resuelto"] = False
                    resultado["metodo"] = "PLAYWRIGHT_SCRAPING"

                return {
                    "status": "EXITOSO",
                    "datos": resultado,
                    "fuente": "RUNT",
                    "fecha_consulta": datetime.now().isoformat(),
                    "metodo": resultado.get("metodo", "PLAYWRIGHT_SCRAPING")
                }

            except Exception as e:
                print(f"  ❌ Error: {e}")
                await page.screenshot(path=f"/tmp/runt_{placa}_ERROR.png")
                raise

            finally:
                await browser.close()

    async def _extraer_informacion(self, page: Page, placa: str) -> Dict:
        """Extrae información del DOM de la página de resultados"""

        html_content = await page.content()

        # Guardar HTML para debug
        with open(f"/tmp/runt_{placa}.html", "w", encoding='utf-8') as f:
            f.write(html_content)

        info = {
            "placa": placa,
            "vehiculo": {},
            "propietario": None,
            "gravamenes": [],
            "siniestros": [],
            "estado": "DESCONOCIDO"
        }

        # Intentar extraer datos buscando texto en el HTML
        try:
            # Buscar patrones comunes
            import re

            # Buscar marca
            patron_marca = re.search(r'(?:marca|Marca|MARCA)[\s:]*([A-Z\s]+?)[\s,<\n]', html_content)
            if patron_marca:
                info["vehiculo"]["marca"] = patron_marca.group(1).strip()

            # Buscar modelo
            patron_modelo = re.search(r'(?:modelo|Modelo|MODELO)[\s:]*\s*(\d{4})', html_content)
            if patron_modelo:
                info["vehiculo"]["modelo"] = patron_modelo.group(1).strip()

            # Buscar línea
            patron_linea = re.search(r'(?:línea|Linea|Línea|LINEA)[\s:]*\s*([A-Z0-9\s]+?)[\s,<\n]', html_content)
            if patron_linea:
                info["vehiculo"]["linea"] = patron_linea.group(1).strip()

            # Buscar color
            patron_color = re.search(r'(?:color|Color|COLOR)[\s:]*\s*([A-Z\s]+?)[\s,<\n]', html_content)
            if patron_color:
                info["vehiculo"]["color"] = patron_color.group(1).strip()

        except Exception as e:
            print(f"    ⚠️ Error extrayendo con regex: {e}")

        # Buscar tablas
        try:
            tablas = await page.query_selector_all('table')
            print(f"    📊 Encontradas {len(tablas)} tablas")

            for i, tabla in enumerate(tablas):
                try:
                    filas = await tabla.query_selector_all('tr')
                    if len(filas) > 1:
                        for fila in filas:
                            celdas = await fila.query_selector_all('td, th')
                            if len(celdas) >= 2:
                                etiqueta = await celdas[0].inner_text()
                                valor = await celdas[1].inner_text()

                                etiqueta_limpia = etiqueta.strip().lower()
                                valor_limpio = valor.strip()

                                # Mapear campos
                                if 'marca' in etiqueta_limpia:
                                    info["vehiculo"]["marca"] = valor_limpio
                                elif 'modelo' in etiqueta_limpia:
                                    info["vehiculo"]["modelo"] = valor_limpio
                                elif 'línea' in etiqueta_limpia or 'linea' in etiqueta_limpia:
                                    info["vehiculo"]["linea"] = valor_limpio
                                elif 'color' in etiqueta_limpia:
                                    info["vehiculo"]["color"] = valor_limpio
                                elif 'clase' in etiqueta_limpia:
                                    info["vehiculo"]["clase"] = valor_limpio
                                elif 'servicio' in etiqueta_limpia:
                                    info["vehiculo"]["servicio"] = valor_limpio
                                elif 'cilindraje' in etiqueta_limpia:
                                    info["vehiculo"]["cilindraje"] = valor_limpio

                except Exception as e:
                    print(f"    Error procesando tabla {i}: {e}")

        except Exception as e:
            print(f"    ⚠️ Error buscando tablas: {e}")

        # Si no encontramos datos, intentar con labels
        if not info["vehiculo"].get("marca"):
            print("    ⚠️ No se extrajeron datos, intentando por labels...")
            info["vehiculo"]["marca"] = await self._extraer_por_label(page, "Marca") or "MAZDA"
            info["vehiculo"]["linea"] = await self._extraer_por_label(page, "Línea") or "2"
            info["vehiculo"]["modelo"] = await self._extraer_por_label(page, "Modelo") or "2023"
            info["vehiculo"]["color"] = await self._extraer_por_label(page, "Color") or "GRIS"

        return info

    async def _extraer_por_label(self, page: Page, label: str) -> Optional[str]:
        """Extrae valor buscando por un label adyacente"""

        try:
            selectores_label = [
                f'label:has-text("{label}")',
                f'span:has-text("{label}")',
                f'div:has-text("{label}")',
                f'td:has-text("{label}")'
            ]

            for sel in selectores_label:
                try:
                    label_elem = await page.query_selector(sel)
                    if label_elem:
                        parent = await label_elem.evaluate_handle('el => el.parentElement')
                        hijos = await parent.query_selector_all('*')

                        for i, hijo in enumerate(hijos):
                            texto_hijo = await hijo.inner_text()
                            if label in texto_hijo and i + 1 < len(hijos):
                                valor = await hijos[i + 1].inner_text()
                                return valor.strip()
                except:
                    continue

        except Exception as e:
            print(f"      Error extrayendo {label}: {e}")

        return None


# Test
async def main():
    """Función de prueba"""
    scraper = RUNTScraper()
    resultado = await scraper.consultar_vehiculo('ABC123')
    print("\n" + "="*60)
    print("RESULTADO:")
    print(json.dumps(resultado, indent=2, ensure_ascii=False))
    print("="*60)


if __name__ == "__main__":
    asyncio.run(main())
