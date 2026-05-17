# 📦 INSTRUCCIONES PARA IA "ANTIGRAVITY" - OSINT Y WEB SCRAPING

**Objetivo:** Crear scripts automatizados para extracción de datos de fuentes SARLAFT usando Playwright y técnicas OSINT

**Fecha:** Mayo 17, 2026
**Destinatario:** IA especializada en OSINT y web scraping

---

## 🎯 MISIÓN

Crear un sistema de **recopilación automatizada de inteligencia de fuentes abiertas (OSINT)** para el sistema SARLAFT, permitiendo consultar en tiempo real:

1. **Listas restrictivas internacionales** (OFAC, ONU, UE, etc.)
2. **Registros nacionales colombianos** (RUNT, SIMIT, Policía, etc.)
3. **Base de datos PEPs** (Personas Expuestas Políticamente)
4. **Medios de comunicación** (noticias sobre lavado de activos)
5. **Redes sociales** (información pública de LinkedIn, etc.)

---

## 📋 ESTRUCTURA DE TRABAJO

### **FASE 1: MAPEO DE FUENTES (Reconocimiento)**
### **FASE 2: SCRIPTS PLAYWRIGHT (Extracción)**
### **FASE 3: NORMALIZACIÓN DE DATOS (Procesamiento)**
### **FASE 4: INTEGRACIÓN CON SARLAFT (API)**

---

## 🌐 FUENTE 1: RUNT (REGISTRO NACIONAL AUTOMOTOR)

### **Información Objetivo:**
- Placa del vehículo
- Marca, línea, modelo
- Propietario (nombre, documento)
- Si tiene gravámenes
- Si ha estado involucrado en accidentes/siniestros

### **URL Objetivo:**
```
https://www.runt.gov.co/consultaCiudadana/consultaVehiculo
```

### **Script Playwright Esperado:**

```python
# archivo: runt_scraper.py
import asyncio
from playwright.async_api import async_playwright
from typing import Dict, Optional
import json

class RUNTScraper:
    """Scraper para consulta de vehículos en RUNT Colombia"""

    def __init__(self):
        self.base_url = "https://www.runt.gov.co/consultaCiudadana/consultaVehiculo"

    async def consultar_vehiculo(self, placa: str) -> Dict:
        """
        Consulta información de un vehículo por placa

        Args:
            placa: Placa del vehículo (ej: "ABC123")

        Returns:
            Dict con {
                "placa": str,
                "propietario": {
                    "tipo_documento": str,
                    "documento": str,
                    "nombre": str
                },
                "vehiculo": {
                    "marca": str,
                    "linea": str,
                    "modelo": int,
                    "color": str,
                    "cilindraje": str,
                    "clase": str,  // AUTOMOVIL, CAMION, etc
                    "servicio": str  // PARTICULAR, PUBLICO
                },
                "gravamenes": list,
                "siniestros": list,
                "estado": str  // ACTIVO, INACTIVO
            }
        """
        async with async_playwright() as p:
            # Lanzar navegador con stealth
            browser = await p.chromium.launch(
                headless=True,
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--no-sandbox',
                    '--disable-setuid-sandbox'
                ]
            )

            context = await browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            )

            page = await context.new_page()

            try:
                # Paso 1: Navegar a la página
                await page.goto(self.base_url, wait_until='networkidle', timeout=30000)
                await asyncio.sleep(2)

                # Paso 2: Seleccionar tipo de consulta (por placa)
                await page.click('input[name="tipoConsulta"][value="placa"]')
                await asyncio.sleep(0.5)

                # Paso 3: Ingresar número de placa
                await page.fill('input[name="numeroPlaca"]', placa.upper())
                await asyncio.sleep(0.5)

                # Paso 4: Resolver captcha si existe
                # NOTA: RUNT puede tener captcha, se requiere solución como 2captcha o anticaptcha

                # Paso 5: Click en consultar
                await page.click('button:has-text("Consultar")')
                await page.wait_for_selector('.resultado-consulta', timeout=15000)
                await asyncio.sleep(3)

                # Paso 6: Extraer información del DOM
                resultado = await self._extraer_informacion(page)

                return {
                    "status": "EXITOSO",
                    "datos": resultado,
                    "fuente": "RUNT",
                    "fecha_consulta": datetime.now().isoformat()
                }

            except Exception as e:
                return {
                    "status": "ERROR",
                    "error": str(e),
                    "placa": placa,
                    "fuente": "RUNT"
                }

            finally:
                await browser.close()

    async def _extraer_informacion(self, page) -> Dict:
        """Extrae la información del DOM de la página de resultados"""
        # Extract vehicle data using CSS selectors
        # NOTA: Los selectores exactos deben ajustarse después de inspeccionar la página real

        info = {}

        # Datos del vehículo
        try:
            info['placa'] = await page.inner_text('#placa-vehiculo')
            info['marca'] = await page.inner_text('#marca-vehiculo')
            info['linea'] = await page.inner_text('#linea-vehiculo')
            info['modelo'] = int(await page.inner_text('#modelo-vehiculo'))
            info['color'] = await page.inner_text('#color-vehiculo')
            info['cilindraje'] = await page.inner_text('#cilindraje-vehiculo')
            info['clase'] = await page.inner_text('#clase-vehiculo')
            info['servicio'] = await page.inner_text('#servicio-vehiculo')
        except:
            pass

        # Datos del propietario
        try:
            info['propietario'] = {
                'tipo_documento': await page.inner_text('#tipo-doc-propietario'),
                'documento': await page.inner_text('#num-doc-propietario'),
                'nombre': await page.inner_text('#nombre-propietario')
            }
        except:
            pass

        # Gravámenes
        try:
            gravamenes_section = await page.query_selector('.gravamenes-list')
            if gravamenes_section:
                info['gravamenes'] = await self._extraer_gravamenes(gravamenes_section)
            else:
                info['gravamenes'] = []
        except:
            info['gravamenes'] = []

        # Siniestros
        try:
            siniestros_section = await page.query_selector('.siniestros-list')
            if siniestros_section:
                info['siniestros'] = await self._extraer_siniestros(siniestros_section)
            else:
                info['siniestros'] = []
        except:
            info['siniestros'] = []

        return info

    async def _extraer_gravamenes(self, section) -> list:
        """Extrae lista de gravámenes si existen"""
        gravamenes = []
        # Implementar extracción de filas de tabla de gravámenes
        return gravamenes

    async def _extraer_siniestros(self, section) -> list:
        """Extrae lista de siniestros si existen"""
        siniestros = []
        # Implementar extracción de filas de tabla de siniestros
        return siniestros
```

---

## 🌐 FUENTE 2: SIMIT (SISTEMA INTEGRADO DE MULTAS Y INFRACCIONES)

### **Información Objetivo:**
- Multas de tránsito asociadas a una persona
- Comparendos pendientes
- Estado de licencia de conducción

### **URL Objetivo:**
```
https://www.fiscalia.gov.co/sijai/consultas/sijai-web/consultaCiudadana/consultas/consultasComparendos
```

### **Script Playwright Esperado:**

```python
# archivo: simit_scraper.py
import asyncio
from playwright.async_api import async_playwright
from typing import Dict, List

class SIMITScraper:
    """Scraper para consulta de multas SIMIT"""

    def __init__(self):
        self.base_url = "https://www.fiscalia.gov.co/sijai/consultas/..."

    async def consultar_multas(self, documento: str, placa: str = None) -> Dict:
        """
        Consulta multas de tránsito por documento o placa

        Args:
            documento: Cédula ciudadana
            placa: (opcional) Placa del vehículo

        Returns:
            Dict con {
                "total_multas": int,
                "valor_total": float,
                "multas": [
                    {
                        "numero_comparendo": str,
                        "fecha": str,
                        "infraccion": str,
                        "valor": float,
                        "estado": str,  // PENDIENTE, PAGADO
                        "secretaria": str
                    }
                ]
            }
        """
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()

            try:
                await page.goto(self.base_url, wait_until='networkidle')

                # Seleccionar tipo de consulta (por documento)
                await page.select_option('select[name="tipoConsulta"]', 'DOCUMENTO')
                await page.fill('input[name="numeroDocumento"]', documento)

                # Submit
                await page.click('button[type="submit"]')
                await page.wait_for_selector('.resultados', timeout=15000)

                # Extraer multas
                multas = await self._extraer_multas(page)

                return {
                    "status": "EXITOSO",
                    "datos": multas,
                    "fuente": "SIMIT"
                }

            except Exception as e:
                return {
                    "status": "ERROR",
                    "error": str(e),
                    "fuente": "SIMIT"
                }
            finally:
                await browser.close()

    async def _extraer_multas(self, page) -> Dict:
        """Extrae lista de multas del DOM"""
        # Implementar extracción de tabla de multas
        pass
```

---

## 🌐 FUENTE 3: LISTA OFAC (USA - SDN LIST)

### **Información Objetivo:**
- Personas y entidades sancionadas por OFAC
- Nombres, direcciones, fecha de inclusión
- Tipo de sanción

### **URL Objetivo:**
```
https://sanctionssearch.ofac.treas.gov/
https://api.public.lu/OFAC/SDN/ (API alternativa)
```

### **Script Playwright + API:**

```python
# archivo: ofac_scraper.py
import asyncio
import httpx
from typing import Dict, List

class OFACScraper:
    """Scraper/Cliente para lista SDN de OFAC"""

    def __init__(self):
        # API OFAC Search Tool (más confiable que scraping)
        self.api_url = "https://sanctionssearch.ofac.treas.gov/api/v2"
        self.fallback_url = "https://ofac-api-wrapper.public.lu/api/SDN"
        self.client = httpx.AsyncClient(timeout=30.0)

    async def consultar_persona(self, nombre: str, documento: str = None) -> Dict:
        """
        Consulta si una persona está en lista OFAC SDN

        Args:
            nombre: Nombre completo a buscar
            documento: (opcional) Documento de identidad

        Returns:
            Dict con {
                "coincidencias": int,
                "en_lista": bool,
                "resultados": [
                    {
                        "nombre": str,
                        "tipo": str,  // individual / entity
                        "programas": [str],
                        "direcciones": [str],
                        "fecha_inclusion": str,
                        "lista": "OFAC-SDN"
                    }
                ]
            }
        """
        try:
            # Método 1: API oficial (si está disponible)
            resultado_api = await self._consulta_api_ofac(nombre, documento)
            if resultado_api:
                return resultado_api

            # Método 2: API wrapper alternativa
            resultado_alt = await self._consulta_api_alternativa(nombre, documento)
            if resultado_alt:
                return resultado_alt

            # Método 3: Descargar lista completa (actualización semanal)
            resultado_lista = await self._consulta_lista_completa(nombre, documento)
            return resultado_lista

        except Exception as e:
            return {
                "status": "ERROR",
                "error": str(e),
                "fuente": "OFAC",
                "consultado": nombre
            }

    async def _consulta_api_ofac(self, nombre: str, documento: str) -> Dict:
        """Consulta API oficial OFAC"""
        try:
            params = {
                "name": nombre,
                "type": "individual"
            }

            response = await self.client.get(
                f"{self.api_url}/search",
                params=params
            )

            if response.status_code == 200:
                data = response.json()

                if data.get("results"):
                    return {
                        "status": "EXITOSO",
                        "en_lista": True,
                        "coincidencias": len(data["results"]),
                        "resultados": data["results"][:10],  # Primeras 10
                        "fuente": "OFAC-API"
                    }
                else:
                    return {
                        "status": "EXITOSO",
                        "en_lista": False,
                        "coincidencias": 0,
                        "resultados": [],
                        "fuente": "OFAC-API"
                    }

        except Exception as e:
            print(f"Error API OFAC: {e}")
            return None

    async def _consulta_api_alternativa(self, nombre: str, documento: str) -> Dict:
        """Consulta API wrapper alternativa"""
        try:
            # Existen varios mirrors de la lista OFAC
            urls = [
                "https://ofac-api-wrapper.public.lu/api/SDN",
                "https://sanctions-list.org/api/ofac",
                "https://api.tr sanctions.io/ofac"
            ]

            for url in urls:
                try:
                    params = {"name": nombre}
                    response = await self.client.get(url, params=params)

                    if response.status_code == 200:
                        data = response.json()
                        # Procesar resultado...
                        return {"status": "EXITOSO", "datos": data}

                except:
                    continue

        except Exception as e:
            print(f"Error API alternativa: {e}")
            return None

    async def _consulta_lista_completa(self, nombre: str, documento: str) -> Dict:
        """Descarga lista completa OFAC (actualizada semanalmente) y busca localmente"""
        try:
            # URL de la lista completa en XML/CSV
            url_lista = "https://sanctionssearch.ofac.treas.gov/api/v2/downloads/sdn.xml"

            # Descargar (o usar cache si se descargó hace < 7 días)
            response = await self.client.get(url_lista)

            # Parsear XML/CSV y buscar coincidencias
            # Usar búsqueda fuzzy matching
            coincidencias = self._buscar_en_lista(response.text, nombre)

            return {
                "status": "EXITOSO",
                "en_lista": len(coincidencias) > 0,
                "coincidencias": len(coincidencias),
                "resultados": coincidencias,
                "fuente": "OFAC-LISTA-COMPLETA"
            }

        except Exception as e:
            print(f"Error lista completa: {e}")
            return None

    def _buscar_en_lista(self, lista_xml: str, nombre_busqueda: str) -> List[Dict]:
        """Busca nombre en lista OFAC usando fuzzy matching"""
        from rapidfuzz import fuzz, process

        # Parsear XML
        import xml.etree.ElementTree as ET
        root = ET.fromstring(lista_xml)

        # Extraer nombres
        nombres_ofac = []
        for item in root.findall('.//sdnEntry'):
            nombre_primario = item.find('.//firstName').text
            apellido_primario = item.find('.//lastName').text
            nombre_completo = f"{nombre_primario} {apellido_primario}"

            nombres_ofac.append({
                "nombre": nombre_completo,
                "uid": item.find('.//uid').text,
                "programas": [p.text for p in item.findall('.//programList')]
            })

        # Búsqueda fuzzy (permite variaciones en nombre)
        resultados = process.extract(
            nombre_busqueda,
            [n["nombre"] for n in nombres_ofac],
            scorer=fuzz.WRatio,
            limit=5
        )

        # Filtrar por score > 85 (coincidencia alta)
        coincidencias = [
            n for r, score, idx in resultados
            if score > 85
            for n in [nombres_ofac[idx]]
        ]

        return coincidencias
```

---

## 🌐 FUENTE 4: LISTA ONU (CONSOLIDATED LIST)

### **Script Similar:**

```python
# archivo: onu_scraper.py
class ONUScraper:
    """Scraper para lista consolidada ONU"""

    def __init__(self):
        self.url_lista = "https://www.un.org/securitycouncil/sanctions/1267/aq_sanctions_list"
        self.url_api = "https://api.un.org/sc/sanctions/1267"

    async def consultar_persona(self, nombre: str) -> Dict:
        """Consulta en lista ONU de terroristas"""
        # Similar a OFAC pero con formato JSON/XML diferente
        pass
```

---

## 🌐 FUENTE 5: PREGUNTA SISBÉN (TÉCNICAMENTE NO DISPONIBLE)

### **NOTA IMPORTANTE:**
SISBÉN **NO TIENE API PÚBLICA** y el acceso está restringido por:
- Ley Habeas Data (protección datos sensibles)
- Acceso solo para entidades estatales autorizadas
- No es ético ni legal acceder sin autorización

### **Alternativa Sugerida:**
NO incluir SISBÉN en scraping. En su lugar, usar:
- Auto-reportado por el cliente (declaración juramentada)
- Estratificación socioeconómica basada en actividad económica y ubicación

---

## 🌐 FUENTE 6: REGISTRO NACIONAL DE PEPs

### **Problema:**
Colombia **NO TIENE** un registro oficial público de PEPs.

### **Solución OSINT:**
Crear base de datos propia usando fuentes abiertas:

1. **Congresistas** - https://www.congreso.gov.co/
2. **Gobernadores** - https://www.gobernadores.gov.co/
3. **Alcaldes** - Cada alcaldía tiene su portal
4. **Funcionarios públicos** - Cada entidad

### **Script Propuesto:**

```python
# archivo: pep_scraper.py
import asyncio
from playwright.async_api import async_playwright
from typing import Dict, List

class PEPScraper:
    """Scraper para construir base de datos de PEPs colombianos"""

    def __init__(self):
        self.fuentes = [
            {
                "nombre": "Congresistas",
                "url": "https://www.congreso.gov.co/",
                "tipo": "LEGISLATIVO_NACIONAL"
            },
            {
                "nombre": "Gobernadores",
                "url": "https://www.gobernadores.gov.co/",
                "tipo": "EJECUTIVO_DEPARTAMENTAL"
            },
            # Agregar más fuentes...
        ]

    async def construir_base_peps(self) -> List[Dict]:
        """
        Construye base de datos de PEPs usando OSINT

        Returns:
            Lista de PEPs con {
                "documento": str,
                "nombre": str,
                "cargo": str,
                "entidad": str,
                "nivel": str,  # NACIONAL, DEPARTAMENTAL, MUNICIPAL
                "ambito": str,  # EJECUTIVO, LEGISLATIVO, JUDICIAL
                "fecha_inicio": str,
                "fecha_fin": str  # null si está en ejercicio
            }
        """
        base_peps = []

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)

            for fuente in self.fuentes:
                try:
                    peps_fuente = await self._extraer_peps_fuente(browser, fuente)
                    base_peps.extend(peps_fuente)
                except Exception as e:
                    print(f"Error scraping {fuente['nombre']}: {e}")

            await browser.close()

        # Guardar en base de datos local
        await self._guardar_base_peps(base_peps)

        return base_peps

    async def _extraer_peps_fuente(self, browser, fuente: Dict) -> List[Dict]:
        """Extrae PEPs de una fuente específica"""
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto(fuente['url'], wait_until='networkidle')

        # Implementar extracción específica por fuente
        # Cada portal tiene estructura diferente

        peps = []

        if fuente['nombre'] == "Congresistas":
            peps = await self._scrapear_congreso(page)
        elif fuente['nombre'] == "Gobernadores":
            peps = await self._scrapear_gobernadores(page)

        return peps

    async def _scrapear_congreso(self, page) -> List[Dict]:
        """Scrapea lista de congresistas"""
        # Navegar a sección de congresistas
        await page.click('a:has-text("Congresistas")')
        await page.wait_for_selector('.lista-congresistas')

        # Extraer información
        congresistas = []
        cards = await page.query_selector_all('.card-congresista')

        for card in cards:
            nombre = await card.inner_text('.nombre')
            partido = await card.inner_text('.partido')
            region = await card.inner_text('.region')

            # Click para ver detalles y obtener documento
            await card.click()
            await page.wait_for_selector('.detalles-congresista')

            documento = await page.inner_text('.documento')

            congresistas.append({
                "nombre": nombre,
                "cargo": "Congresista",
                "entidad": "Congreso de la República",
                "nivel": "NACIONAL",
                "ambito": "LEGISLATIVO",
                "documento": documento,
                "partido": partido,
                "region": region
            })

            # Volver a la lista
            await page.go_back()
            await page.wait_for_selector('.lista-congresistas')

        return congresistas

    async def _scrapear_gobernadores(self, page) -> List[Dict]:
        """Scrapea lista de gobernadores"""
        # Similar al anterior pero con estructura diferente
        pass

    async def _guardar_base_peps(self, peps: List[Dict]):
        """Guarda base de PEPs en SQLite/PostgreSQL"""
        # Implementar guardado en BD local
        pass

    async def consultar_pep(self, documento: str) -> Dict:
        """Consulta si un documento está en base de PEPs"""
        # Buscar en BD local
        # Si no está, intentar scraping en tiempo real (más lento)
        pass
```

---

## 🔧 TÉCNICAS OSINT AVANZADAS

### **1. FUZZY MATCHING PARA NOMBRES**

```python
# archivo: fuzzy_matching.py
from rapidfuzz import fuzz, process

def normalizar_nombre(nombre: str) -> str:
    """Normaliza nombre para comparación"""
    import unicodedata
    import re

    # Eliminar acentos
    nombre = unicodedata.normalize('NFKD', nombre)
    nombre = ''.join([c for c in nombre if not unicodedata.combining(c)])

    # Convertir a mayúsculas
    nombre = nombre.upper()

    # Eliminar caracteres especiales
    nombre = re.sub(r'[^A-Z\s]', '', nombre)

    # Eliminar palabras comunes
    stopwords = ['DE', 'LA', 'EL', 'LOS', 'LAS', 'DEL', 'Y', 'EN']
    for stop in stopwords:
        nombre = nombre.replace(f' {stop} ', ' ')

    return nombre.strip()

def buscar_coincidencia(nombre_busqueda: str, lista_nombres: List[str]) -> List[Dict]:
    """Busca coincidencias usando fuzzy matching"""

    nombre_normalizado = normalizar_nombre(nombre_busqueda)
    lista_normalizada = [normalizar_nombre(n) for n in lista_nombres]

    # Búsqueda con varios algoritmos
    resultados = process.extract(
        nombre_normalizado,
        lista_normalizada,
        scorer=fuzz.WRatio,  # Weighted Ratio (mejor para nombres)
        limit=10
    )

    # Filtrar por umbral
    coincidencias = []
    for resultado, score, idx in resultados:
        if score >= 85:  # 85% de similitud
            coincidencias.append({
                "nombre": lista_nombres[idx],
                "score": score,
                "match_normalizado": resultado
            })

    return coincidencias
```

---

### **2. EVASIÓN DE DETECCIÓN (ANTI-BOT)**

```python
# archivo: stealth_mode.py
from playwright.async_api import async_playwright

async def crear_navegador_stealth():
    """Crea navegador con configuración anti-detección"""

    p = await async_playwright().start()

    browser = await p.chromium.launch(
        headless=True,
        args=[
            '--disable-blink-features=AutomationControlled',
            '--disable-dev-shm-usage',
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-web-security',
            '--disable-features=IsolateOrigins,site-per-process',
            '--window-size=1920,1080'
        ]
    )

    context = await browser.new_context(
        viewport={'width': 1920, 'height': 1080},
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        locale='es-CO',
        timezone_id='America/Bogota',
        permissions=['geolocation', 'notifications']
    )

    # Inyectar script para ocultar automatización
    await context.add_init_script("""
        // Ocultar webdriver
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        });

        // Ocultar plugins
        Object.defineProperty(navigator, 'plugins', {
            get: () => [1, 2, 3, 4, 5]
        });

        // Ocultar languages
        Object.defineProperty(navigator, 'languages', {
            get: () => ['es-CO', 'es', 'en-US', 'en']
        });
    """)

    return browser, context
```

---

### **3. MANEJO DE CAPTCHAS**

```python
# archivo: captcha_solver.py
class CaptchaSolver:
    """Solucionador de CAPTCHAs usando servicios externos"""

    def __init__(self, api_key_2captcha: str = None):
        self.api_key = api_key_2captcha
        # Alternativas: anticaptcha, capmonster, deathbycaptcha

    async def resolver_recaptcha_v2(self, page, site_key: str, url: str):
        """Resuelve reCAPTCHA v2 usando 2captcha"""

        if not self.api_key:
            raise ValueError("Se requiere API key de 2captcha")

        # Enviar CAPTCHA a 2captcha
        # Poll para esperar resultado
        # Inyectar token en página

        pass

    async def_resolver_captcha_imagen(self, imagen_base64: str):
        """Resuelve CAPTCHA de imagen"""

        # Enviar imagen a 2captcha
        # Esperar solución (texto)
        # Retornar texto

        pass
```

---

### **4. CACHE Y RATE LIMITING**

```python
# archivo: cache_manager.py
import asyncio
from datetime import datetime, timedelta
from typing import Dict, Optional
import hashlib
import json

class CacheManager:
    """Maneja cache de consultas para evitar bans"""

    def __init__(self, ttl_horas: int = 24):
        self.cache: Dict[str, Dict] = {}
        self.ttl = timedelta(hours=ttl_horas)

    def _generar_key(self, fuente: str, consulta: str) -> str:
        """Genera key única para cache"""
        texto = f"{fuente}:{consulta}"
        return hashlib.sha256(texto.encode()).hexdigest()

    async def obtener(self, fuente: str, consulta: str) -> Optional[Dict]:
        """Obtiene resultado cacheado si existe y no ha expirado"""
        key = self._generar_key(fuente, consulta)

        if key in self.cache:
            entrada = self.cache[key]

            if datetime.now() - entrada['timestamp'] < self.ttl:
                print(f"✅ Cache HIT: {fuente} - {consulta}")
                return entrada['datos']
            else:
                # Expiró, eliminar
                del self.cache[key]

        return None

    async def guardar(self, fuente: str, consulta: str, datos: Dict):
        """Guarda resultado en cache"""
        key = self._generar_key(fuente, consulta)

        self.cache[key] = {
            'datos': datos,
            'timestamp': datetime.now()
        }

    async def limpiar_expirados(self):
        """Limpia entradas expiradas del cache"""
        ahora = datetime.now()

        keys_a_borrar = [
            key for key, entrada in self.cache.items()
            if ahora - entrada['timestamp'] >= self.ttl
        ]

        for key in keys_a_borrar:
            del self.cache[key]

        print(f"🧹 Limpiados {len(keys_a_borrar)} entries expirados")

# Rate limiter para evitar bans
class RateLimiter:
    """Limita frecuencia de peticiones"""

    def __init__(self, peticiones_por_minuto: int = 10):
        self.ppm = peticiones_por_minuto
        self.peticiones = []
        self.lock = asyncio.Lock()

    async def acquire(self):
        """Espera si se excede el rate limit"""
        async with self.lock:
            ahora = datetime.now()

            # Eliminar peticiones antiguas (más de 1 minuto)
            self.peticiones = [
                p for p in self.peticiones
                if ahora - p < timedelta(minutes=1)
            ]

            # Si se excede el límite, esperar
            if len(self.peticiones) >= self.ppm:
                tiempo_espera = timedelta(minutes=1) / self.ppm
                print(f"⏸️ Rate limit alcanzado. Esperando {tiempo_espera.total_seconds():.1f}s")
                await asyncio.sleep(tiempo_espera.total_seconds())

            # Registrar petición
            self.peticiones.append(ahora)
```

---

## 📁 ESTRUCTURA DE ARCHIVOS FINAL

```
/home/ubuntu/LABORATORIO/sarlaft-modern/backend/app/scrapers/
├── __init__.py
├── runt_scraper.py          # RUNT vehículo
├── simit_scraper.py         # SIMIT multas
├── ofac_scraper.py          # OFAC SDN List
├── onu_scraper.py           # ONU Consolidated List
├── eu_scraper.py            # European Union Sanctions
├── policia_scraper.py       # Certificado judicial
├── procuraduria_scraper.py  # Antecedentes disciplinarios
├── pep_scraper.py           # Base de datos PEPs OSINT
├── utils/
│   ├── fuzzy_matching.py    # Matching de nombres
│   ├── stealth_mode.py      # Anti-detección
│   ├── captcha_solver.py    # Solución CAPTCHAs
│   ├── cache_manager.py     # Cache y rate limiting
│   └── normalizador.py      # Normalización de datos
└── config.py                # Configuración (API keys, etc.)
```

---

## 🚀 PLAN DE EJECUCIÓN

### **SEMANA 1: MAPEO Y PRUEBAS**

**Día 1-2: Mapeo de fuentes**
- [ ] Identificar URLs exactas de cada fuente
- [ ] Documentar estructura de cada página web
- [ ] Crear diagramas de flujo de navegación

**Día 3-4: Prototipos**
- [ ] Crear prototipo RUNT scraper
- [ ] Crear prototipo OFAC scraper
- [ ] Testear con datos reales

**Día 5: Evaluación**
- [ ] Medir tiempos de respuesta
- [ ] Identificar CAPTCHAs y bloqueos
- [ ] Documentar limitaciones

---

### **SEMANA 2: IMPLEMENTACIÓN**

**Día 1-3: Scrapers principales**
- [ ] RUNT scraper completo
- [ ] SIMIT scraper completo
- [ ] OFAC scraper completo

**Día 4-5: Scrapers secundarios**
- [ ] ONU scraper
- [ ] UE scraper
- [ ] Policías scraper

---

### **SEMANA 3: INTEGRACIÓN**

**Día 1-2: Integración con SARLAFT**
- [ ] Conectar scrapers al orquestador
- [ ] Normalizar datos de salida
- [ ] Manejo de errores robusto

**Día 3-5: Testing**
- [ ] Test end-to-end con 100 consultas
- [ ] Medir tasa de éxito
- [ ] Optimizar performance

---

## ⚠️ CONSIDERACIONES ÉTICAS Y LEGALES

### **✅ PERMITIDO:**
- Consulta de datos públicos
- Web scraping de sitios gubernamentales
- Uso de APIs oficiales
- OSINT sobre figuras públicas

### **❌ PROHIBIDO:**
- Acceder a bases de datos privadas (SISBÉN)
- Evadir CAPTCHAs de forma maliciosa
- Sobrecargar servidores (DDoS)
- Violar términos de servicio
- Acceder a datos personales sin autorización

### **📋 MEJORES PRÁCTICAS:**
1. **Rate limiting:** Máximo 10 peticiones/minuto por fuente
2. **Cache:** Reutilizar resultados por 24 horas
3. **User-Agent:** Identificarse claramente
4. **Respetar robots.txt:** Seguir reglas del sitio
5. **Transparencia:** Documentar fuentes y métodos

---

## 📞 CONTACTO Y SOPORTE

**Archivos creados:** `/home/ubuntu/LABORATORIO/sarlaft-modern/backend/app/scrapers/`

**Documentación:**
- `GUIA_IMPLEMENTACION_COMPLETA.md`
- `DIAGRAMA_FLUJO_COMPLETO.md`

**Próximos pasos:**
1. Revisar instrucciones
2. Crear carpeta `scrapers/`
3. Iniciar con RUNT scraper
4. Testear con placas reales

---

**¿NECESITAS ACLARACIONES ANTES DE COMENZAR?**
