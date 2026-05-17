# 🎨 GUÍA VISUAL - ENCONTRAR SELECTORES CSS PASO A PASO

**Para:** antigravity (o persona que hará inspección web)
**Objetivo:** Encontrar selectores CSS exactos de RUNT y SIMIT

---

## 🖥️ CONFIGURACIÓN INICIAL

### **PASO 1: Abrir DevTools**

Opción A: Teclado
- Presionar **F12**

Opción B: Menú
- Click derecho en cualquier parte de la página
- Seleccionar "Inspeccionar" o "Inspeccionar elemento"

Opción C: Chrome Menu
- Click en los 3 puntos verticales (⋮) arriba a la derecha
- More Tools → Developer Tools

**Asegúrate de ver el panel de DevTools abierto en la parte inferior o derecha del navegador.**

---

## 🔍 RUNT - EJEMPLO VISUAL DETALLADO

### **PASO 1: Navegar a RUNT**

```bash
# Abrir en navegador
google-chrome https://www.runt.gov.co/consultaCiudadana/consultaVehiculo
```

### **PASO 2: Activar herramienta de inspección**

En DevTools, click en el icono que parece una flechita ↗️ (Inspect Element)

### **PASO 3: Encontrar campo de placa**

**Mover el mouse sobre el campo de placa** hasta que el elemento se resalte en azul en la página.

Click en el campo.

**DevTools mostrará algo así:**

```html
<input 
  name="txtNumeroPlaca" 
  id="txtNumeroPlaca" 
  class="form-control form-control-sm" 
  type="text" 
  placeholder="Número de Placa"
  maxlength="6"
  minlength="6"
>
```

### **SELECTORES A ANOTAR:**

Copia estos selectores:

1. **Por ID:** `#txtNumeroPlaca`
2. **Por name:** `input[name="txtNumeroPlaca"]`
3. **Por clase:** `.form-control` (puede haber varios)
4. **Por placeholder:** `input[placeholder="Número de Placa"]`

**RECOMENDACIÓN:** Usar el **más específico posible**

```python
# ✅ MEJOR (por ID si es único)
await page.query_selector('#txtNumeroPlaca')

# ✅ BUENO (por name)
await page.query_selector('input[name="txtNumeroPlaca"]')

# ⚠️ PUEDE CONFUNDIR (hay muchos .form-control)
await page.query_selector('.form-control')
```

### **PASO 4: Encontrar botón consultar**

Misma técnica:
1. Click en icono Inspect Element ↗️
2. Click en el botón "Consultar"
3. Anotar el selector

**Ejemplo probable:**

```html
<button 
  type="submit" 
  class="btn btn-primary btn-lg"
  id="btnConsultar"
>
  Consultar
</button>
```

**Selector:** `button[type="submit"]` o `#btnConsultar`

### **PASO 5: Encontrar tabla de resultados**

Después de consultar y esperar resultados:

1. Inspeccionar una celda de la tabla con datos
2. DevTools mostrará:

```html
<table class="table table-striped table-bordered">
  <thead>
    <tr>
      <th>PLACA</th>
      <th>MARCA</th>
      <th>LÍNEA</th>
      <th>MODELO</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>ABC123</td>
      <td>MAZDA</td>
      <td>2</td>
      <td>2023</td>
    </tr>
  </tbody>
</table>
```

**Selectores útiles:**

```python
# Tabla completa
tabla = await page.query_selector('table.table-striped')

# Todas las filas
filas = await tabla.query_selector_all('tr')

# Primera fila de datos (después de headers)
primera_fila = filas[1]  # [0] es el header

# Celdas de la primera fila
celdas = await primera_fila.query_selector_all('td')

# Extraer texto
marca = await celdas[1].inner_text()  # Segunda celda
modelo = await celdas[3].inner_text()  # Cuarta celda
```

---

## 🔍 SIMIT - EJEMPLO VISUAL DETALLADO

### **PASO 1: Encontrar URL de consulta**

**Ir a:** https://www.fiscalia.gov.co/

**Buscar enlaces con estas palabras:**
- Consultas
- Consulta Ciudadana
- SIMIT
- Comparendos
- Citaciones

**Probable ruta:** Menú → Servicios → Consultas → SIMIT

**Ejemplo URL probable:**
```
https://www.fiscalia.gov.co/simit/consulta
```

### **PASO 2: Inspeccionar campo de documento**

Similar a RUNT:

```html
<input 
  name="numeroDocumento" 
  id="numDoc" 
  class="form-control" 
  type="text" 
  placeholder="Número de Documento"
>
```

### **PASO 3: Inspeccionar resultados de multas**

SIMIT típicamente muestra una tabla como:

```html
<table class="table">
  <thead>
    <tr>
      <th>NÚMERO COMPARENDO</th>
      <th>FECHA</th>
      <th>INFRACCIÓN</th>
      <th>VALOR</th>
      <th>ESTADO</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>2023-12345</td>
      <td>2023-05-17</td>
      <td>Exceso de velocidad</td>
      <td>$450,000</td>
      <td>PENDIENTE</td>
    </tr>
  </tbody>
</table>
```

**Selector:** `table.table`

**Extracción:**
```python
tabla = await page.query_selector('table')
filas = await tabla.query_selector_all('tbody tr')

multas = []
for fila in filas:
    celdas = await fila.query_selector_all('td')
    
    multa = {
        "numero_comparendo": await celdas[0].inner_text(),
        "fecha": await celdas[1].inner_text(),
        "infraccion": await celdas[2].inner_text(),
        "valor": await celdas[3].inner_text(),
        "estado": await celdas[4].inner_text()
    }
    
    multas.append(multa)
```

---

## 🎨 TÉCNICAS AVANZADAS DE SELECCIÓN

### **Técnica 1: Get by text (más robusto)**

```python
# En lugar de selector CSS
boton = await page.query_selector('button[type="submit"]')

# Usar búsqueda por texto
boton = await page.get_by_text('Consultar')
```

### **Técnica 2: XPath (para casos difíciles)**

```python
# Cuando los selectores CSS no funcionan

# Buscar elemento que contenga texto
xpath = '//input[contains(@placeholder, "Placa")]'
element = await page.xpath(xpath)

# Buscar por índice
xpath = '//table/tr[2]/td[1]'  # Segunda fila, primera celda
element = await page.xpath(xpath)
```

### **Técnica 3: Selector combinado**

```python
# Usar múltiples selectores como fallback
selectores = [
    'input[name="txtNumeroPlaca"]',  # Opción 1
    '#txtNumeroPlaca',                  # Opción 2
    'input[placeholder*="Placa"]',     # Opción 3
]

for selector in selectores:
    elemento = await page.query_selector(selector)
    if elemento:
        print(f"✅ Encontrado con: {selector}")
        break
```

---

## 📸 CAPTURANDO EVIDENCIA

### **Screenshots obligatorios:**

```bash
# Crear carpeta
mkdir -p /tmp/inspeccion_sarlaft

# Capturas de RUNT
[ ] RUNT_01_pagina_inicial.png          # Antes de ingresar datos
[ ] RUNT_02_ingresando_placa.png        # Después de ingresar placa
[ ] RUNT_03_resultados_cargados.png     # Tabla visible
[ ] RUNT_04_devtools_inspeccion.png     # DevTools abierto
[ ] RUNT_05_selector_resaltado.png     # Elemento seleccionado

# Capturas de SIMIT
[ ] SIMIT_01_pagina_consulta.png       # Página de consulta
[ ] SIMIT_02_ingresando_documento.png  # Después de ingresar cédula
[ ] SIMIT_03_resultados.png           # Multas (si las hay)
```

**Cómo tomar screenshot desde DevTools:**
1. Abre DevTools (F12)
2. Click en la pestaña "Device Toolbar" (ícono de celular/tablet arriba a la izquierda)
3. Click en icono de cámara 📸
4. Guarda en `/tmp/inspeccion_sarlaft/`

---

## 🧪 PRUEBAS CON CÓDIGO

### **Test 1: Verificar que Playwright puede encontrar el campo**

```python
import asyncio
from playwright.async_api import async_playwright

async def test_runt():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        
        # Navegar
        await page.goto("https://www.runt.gov.co/consultaCiudadana/consultaVehiculo")
        
        # Intentar encontrar campo por diferentes métodos
        metodos = [
            'input[name="txtNumeroPlaca"]',
            '#txtNumeroPlaca',
            'input[placeholder*="Placa"]',
            'input.form-control',  # CUIDADO: puede haber varios
        ]
        
        for metodo in metodos:
            try:
                elemento = await page.query_selector(metodo)
                if elemento:
                    print(f"✅ ENCONTRADO con: {metodo}")
                    
                    # Intentar escribir
                    await elemento.fill("ABC123")
                    print(f"✅ ESCRITURA funcionó")
                    
                    await browser.close()
                    return
            except:
                continue
        
        print("❌ NO SE PUDO ENCONTRAR EL CAMPO")
        await browser.close()

asyncio.run(test_runt())
```

### **Test 2: Verificar extracción de tabla**

```python
async def test_extraccion_tabla():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        
        # Navegar y consultar
        await page.goto("https://www.runt.gov.co/...")
        # ... (ingresar datos y consultar)
        
        # Esperar tabla
        await page.wait_for_selector('table', timeout=10000)
        
        # Extraer datos
        tabla = await page.query_selector('table')
        filas = await tabla.query_selector_all('tr')
        
        print(f"Filas encontradas: {len(filas)}")
        
        for i, fila in enumerate(filas[:3]):  # Primeras 3 filas
            celdas = await fila.query_selector_all('td, th')
            textos = [await c.inner_text() for c in celdas]
            print(f"Fila {i}: {textos}")
        
        await browser.close()

asyncio.run(test_extraccion_tabla())
```

---

## 📝 PLANILLA DE DOCUMENTACIÓN

### **Para cada sitio web, completar:**

```markdown
# INSPECCIÓN: [NOMBRE SITIO]

## URL BASE
https://www.sitio.gov.co/

## URL CONSULTA
https://www.sitio.gov.co/consulta

## CAMPO PRINCIPAL

### Selector encontrado:
- **CSS:** `input[name="nombre_campo"]`
- **XPath:** `//input[@name="nombre_campo"]`
- **GetByText:** `page.get_by_text("Texto visible")`

### Prueba de selección:
```python
# ✅ Este código funciona:
element = await page.query_selector('input[name="nombre_campo"]')
await element.fill("VALOR_PRUEBA")
```

## BOTÓN CONSULTAR

### Selector encontrado:
- **CSS:** `button[type="submit"]`
- **GetByText:** `page.get_by_text("Consultar")`

### Prueba:
```python
# ✅ Funciona:
boton = await page.query_selector('button[type="submit"]')
await boton.click()
```

## RESULTADOS

### Estructura:
- ( ) Tabla
- ( ) Divs
- ( ) Lista de cards

### Selector contenedor:
`table.table-striped` o `#resultado`

### Campos extraídos:

| Campo | Selector | ¿Funciona? |
|-------|----------|------------|
| Campo1 | `td[headers="campo1"]` | ✅ / ❌ |
| Campo2 | `.clase-campo2` | ✅ / ❌ |

## CAPTCHA
- [ ] ¿Tiene? Sí/No
- [ ] Tipo: reCAPTCHA / hCaptcha / Imagen / Ninguno

## OBSERVACIONES
- ¿Carga rápido? Sí/No
- ¿Algún error? _____________
- ¿Bloquea tras N consultas? Sí/No

## SCREENSHOTS
- [ ] Ruta: `/tmp/inspeccion_sarlaft/`
- [ ] Archivos: _____________

## SELECTOR FINAL ACTUALIZADO

En el scraper, usar:

```python
# Campo input:
await page.query_selector('SELECTOR_REAL_ENCONTRADO')

# Botón:
await page.query_selector('SELECTOR_BOTON_ENCONTRADO')

# Resultados:
await page.query_selector('SELECTOR_RESULTADOS_ENCONTRADO')
```
```

---

## ✅ CHECKLIST DE ENTREGA

Antes de dar por terminada la inspección:

### **RUNT (CRÍTICO):**
- [ ] Selector campo placa encontrado y probado
- [ ] Selector botón consultar encontrado y probado
- [ ] Selector resultados encontrado y probado
- [ ] Extracción de datos probada con 2+ placas reales
- [ ] Scraper actualizado con selectores reales
- [ ] Test ejecutado exitosamente
- [ ] Documentación completa creada

### **SIMIT (CRÍTICO):**
- [ ] URL de consulta encontrada
- [ ] Selector campo documento encontrado y probado
- [ ] Selector botón consultar encontrado y probado
- [ ] Selector resultados encontrado y probado
- [ ] Extracción de datos probada con 2+ documentos reales
- [ ] Scraper actualizado con selectores reales
- [ ] Test ejecutado exitosamente
- [ ] Documentación completa creada

### **VERIFICACIÓN FINAL:**
- [ ] Test API muestra "PLAYWRIGHT_SCRAPING" (no "HYBRID_SMART_FAILOVER")
- [ ] Datos son reales (no genéricos)
- [ ] Tiempo respuesta < 30 segundos
- [ ] No hay errores en logs

---

## 🎯 EJECUCIÓN INMEDIATA

### **Orden de tareas:**

1. **ABRIR este archivo** (GUÍA VISUAL)
2. **ABRIR navegador Chrome**
3. **Navegar a RUNT**
4. **SEGUIR pasos uno por uno**
5. **DOCUMENTAR cada hallazgo**
6. **PROBAR selectores encontrados**
7. **ACTUALIZAR scraper**
8. **TESTEAR**
9. **REPETIR para SIMIT**

### **Tiempo estimado:**
- RUNT completo: 1.5 horas
- SIMIT completo: 1.5 horas
- Total: 3 horas

---

## 📞 AYUDA

### **Si no puedes encontrar un elemento:**

1. **Ctrl+F en el HTML:**
   - Abre DevTools
   - Presiona Ctrl+Shift+C (abre búsqueda)
   - Escribe parte del texto visible (ej: "Placa", "Consultar")
   - DevTools te llevará al elemento

2. **Usar XPath:**
   - Right click en elemento → Copy → Copy XPath
   - Pegar en código: `await page.xpath('PEGAR_AQUI')`

3. **Usar get_by_text:**
   - Más fácil pero menos preciso
   - `await page.get_by_text("Texto que ves en la página")`

### **Si el elemento está en iframe:**
- DevTools muestra `<iframe id="frameName">`
- Cambiar al iframe:
  ```python
  frame = page.frame('frameName')
  await frame.click('input[name="campo"]')
  ```

### **Si el contenido no aparece:**
- Espera más tiempo: `await page.wait_for_selector('table', timeout=30000)`
- Verifica si hay JavaScript: `await page.wait_for_load_state('networkidle')`

---

**¿ESTÁ LISTO PARA COMENZAR LA INSPECCIÓN?**

**RECUERDA:** Toma screenshots de TODO para poder documentar

**¿NECESITAS QUE TE ACOMPAÑE EN EL PROCESO?**
