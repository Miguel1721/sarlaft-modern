"""
SIMIT SCRAPER - Consulta de multas e infracciones en SIMIT Colombia
Autor: antigravity AI
Fecha: Mayo 17, 2026
"""

import asyncio
import json
import os
from datetime import datetime
from typing import Dict, List, Optional
from playwright.async_api import async_playwright, Browser, Page

from .utils.cache_manager import CacheManager
from .utils.stealth_mode import crear_navegador_stealth


class SIMITScraper:
    """Scraper para consulta de multas e infracciones en SIMIT Colombia"""

    def __init__(self):
        self.base_url = "https://www.fcm.org.co/simit/"
        self.cache = CacheManager(ttl_horas=24)  # Cache 24h

    async def consultar_multas(self, documento: str, usar_cache: bool = True) -> Dict:
        """
        Consulta multas asociadas a una cédula de ciudadanía

        Args:
            documento: Cédula de ciudadanía
            usar_cache: Si True, usa cache
        """
        documento = documento.strip()

        # Verificar cache
        if usar_cache:
            cacheado = await self.cache.obtener("SIMIT", documento)
            if cacheado:
                print(f"✅ CACHE HIT: SIMIT - {documento}")
                return cacheado

        print(f"🔍 Consultando SIMIT: {documento}")

        try:
            resultado = await self._scrapear_simit(documento)

            # Guardar en cache
            await self.cache.guardar("SIMIT", documento, resultado)

            return resultado

        except Exception as e:
            return {
                "status": "ERROR",
                "error": str(e),
                "documento": documento,
                "fuente": "SIMIT",
                "fecha_consulta": datetime.now().isoformat()
            }

    async def _scrapear_simit(self, documento: str) -> Dict:
        """Ejecuta el scraping real de SIMIT"""

        async with async_playwright() as p:
            # Crear navegador en modo stealth
            browser, context = await crear_navegador_stealth()
            page = await context.new_page()

            try:
                # Paso 1: Navegar a SIMIT
                print("  → Navegando a SIMIT...")
                await page.goto(
                    self.base_url,
                    wait_until='domcontentloaded',
                    timeout=30000
                )
                await asyncio.sleep(4)

                # Paso 2: Buscar campo de consulta
                print("  → Buscando formulario...")

                selectores_input = [
                    'input#txtBusqueda',
                    'input[placeholder*="placa"]',
                    'input[placeholder*="documento"]',
                    'input[name*="documento"]',
                    'input#txtConsulta',
                    'input[type="text"]'
                ]

                input_consulta = None
                for sel in selectores_input:
                    try:
                        input_consulta = await page.query_selector(sel)
                        if input_consulta:
                            print(f"  ✅ Encontrado input: {sel}")
                            break
                    except:
                        continue

                if not input_consulta:
                    raise Exception("No se encontró el campo de búsqueda de SIMIT.")

                # Paso 3: Ingresar documento
                print(f"  → Ingresando cédula/placa: {documento}")
                await input_consulta.fill(documento)
                await asyncio.sleep(1)

                # Paso 4: Buscar y hacer click en botón de consulta
                selectores_boton = [
                    'button#consultar',
                    'button[type="submit"]',
                    'button#btnConsultar',
                    'span:has-text("Consultar")',
                    'i.fa-search',
                    'button:has-text("Consultar")'
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
                    raise Exception("No se encontró el botón de búsqueda de SIMIT.")

                # Opcional: Cerrar cualquier modal informativo que intercepte clics
                try:
                    modal_close = await page.query_selector("button.close.modal-info-close, button.close, .modal.show button.close")
                    if modal_close:
                        print("  ⚙️ Detectado popup informativo, cerrándolo...")
                        await modal_close.click(force=True)
                        await asyncio.sleep(1)
                except Exception as modal_err:
                    print(f"  ⚠️ No se pudo cerrar modal (inexistente o no visible): {modal_err}")

                print("  → Click en consultar...")
                # Usar fuerza y evaluación JS directa para sortear cualquier solapamiento CSS de banners
                try:
                    await boton_consultar.click(force=True, timeout=5000)
                except Exception:
                    print("  ⚠️ Click por puntero interceptado, forzando click directo vía JS...")
                    await page.evaluate("el => el.click()", boton_consultar)

                # Paso 5: Esperar resultados
                print("  → Esperando resultados...")
                await asyncio.sleep(5)

                # Paso 6: Extraer información
                print("  → Extrayendo multas...")
                resultado = await self._extraer_informacion(page, documento)

                return {
                    "status": "EXITOSO",
                    "datos": resultado,
                    "fuente": "SIMIT",
                    "fecha_consulta": datetime.now().isoformat(),
                    "metodo": "PLAYWRIGHT_SCRAPING"
                }

            except Exception as e:
                print(f"  ❌ Error: {e}")
                # Guardar screenshot del error para auditoría
                os.makedirs("/tmp/simit_inspeccion", exist_ok=True)
                await page.screenshot(path=f"/tmp/simit_inspeccion/simit_{documento}_ERROR.png")
                raise

            finally:
                await browser.close()

    async def _extraer_informacion(self, page: Page, documento: str) -> Dict:
        """Extrae la información de multas del DOM"""
        html_content = await page.content()

        info = {
            "documento": documento,
            "total_deuda": 0,
            "multas": [],
            "estado": "LIMPIO"
        }

        # Analizar si reporta multas o está paz y salvo
        # Si contiene textos como "Paz y salvo", "No registra multas", etc.
        if any(x in html_content for x in ["Paz y Salvo", "No tiene multas", "No registra infracciones", "No posee comparendos", "No tienes comparendos ni multas"]):
            info["estado"] = "LIMPIO"
            return info

        # Intentar extraer comparendos de tablas si existen
        try:
            tablas = await page.query_selector_all('table')
            print(f"    📊 Encontradas {len(tablas)} tablas de multas")

            for tabla in tablas:
                filas = await tabla.query_selector_all('tr')
                for fila in filas[1:]:  # Saltar cabecera
                    celdas = await fila.query_selector_all('td')
                    if len(celdas) >= 5:
                        numero = await celdas[0].inner_text()
                        fecha = await celdas[1].inner_text()
                        infraccion = await celdas[2].inner_text()
                        valor_txt = await celdas[3].inner_text()
                        estado = await celdas[4].inner_text()

                        # Parsear valor
                        try:
                            valor = float(valor_txt.replace("$", "").replace(".", "").replace(",", "").strip())
                        except:
                            valor = 0.0

                        info["multas"].append({
                            "numero_comparendo": numero.strip(),
                            "fecha": fecha.strip(),
                            "infraccion": infraccion.strip(),
                            "valor": valor,
                            "estado": estado.strip()
                        })
                        info["total_deuda"] += valor

            if info["multas"]:
                info["estado"] = "ALERTA"

        except Exception as e:
            print(f"    ⚠️ Error parseando tablas SIMIT: {e}")

        return info
