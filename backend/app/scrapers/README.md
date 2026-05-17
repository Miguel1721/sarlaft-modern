# 🕷️ SCRAPERS SARLAFT - OSINT Y WEB SCRAPING

**Autor:** antigravity AI
**Fecha:** Mayo 17, 2026
**Objetivo:** Sistema automatizado de recopilación de inteligencia de fuentes abiertas para SARLAFT

---

## 📋 ESTRUCTURA DEL PROYECTO

```
scrapers/
├── README.md                    # Este archivo
├── requirements.txt             # Dependencias Python
├── __init__.py                  # Init del módulo
├── runt_scraper.py             # RUNT vehículos
├── simit_scraper.py            # SIMIT multas
├── ofac_scraper.py             # OFAC SDN List
├── onu_scraper.py              # ONU Consolidated List
├── eu_scraper.py               # European Union Sanctions
├── policia_scraper.py          # Certificado judicial
├── procuraduria_scraper.py     # Antecedentes disciplinarios
├── pep_scraper.py              # Base de datos PEPs OSINT
├── fuzzy_matching.py           # Matching de nombres
├── utils/
│   ├── __init__.py
│   ├── stealth_mode.py         # Anti-detección
│   ├── cache_manager.py        # Cache y rate limiting
│   └── normalizador.py         # Normalización de datos
└── tests/
    ├── test_runt.py
    ├── test_ofac.py
    └── test_fuzzy.py
```

---

## 🚀 INSTALACIÓN

### **1. Instalar dependencias**

```bash
cd /home/ubuntu/LABORATORIO/sarlaft-modern/backend/app/scrapers

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar paquetes
pip install -r requirements.txt

# Instalar Playwright browsers
playwright install chromium
```

### **2. Verificar instalación**

```bash
python3 -c "import playwright; print('Playwright OK')"
python3 -c "import rapidfuzz; print('RapidFuzz OK')"
python3 -c "import httpx; print('HTTPX OK')"
```

---

## 📖 USO

### **EJEMPLO 1: Consultar RUNT**

```python
import asyncio
from scrapers.runt_scraper import RUNTScraper

async def main():
    scraper = RUNTScraper()
    
    resultado = await scraper.consultar_vehiculo("ABC123")
    
    print(resultado)
    # {
    #     "status": "EXITOSO",
    #     "datos": {
    #         "placa": "ABC123",
    #         "vehiculo": {
    #             "marca": "MAZDA",
    #             "linea": "3",
    #             "modelo": 2020,
    #             ...
    #         }
    #     }
    # }

asyncio.run(main())
```

### **EJEMPLO 2: Consultar OFAC**

```python
from scrapers.ofac_scraper import OFACScraper

async def main():
    scraper = OFACScraper()
    
    resultado = await scraper.consultar_persona("JUAN PEREZ GARCIA")
    
    print(resultado)
    # {
    #     "status": "EXITOSO",
    #     "en_lista": False,
    #     "coincidencias": 0,
    #     "resultados": []
    # }

asyncio.run(main())
```

### **EJEMPLO 3: Fuzzy Matching**

```python
from scrapers.fuzzy_matching import buscar_coincidencia

nombres_buscar = ["JUAN PEREZ", "MARIA GARCIA", "CARLOS LOPEZ"]
nombre_consulta = "JUAN ALBERTO PEREZ"

coincidencias = buscar_coincidencia(
    nombre_consulta,
    nombres_buscar,
    umbral=85
)

for c in coincidencias:
    print(f"{c['nombre_original']} - Score: {c['score']}%")
    # JUAN PEREZ - Score: 91%
```

---

## ⚙️ CONFIGURACIÓN

### **Cache y Rate Limiting**

```python
from scrapers.utils.cache_manager import CacheManager, RateLimiter

# Cache de 24 horas
cache = CacheManager(ttl_horas=24)

# Rate limiter: 10 peticiones por minuto
rate_limiter = RateLimiter(peticiones_por_minuto=10)
```

### **Modo Stealth (Anti-detección)**

```python
from scrapers.utils.stealth_mode import crear_navegador_stealth

# Crear navegador camuflado
browser, context = await crear_navegador_stealth(headless=True)
```

---

## 🧪 TESTING

### **Ejecutar todos los tests**

```bash
cd /home/ubuntu/LABORATORIO/sarlaft-modern/backend/app/scrapers

# Test RUNT
python3 tests/test_runt.py

# Test OFAC
python3 tests/test_ofac.py

# Test Fuzzy
python3 tests/test_fuzzy.py
```

### **Test individual de scrapers**

```bash
# RUNT
python3 runt_scraper.py

# OFAC
python3 ofac_scraper.py
```

---

## 📊 INTEGRACIÓN CON SARLAFT

### **Conectar al orquestador**

```python
# En backend/app/services/orchestrator_service.py

from scrapers.runt_scraper import RUNTScraper
from scrapers.ofac_scraper import OFACScraper
from scrapers.simit_scraper import SIMITScraper

async def run_full_audit_v2(
    placa: str = None,
    cedula: str = None,
    client_id: str = None
):
    """Orquestador con scrapers reales"""

    resultados = {}

    # RUNT (si hay placa)
    if placa:
        runt_scraper = RUNTScraper()
        resultados['runt'] = await runt_scraper.consultar_vehiculo(placa)

    # OFAC (listas restrictivas)
    ofac_scraper = OFACScraper()
    resultados['ofac'] = await ofac_scraper.consultar_persona(
        nombre="",  # Debe pasarse el nombre real
        documento=cedula
    )

    # SIMIT
    if cedula:
        simit_scraper = SIMITScraper()
        resultados['simit'] = await simit_scraper.consultar_multas(cedula)

    return resultados
```

---

## ⚠️ LIMITACIONES Y CONSIDERACIONES

### **CAPTCHAS**
Algunos sitios web usan CAPTCHAs para bloquear bots. Opciones:
1. Usar servicios como 2captcha o anticaptcha
2. Rotar proxies
3. Reducir frecuencia de peticiones
4. Usar APIs oficiales cuando estén disponibles

### **RATE LIMITING**
- No exceder 10 peticiones/minuto por fuente
- Usar cache para reutilizar resultados
- Implementar backoff exponencial en caso de error

### **PRECISIÓN**
- Fuzzy matching con umbral 85% = balance optimal
- Revisión manual recomendada para casos sospechosos
- False positives posibles en nombres comunes

### **ALMACENAMIENTO**
- Cache en memoria se pierde al reiniciar
- Considerar Redis para cache persistente
- Guardar HTML de respuesta para debug

---

## 📝 LOGGING

### **Activar logging detallado**

```python
import logging
from loguru import logger

# Configurar
logger.add("scrapers.log", rotation="10 MB", level="DEBUG")

# Usar
logger.info("Consultando RUNT: {}", placa)
logger.error("Error scraping: {}", error)
```

---

## 🚨 PROBLEMAS COMUNES

### **Error: "Playwright not installed"**
```bash
playwright install chromium
```

### **Error: "No se encontró elemento"**
- La página web puede haber cambiado
- Verificar selectores CSS
- Usar modo headless=False para debug

### **Error: "Timeout"**
- Aumentar timeout en page.goto()
- Verificar conexión a internet
- Revisar si el sitio está caído

### **Error: "Rate limit exceeded"**
- Reducir frecuencia de peticiones
- Usar proxies rotativos
- Implementar backoff exponencial

---

## 📞 SOPORTE

**Documentación principal:** `/home/ubuntu/LABORATORIO/sarlaft-modern/GUIA_IMPLEMENTACION_COMPLETA.md`

**Instrucciones antigravity:** `/home/ubuntu/LABORATORIO/sarlaft-modern/INSTRUCCIONES_ANTIGRAVITY.md`

**Diagnósticos:** `/home/ubuntu/LABORATORIO/sarlaft-modern/DIAGRAMA_FLUJO_COMPLETO.md`

---

## 🔄 ACTUALIZACIONES

### **TODO - Próximos scrapers a implementar:**

- [ ] Procuraduría scraper
- [ ] Contraloría scraper
- [ ] Policías scraper (certificado judicial)
- [ ] ONU scraper (consolidated list)
- [ ] UE scraper (European sanctions)
- [ ] PEPs scraper (OSINT)

- [ ] Integración con orquestador principal
- [ ] Implementar cache Redis
- [ ] Agregar sistema de colas (Celery)
- [ ] Dashboard de monitoreo de scrapers

---

## 📄 LICENCIA Y ÉTICA

Este código es para uso **exclusivamente en el sistema SARLAFT** bajo las siguientes condiciones:

✅ **PERMITIDO:**
- Consulta de datos públicos
- Scraping de sitios gubernamentales
- Uso para debida diligencia SARLAFT
- OSINT sobre figuras públicas

❌ **PROHIBIDO:**
- Acceso a datos privados (SISBÉN, etc.)
- Evadir CAPTCHAs de forma maliciosa
- Sobrecargar servidores (DDoS)
- Uso fuera del contexto SARLAFT
- Violar términos de servicio de los sitios

---

**Última actualización:** Mayo 17, 2026
**Versión:** 1.0.0
**Estado:** En desarrollo
