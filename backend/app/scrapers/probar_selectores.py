#!/usr/bin/env python3
"""
PROBADOR DE SELECTORES CSS - HERRAMIENTA PARA ANTIGRAVITY
Permite probar selectores CSS rápidamente sin ejecutar todo el scraper

Autor: antigravity
Fecha: Mayo 17, 2026
"""

import asyncio
from playwright.async_api import async_playwright
import sys

async def probar_selector_runt():
    """Prueba selectores en RUNT"""

    print("\n" + "="*60)
    print("🔧 PROBADOR DE SELECTORES - RUNT")
    print("="*60)

    async with async_playwright() as p:
        # Lanzar navegador visible
        browser = await p.chromium.launch(headless=False, slow_mo=500)
        context = await browser.new_context()
        page = await context.new_page()

        try:
            print("\n📂 Navegando a RUNT...")
            await page.goto("https://www.runt.gov.co/consultaCiudadana/consultaVehiculo")
            await asyncio.sleep(3)

            print("✅ Página cargada")
            print("\n" + "-"*60)

            # Probar selectores de input
            print("\n1️⃣  PROBANDO SELECTORES DE INPUT (campo placa)")
            print("-"*60)

            selectores_input = [
                'input[name="txtNumeroPlaca"]',
                'input[name="numeroPlaca"]',
                'input[name="placa"]',
                'input[id*="placa" i]',
                'input[placeholder*="placa" i]',
                'input.form-control',
                '#txtNumeroPlaca',
                '#placa'
            ]

            for selector in selectores_input:
                try:
                    elemento = await page.query_selector(selector)
                    if elemento:
                        # Obtener atributos
                        attrs = {}
                        for attr in ['name', 'id', 'class', 'placeholder', 'type']:
                            val = await elemento.get_attribute(attr)
                            if val:
                                attrs[attr] = val

                        print(f"\n✅ ENCONTRADO: {selector}")
                        print(f"   Atributos: {attrs}")

                        # Intentar escribir
                        await elemento.fill("ABC123")
                        print(f"   ✅ ESCRITURA funcionó")

                        valor = await elemento.input_value()
                        print(f"   ✅ LECTURA: '{valor}'")

                        # Limpiar para siguiente prueba
                        await elemento.fill("")
                        break
                except Exception as e:
                    print(f"\n❌ FALLÓ: {selector}")
                    print(f"   Error: {e}")

            # Probar selectores de botón
            print("\n\n2️⃣  PROBANDO SELECTORES DE BOTÓN (consultar)")
            print("-"*60)

            selectores_boton = [
                'button[type="submit"]',
                'button:has-text("Consultar")',
                'button:has-text("Buscar")',
                'input[type="submit"]',
                'button.btn-primary',
                '#btnConsultar',
                '#btnBuscar'
            ]

            for selector in selectores_boton:
                try:
                    elemento = await page.query_selector(selector)
                    if elemento:
                        texto = await elemento.inner_text()
                        tag = await elemento.evaluate('el => el.tagName')

                        print(f"\n✅ ENCONTRADO: {selector}")
                        print(f"   Tag: {tag}")
                        print(f"   Texto: '{texto.strip()}'")
                        break
                except Exception as e:
                    print(f"\n❌ FALLÓ: {selector}")
                    print(f"   Error: {e}")

            # Esperar intervención manual
            print("\n\n⏸️  MODO INSPECCIÓN MANUAL")
            print("-"*60)
            print("El navegador permanecerá abierto.")
            print("Presiona Enter cuando termines de inspeccionar manualmente...")
            input()

        except Exception as e:
            print(f"\n❌ ERROR GENERAL: {e}")

        finally:
            await browser.close()


async def probar_selector_simit():
    """Prueba selectores en SIMIT"""

    print("\n" + "="*60)
    print("🔧 PROBADOR DE SELECTORES - SIMIT")
    print("="*60)

    # Primero preguntar URL
    print("\n⚠️  SIMIT requiere navegación manual desde fiscalia.gov.co")
    print("¿Ya tienes la URL directa de SIMIT?")
    print("Si no, abre Chrome y navega a: https://www.fiscalia.gov.co/")
    print("Luego busca: Servicios → Consultas → SIMIT")

    url_simit = input("\nIngresa URL de SIMIT (o Enter para intentar URL conocida): ").strip()

    if not url_simit:
        url_simit = "https://www.simit.org.co/"

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=500)
        context = await browser.new_context()
        page = await context.new_page()

        try:
            print(f"\n📂 Navegando a: {url_simit}")
            await page.goto(url_simit, wait_until='domcontentloaded')
            await asyncio.sleep(3)

            print("✅ Página cargada")
            print("\n" + "-"*60)

            # Probar selectores de input
            print("\n1️⃣  PROBANDO SELECTORES DE INPUT")
            print("-"*60)

            selectores_input = [
                'input[placeholder*="placa" i]',
                'input[placeholder*="documento" i]',
                'input[name*="documento" i]',
                'input[name*="cedula" i]',
                'input#txtConsulta',
                'input#txtDocumento',
                'input[type="text"]'
            ]

            for selector in selectores_input:
                try:
                    elemento = await page.query_selector(selector)
                    if elemento:
                        attrs = {}
                        for attr in ['name', 'id', 'class', 'placeholder', 'type']:
                            val = await elemento.get_attribute(attr)
                            if val:
                                attrs[attr] = val

                        print(f"\n✅ ENCONTRADO: {selector}")
                        print(f"   Atributos: {attrs}")

                        # Intentar escribir
                        await elemento.fill("1022394742")
                        print(f"   ✅ ESCRITURA funcionó")

                        valor = await elemento.input_value()
                        print(f"   ✅ LECTURA: '{valor}'")

                        await elemento.fill("")
                        break
                except Exception as e:
                    print(f"\n❌ FALLÓ: {selector}")

            # Probar selectores de botón
            print("\n\n2️⃣  PROBANDO SELECTORES DE BOTÓN")
            print("-"*60)

            selectores_boton = [
                'button[type="submit"]',
                'button:has-text("Consultar")',
                'button:has-text("Buscar")',
                'button#btnConsultar',
                'span:has-text("Consultar")',
                'i.fa-search'
            ]

            for selector in selectores_boton:
                try:
                    elemento = await page.query_selector(selector)
                    if elemento:
                        texto = await elemento.inner_text()
                        tag = await elemento.evaluate('el => el.tagName')

                        print(f"\n✅ ENCONTRADO: {selector}")
                        print(f"   Tag: {tag}")
                        print(f"   Texto: '{texto.strip()}'")
                        break
                except Exception as e:
                    print(f"\n❌ FALLÓ: {selector}")

            print("\n\n⏸️  Presiona Enter cuando termines...")
            input()

        except Exception as e:
            print(f"\n❌ ERROR: {e}")

        finally:
            await browser.close()


async def probar_selector_personalizado():
    """Prueba un selector CSS personalizado en cualquier URL"""

    print("\n" + "="*60)
    print("🔧 PROBADOR DE SELECTOR PERSONALIZADO")
    print("="*60)

    url = input("\n1. Ingresa URL: ").strip()
    if not url:
        print("❌ URL requerida")
        return

    selector = input("2. Ingresa selector CSS: ").strip()
    if not selector:
        print("❌ Selector requerido")
        return

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=500)
        context = await browser.new_context()
        page = await context.new_page()

        try:
            print(f"\n📂 Navegando a: {url}")
            await page.goto(url, wait_until='domcontentloaded')
            await asyncio.sleep(3)

            print(f"\n🔍 Probando selector: {selector}")

            elementos = await page.query_selector_all(selector)

            if elementos:
                print(f"\n✅ ENCONTRADOS: {len(elementos)} elementos")

                for i, elem in enumerate(elementos[:3]):  # Primeros 3
                    print(f"\n   Elemento {i+1}:")

                    # Atributos
                    for attr in ['name', 'id', 'class', 'type', 'href']:
                        val = await elem.get_attribute(attr)
                        if val:
                            print(f"      {attr}: {val}")

                    # Texto
                    try:
                        tag = await elem.evaluate('el => el.tagName')
                        texto = await elem.inner_text()
                        print(f"      tag: {tag}")
                        print(f"      texto: '{texto[:50]}'")
                    except:
                        pass
            else:
                print(f"\n❌ NO ENCONTRADO: {selector}")

            print("\n⏸️  Presiona Enter para cerrar...")
            input()

        except Exception as e:
            print(f"\n❌ ERROR: {e}")

        finally:
            await browser.close()


def mostrar_menu():
    """Muestra menú principal"""
    print("\n" + "="*60)
    print("🔧 PROBADOR DE SELECTORES CSS")
    print("="*60)
    print("\nSelecciona una opción:")
    print("1. Probar selectores RUNT")
    print("2. Probar selectores SIMIT")
    print("3. Probar selector personalizado")
    print("0. Salir")
    print("-"*60)


async def main():
    """Función principal"""

    while True:
        mostrar_menu()
        opcion = input("\nOpción: ").strip()

        if opcion == "1":
            await probar_selector_runt()
        elif opcion == "2":
            await probar_selector_simit()
        elif opcion == "3":
            await probar_selector_personalizado()
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
