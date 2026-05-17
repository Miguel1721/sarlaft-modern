# 📋 CHECKLIST PARA ANTIGRAVITY - LLEVAR SISTEMA AL 100%

**Fecha:** Mayo 17, 2026
**Objetivo:** Encontrar selectores CSS reales de RUNT y SIMIT
**Tiempo estimado:** 2-3 horas

---

## 🎯 MISIÓN

El sistema usa **Hybrid Smart Failover** (retorna datos simulados cuando falla el scraping). Tu trabajo:
1. Inspeccionar páginas web manualmente con Chrome DevTools
2. Encontrar selectores CSS exactos de cada campo
3. Actualizar scrapers con selectores reales
4. Probar con datos reales

---

## 📋 ORDEN DE TAREAS

### ✅ TAREA 1: Preparar entorno (5 min)

```bash
# Instalar dependencias
cd /home/ubuntu/LABORATORIO/sarlaft-modern/backend
pip3 install playwright rapidfuzz
playwright install chromium

# Verificar instalación
python3 -c "import playwright; print('✅ Playwright OK')"
python3 -c "import rapidfuzz; print('✅ RapidFuzz OK')"

# Abrir Chrome para inspección
google-chrome https://www.runt.gov.co/consultaCiudadana/consultaVehiculo &
```

---

### ✅ TAREA 2: Inspeccionar RUNT (45 min)

#### PASO 2.1: Abrir DevTools
- Presiona **F12** en Chrome
- Click en icono "Inspect Element" (↗️)

#### PASO 2.2: Encontrar campo de placa

1. Click en icono Inspect Element (↗️)
2. Click en el campo "Número de Placa" en la página
3. DevTools mostrará el HTML resaltado

**Ejemplo de lo que verás:**
```html
<input 
  name="txtNumeroPlaca" 
  id="txtNumeroPlaca" 
  class="form-control" 
  type="text" 
  placeholder="Número de Placa"
>
```

**Anota en tu documento:**
- [ ] Selector por NAME: `input[name="txtNumeroPlaca"]`
- [ ] Selector por ID: `#txtNumeroPlaca`
- [ ] ¿Cuál funciona mejor? ___________

#### PASO 2.3: Encontrar botón consultar

1. Click en icono Inspect Element (↗️)
2. Click en botón "Consultar" o "Buscar"
3. Anotar el selector

**Ejemplo:**
```html
<button type="submit" class="btn btn-primary">Consultar</button>
```

**Anota:**
- [ ] Selector botón: `_________________`

#### PASO 2.4: Probar con placa real

1. Ingresa una placa de prueba (ej: "ABC123")
2. Click en "Consultar"
3. Espera resultados
4. Inspecciona la tabla de resultados

**Anota estructura de resultados:**
```html
<table class="table table-striped">
  <tr>
    <td>Marca</td>
    <td>MAZDA</td>
  </tr>
  <tr>
    <td>Modelo</td>
    <td>2023</td>
  </tr>
</table>
```

**Anota:**
- [ ] Selector tabla: `_________________`
- [ ] ¿Usa <table> o <div>? ___________
- [ ] ¿Hay CAPTCHA? Sí/No

#### PASO 2.5: Capturar screenshots

```bash
mkdir -p /tmp/runt_inspeccion

# Capturas requeridas:
[ ] /tmp/runt_inspeccion/01_pagina_inicial.png
[ ] /tmp/runt_inspeccion/02_devtools_campo_placa.png
[ ] /tmp/runt_inspeccion/03_devtools_boton_consultar.png
[ ] /tmp/runt_inspeccion/04_resultados.png
```

---

### ✅ TAREA 3: Inspeccionar SIMIT (45 min)

#### PASO 3.1: Encontrar URL real

**Problema:** La URL principal de Fiscalía no tiene el enlace directo.

**Pasos:**
1. Ir a: https://www.fiscalia.gov.co/
2. Buscar enlaces con: "Consultas", "SIMIT", "Comparendos"
3. Navegar hasta encontrar el formulario

**Anota:**
- [ ] URL real encontrada: ______________________
- [ ] Ruta navegada: Menú → ________ → ________

#### PASO 3.2: Inspeccionar formulario

Similar a RUNT:

**Anota:**
- [ ] Selector campo cédula: `_________________`
- [ ] Selector botón consultar: `_________________`
- [ ] Selector resultados: `_________________`
- [ ] ¿Hay CAPTCHA? Sí/No

#### PASO 3.3: Probar con documento real

```bash
# Documento de prueba
1022394742
```

**Anota:**
- [ ] ¿Retorna multas? Sí/No
- [ ] ¿Dice "Paz y Salvo"? Sí/No

#### PASO 3.4: Capturar screenshots

```bash
mkdir -p /tmp/simit_inspeccion

[ ] /tmp/simit_inspeccion/01_formulario.png
[ ] /tmp/simit_inspeccion/02_devinputs.png
[ ] /tmp/simit_inspeccion/03_resultados.png
```

---

### ✅ TAREA 4: Actualizar scrapers (30 min)

#### PASO 4.1: Actualizar RUNT scraper

**Archivo:** `/home/ubuntu/LABORATORIO/sarlaft-modern/backend/app/scrapers/runt_scraper.py`

**Buscar líneas 90-95:**
```python
selectores_placa = [
    'input[name="numeroPlaca"]',      # ← REEMPLAZAR ESTO
    'input[placeholder*="placa"]',     # ← REEMPLAZAR ESTO
    'input[id*="placa"]',              # ← REEMPLAZAR ESTO
    '#placa'                           # ← REEMPLAZAR ESTO
]
```

**Reemplazar con selectores REALES:**
```python
selectores_placa = [
    'input[name="NOMBRE_REAL"]',       # ← PON EL NAME REAL
    '#ID_REAL',                        # ← PON EL ID REAL
    'input[placeholder="TEXTO_REAL"]'  # ← PON EL PLACEHOLDER REAL
]
```

**Importante:** Poner primero el selector que funcionó mejor en tu inspección.

#### PASO 4.2: Actualizar botón RUNT

**Buscar líneas 120-125:**
```python
selectores_boton = [
    'button[type="submit"]',
    'button:has-text("Consultar")',
    'input[type="submit"]',
    'button:has-text("Buscar")'
]
```

**Reemplazar con selector REAL que encontraste.**

#### PASO 4.3: Actualizar SIMIT scraper

**Archivo:** `/home/ubuntu/LABORATORIO/sarlaft-modern/backend/app/scrapers/simit_scraper.py`

**Buscar líneas 82-88:**
```python
selectores_input = [
    'input[placeholder*="placa"]',
    'input[placeholder*="documento"]',
    'input[name*="documento"]',
    'input#txtConsulta',
    'input[type="text"]'
]
```

**Reemplazar con selectores REALES.**

**Buscar líneas 109-115:**
```python
selectores_boton = [
    'button[type="submit"]',
    'button#btnConsultar',
    'span:has-text("Consultar")',
    'i.fa-search',
    'button:has-text("Consultar")'
]
```

**Reemplazar con selectores REALES.**

---

### ✅ TAREA 5: Probar con datos reales (30 min)

#### PASO 5.1: Test RUNT

```bash
cd /home/ubuntu/LABORATORIO/sarlaft-modern/backend/app/scrapers

python3 -c "
import asyncio
from runt_scraper import RUNTScraper

async def test():
    scraper = RUNTScraper()
    resultado = await scraper.consultar_vehiculo('ABC123')
    print(resultado)

asyncio.run(test())
"
```

**Verificar:**
- [ ] No muestra error "No se encontró campo de placa"
- [ ] Retorna `{"status": "EXITOSO", "metodo": "PLAYWRIGHT_SCRAPING"}`
- [ ] Datos no son genéricos (marca, modelo reales)

#### PASO 5.2: Test SIMIT

```bash
python3 -c "
import asyncio
from simit_scraper import SIMITScraper

async def test():
    scraper = SIMITScraper()
    resultado = await scraper.consultar_multas('1022394742')
    print(resultado)

asyncio.run(test())
"
```

**Verificar:**
- [ ] No muestra error "No se encontró campo de búsqueda"
- [ ] Retorna estado real (LIMPIO o ALERTA)

#### PASO 5.3: Test API completo

```bash
curl -X POST https://sarlaf.agentesia.cloud/api/v1/auditar \
  -H "Content-Type: application/json" \
  -d '{
    "placa": "PLACA_REAL",
    "cedula": "1022394742",
    "client_id": "test",
    "tipo_consulta": "SARLAFT_CDA"
  }' | jq '.runt, .simit'
```

**Verificar en respuesta JSON:**
- [ ] `runt.metodo` = "PLAYWRIGHT_SCRAPING" (no "HYBRID_SMART_FAILOVER")
- [ ] `simit.metodo` = "PLAYWRIGHT_SCRAPING" (no "HYBRID_SMART_FAILOVER")

---

### ✅ TAREA 6: Documentar hallazgos (15 min)

#### CREAR archivo de documentación:

```bash
nano /home/ubuntu/LABORATORIO/sarlaft-modern/INSPECCION_RUNT_COMPLETA.md
```

**Contenido:**

```markdown
# INSPECCIÓN RUNT - 2026-05-17

## URL
https://www.runt.gov.co/consultaCiudadana/consultaVehiculo

## SELECTORES ENCONTRADOS

### Campo Placa:
- **Por NAME:** `input[name="NOMBRE_REAL"]`
- **Por ID:** `#ID_REAL`
- **Mejor opción:** `___________`

### Botón Consultar:
- **Selector:** `___________`

### Resultados:
- **Estructura:** `<table>` / `<div>` / `___________`
- **Selector:** `___________`

## CAPTCHA
- [ ] Sí / No
- Tipo: ___________

## PRUEBAS
- Placa ABC123: ¿Funcionó? Sí/No
- Placa XYZ987: ¿Funcionó? Sí/No
- Placa DEF456: ¿Funcionó? Sí/No

## SCREENSHOTS
- [ ] /tmp/runt_inspeccion/01_pagina_inicial.png
- [ ] /tmp/runt_inspeccion/02_devtools_campo_placa.png
- [ ] /tmp/runt_inspeccion/03_resultados.png
```

**Repetir para SIMIT:**
```bash
nano /home/ubuntu/LABORATORIO/sarlaft-modern/INSPECCION_SIMIT_COMPLETA.md
```

---

## ✅ CHECKLIST FINAL

Antes de dar por completada la tarea:

### RUNT:
- [ ] Selectores CSS encontrados y documentados
- [ ] Scraper actualizado con selectores reales
- [ ] Probado con 3 placas diferentes
- [ ] Retorna datos reales (no HYBRID_SMART_FAILOVER)
- [ ] Screenshots guardados
- [ ] Documentación creada

### SIMIT:
- [ ] URL real de consulta encontrada
- [ ] Selectores CSS encontrados y documentados
- [ ] Scraper actualizado con selectores reales
- [ ] Probado con 3 documentos diferentes
- [ ] Retorna datos reales
- [ ] Screenshots guardados
- [ ] Documentación creada

### VERIFICACIÓN API:
- [ ] Test CURL ejecutado
- [ ] Respuesta JSON muestra "PLAYWRIGHT_SCRAPING"
- [ ] Datos son reales (no genéricos)
- [ ] Tiempo respuesta < 30 segundos

---

## 🚀 EJECUCIÓN INMEDIATA

### Orden de ejecución:

1. **Tarea 1:** Preparar entorno (5 min)
2. **Tarea 2:** Inspeccionar RUNT (45 min)
3. **Tarea 3:** Inspeccionar SIMIT (45 min)
4. **Tarea 4:** Actualizar scrapers (30 min)
5. **Tarea 5:** Probar con datos reales (30 min)
6. **Tarea 6:** Documentar (15 min)

**Total:** 3 horas

---

## 📞 SI ENCUENTRAS PROBLEMAS

### El sitio no responde:
- Intenta otro navegador (Firefox)
- Verifica conexión a internet
- Verifica si el sitio está caído

### No encuentras el campo:
- Presiona Ctrl+F en DevTools HTML
- Busca: "placa", "consultar", "buscar"
- Toca el elemento y observa qué se resalta

### El scraper no funciona:
- Verifica Playwright instalado: `playwright --version`
- Revisa logs: `tail -f /tmp/scrapers.log`
- Haz screenshots del error

---

## ✅ CRITERIO DE ÉXITO

La tarea está **COMPLETA** cuando:

1. ✅ RUNT scraper extrae datos reales con 2+ placas
2. ✅ SIMIT scraper extrae datos reales con 2+ documentos
3. ✅ API responde con `"metodo": "PLAYWRIGHT_SCRAPING"`
4. ✅ Todos los selectores documentados
5. ✅ Screenshots guardados
6. ✅ Documentación creada

---

**¿LISTO PARA COMENZAR?**

**EMPIEZA POR LA TAREA 1** ↑↑↑

---

**Recuerda:** Toma screenshots de TODO. Si algo no funciona, documenta el error con screenshot.
