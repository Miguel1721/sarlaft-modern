# 🔧 SOLUCIONES PARA RESOLVER CAPTCHA - RUNT & SIMIT

**Fecha:** Mayo 17, 2026
**Objetivo:** Resolver CAPTCHA de RUNT para tener datos 100% reales

---

## 🎯 TIPOS DE CAPTCHA Y SOLUCIONES

### 1. Servicios Comerciales de Resolución (Más confiables)

#### A) 2Captcha
- **Costo:** $0.50 - $3.00 por 1000 CAPTCHAs
- **Tipos soportados:** reCAPTCHA v2/v3, hCaptcha, imagen, texto
- **API:** REST API
- **Tiempo respuesta:** 15-30 segundos
- **Precisión:** 95-99%

**Integración con Python:**
```python
import requests

# Enviar CAPTCHA para resolver
payload = {
    'key': 'TU_API_KEY',
    'method': 'userrecaptcha',  # para reCAPTCHA v2
    'googlekey': 'SITE_KEY_DE_RUNT',  # necesario obtener
    'pageurl': 'https://www.runt.gov.co/consultaCiudadana/consultaVehiculo',
    'json': 1
}

response = requests.post('http://2captcha.com/in.php', data=payload)
task_id = response.json()['request']

# Esperar resolución (polling)
import time
time.sleep(20)  # esperar ~20 seg

result = requests.get(f'http://2captcha.com/res.php?key=TU_API_KEY&action=get&id={task_id}&json=1')
captcha_solution = result.json()['request']
```

**Costo mensual estimado:**
- 100 consultas/día = $15/mes
- 1000 consultas/día = $150/mes

---

#### B) Anti-Captcha.com
- **Costo:** $1.00 - $5.00 por 1000 CAPTCHAs
- **Tipos soportados:** reCAPTCHA v2/v3, hCaptcha, FunCaptcha, imagen
- **API:** REST + SDKs
- **Tiempo respuesta:** 10-25 segundos
- **Precisión:** 95-99%

**Librería Python:**
```bash
pip install python-anticaptcha
```

```python
from anticaptchaofficial.recaptchav2proxyless import recaptchaV2Proxyless

solver = recaptchaV2Proxyless()
solver.set_key('TU_API_KEY')
solver.set_website_url('https://www.runt.gov.co/consultaCiudadana/consultaVehiculo')
solver.set_website_key('SITE_KEY_DE_RUNT')

# Resolver
g_response = solver.solve_and_return_solution()
print(f"Token g-response: {g_response}")
```

---

#### C) DeathByCaptcha
- **Costo:** $1.99 - $5.99 por 1000 CAPTCHAs
- **Tipos soportados:** reCAPTCHA, imágenes
- **API:** REST
- **Tiempo respuesta:** 15-30 segundos

---

### 2. Soluciones Open Source (Gratis pero menos confiables)

#### A) Playwright con Extra-Stealth

**Librería:** `playwright-stealth`

```bash
pip install playwright-stealth
```

```python
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async

async with async_playwright() as p:
    browser = await p.chromium.launch(headless=False)
    context = await browser.new_context()
    page = await context.new_page()

    # Aplicar stealth (ya lo tenemos en el código)
    await stealth_async(page)

    # Navegar y llenar formulario
    await page.goto('https://www.runt.gov.co/...')

    # El CAPTCHA puede no aparecer si el navegador es "humano"
```

**Eficacia:** 20-40% (no confiable)

---

#### B) Playwright + 2Captcha Plugin (Automático)

```bash
pip install playwright-recaptcha-solver
```

```python
from playwright_recaptcha import recaptchav2

async with async_playwright() as p:
    browser = await p.chromium.launch(headless=False)
    context = await browser.new_context()
    page = await context.new_page()

    # El plugin detecta y resuelve automáticamente
    async with recaptchav2.SyncRecaptchaV2(page, api_key='TU_2CAPTCHA_KEY') as solver:
        await page.goto('https://www.runt.gov.co/...')
        await solver.solve_recaptcha()
        # El CAPTCHA se resuelve automáticamente
```

---

#### C) Playwright + Puppeteer-Extra Approach

**Librerías disponibles:**
- `playwright-extra`
- `playwright-extra-plugin-recaptcha`

```bash
pip install playwright-extra
pip install playwright-extra-plugin-recaptcha
```

```python
from playwright.sync_api import sync_playwright
from playwright_extra import PlaywrightExtra
from playwright_extra.plugins.recaptcha import RecaptchaPlugin

with sync_playwright() as p:
    extra = PlaywrightExtra(p.chromium)
    extra.add(RecaptchaPlugin(api_key='TU_API_KEY'))

    browser = extra.launch(headless=False)
    page = browser.new_page()

    # El plugin detecta y resuelve reCAPTCHA automáticamente
    page.goto('https://www.runt.gov.co/...')
```

---

### 3. Machine Learning (Experimental)

#### A) Python + TensorFlow para reCAPTCHA

**Librería:** `captcha-solver`

```bash
pip install captcha-solver
```

**Eficacia:** 60-80% (experimental, requiere entrenamiento)

---

#### B) OCR para CAPTCHA de imagen

```python
import pytesseract
from PIL import Image

# Para CAPTCHAs de imagen simples
image = Image.open('/tmp/captcha_image.png')
text = pytesseract.image_to_string(image)
```

**Eficacia:** 30-50% (solo para CAPTCHAs simples)

---

## 🔍 PASO 1: IDENTIFICAR EL TIPO DE CAPTCHA DE RUNT

Antes de elegir solución, necesitamos saber qué CAPTCHA usa:

### Instrucciones para antigravity:

```bash
# 1. Abrir RUNT manualmente
google-chrome https://www.runt.gov.co/consultaCiudadana/consultaVehiculo &

# 2. Llenar formulario y ver qué CAPTCHA aparece

# 3. Presiona F12 → Elements → Buscar:
#    - "data-sitekey" (indica reCAPTCHA v2)
#    - "iframe" con "recaptcha" (reCAPTCHA)
#    - "iframe" con "hcaptcha" (hCaptcha)
#    - "captcha" (imagen simple)

# 4. Documentar:
#    - Tipo de CAPTCHA: ___________
#    - Site Key (si es reCAPTCHA): ___________
```

**Si es reCAPTCHA v2:**
- Usar 2Captcha o Anti-Captcha
- Site Key es necesario

**Si es reCAPTCHA v3:**
- Más difícil de resolver
- Requiere enfoque diferente

**Si es imagen simple:**
- Se puede resolver con OCR

---

## 🔧 PASO 2: IMPLEMENTAR SOLUCIÓN ELEGIDA

### Opción Recomendada: 2Captcha (Balance costo/confiabilidad)

#### Instalación:
```bash
pip install requests
```

#### Código para RUNT scraper:

```python
# En runt_scraper.py

import requests
import time

class RUNTScraper:
    def __init__(self):
        self.api_key = 'TU_2CAPTCHA_KEY'  # Obtener en 2captcha.com
        self.base_url = "https://www.runt.gov.co/consultaCiudadana/consultaVehiculo"

    async def _resolver_captcha(self, page):
        """Resuelve CAPTCHA usando 2Captcha"""

        # 1. Obtener site key de la página
        site_key = await page.evaluate('''
            () => {
                const iframe = document.querySelector('iframe[src*="recaptcha"]');
                if (iframe) {
                    return iframe.getAttribute('data-sitekey') ||
                           document.querySelector('[data-sitekey]')?.getAttribute('data-sitekey');
                }
                return null;
            }
        ''')

        if not site_key:
            print("  ❌ No se encontró site key de reCAPTCHA")
            return None

        print(f"  ✅ Site Key encontrado: {site_key}")

        # 2. Enviar a 2Captcha
        payload = {
            'key': self.api_key,
            'method': 'userrecaptcha',
            'googlekey': site_key,
            'pageurl': self.base_url,
            'json': 1
        }

        response = requests.post('http://2captcha.com/in.php', data=payload)
        result = response.json()

        if result['status'] != 1:
            print(f"  ❌ Error enviando CAPTCHA: {result}")
            return None

        task_id = result['request']
        print(f"  📤 CAPTCHA enviado, ID: {task_id}")

        # 3. Esperar resolución (polling)
        max_wait = 120  # 2 minutos máximo
        start_time = time.time()

        while time.time() - start_time < max_wait:
            await asyncio.sleep(15)  # consultar cada 15 seg

            result_response = requests.get(
                f'http://2captcha.com/res.php?key={self.api_key}&action=get&id={task_id}&json=1'
            )
            result = result_response.json()

            if result['status'] == 1:
                captcha_token = result['request']
                print(f"  ✅ CAPTCHA resuelto: {captcha_token[:20]}...")
                return captcha_token

            print(f"  ⏳ Esperando resolución... {result['request']}")

        print("  ❌ Timeout esperando resolución de CAPTCHA")
        return None

    async def _scrapear_runt(self, placa: str):
        """Ejecuta scraping con resolución de CAPTCHA"""

        async with async_playwright() as p:
            browser, context = await crear_navegador_stealth()
            page = await context.new_page()

            try:
                await page.goto(self.base_url, wait_until='networkidle')
                await asyncio.sleep(3)

                # Llenar placa
                input_placa = await page.query_selector('input#mat-input-2')
                await input_placa.fill(placa)

                # **RESOLVER CAPTCHA**
                captcha_token = await self._resolver_captcha(page)

                if captcha_token:
                    # Inyectar token en la página
                    await page.evaluate(f'''
                        () => {{
                            document.getElementById('g-recaptcha-response').innerHTML = '{captcha_token}';
                            if (typeof grecaptcha !== 'undefined') {{
                                grecaptcha.getResponse = function() {{ return '{captcha_token}'; }};
                            }}
                        }}
                    ''')

                # Hacer click en consultar
                boton = await page.query_selector('button:has-text("Consultar Información")')
                await boton.click()

                # Esperar resultados
                await asyncio.sleep(10)

                # Extraer datos
                resultado = await self._extraer_informacion(page, placa)
                return resultado

            finally:
                await browser.close()
```

---

## 💰 ANÁLISIS DE COSTOS

### Escenario 1: 100 CDAs al día
- Consultas por CDA: 2 (RUNT + SIMIT)
- Total consultas diarias: 200
- CAPTCHAs por día: 200 (solo RUNT)
- Costo 2Captcha: $0.50/1000 = $0.0001 por CAPTCHA
- **Costo mensual:** $0.60 USD 💰

### Escenario 2: 1000 CDAs al día
- Total consultas diarias: 2000
- CAPTCHAs por día: 2000
- **Costo mensual:** $6.00 USD 💰

### Escenario 3: 10,000 CDAs al día
- Total consultas diarias: 20,000
- CAPTCHAs por día: 20,000
- **Costo mensual:** $60.00 USD 💰

**Conclusión:** Muy económico incluso a escala grande.

---

## 📋 ¿CON LOS 8 CONECTORES CUBRIMOS TODO PARA CDAS?

### Requisitos para CDAs (Resolución 2328 de 2025):

#### 1. **Certificado de Antecedentes de Tránsito** ✅
- **Fuente:** RUNT
- **Estado:** ⚠️ Con CAPTCHA (necesita solver)

#### 2. **Consulta de Multas/Comparendos** ✅
- **Fuente:** SIMIT
- **Estado:** ✅ 100% funcional

#### 3. **Certificado Judicial** ✅
- **Fuente:** Policía Nacional
- **Estado:** ⚠️ Con fallback (puerto 7005)

#### 4. **Consulta Sanciones - Procuraduría** ✅
- **Fuente:** SIRI
- **Estado:** ✅ 100% funcional (OSINT)

#### 5. **Consulta Antecedentes Fiscales - Contraloría** ✅
- **Fuente:** SIRE
- **Estado:** ✅ 100% funcional (OSINT)

#### 6. **Situación Militar** ✅
- **Fuente:** Libreta Militar
- **Estado:** ✅ 100% funcional (OSINT)

#### 7. **Listas Restrictivas Internacionales** ✅
- **Fuentes:** OFAC, ONU, UE, UK, FBI, Interpol
- **Estado:** ✅ 100% funcional

#### 8. **Antecedentes Disciplinarios** ⚠️
- **Fuente:** Procuraduría (Fiscalía)
- **Estado:** ⚠️ No incluido (SIRI es inhabilidades, no antecedentes disciplinarios)

### Conclusión:

**Cubrimos ~85-90% de los requisitos para CDAs:**

✅ **SÍ cubrimos:**
- RUNT (con CAPTCHA solver)
- SIMIT
- Policía
- Procuraduría (SIRI)
- Contraloría (SIRE)
- Libreta Militar
- Listas internacionales

❌ **NO cubrimos:**
- Antecedentes disciplinarios de la Procuraduría (SIRI-Pro)
- Certificado de tradición (también RUNT pero diferente consulta)

---

## 🚀 PLAN DE IMPLEMENTACIÓN

### FASE 1: Identificar CAPTCHA (1 hora)
1. Abrir RUNT manualmente
2. Identificar tipo de CAPTCHA
3. Obtener site key si es reCAPTCHA

### FASE 2: Crear cuenta en 2Captcha (15 min)
1. Registrarse en https://2captcha.com
2. Obtener API key
3. Depositar $10 (suficiente para meses)

### FASE 3: Implementar solver (2-3 horas)
1. Instalar librería `requests`
2. Implementar función `_resolver_captcha()`
3. Inyectar token en página
4. Probar con 5 placas diferentes

### FASE 4: Testing (1 hora)
1. Test unitario: 10 placas
2. Test integración: API completa
3. Verificar que extrae datos reales
4. Verificar tiempo respuesta (< 60 seg)

### FASE 5: Deploy (30 min)
1. Actualizar contenedor Docker
2. Configurar API key como variable de entorno
3. Monitorear primeros 100 usos

**Tiempo total:** 4-6 horas
**Costo:** $10 inicial + $0.60-60/mes según volumen

---

## 🎯 RECOMENDACIÓN FINAL

### Usar **2Captcha** porque:

1. ✅ **Barato:** $0.50 por 1000 CAPTCHAs
2. ✅ **Confiable:** 95-99% precisión
3. ✅ **Fácil:** API REST simple
4. ✅ **Rápido:** 15-30 segundos
5. ✅ **Soporta todos los tipos:** reCAPTCHA v2/v3, hCaptcha

### Plan de acción:

**HOY:**
1. Identificar tipo de CAPTCHA de RUNT (1 hora)
2. Crear cuenta en 2captcha.com (15 min)

**MAÑANA:**
3. Implementar solver en runt_scraper.py (2-3 horas)
4. Testing con placas reales (1 hora)

**ESTA SEMANA:**
5. Deploy a producción
6. Monitorear primeros 100 usos

---

## 📞 SERVICIOS ALTERNATIVOS

Si 2Captcha no funciona:

1. **Anti-Captcha.com** - Similar, más caro
2. **DeathByCaptcha** - Más barato, menos confiable
3. **CapSolver** - Nuevo, prometedor
4. **YesCaptcha** - ML-based, experimental

---

**¿Quieres que implemente la solución con 2Captcha?**

Costo inicial: $10 USD
Tiempo: 4-6 horas
Resultado: RUNT 100% funcional con datos reales

Opción alternativa: Mantener fallback actual (0% costo, 87.5% funcional)

**Tu decisión.**
