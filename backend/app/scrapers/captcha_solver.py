#!/usr/bin/env python3
"""
CAPTCHA SOLVER - Integración con 2Captcha
Lista para usar en RUNT scraper

Autor: antigravity
Fecha: Mayo 17, 2026
"""

import requests
import asyncio
import time
from typing import Optional

class CaptchaSolver:
    """Resuelve CAPTCHAs usando 2Captcha"""

    def __init__(self, api_key: str):
        """
        Inicializa solver con API key de 2Captcha

        Obtener API key en: https://2captcha.com/settings
        """
        self.api_key = api_key
        self.base_url = "http://2captcha.com"

    async def resolver_recaptcha_v2(
        self,
        page_url: str,
        site_key: str,
        timeout: int = 120
    ) -> Optional[str]:
        """
        Resuelve reCAPTCHA v2 usando 2Captcha

        Args:
            page_url: URL completa de la página
            site_key: Site key de reCAPTCHA (data-sitekey)
            timeout: Tiempo máximo espera en segundos

        Returns:
            Token g-response o None si falla
        """

        print(f"  📤 Enviando CAPTCHA a 2Captcha...")
        print(f"     Site Key: {site_key}")

        # Paso 1: Enviar CAPTCHA para resolver
        payload = {
            'key': self.api_key,
            'method': 'userrecaptcha',
            'googlekey': site_key,
            'pageurl': page_url,
            'json': 1
        }

        try:
            response = requests.post(f'{self.base_url}/in.php', data=payload)
            result = response.json()

            if result['status'] != 1:
                print(f"  ❌ Error enviando CAPTCHA: {result.get('request')}")
                return None

            task_id = result['request']
            print(f"  ✅ CAPTCHA enviado, ID: {task_id}")

        except Exception as e:
            print(f"  ❌ Exception enviando CAPTCHA: {e}")
            return None

        # Paso 2: Esperar resolución (polling)
        print(f"  ⏳ Esperando resolución (máx {timeout} seg)...")

        start_time = time.time()
        poll_interval = 15  # consultar cada 15 seg

        while time.time() - start_time < timeout:
            await asyncio.sleep(poll_interval)

            try:
                result_response = requests.get(
                    f'{self.base_url}/res.php',
                    params={
                        'key': self.api_key,
                        'action': 'get',
                        'id': task_id,
                        'json': 1
                    }
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

        print(f"  ❌ Timeout de {timeout} seg excedido")
        return None

    async def inyectar_token_pagina(self, page, token: str):
        """
        Inyecta el token resuelto en la página

        Args:
            page: Página de Playwright
            token: Token g-response resuelto
        """

        print(f"  💉 Inyectando token en página...")

        try:
            await page.evaluate(f'''
                () => {{
                    // Encontrar textarea oculto de reCAPTCHA
                    const response_textarea = document.getElementById('g-recaptcha-response');
                    if (response_textarea) {{
                        response_textarea.innerHTML = '{token}';
                    }}

                    // Sobrescribir funcióngetResponse
                    if (typeof grecaptcha !== 'undefined') {{
                        const originalGetResponse = grecaptcha.getResponse;
                        grecaptcha.getResponse = function() {{
                            return '{token}';
                        }};
                    }}

                    // Disparar evento callback si existe
                    if (typeof grecaptcha !== 'undefined' && grecaptcha.render) {{
                        grecaptcha.getResponse = function() {{ return '{token}'; }};
                    }}
                }}
            ''')

            print(f"  ✅ Token inyectado correctamente")
            return True

        except Exception as e:
            print(f"  ❌ Error inyectando token: {e}")
            return False


# Función auxiliar para extraer site key de una página
async def extraer_site_key(page) -> Optional[str]:
    """
    Extrae el site key de reCAPTCHA de una página

    Returns:
        Site key o None si no encuentra
    """

    try:
        site_key = await page.evaluate('''
            () => {
                // Buscar en iframes de reCAPTCHA
                const iframes = document.querySelectorAll('iframe');
                for (let iframe of iframes) {
                    const src = iframe.getAttribute('src');
                    if (src && src.includes('recaptcha')) {
                        // Intentar obtener de data-sitekey
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
                }

                return null;
            }
        ''')

        return site_key

    except Exception as e:
        print(f"  ❌ Error extrayendo site key: {e}")
        return None


# Test rápido
async def main():
    """Función de prueba"""

    print("\n" + "="*60)
    print("🔧 CAPTCHA SOLVER - TEST")
    print("="*60)

    # Paso 1: Obtener API key
    api_key = input("\nIngresa tu API key de 2Captcha: ").strip()

    if not api_key:
        print("❌ API key requerida")
        print("Obtén una en: https://2captcha.com/settings")
        return

    solver = CaptchaSolver(api_key)

    # Paso 2: Test de extracción de site key
    print("\n📂 Test de extracción de site key...")
    print("   1. Abre https://www.google.com/recaptcha/api2/demo en tu navegador")
    print("   2. Extraeremos el site key automáticamente")
    print("   3. Resolveremos el CAPTCHA")

    from playwright.async_api import async_playwright

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        try:
            await page.goto('https://www.google.com/recaptcha/api2/demo')
            await asyncio.sleep(3)

            site_key = await extraer_site_key(page)

            if not site_key:
                print("❌ No se pudo extraer site key")
                return

            print(f"✅ Site Key extraído: {site_key}")

            # Resolver CAPTCHA
            token = await solver.resolver_recaptcha_v2(
                page_url='https://www.google.com/recaptcha/api2/demo',
                site_key=site_key,
                timeout=120
            )

            if token:
                print(f"✅ Test exitoso! Token: {token[:50]}...")
            else:
                print("❌ No se pudo resolver CAPTCHA")

        finally:
            await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
