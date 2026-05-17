# 📋 INSTRUCCIONES DETALLADAS PARA ANTIGRAVITY - INSPECCIÓN Y PRUEBAS REALES

**Objetivo:** Llevar el sistema de 95% a 100% completitud
**Fecha:** Mayo 17, 2026
**Duración estimada:** 2-4 horas

---

## 🎯 MISIÓN

Actualmente los conectores usan **Hybrid Smart Failover**, que retorna datos simulados cuando el scraping falla. Tu misión es:

1. **Inspeccionar cada página web** manualmente con DevTools
2. **Encontrar los selectores CSS exactos** de cada campo
3. **Actualizar los scrapers** con selectores reales
4. **Probar con datos reales** y verificar extracción

---

## 📋 SITIOS WEB A INSPECCIONAR (ORDEN DE PRIORIDAD)

### **PRIORIDAD ALTA (CRÍTICO PARA CDAs):**

1. **RUNT** - Registro Nacional Automotor
   - URL: https://www.runt.gov.co/consultaCiudadana/consultaVehiculo
   - Campo: Placa del vehículo
   - Datos: Marca, línea, modelo, propietario

2. **SIMIT** - Multas de tránsito
   - URL: https://www.fiscalia.gov.co/
   - **Tarea:** Encontrar enlace real de consulta SIMIT
   - Campo: Cédula ciudadana
   - Datos: Multas, valores, fechas

### **PRIORIDAD MEDIA (COMPLEMENTARIO):**

3. **Policía Nacional** - Certificado Judicial
   - URL: https://antecedentes.policia.gov.co:7005/WebJudicial/
   - Campo: Cédula ciudadana
   - Datos: Antecedentes judiciales

4. **OFAC** - Lista SDN (Ya funcional, solo verificar)
   - URL: https://sanctionssearch.ofac.treas.gov/
   - Verificar que API o scraping funcione

---

## 🔧 HERRAMIENTAS NECESARIAS

### **Navegadores:**
- Chrome/Chromium (recomendado) con DevTools
- Firefox Developer Tools (alternativa)

### **Extensiones útiles:**
- SelectorGadget (ayuda a encontrar selectores CSS)
- XPath Helper (para XPath queries)

---

## 📝 PROCEDIMIENTO PASO A PASO

### **FASE 1: RUNT (PRIORIDAD MÁXIMA)**

#### **PASO 1.1: Abrir RUNT en navegador**

```bash
# Abrir en Chrome/Chromium
google-chrome https://www.runt.gov.co/consultaCiudadana/consultaVehiculo
```

#### **PASO 1.2: Inspeccionar campo de placa**

1. Presiona **F12** para abrir DevTools
2. Click en icono "Inspect element" (flechita ↗️ arriba a la izquierda)
3. Click en el campo de "Número de placa" en la página
4. DevTools mostrará el HTML resaltado

**Tarea:** Documenta el selector exacto:

```html
<!-- EJEMPLO de lo que buscas (selecciona el elemento real) -->
<input name="txtNumeroPlaca" id="txtNumeroPlaca" class="form-control" type="text">
```

**Anota:**
- [ ] Selector CSS: `input[name="txtNumeroPlaca"]` o `#txtNumeroPlaca`
- [ ] ID del campo: `txtNumeroPlaca`
- [ ] Name del campo: `txtNumeroPlaca`
- [ ] ¿Tiene placeholder? Cuál: `_________________`

#### **PASO 1.3: Inspeccionar botón consultar**

1. En DevTools, click en icono "Inspect element"
2. Click en el botón "Consultar" o "Buscar"
3. Documenta el selector:

**Anota:**
- [ ] Selector CSS: `_____________________`
- [ ] Tipo: `button` o `input[type="submit"]`
- [ ] Texto visible: `_________________`

#### **PASO 1.4: Inspeccionar resultados**

1. Ingresa una placa de prueba (ej: "ABC123")
2. Click en "Consultar"
3. Espera a que carguen los resultados
4. Inspecciona la tabla o sección de resultados

**Anota estructura de resultados:**

```
[ ] ¿Cómo se muestran los resultados?
    - ( ) Tabla HTML: <table>
    - ( ) Divs: <div class="resultado">
    - ( ) Cards: <div class="card">
    - ( ) Otro: __________________

[ ] Selector del contenedor de resultados:
    _____________________________

[ ] Estructura de datos (ejemplo):
    - Marca: ¿En qué etiqueta está? ________
    - Línea: ¿En qué etiqueta está? ________
    - Modelo: ¿En qué etiqueta está? ________
    - Color: ¿En qué etiqueta está? ________
    - Propietario: ¿En qué etiqueta está? ________

[ ] ¿Hay gravámenes/siniestros?
    - ( ) Sí, en tabla separada
    - ( ) Sí, en misma tabla
    - ( ) No visible
```

#### **PASO 1.5: Verificar si hay CAPTCHA**

**Anota:**
- [ ] ¿Hay CAPTCHA antes de consultar?
    - ( ) Sí: reCAPTCHA v2
    - ( ) Sí: hCaptcha
    - ( ) Sí: CAPTCHA de imagen
    - ( ) No

- [ ] ¿Hay CAPTCHA después de consultar?
    - ( ) Sí
    - ( ) No

#### **PASO 1.6: Capturar screenshots**

```bash
# Crear carpeta para screenshots
mkdir -p /tmp/runt_inspeccion

# Capturas a tomar:
[ ] Página inicial (antes de ingresar datos)
[ ] Después de ingresar placa
[ ] Después de click en consultar
[ ] Resultados cargados
[ ] Inspección de campo de placa
[ ] Inspección de tabla de resultados
```

#### **PASO 1.7: Probar con 3 placas diferentes**

```bash
# Placas para probar:
1. ABC123 (placa normal)
2. XYZ987 (otra placa)
3. DEF456 (tercera placa)

# Anota resultados:
[ ] Placa 1: ¿Se encontró? Sí/No
[ ] Placa 2: ¿Se encontró? Sí/No
[ ] Placa 3: ¿Se encontró? Sí/No
```

---

### **FASE 2: SIMIT (PRIORIDAD ALTA)**

#### **PASO 2.1: Encontrar URL real de consulta SIMIT**

**Tarea:** La URL principal de Fiscalía no tiene el enlace directo de SIMIT.

**Pasos:**
1. Ir a: https://www.fiscalia.gov.co/
2. Buscar enlaces que digan:
   - "Consultas"
   - "SIMIT"
   - "Comparendos"
   - "Multas"
   - "Citación"
3. Navegar por menús hasta encontrar el formulario

**Anota:**
- [ ] URL real de SIMIT: ________________________
- [ ] Ruta navegada: Menú → Submenú → Formulario

#### **PASO 2.2: Inspeccionar formulario SIMIT**

Seguir mismo procedimiento que RUNT:

**Anota:**
- [ ] Selector CSS campo cédula: `_________________`
- [ ] Selector CSS botón consultar: `_________________`
- [ ] ¿Hay CAPTCHA? Sí/No
- [ ] Tipo de CAPTCHA: _____________

#### **PASO 2.3: Inspeccionar resultados**

**Anota:**
```
[ ] Estructura de resultados:
    - ( ) Tabla con columnas: ________
    - ( ) Lista de cards
    - ( ) Otro: ____________

[ ] Campos extraídos:
    - Número comparendo: En etiqueta ________
    - Fecha: En etiqueta ________
    - Infracción: En etiqueta ________
    - Valor: En etiqueta ________
    - Estado: En etiqueta ________
```

#### **PASO 2.4: Probar con 3 documentos**

```bash
# Cédulas para probar:
1. 1022394742 (documento de prueba)
2. 1026575786 (otro documento)
3. Tercer documento real

# Anota resultados:
[ ] Doc 1: ¿Multas encontradas? 0 / ___
[ ] Doc 2: ¿Multas encontradas? 0 / ___
[ ] Doc 3: ¿Multas encontradas? 0 / ___
```

---

### **FASE 3: ACTUALIZAR SCRAPERS CON SELECTORES REALES**

#### **PASO 3.1: Actualizar RUNT scraper**

**Archivo:** `/home/ubuntu/LABORATORIO/sarlaft-modern/backend/app/scrapers/runt_scraper.py`

**Ubicar sección de selectores:**
```python
# Buscar estas líneas en el archivo (~línea 115-130):
async def _extraer_informacion(self, page: Page, placa: str) -> Dict:
```

**Reemplazar con selectores reales:**

```python
# ANTES (ejemplo - selectores genéricos):
input_placa = await page.query_selector('input[name="numeroPlaca"]')

# DESPUÉS (con selectores reales que encontraste):
input_placa = await page.query_selector('input[name="NOMBRE_REAL"]')
# O usar ID si es único:
input_placa = await page.query_selector('#ID_REAL')
```

**PASO 3.2: Actualizar extracción de datos**

Ubicar función `_extraer_por_label` y actualizar con etiquetas reales que encontraste:

```python
# ANTES:
info["vehiculo"]["marca"] = await self._extraer_por_label(page, "Marca")

# DESPUÉS (con etiquetas reales del HTML):
info["vehiculo"]["marca"] = await page._extraer_por_label(page, "MARCA_REAL")
```

#### **PASO 3.3: Actualizar SIMIT scraper**

Mismo proceso que RUNT pero con archivo:
`/home/ubuntu/LABORATORIO/sarlaft-modern/backend/app/scrapers/simit_scraper.py`

---

### **FASE 4: PRUEBAS REALES**

#### **PASO 4.1: Test RUNT con datos reales**

```bash
cd /home/ubuntu/LABORATORIO/sarlaft-modern/backend/app/scrapers

# Ejecutar test RUNT
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
- [ ] Retorna datos reales (no HYBRID_SMART_FAILOVER)
- [ ] Contiene marca, línea, modelo reales
- [ ] Tiempo de respuesta < 30 segundos

#### **PASO 4.2: Test SIMIT con datos reales**

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
- [ ] Retorna multas reales o "LIMPIO" correctamente
- [ ] Tiempo de respuesta < 30 segundos

#### **PASO 4.3: Test completo vía API**

```bash
# Test de integración completo
curl -X POST https://sarlaf.agentesia.cloud/api/v1/auditar \
  -H "Content-Type: application/json" \
  -d '{
    "placa": "PLACA_REAL",
    "cedula": "1022394742",
    "client_id": "test",
    "tipo_consulta": "SARLAFT_CDA"
  }'
```

**Verificar en la respuesta JSON:**
- [ ] `runt.metodo` = "PLAYWRIGHT_SCRAPING" (no "HYBRID_SMART_FAILOVER")
- [ ] `simit.metodo` = "PLAYWRIGHT_SCRAPING" (no "HYBRID_SMART_FAILOVER")
- [ ] Los datos son reales (no genéricos)

---

### **FASE 5: DOCUMENTACIÓN

#### **CREAR HOJA DE CÁLCULO**

Crear archivo con tus hallazgos:

```bash
nano /home/ubuntu/LABORATORIO/sarlaft-modern/INSPECCION_RUNT.md
```

**Contenido:**

```markdown
# INSPECCIÓN RUNT - FECHA: 2026-05-17

## URL
https://www.runt.gov.co/consultaCiudadana/consultaVehiculo

## SELECTORES ENCONTRADOS

### Campo Placa:
- **Selector CSS:** `input[name="txtNumeroPlaca"]`
- **ID:** `#txtNumeroPlaca`
- **Clase:** `.form-control`

### Botón Consultar:
- **Selector CSS:** `button[type="submit"]`
- **Texto:** "Consultar"

### Resultados:
- **Contenedor:** `#divResultado`
- **Estructura:** `<table class="table table-striped">`

### Campos de la tabla:
- **Marca:** `td[headers="marca"]`
- **Línea:** `td[headers="linea"]`
- **Modelo:** `td[headers="modelo"]`

## CAPTCHAS
- **¿Tiene?** Sí/No
- **Tipo:** _____________

## PRUEBAS REALIZADAS

### Placa ABC123:
- [ ] Se encontró: Sí/No
- [ ] Marca extraída: ________
- [ ] Línea extraída: ________

### Placa XYZ987:
- [ ] Se encontró: Sí/No
- [ ] Marca extraída: ________
- [ ] Línea extraída: ________

## SCREENSHOTS

- [ ] `/tmp/runt_inspeccion/01_pagina_inicial.png`
- [ ] `/tmp/runt_inspeccion/02_resultados.png`
- [ ] `/tmp/runt_inspeccion/03_inspeccion_campos.png`

## OBSERVACIONES

- ¿La página carga lento? Sí/No
- ¿Bloquea después de X consultas? Sí/No
- ¿Algún problema encontrado? _____________
```

---

## 🎯 ESTRUCTURA DE SELECTORES TÍPICOS

### **INPUTS DE FORMULARIO:**

Busca selectores como:
```html
<!-- Por name -->
<input name="campoTexto">

<!-- Por id -->
<input id="campoId">

<!-- Por clase -->
<input class="form-control input-lg">

<!-- Por placeholder -->
<input placeholder="Ingrese placa">

<!-- Múltiples atributos -->
<input name="txtPlaca" id="placa" class="form-control" type="text">
```

### **BOTONES:**

Busca selectores como:
```html
<!-- Por tipo -->
<button type="submit">

<!-- Por texto -->
<button>Consultar</button>

<!-- Por clase -->
<button class="btn btn-primary">

<!-- Múltiples -->
<button type="submit" class="btn btn-primary">Buscar</button>
```

### **TABLAS:**

Busca selectores como:
```html
<!-- Tabla -->
<table>
  <thead>
    <tr>
      <th>Marca</th>
      <th>Línea</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>MAZDA</td>
      <td>2</td>
    </tr>
  </tbody>
</table>

<!-- Selectores útiles -->
table                           # Toda la tabla
table tbody                     # Cuerpo de la tabla
tr                              # Fila
td                              # Celda
td:nth-child(1)                 # Primera celda
```

---

## ⚠️ PROBLEMAS COMUNES Y SOLUCIONES

### **Problema 1: Selectores dinámicos**

**Síntoma:** Los IDs cambian cada vez (ej: `txtPlaca_12345`)

**Solución:**
```python
# Usar selectores más robustos
# En lugar de:
await page.query_selector('#txtPlaca_12345')

# Usar:
await page.query_selector('input[name="placa"]')
# O
await page.get_by_text('Placa')
```

### **Problema 2: Contenido cargado con JavaScript**

**Síntoma:** La tabla aparece vacía al inspeccionar HTML

**Solución:**
```python
# Esperar a que el contenido aparezca
await page.wait_for_selector('table', timeout=10000)
await page.wait_for_load_state('networkidle')
```

### **Problema 3: Iframe**

**Síntoma:** El formulario está dentro de un iframe

**Solución:**
```python
# Cambiar al iframe
frame = page.frame('nombre_o_id_del_iframe')
await frame.click('input[name="campo"]')
```

### **Problema 4: CAPTCHA**

**Síntoma:** Bloquea con reCAPTCHA

**Solución:**
```python
# Documentar y usar Hybrid Smart Failover
# El sistema ya está preparado para esto
logger.warning("CAPTCHA detectado. Activando failover.")
```

---

## 📋 CHECKLIST FINAL

Antes de dar por completada la tarea, verifica:

### **RUNT:**
- [ ] Inspeccionado campo de placa
- [ ] Inspeccionado botón consultar
- [ ] Inspeccionado tabla de resultados
- [ ] Selectores documentados
- [ ] Scraper actualizado con selectores reales
- [ ] Probado con 3 placas diferentes
- [ ] Retornando datos reales (no HYBRID_SMART_FAILOVER)
- [ ] Screenshots guardados
- [ ] Documentación creada

### **SIMIT:**
- [ ] Encontrada URL real de consulta
- [ ] Inspeccionado campo de cédula
- [ ] Inspeccionado botón consultar
- [ ] Inspeccionados resultados
- [ ] Selectores documentados
- [ ] Scraper actualizado
- [ ] Probado con 3 documentos
- [ ] Retornando datos reales
- [ ] Screenshots guardados
- [ ] Documentación creada

### **VERIFICACIÓN API:**
- [ ] Test CURL exitoso
- [ ] Respuesta JSON no muestra "HYBRID_SMART_FAILOVER"
- [ ] Datos son reales (no genéricos)
- [ ] Tiempo de respuesta < 30 segundos

---

## 🚀 EJECUCIÓN

### **TIEMPO ESTIMADO:**
- RUNT: 1-2 horas
- SIMIT: 1-2 horas
- Pruebas: 30 minutos
- Total: 3-4 horas

### **ORDEN DE TRABAJO:**
1. RUNT inspección (45 min)
2. RUNT pruebas (15 min)
3. SIMIT inspección (45 min)
4. SIMIT pruebas (15 min)
5. Actualización scrapers (30 min)
6. Test completo API (15 min)
7. Documentación (30 min)

---

## 📞 SI ENCUENTRAS PROBLEMAS

### **El sitio web no responde:**
- Intenta otro navegador (Firefox)
- Verifica tu conexión a internet
- Verifica si el sitio está caído (downforeveryone.com)

### **No encuentras el campo:**
- Intenta búsqueda de texto Ctrl+F en DevTools HTML
- Busca palabras clave: "placa", "consultar", "buscar"
- Pide ayuda identificando el HTML

### **El scraper no funciona:**
- Verifica que Playwright está instalado: `playwright --version`
- Revisa los logs: `tail -f /tmp/scrapers.log`
- Haz screenshots del error

---

## ✅ CRITERIO DE ÉXITO

La tarea se considera COMPLETA cuando:

1. ✅ RUNT scraper extrae datos reales al menos con 2 placas diferentes
2. ✅ SIMIT scraper extrae datos reales al menos con 2 documentos
3. ✅ El método en JSON respuesta API dice "PLAYWRIGHT_SCRAPING" (no "HYBRID_SMART_FAILOVER")
4. ✅ Todos los selectores están documentados
5. ✅ Screenshots guardados de cada sitio
6. ✅ Documentación creada en `INSPECCION_RUNT.md`

---

**¿LISTO PARA COMENZAR LA INSPECCIÓN?**

**¿O NECESITAS ACLARACIONES ANTES DE EMPEZAR?**
