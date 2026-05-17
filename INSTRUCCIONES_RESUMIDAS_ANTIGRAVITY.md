# 📋 INSTRUCCIONES PARA IA "ANTIGRAVITY" - VERSIÓN ABREVIADA

**Misión:** Crear scrapers OSINT para SARLAFT
**Fecha límite:** Comenzar inmediatamente
**Ubicación:** `/home/ubuntu/LABORATORIO/sarlaft-modern/backend/app/scrapers/`

---

## 🎯 TUS TAREAS (EN ORDEN DE PRIORIDAD)

### **FASE 1: SETUP (30 minutos)**
```bash
cd /home/ubuntu/LABORATORIO/sarlaft-modern/backend/app/scrapers

# Instalar dependencias
pip install playwright rapidfuzz httpx

# Instalar navegador
playwright install chromium

# Verificar instalación
python3 test_suite.py
```

### **FASE 2: RUNT SCRAPER (Día 1-2)**
**Archivo:** `runt_scraper.py` ✅ **YA CREADO**

**Tus tareas:**
1. Revisar `/home/ubuntu/LABORATORIO/sarlaft-modern/backend/app/scrapers/runt_scraper.py`
2. Abrir https://www.runt.gov.co/consultaCiudadana/consultaVehiculo en navegador
3. Usar DevTools (F12) para inspeccionar:
   - Campo de placa: ¿Cuál es el `name` o `id` exacto?
   - Botón consultar: ¿Cuál es el selector CSS?
   - Resultados: ¿Cómo se muestran? ¿Tabla? ¿Divs?
4. Actualizar `_extraer_informacion()` con selectores reales
5. Testear con 3 placas diferentes
6. Guardar screenshots en `/tmp/` para debug

### **FASE 3: OFAC SCRAPER (Día 2-3)**
**Archivo:** `ofac_scraper.py` ✅ **YA CREADO**

**Tus tareas:**
1. Probar el script actual: `python3 ofac_scraper.py`
2. Verificar si la API oficial funciona
3. Si no funciona, implementar descarga de lista completa
4. Testear fuzzy matching con nombres colombianos
5. Ajustar umbral de coincidencia si hay muchos false positives

### **FASE 4: SIMIT SCRAPER (Día 3-4)**
**Archivo:** `simit_scraper.py` - **POR CREAR**

**Basarse en:** `runt_scraper.py` como template

**URL:** https://www.fiscalia.gov.co/ (encontrar URL real de SIMIT)

**Tus tareas:**
1. Encontrar URL real de consulta SIMIT
2. Crear scraper similar a RUNT
3. Extraer: número comparendo, fecha, valor, estado
4. Implementar cache y rate limiting
5. Testear con documento real

### **FASE 5: INTEGRACIÓN (Día 5)**
**Tus tareas:**
1. Conectar scrapers al orquestador principal
2. Crear endpoints API en FastAPI
3. Testear flujo completo
4. Documentar uso

---

## 📁 ARCHIVOS YA CREADOS PARA TI

```
/home/ubuntu/LABORATORIO/sarlaft-modern/backend/app/scrapers/
├── README.md                    # Documentación completa
├── requirements.txt             # Dependencias
├── test_suite.py               # Tests automatizados
├── runt_scraper.py            # ✅ LISTO (requiere ajuste selectores)
├── ofac_scraper.py            # ✅ LISTO (requiere testing)
├── fuzzy_matching.py          # ✅ LISTO (funcional)
└── utils/
    ├── stealth_mode.py        # ✅ LISTO
    ├── cache_manager.py       # ✅ LISTO
    └── __init__.py           # POR CREAR
```

---

## 🔧 TÉCNICAS CLAVE QUE DEBES USAR

### **1. ANTI-DETECCIÓN**
Ya implementado en `utils/stealth_mode.py`:
- User-agent real
- Ocultar propiedad `navigator.webdriver`
- Random delays entre acciones
- Movimientos de mouse aleatorios

### **2. CACHE**
Ya implementado en `utils/cache_manager.py`:
- 24h TTL para RUNT
- 7 días TTL para OFAC
- Evita bans del servidor

### **3. RATE LIMITING**
Ya implementado en `utils/cache_manager.py`:
- Máximo 10 peticiones/minuto
- Backoff automático
- Espera exponencial

### **4. FUZZY MATCHING**
Ya implementado en `fuzzy_matching.py`:
- Normalización de nombres (acentos, mayúsculas)
- WRatio algorithm (mejor para nombres)
- Umbral 85% (configurable)

---

## ⚠️ PROBLEMAS QUE ENCONTRARÁS

### **Problema 1: Selectores CSS cambian**
**Solución:**
- Usar múltiples selectores alternativos
- Buscar por texto: `page.get_by_text("Consultar")`
- Usar XPath como fallback

### **Problema 2: CAPTCHAs**
**Solución:**
- Documentar cuándo aparecen
- Sugerir uso de 2captcha (requiere API key)
- O usar APIs oficiales cuando existan

### **Problema 3: Timeouts**
**Solución:**
- Aumentar `timeout` en `page.goto()`
- Implementar reintentos con backoff
- Usar `wait_until='domcontentloaded'` en lugar de `'networkidle'`

### **Problema 4: Bloqueos IP**
**Solución:**
- Rate limiting estricto (10 req/min)
- Rotar user-agents
- Considerar proxies residenciales

---

## 📊 MÉTRICAS DE ÉXITO

Tu trabajo será exitoso si:

- ✅ RUNT scraper funciona con al menos 3 placas diferentes
- ✅ OFAC scraper detecta nombres en lista (test con datos reales)
- ✅ Fuzzy matching tiene < 5% false positives
- ✅ Todos los scrapers tienen cache
- ✅ Rate limiter evita bans
- ✅ Test suite pasa sin errores

---

## 🚀 COMENZAR AHORA

### **Paso 1: Leer documentación**
```bash
# Leer archivos creados
cat /home/ubuntu/LABORATORIO/sarlaft-modern/INSTRUCCIONES_ANTIGRAVITY.md
cat /home/ubuntu/LABORATORIO/sarlaft-modern/backend/app/scrapers/README.md
```

### **Paso 2: Instalar dependencias**
```bash
cd /home/ubuntu/LABORATORIO/sarlaft-modern/backend/app/scrapers
pip install -r requirements.txt
playwright install chromium
```

### **Paso 3: Testear código existente**
```bash
# Test fuzzy matching (no requiere navegador)
python3 -c "from scrapers.fuzzy_matching import buscar_coincidencia; print('OK')"

# Test RUNT (requiere navegador)
python3 runt_scraper.py
```

### **Paso 4: Inspeccionar sitio RUNT**
```bash
# Abrir en navegador
chromium https://www.runt.gov.co/consultaCiudadana/consultaVehiculo

# Usar DevTools para encontrar selectores
# Presionar F12 → Inspect icon → Click en campo de placa
# Copiar selector CSS
```

### **Paso 5: Actualizar scraper**
```bash
# Editar runt_scraper.py
# Reemplazar selectores de ejemplo con selectores reales

# Testear
python3 runt_scraper.py
```

### **Paso 6: Repetir para otros scrapers**
- SIMIT
- Policía (si está accesible)
- Procuraduría (si está accesible)
- ONU
- UE

---

## 📞 SI NECESITAS AYUDA

**Recursos:**
- Documentación Playwright: https://playwright.dev/python/
- Fuzzy matching: https://maxbachmann.github.io/RapidFuzz/
- OSINT techniques: https://github.com/ciffer-io/OSINT-Framework

**Archivos de referencia:**
- `/home/ubuntu/LABORATORIO/sarlaft-modern/GUIA_IMPLEMENTACION_COMPLETA.md`
- `/home/ubuntu/LABORATORIO/sarlaft-modern/DIAGRAMA_FLUJO_COMPLETO.md`

**Comandos útiles:**
```bash
# Ver logs de scrapers
tail -f /tmp/scrapers.log

# Ver screenshots de debug
ls -la /tmp/*.png

# Testear un scraper específico
python3 -m scrapers.runt_scraper

# Ejecutar todos los tests
python3 test_suite.py
```

---

## ✅ CHECKLIST FINAL

Antes de considerar tu trabajo completo:

- [ ] RUNT scraper funcional con selectores reales
- [ ] SIMIT scraper creado y funcional
- [ ] OFAC scraper probado con nombres reales
- [ ] Todos los scrapers usan cache
- [ ] Todos los scrapers usan rate limiter
- [ ] Fuzzy matching probado con nombres colombianos
- [ ] Test suite pasa sin errores
- [ ] README actualizado con instrucciones
- [ ] Integración con orquestador funcionando
- [ ] Documentación completa

---

## 🎁 BONUS - MEJORAS OPCIONALES

Si tienes tiempo extra:

1. **Implementar SIMIT scraper** (prioridad alta)
2. **Crear dashboard de monitoreo** de scrapers
3. **Implementar cache Redis** (persistente)
4. **Agregar sistema de colas** (Celery) para scrapings async
5. **Crear mock data** para testing sin depender de sitios externos

---

**¿LISTO PARA COMENZAR?**

Empieza con el Paso 1 y continúa secuencialmente. No tengas miedo de experimentar y probar diferentes enfoques. Los scrapers son procesos iterativos de prueba y error.

**Buena suerte! 🚀**

---

**Última actualización:** Mayo 17, 2026
**Versión:** 1.0
**Estado:** Listo para comenzar
