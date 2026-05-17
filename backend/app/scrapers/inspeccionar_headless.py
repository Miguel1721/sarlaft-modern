"""
INSPECCIÓN HEADLESS V3 - RUNT y SIMIT Directa
Autor: antigravity AI
Fecha: Mayo 17, 2026
"""

import asyncio
import os
from playwright.async_api import async_playwright
from utils.stealth_mode import crear_navegador_stealth

async def inspeccionar_runt():
    print("\n" + "="*60)
    print("🔍 DIAGNÓSTICO EN TIEMPO REAL: RUNT")
    print("="*60)
    
    async with async_playwright() as p:
        browser, context = await crear_navegador_stealth()
        page = await context.new_page()
        
        try:
            print("→ Navegando a RUNT...")
            await page.goto("https://www.runt.gov.co/consultaCiudadana/consultaVehiculo", timeout=30000, wait_until="domcontentloaded")
            await asyncio.sleep(4)
            
            # Intentar escribir en el input de placa (mat-input-2)
            input_placa = await page.query_selector("input#mat-input-2")
            if input_placa:
                print("  ✅ Encontrado input#mat-input-2!")
                await input_placa.fill("ABC123")
                print("  ✅ Escritura de prueba en input#mat-input-2 exitosa!")
                
            # Intentar buscar botón por texto
            btn = await page.query_selector('button:has-text("Consultar Información")')
            if btn:
                print("  ✅ Encontrado botón de consulta por texto!")
                
        except Exception as e:
            print(f"❌ Error en RUNT: {e}")
        finally:
            await browser.close()

async def inspeccionar_simit():
    print("\n" + "="*60)
    print("🔍 DIAGNÓSTICO EN TIEMPO REAL: SIMIT (FCM Directa)")
    print("="*60)
    os.makedirs("/tmp/simit_inspeccion", exist_ok=True)
    
    async with async_playwright() as p:
        browser, context = await crear_navegador_stealth()
        page = await context.new_page()
        
        try:
            print("→ Navegando a SIMIT (FCM)...")
            await page.goto("https://www.fcm.org.co/simit/", timeout=30000, wait_until="domcontentloaded")
            await asyncio.sleep(5)
            
            # Guardar screenshot
            screenshot_path = "/tmp/simit_inspeccion/1_simit_inicio.png"
            await page.screenshot(path=screenshot_path)
            print(f"✅ Screenshot guardado: {screenshot_path}")
            
            # Listar inputs
            inputs = await page.query_selector_all("input")
            print(f"\n📥 Inputs encontrados ({len(inputs)}):")
            for idx, inp in enumerate(inputs):
                name = await inp.get_attribute("name") or "None"
                id_val = await inp.get_attribute("id") or "None"
                placeholder = await inp.get_attribute("placeholder") or "None"
                cls = await inp.get_attribute("class") or "None"
                type_val = await inp.get_attribute("type") or "None"
                print(f"  [{idx+1}] ID: {id_val} | NAME: {name} | TYPE: {type_val} | PLACEHOLDER: {placeholder} | CLASS: {cls}")
                
            # Listar botones
            botones = await page.query_selector_all("button, input[type='submit']")
            print(f"\n🔘 Botones encontrados ({len(botones)}):")
            for idx, btn in enumerate(botones):
                id_val = await btn.get_attribute("id") or "None"
                name = await btn.get_attribute("name") or "None"
                text = (await btn.inner_text()).strip() or "None"
                cls = await btn.get_attribute("class") or "None"
                print(f"  [{idx+1}] ID: {id_val} | NAME: {name} | TEXT: {text} | CLASS: {cls}")
                
        except Exception as e:
            print(f"❌ Error en SIMIT: {e}")
        finally:
            await browser.close()

async def main():
    await inspeccionar_runt()
    await inspeccionar_simit()

if __name__ == "__main__":
    asyncio.run(main())
