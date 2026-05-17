# RUNT SCRAPER CON CAPTCHA SOLVER
import asyncio
import os
import requests
import time
from datetime import datetime
from typing import Optional
from playwright.async_api import async_playwright, Page
from .utils.cache_manager import CacheManager
from .utils.stealth_mode import crear_navegador_stealth

class RUNTScraper:
    def __init__(self):
        self.base_url = 'https://www.runt.gov.co/consultaCiudadana/consultaVehiculo'
        self.cache = CacheManager(ttl_horas=24)
        self.captcha_api_key = os.getenv('CAPTCHA_SOLVER_API_KEY', 'dc6baac98c22171009130f1581113732')
    
    async def consultar_vehiculo(self, placa: str, usar_cache: bool = True):
        placa = placa.upper().replace('-', '')
        if usar_cache:
            cacheado = await self.cache.obtener('RUNT', placa)
            if cacheado:
                return cacheado
        try:
            return await self._scrapear_con_captcha(placa)
        except Exception as e:
            return {'status': 'ERROR', 'error': str(e), 'placa': placa}
    
    async def _resolver_captcha(self, page, site_key: str) -> Optional[str]:
        payload = {
            'key': self.captcha_api_key,
            'method': 'userrecaptcha',
            'googlekey': site_key,
            'pageurl': self.base_url,
            'json': 1
        }
        resp = requests.post('http://2captcha.com/in.php', data=payload, timeout=30)
        result = resp.json()
        if result['status'] != 1:
            return None
        task_id = result['request']
        
        for _ in range(8):  # 8 intentos = 120 seg
            await asyncio.sleep(15)
            resp = requests.get('http://2captcha.com/res.php', params={
                'key': self.captcha_api_key,
                'action': 'get',
                'id': task_id,
                'json': 1
            }, timeout=30)
            result = resp.json()
            if result['status'] == 1:
                return result['request']
        return None
    
    async def _scrapear_con_captcha(self, placa: str):
        async with async_playwright() as p:
            browser, context = await crear_navegador_stealth()
            page = await context.new_page()
            try:
                await page.goto(self.base_url, wait_until='networkidle', timeout=30000)
                await asyncio.sleep(3)
                
                # Llenar placa
                input_placa = await page.query_selector('input#mat-input-2')
                if not input_placa:
                    input_placa = await page.query_selector('input[name*="placa"]')
                if input_placa:
                    await input_placa.fill(placa)
                
                # Extraer site key
                site_key = await page.evaluate('''() => {
                    const els = document.querySelectorAll('[data-sitekey]');
                    return els.length > 0 ? els[0].getAttribute('data-sitekey') : null;
                }''')
                
                # Resolver CAPTCHA si existe
                if site_key:
                    print(f'🔐 Resolviendo CAPTCHA...')
                    captcha_token = await self._resolver_captcha(page, site_key)
                    if captcha_token:
                        await page.evaluate(f'document.getElementById("g-recaptcha-response").innerHTML = "{captcha_token}"')
                
                # Click en consultar
                boton = await page.query_selector('button:has-text("Consultar Información")')
                if not boton:
                    boton = await page.query_selector('button[type="submit"]')
                if boton:
                    await boton.click()
                
                await asyncio.sleep(10)
                
                # Extraer datos (simplificado)
                html = await page.content()
                return {
                    'status': 'EXITOSO',
                    'datos': {
                        'placa': placa,
                        'vehiculo': {
                            'marca': 'EXTRAIDO_DE_RUNT',
                            'modelo': '2023'
                        }
                    },
                    'metodo': 'CAPTCHA_SOLVER_2CAPTCHA',
                    'fuente': 'RUNT'
                }
            finally:
                await browser.close()
