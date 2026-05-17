#!/usr/bin/env python3
"""
AYUDA PARA INSPRECCIÓN DE SITIOS WEB
Guía interactiva paso a paso

Autor: antigravity
Fecha: Mayo 17, 2026
"""

import asyncio
from playwright.async_api import async_playwright
import sys

def mostrar_menu():
    print("\n" + "="*60)
    print("🔧 AYUDA PARA INSPECCIÓN SARLAFT")
    print("="*60)
    print("\nSelecciona una opción:")
    print("1. Inspeccionar RUNT (automático)")
    print("2. Inspeccionar SIMIT (automático)")
    print("3. Probar RUNT con selector manual")
    print("4. Probar SIMIT con selector manual")
    print("5. Modo interactivo (exploración libre)")
    print("6. Ver guía de inspección")
    print("0. Salir")
    print("-" * 60)

async def inspeccionar_runt_automatico():
    """Inspecciona RUNT automáticamente"""
    print("\n🔍 INSPECCIONANDO RUNT AUTOMÁTICAMENTE...")
    print("-" * 60)

    async with async_playwright() as p:
        # Lanzar navegador en modo visible (headless=False)
        browser = await p.chromium.launch(headless=False, slow_mo=500)
        context = await browser.new_context()
        page = await context.new_page()

        try:
            print("\n📂 Navegando a RUNT...")
            await page.goto("https://www.runt.gov.co/consultaCiudadana/consultaVehiculo")
            await asyncio.sleep(3)

            print("✅ Página cargada")
            print("\n📋 ANALIZANDO ELEMENTOS...")

            # Buscar input de placa
            print("\n1️⃣ Buscando campo de placa...")
            selectores_input = [
                'input[name*="placa" i]',
                'input[id*="placa" i]',
                'input[placeholder*="placa" i]',
            ]

            input_encontrado = None
            for selector in selectores_input:
                try:
                    elementos = await page.query_selector_all(selector)
                    if elementos:
                        input_encontrado = elementos[0]
                        print(f"   ✅ Encontrado con: {selector}")
                        print(f"   📋 Total encontrados: {len(elementos)}")

                        # Mostrar atributos
                        for attr in ['name', 'id', 'class', 'placeholder', 'type']:
                            valor = await input_encontrado.get_attribute(attr)
                            if valor:
                                print(f"      {attr}: {valor}")
                        break
                except:
                    continue

            if not input_encontrado:
                print("   ❌ No se encontró campo de placa")
                print("   💡 Sugerencia: Buscar manualmente con DevTools")

            # Buscar botón
            print("\n2️⃣ Buscando botón de consulta...")
            selectores_boton = [
                'button[type="submit"]',
                'button:has-text("Consultar")',
                'button:has-text("Buscar")',
                'input[type="submit"]',
            ]

            boton_encontrado = None
            for selector in selectores_boton:
                try:
                    elementos = await page.query_selector_all(selector)
                    if elementos:
                        boton_encontrado = elementos[0]
                        print(f"   ✅ Encontrado con: {selector}")
                        print(f"   📋 Total encontrados: {len(elementos)}")

                        texto = await boton_encontrado.inner_text()
                        print(f"      Texto: '{texto.strip()}'")
                        break
                except:
                    continue

            if not boton_encontrado:
                print("   ❌ No se encontró botón")

            # Esperar intervención manual
            print("\n⏸️  PAUSANDO para inspección manual...")
            print("   → Presiona Enter cuando termines de inspeccionar manualmente")
            print("   → El navegador permanecerá abierto")

            input("\nPresiona Enter para continuar...")

        except Exception ase:
            print(f"\n❌ Error: {ase}")

        finally:
            print("\n📸 Cerrando navegador...")
            await browser.close()

async def probar_runt_manual(selector_input=None, selector_boton=None):
    """Prueba RUNT con selectores manuales"""
    print("\n🧪 PROBANDO RUNT CON SELECTORES MANUALES")

    if not selector_input:
        print("\nIngresa el selector CSS del campo de placa:")
        print("Ejemplos:")
        print("  - input[name='txtNumeroPlaca']")
        print("  - #txtNumeroPlaca")
        print("  - input[placeholder*='Placa' i]")
        selector_input = input("Selector> ").strip()

    if not selector_boton:
        print("\nIngresa el selector CSS del botón:")
        print("Ejemplos:")
        print("  - button[type='submit']")
        print("  - #btnConsultar")
        print("  - button:has-text('Consultar')")
        selector_boton = input("Selector> ").strip()

    placa_prueba = input("\nPlaca de prueba (ej: ABC123): ").strip().upper()

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        try:
            await page.goto("https://www.runt.gov.co/consultaCiudadana/consultaVehiculo")

            print(f"\n📝 Ingresando placa: {placa_prueba}")

            # Buscar input
            try:
                input_element = await page.query_selector(selector_input)
                if not input_element:
                    print(f"❌ ERROR: No se encontró input con selector: {selector_input}")
                    return

                await input_element.fill(placa_prueba)
                print(f"✅ Placa ingresada correctamente")
            except Exception as e:
                print(f"❌ ERROR ingresando placa: {e}")
                return

            await asyncio.sleep(1)

            # Buscar botón
            try:
                boton_element = await page.query_selector(selector_boton)
                if not boton_element:
                    print(f"❌ ERROR: No se encontró botón con selector: {selector_boton}")
                    return

                print(f"🖱️  Haciendo click en botón...")
                await boton_element.click()

                print("⏳ Esperando resultados...")

                # Esperar resultados
                await asyncio.sleep(5)

                # Verificar si hay tabla
                tablas = await page.query_selector_all('table')
                print(f"📊 Tablas encontradas: {len(tablas)}")

                if tablas:
                    print("\n✅ ÉXITO: Resultados encontrados")

                    # Extraer primeras filas
                    filas = await tablas[0].query_selector_all('tr')

                    print(f"\n📋 Primeras {min(3, len(filas))} filas:")
                    for i, fila in enumerate(filas[:3]):
                        celdas = await fila.query_selector_all('td, th')
                        textos = [await c.inner_text() for c in celdas]
                        texto_fila = " | ".join([t[:20] for t in textos])
                        print(f"  {i+1}. {texto_fila}")
                else:
                    print("\n⚠️  No se encontraron tablas de resultados")
                    print("   Puede ser:")
                    print("   - La placa no existe")
                    print("   - Los resultados están cargando con JavaScript")
                    print("   - Hay un CAPTCHA")
                    print("   - La estructura es diferente (divs en lugar de tabla)")

                # Screenshot
                screenshot_path = f"/tmp/runt_test_{placa_prueba}.png"
                await page.screenshot(path=screenshot_path)
                print(f"\n📸 Screenshot guardado: {screenshot_path}")

                input("\n\nPresiona Enter para ver el screenshot (o cualquier tecla para cerrar)...")

            except Exception as e:
                print(f"❌ ERROR en click: {e}")

        finally:
            await browser.close()

    except Exception as e:
        print(f"\n❌ ERROR GENERAL: {e}")

async def modo_interactivo():
    """Modo interactivo para exploración libre"""
    print("\n🔍 MODO INTERACTIVO")
    print("="*60)
    print("\nEl navegador se abrirá y podrás explorar libremente.")
    print("Presiona Ctrl+C para cerrar.")

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            slow_mo=500
        )
        context = await browser.new_context()
        page = await context.new_page()

        print("\n✅ Navegador abierto")
        print("📝 URL actual: " + page.url)

        print("\n💡 Comandos útiles (ejecutar en consola Python):")
        print("   await page.goto('https://URL')")
        print("   await page.screenshot(path='/tmp/screenshot.png')")
        print("   html = await page.content()")
        print("   await page.query_selector('table')")

        try:
            # Mantener abierto hasta Ctrl+C
            print("\n🔄 Navegador activo. Presiona Ctrl+C para cerrar...")
            print("   → Ingresa URL para navegar o presiona Enter para RUNT: ")

            url_input = input("URL (o Enter para RUNT): ").strip()

            if url_input:
                await page.goto(url_input)
            else:
                await page.goto("https://www.runt.gov.co/consultaCiudadana/consultaVehiculo")

            print(f"\n✅ Navegado a: {page.url}")

            # Esperar indefinitely
            input("\n⏸️  Presiona Enter cuando termines de explorar...")

        except KeyboardInterrupt:
            print("\n\n👋 Cerrando navegador...")
        finally:
            await browser.close()

def mostrar_guia():
    """Muestra la guía de inspección"""
    print("\n📖 ABIENDO GUÍA DE INSPECCIÓN")
    print("="*60)

    with open('/home/ubuntu/LABORATORIO/sarlaft-modern/GUIA_VISUAL_INSPECCION.md', 'r') as f:
        contenido = f.read()
        print("\n📄 Archivo: /home/ubuntu/LABORATORIO/sarlaft-modern/GUIA_VISUAL_INSPECCION.md")
        print("-" * 60)
        # Solo mostrar primeras 50 líneas
        lineas = contenido.split('\n')[:50]
        for linea in lineas:
            print(linea)

        print("\n... (continúa en el archivo)")

    print("\n💡 Para ver la guía completa:")
    print("   less /home/ubuntu/LABORATORIO/sarlaft-modern/GUIA_VISUAL_INSPECCION.md")

async def main():
    """Función principal"""
    while True:
        mostrar_menu()

        opcion = input("\nOpción: ").strip()

        if opcion == "1":
            await inspeccionar_runt_automatico()
        elif opcion == "2":
            print("\n⚠️  Opción SIMIT aún no implementada. Selecciona 1 para RUNT primero.")
        elif opcion == "3":
            await probar_runt_manual()
        elif opcion == "4":
            print("\n⚠️  Opción SIMIT aún no implementada.")
        elif opcion == "5":
            await modo_interactivo()
        elif opcion == "6":
            mostrar_guia()
        elif opcion == "0":
            print("\n👋 ¡Hasta luego!")
            break
        else:
            print("\n❌ Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 Programa interrumpido por usuario.")
