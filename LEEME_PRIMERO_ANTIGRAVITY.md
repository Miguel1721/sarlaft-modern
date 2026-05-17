# 🚀 INSTRUCCIONES PARA ANTIGRAVITY - LLEVAR SISTEMA AL 100%

**Fecha:** Mayo 17, 2026
**Tiempo total:** 2-3 horas
**Objetivo:** Encontrar selectores CSS reales de RUNT y SIMIT

---

## 📋 QUÉ NECESITAS HACER

El sistema SARLAFT funciona con **Hybrid Smart Failover**: retorna datos simulados cuando el scraping falla. Tu trabajo es hacerlo funcionar al **100%** con datos reales.

### Estado actual: 95% ✅
- Scrapers creados ✅
- Conectores implementados ✅
- API funcionando ✅

### Lo que falta: 5% ❌
- Selectores CSS reales ❌
- Pruebas con datos reales ❌

---

## 🎯 TUS TAREAS (EN ORDEN)

### ✅ TAREA 1: Preparar entorno (5 min)

```bash
# 1. Instalar dependencias
cd /home/ubuntu/LABORATORIO/sarlaft-modern/backend
pip3 install playwright rapidfuzz
playwright install chromium

# 2. Verificar instalación
python3 -c "import playwright; print('✅ Playwright OK')"

# 3. Abrir Chrome para inspección manual
google-chrome https://www.runt.gov.co/consultaCiudadana/consultaVehiculo &
```

---

### ✅ TAREA 2: Inspeccionar RUNT (45 min)

#### PASO 1: Abrir DevTools
- Presiona **F12** en Chrome
- Click en icono "Inspect Element" (↗️ arriba a la izquierda)

#### PASO 2: Encontrar campo de placa

1. Click en icono Inspect Element (↗️)
2. Click en el campo "Número de Placa"
3. DevTools mostrará el HTML resaltado

**Verás algo así:**
```html
<input name="txtNumeroPlaca" id="txtNumeroPlaca" class="form-control">
```

**Anota estos selectores:**
- `input[name="txtNumeroPlaca"]` ← Selector por NAME
- `#txtNumeroPlaca` ← Selector por ID

#### PASO 3: Encontrar botón consultar

1. Click en icono Inspect Element (↗️)
2. Click en botón "Consultar"
3. Anotar el selector

**Ejemplo:**
- `button[type="submit"]` o `button.btn-primary`

#### PASO 4: Probar con placa real

1. Ingresa placa: `ABC123`
2. Click en "Consultar"
3. Espera resultados
4. Inspecciona la tabla de resultados

**Anota:**
- ¿Usa `<table>` o `<div>`?
- Selector de la tabla: `table.table-striped`

#### PASO 5: Capturar screenshots

```bash
mkdir -p /tmp/runt_inspeccion

# En Chrome, presiona F12 y toma screenshots de:
# 1. Página inicial
# 2. Campo de placa seleccionado en DevTools
# 3. Botón consultar seleccionado en DevTools
# 4. Resultados cargados
```

---

### ✅ TAREA 3: Inspeccionar SIMIT (45 min)

#### PASO 1: Encontrar URL real

1. Ir a: https://www.fiscalia.gov.co/
2. Buscar: "Consultas" → "SIMIT" o "Comparendos"
3. Anotar URL real del formulario

**Anota:**
- URL encontrada: ____________________

#### PASO 2: Inspeccionar formulario

Igual que RUNT:
- Campo de cédula: anotar selector
- Botón consultar: anotar selector
- Resultados: anotar selector

#### PASO 3: Probar con documento

```bash
# Documento de prueba
1022394742
```

**Anota:**
- ¿Retorna multas? Sí/No
- ¿Dice "Paz y Salvo"? Sí/No

#### PASO 4: Capturar screenshots

```bash
mkdir -p /tmp/simit_inspeccion
# Tomar screenshots del proceso
```

---

### ✅ TAREA 4: Probar selectores rápidamente (opcional)

```bash
cd /home/ubuntu/LABORATORIO/sarlaft-modern/backend/app/scrapers

# Ejecutar probador de selectores
python3 probar_selectores.py

# Seleccionar:
# - Opción 1: Probar RUNT
# - Opción 2: Probar SIMIT

# El script probará selectores automáticamente y te mostrará
# cuáles funcionan y cuáles no
```

---

### ✅ TAREA 5: Actualizar scrapers (30 min)

#### Archivo RUNT:
`/home/ubuntu/LABORATORIO/sarlaft-modern/backend/app/scrapers/runt_scraper.py`

**Buscar líneas 90-95:**
```python
selectores_placa = [
    'input[name="numeroPlaca"]',      # ← REEMPLAZAR ESTO
    'input[placeholder*="placa"]',     # ← CON SELECTOR REAL
    'input[id*="placa"]',              # ← QUE ENCONTRASTE
    '#placa'
]
```

**Reemplazar con selectores REALES que encontraste:**
```python
selectores_placa = [
    'input[name="txtNumeroPlaca"]',  # ← EJEMPLO (pon el real)
    '#txtNumeroPlaca',                # ← EJEMPLO (pon el real)
]
```

**Importante:** Poner primero el selector que mejor funcionó.

**Hacer lo mismo con el botón (líneas 120-125).**

#### Archivo SIMIT:
`/home/ubuntu/LABORATORIO/sarlaft-modern/backend/app/scrapers/simit_scraper.py`

**Buscar líneas 82-88 y reemplazar con selectores REALES.**

---

### ✅ TAREA 6: Probar con datos reales (30 min)

#### Test RUNT:

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

**Lo que debe pasar:**
- ✅ Retorna: `{"status": "EXITOSO", "metodo": "PLAYWRIGHT_SCRAPING"}`
- ✅ NO retorna: `"HYBRID_SMART_FAILOVER"` (eso es failover)

#### Test SIMIT:

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

#### Test API completo:

```bash
curl -X POST https://sarlaf.agentesia.cloud/api/v1/auditar \
  -H "Content-Type: application/json" \
  -d '{
    "placa": "ABC123",
    "cedula": "1022394742",
    "client_id": "test",
    "tipo_consulta": "SARLAFT_CDA"
  }' | jq '.runt, .simit'
```

**Verificar en la respuesta:**
- `runt.metodo` = "PLAYWRIGHT_SCRAPING" ✅
- `simit.metodo` = "PLAYWRIGHT_SCRAPING" ✅

Si dice `"HYBRID_SMART_FAILOVER"`, significa que el scraping falló.

---

### ✅ TAREA 7: Documentar hallazgos (15 min)

#### CREAR archivo de RUNT:

```bash
nano /home/ubuntu/LABORATORIO/sarlaft-modern/INFORME_RUNT.md
```

**Contenido:**
```markdown
# INFORME INSPECCIÓN RUNT

## URL
https://www.runt.gov.co/consultaCiudadana/consultaVehiculo

## SELECTORES ENCONTRADOS

### Campo Placa:
- NAME: `input[name="txtNumeroPlaca"]`
- ID: `#txtNumeroPlaca`
- Mejor opción: `input[name="txtNumeroPlaca"]`

### Botón Consultar:
- Selector: `button[type="submit"]`

### Resultados:
- Estructura: `<table class="table table-striped">`
- Selector: `table.table-striped`

## CAPTCHA
- No tiene

## PRUEBAS
- Placa ABC123: ✅ Funcionó
- Placa XYZ987: ✅ Funcionó
- Placa DEF456: ✅ Funcionó

## SCREENSHOTS
- /tmp/runt_inspeccion/
```

**Repetir para SIMIT:**
```bash
nano /home/ubuntu/LABORATORIO/sarlaft-modern/INFORME_SIMIT.md
```

---

## ✅ CHECKLIST FINAL

Antes de terminar, verifica:

- [ ] RUNT: Selectores encontrados y probados
- [ ] RUNT: Scraper actualizado
- [ ] RUNT: Test con 3 placas funcionó
- [ ] SIMIT: Selectores encontrados y probados
- [ ] SIMIT: Scraper actualizado
- [ ] SIMIT: Test con 3 documentos funcionó
- [ ] API responde con "PLAYWRIGHT_SCRAPING"
- [ ] Informes creados (INFORME_RUNT.md y INFORME_SIMIT.md)
- [ ] Screenshots guardados

---

## 📚 DOCUMENTACIÓN ADICIONAL

Si necesitas más detalles, consulta:

- **GUÍA COMPLETA:** `/home/ubuntu/LABORATORIO/sarlaft-modern/CHECKLIST_ANTIGRAVITY.md`
- **GUÍA VISUAL:** `/home/ubuntu/LABORATORIO/sarlaft-modern/GUIA_VISUAL_INSPECCION.md`
- **INSTRUCCIONES DETALLADAS:** `/home/ubuntu/LABORATORIO/sarlaft-modern/INSTRUCCIONES_ANTIGRAVITY_PASO_A_PASO.md`

---

## 🆘 SI ENCUENTRAS PROBLEMAS

### El sitio no responde:
- Intenta otro navegador (Firefox)
- Verifica tu conexión a internet

### No encuentras el campo:
- Presiona Ctrl+F en DevTools
- Busca: "placa", "consultar"
- El HTML se resaltará cuando lo encuentres

### El scraper no funciona:
- Verifica que Playwright está instalado
- Revisa los screenshots en `/tmp/`
- Documenta el error con screenshot

---

## ✅ CRITERIO DE ÉXITO

La tarea está **COMPLETA** cuando:

1. ✅ RUNT extrae datos reales (no genéricos)
2. ✅ SIMIT extrae datos reales (no genéricos)
3. ✅ API responde `"metodo": "PLAYWRIGHT_SCRAPING"`
4. ✅ Todo documentado en informes

---

## 🚀 EMPEZAR AHORA

**Sigue las tareas en orden:**
1. Preparar entorno
2. Inspeccionar RUNT
3. Inspeccionar SIMIT
4. Probar selectores
5. Actualizar scrapers
6. Probar con datos reales
7. Documentar

**Tiempo total: 2-3 horas**

---

**¿LISTO? EMPIEZA POR LA TAREA 1** ↑↑↑

---

**Recuerda:** Toma screenshots de TODO. Si algo no funciona, documenta el error.

**Buena suerte! 🚀**
