#!/usr/bin/env python3
"""
OBSERVADOR EN VIVO - HERRAMIENTA PARA VER QUÉ PASA EN RUNT/SIMIT
Permite abrir el navegador y OBSERVAR qué sucede realmente

Autor: antigravity
Fecha: Mayo 17, 2026
"""

import asyncio
from playwright.async_api import async_playwright
import sys


async def observar_runt_en_vivo():
    """Abre RUNT y espera a que observes qué pasa"""

    print("\n" + "="*60)
    print("🔍 OBSERVANDO RUNT EN VIVO")
    print("="*60)

    async with async_playwright() as p:
        # Lanzar navegador visible
        browser = await p.chromium.launch(
            headless=False,  # NAVEGADOR VISIBLE
            slow_mo=1000     # Clicks lentos para ver qué pasa
        )
        context = await browser.new_context()
        page = await context.new_page()

        try:
            print("\n📂 Abriendo RUNT...")
            await page.goto("https://www.runt.gov.co/consultaCiudadana/consultaVehiculo")
            await asyncio.sleep(3)

            print("\n✅ Página cargada")
            print("\n" + "-"*60)
            print("🔍 INSTRUCCIONES PARA TI:")
            print("-"*60)
            print("1. La ventana de Chrome está ABIERTA")
            print("2. Presiona F12 para abrir DevTools")
            print("3. Ve a la pestaña 'Network'")
            print("4. Voy a ingresar una placa automáticamente...")
            print("\nPresiona Enter cuando estés listo...")
            input()

            # Ingresar placa
            print("\n📝 Ingresando placa: ABC123")

            selectores_placa = [
                'input#mat-input-2',
                'input[name="numeroPlaca"]',
                'input[placeholder*="placa"]',
                'input[id*="placa"]'
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
                print("  ❌ No encontré input. Ayúdame a encontrarlo manualmente.")
                print("\n→ Presiona Enter cuando hayas ingresado la placa manualmente...")
                input()
            else:
                await input_placa.fill("ABC123")
                await asyncio.sleep(1)
                print("  ✅ Placa ingresada")

            print("\n🖱️  Voy a hacer click en 'Consultar Información'...")
            print("OBSERVA la pestaña Network de DevTools...")
            print("\nPresiona Enter cuando estés listo...")
            input()

            # Buscar botón
            selectores_boton = [
                'button:has-text("Consultar Información")',
                'button[type="submit"]',
                'button:has-text("Consultar")'
            ]

            boton_consultar = None
            for sel in selectores_boton:
                try:
                    boton_consultar = await page.query_selector(sel)
                    if boton_consultar:
                        print(f"\n  ✅ Encontrado botón: {sel}")
                        break
                except:
                    continue

            if not boton_consultar:
                print("  ❌ No encontré botón. Ayúdame a encontrarlo manualmente.")
                print("\n→ Presiona Enter cuando hayas hecho click manualmente...")
                input()
            else:
                print("\n  → Haciendo click...")
                await boton_consultar.click()

            print("\n⏳ Esperando resultados...")
            print("👀 OBSERVA:")
            print("   - ¿Aparece un spinner de carga?")
            print("   - ¿Cuánto tiempo tarda?")
            print("   - ¿Aparece una tabla con datos?")
            print("   - ¿En DevTools → Network aparecen peticiones XHR?")

            # Esperar largo tiempo para observar
            print("\n   Esperando 15 segundos para que veas todo...")
            await asyncio.sleep(15)

            # Capturar screenshot
            screenshot_path = "/tmp/runt_observacion_en_vivo.png"
            await page.screenshot(path=screenshot_path, full_page=True)
            print(f"\n📸 Screenshot guardado: {screenshot_path}")

            # Intentar inspeccionar
            print("\n🔍 Intentando encontrar datos en el HTML...")

            # Buscar cualquier tabla
            tablas = await page.query_selector_all('table')
            print(f"   Tablas encontradas: {len(tablas)}")

            # Buscar elementos comunes de Angular
            angular_cells = await page.query_selector_all('mat-cell')
            print(f"   Celdas Angular (mat-cell): {len(angular_cells)}")

            # Buscar cualquier elemento con texto de marca/modelo
            elementos_marca = await page.query_selector_all(':has-text("MAZDA")')
            print(f"   Elementos con 'MAZDA': {len(elementos_marca)}")

            # Obtener HTML actual
            html = await page.content()
            tiene_datos_vehiculo = 'MAZDA' in html or 'modelo' in html or 'marca' in html
            print(f"   HTML tiene datos de vehículo: {tiene_datos_vehiculo}")

            print("\n" + "-"*60)
            print("🔍 AHORA ES TU TURNO DE INVESTIGAR:")
            print("-"*60)
            print("1. En la ventana de Chrome, presiona F12")
            print("2. Ve a la pestaña 'Elements' o 'Inspector'")
            print("3. Busca datos del vehículo (si los ves)")
            print("4. Click derecho en un dato → Inspeccionar")
            print("5. Anota el selector del elemento")
            print("\nPresiona Enter cuando hayas terminado de investigar...")
            input()

            print("\n✅ Observación completada")

        except Exception as e:
            print(f"\n❌ Error: {e}")

        finally:
            print("\n⏸️  Presiona Enter para cerrar el navegador...")
            input()
            await browser.close()


async def observar_simit_en_vivo():
    """Abre SIMIT y espera a que observes qué pasa"""

    print("\n" + "="*60)
    print("🔍 OBSERVANDO SIMIT EN VIVO")
    print("="*60)

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            slow_mo=1000
        )
        context = await browser.new_context()
        page = await context.new_page()

        try:
            print("\n📂 Abriendo SIMIT...")
            await page.goto("https://www.fcm.org.co/simit/")
            await asyncio.sleep(4)

            print("\n✅ Página cargada")
            print("\n" + "-"*60)
            print("🔍 INSTRUCCIONES:")
            print("-"*60)
            print("1. La ventana de Chrome está ABIERTA")
            print("2. Presiona F12 para abrir DevTools")
            print("3. Ve a la pestaña 'Network'")
            print("4. Voy a ingresar un documento automáticamente...")
            print("\nPresiona Enter cuando estés listo...")
            input()

            # Ingresar documento
            print("\n📝 Ingresando documento: 1022394742")

            selectores_input = [
                'input#txtBusqueda',
                'input[placeholder*="documento"]',
                'input[type="text"]'
            ]

            input_doc = None
            for sel in selectores_input:
                try:
                    input_doc = await page.query_selector(sel)
                    if input_doc:
                        print(f"  ✅ Encontrado input: {sel}")
                        break
                except:
                    continue

            if not input_doc:
                print("  ❌ No encontré input. Ayúdame a encontrarlo manualmente.")
                print("\n→ Presiona Enter cuando hayas ingresado el documento manualmente...")
                input()
            else:
                await input_doc.fill("1022394742")
                await asyncio.sleep(1)
                print("  ✅ Documento ingresado")

            print("\n🖱️  Voy a hacer click en 'Consultar'...")
            print("OBSERVA la pestaña Network de DevTools...")
            print("\nPresiona Enter cuando estés listo...")
            input()

            # Buscar botón
            selectores_boton = [
                'button#consultar',
                'button[type="submit"]',
                'button:has-text("Consultar")'
            ]

            boton_consultar = None
            for sel in selectores_boton:
                try:
                    boton_consultar = await page.query_selector(sel)
                    if boton_consultar:
                        print(f"\n  ✅ Encontrado botón: {sel}")
                        break
                except:
                    continue

            if not boton_consultar:
                print("  ❌ No encontré botón. Ayúdame a encontrarlo manualmente.")
                print("\n→ Presiona Enter cuando hayas hecho click manualmente...")
                input()
            else:
                # Cerrar modal si aparece
                print("\n  → Cerrando modal informativo (si existe)...")
                try:
                    modal_close = await page.query_selector('button.close.modal-info-close')
                    if modal_close:
                        await modal_close.click()
                        await asyncio.sleep(1)
                except:
                    pass

                print("\n  → Haciendo click en consultar...")
                await boton_consultar.click()

            print("\n⏳ Esperando resultados...")
            print("👀 OBSERVA:")
            print("   - ¿Aparece 'Paz y Salvo'?")
            print("   - ¿Aparece una tabla de multas?")
            print("   - ¿En DevTools → Network aparecen peticiones XHR?")

            print("\n   Esperando 15 segundos para que veas todo...")
            await asyncio.sleep(15)

            # Capturar screenshot
            screenshot_path = "/tmp/simit_observacion_en_vivo.png"
            await page.screenshot(path=screenshot_path, full_page=True)
            print(f"\n📸 Screenshot guardado: {screenshot_path}")

            # Intentar inspeccionar
            print("\n🔍 Intentando encontrar datos en el HTML...")

            tablas = await page.query_selector_all('table')
            print(f"   Tablas encontradas: {len(tablas)}")

            # Buscar "Paz y Salvo"
            elementos_paz = await page.query_selector_all(':has-text("Paz y Salvo")')
            print(f"   Elementos con 'Paz y Salvo': {len(elementos_paz)}")

            html = await page.content()
            tiene_multas = 'comparendo' in html.lower() or 'multa' in html.lower()
            print(f"   HTML menciona multas/comparendos: {tiene_multas}")

            print("\n" + "-"*60)
            print("🔍 AHORA ES TU TURNO DE INVESTIGAR:")
            print("-"*60)
            print("1. En la ventana de Chrome, presiona F12")
            print("2. Ve a la pestaña 'Elements'")
            print("3. Busca la tabla de resultados (si existe)")
            print("4. Click derecho → Inspeccionar")
            print("5. Anota los selectores")
            print("\nPresiona Enter cuando hayas terminado de investigar...")
            input()

            print("\n✅ Observación completada")

        except Exception as e:
            print(f"\n❌ Error: {e}")

        finally:
            print("\n⏸️  Presiona Enter para cerrar el navegador...")
            input()
            await browser.close()


async def investigar_ajax_runt():
    """Investiga peticiones AJAX de RUNT"""

    print("\n" + "="*60)
    print("🔍 INVESTIGANDO PETICIONES AJAX - RUNT")
    print("="*60)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        # Capturar peticiones
        peticiones = []

        def log_request(request):
            print(f"📤 Request: {request.method} {request.url}")

        def log_response(response):
            if '/api/' in response.url or response.request.resource_type in ['xhr', 'fetch']:
                print(f"📥 Response: {response.status} {response.url}")
                peticiones.append({
                    'url': response.url,
                    'status': response.status,
                    'type': response.request.resource_type
                })

        page.on('request', log_request)
        page.on('response', log_response)

        try:
            print("\n📂 Abriendo RUNT con captura de peticiones...")
            await page.goto("https://www.runt.gov.co/consultaCiudadana/consultaVehiculo")

            print("\n📝 Ingresa una placa y haz click en consultar")
            print("OBSERVA las peticiones que aparecen aquí...")
            print("\nPresiona Enter cuando estés listo...")
            input()

            # Ingresar placa
            input_placa = await page.query_selector('input#mat-input-2')
            if input_placa:
                await input_placa.fill("ABC123")
                await asyncio.sleep(1)

            # Click en consultar
            boton = await page.query_selector('button:has-text("Consultar Información")')
            if boton:
                await boton.click()

            print("\n⏳ Esperando peticiones (10 segundos)...")
            await asyncio.sleep(10)

            print("\n📊 PETICIONES CAPTURADAS:")
            print("-"*60)
            for peticion in peticiones:
                print(f"{peticion['type']}: {peticion['url']}")
                print(f"  Status: {peticion['status']}")

            if not peticiones:
                print("\n⚠️  No se capturaron peticiones XHR/Fetch")
                print("   Esto puede significar:")
                print("   - Los datos se renderizan en el cliente")
                print("   - Las peticiones no tienen /api/ en la URL")

            print("\nPresiona Enter para cerrar...")
            input()

        finally:
            await browser.close()


def mostrar_menu():
    """Muestra menú principal"""
    print("\n" + "="*60)
    print("🔍 OBSERVADOR EN VIVO - RUNT/SIMIT")
    print("="*60)
    print("\nSelecciona una opción:")
    print("1. Observar RUNT en vivo (recomendado)")
    print("2. Observar SIMIT en vivo (recomendado)")
    print("3. Investigar peticiones AJAX de RUNT")
    print("4. Modo libre (explora tú mismo)")
    print("0. Salir")
    print("-"*60)


async def modo_libre():
    """Modo libre de exploración"""
    print("\n" + "="*60)
    print("🔍 MODO LIBRE - EXPLORACIÓN")
    print("="*60)

    url = input("\n1. Ingresa URL (o Enter para RUNT): ").strip()
    if not url:
        url = "https://www.runt.gov.co/consultaCiudadana/consultaVehiculo"

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=500)
        context = await browser.new_context()
        page = await context.new_page()

        try:
            print(f"\n📂 Abriendo: {url}")
            await page.goto(url)

            print("\n✅ Navegador abierto")
            print("🔍 Tú tienes el control:")
            print("   - Presiona F12 para DevTools")
            print("   - Explora la página tú mismo")
            print("   - Usa la consola de JavaScript para probar")
            print("   - Observa Network, Elements, etc.")

            print("\n⏸️  Presiona Enter cuando termines...")
            input()

        finally:
            await browser.close()


async def main():
    """Función principal"""

    while True:
        mostrar_menu()
        opcion = input("\nOpción: ").strip()

        if opcion == "1":
            await observar_runt_en_vivo()
        elif opcion == "2":
            await observar_simit_en_vivo()
        elif opcion == "3":
            await investigar_ajax_runt()
        elif opcion == "4":
            await modo_libre()
        elif opcion == "0":
            print("\n👋 ¡Hasta luego!")
            break
        else:
            print("\n❌ Opción no válida")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 Programa interrumpido.")
