# 🚀 PARA ANTIGRAVITY - EJECUTAR AHORA

**Fecha:** Mayo 17, 2026
**Misión:** Ver con tus propios ojos qué pasa en RUNT y SIMIT
**Tiempo:** 1.5 - 2 horas

---

## 🎯 LO QUE TENEMOS QUE DESCUBRIR

El sistema actual:
- ✅ **NAVEGA** correctamente a RUNT y SIMIT
- ✅ **LLENA** los formularios correctamente
- ✅ **HACE CLICK** en los botones
- ❌ **NO EXTRAE** datos (encuentra 0 tablas)

**Tu misión:** Ver QUÉ PASA realmente después de hacer click en "Consultar"

---

## 📋 PASO 1: EJECUTAR EL OBSERVADOR EN VIVO

```bash
cd /home/ubuntu/LABORATORIO/sarlaft-modern/backend/app/scrapers
python3 observar_en_vivo.py
```

### Opción 1: "Observar RUNT en vivo"

Este script:
1. Abre Chrome visible con RUNT
2. Ingreso placa ABC123 automáticamente
3. Hago click en "Consultar Información"
4. **ESPERO 15 segundos para que TÚ observes**
5. Tomo screenshot
6. Te dejo investigar con DevTools

**Mientras se ejecuta:**
- Presiona **F12** para abrir DevTools
- Ve a la pestaña **"Network"** (Red)
- **OBSERVA qué pasa después del click:**
  - ¿Aparecen peticiones XHR/Fetch?
  - ¿Aparece una tabla con datos?
  - ¿Cuánto tarda en cargar?

### Opción 2: "Observar SIMIT en vivo"

Lo mismo pero para SIMIT con documento 1022394742

### Opción 3: "Investigar peticiones AJAX"

Captura todas las peticiones de red y te muestra cuáles hay

### Opción 4: "Modo libre"

Tú controlas el navegador, exploras a tu ritmo

---

## 📋 PASO 2: LO QUE DEBES ANOTAR

Crea este archivo mientras observas:

```bash
nano /home/ubuntu/LABORATORIO/sarlaft-modern/OBSERVACION_ANTIGRAVITY.md
```

**Contenido a llenar:**

```markdown
# OBSERVACIÓN - ANTIGRAVITY

## RUNT - Placa ABC123

### Después de hacer click en "Consultar":

1. ¿Aparecen datos VISIBLES en la página?
   - [ ] Sí, veo una tabla con datos del vehículo
   - [ ] No, no veo nada
   - [ ] Aparece un spinner de carga pero nunca muestra datos

2. Si aparecen datos, ¿en qué formato?
   - [ ] Tabla HTML (<table>)
   - [ ] Cards o divs
   - [ ] No aparecen

3. En DevTools → Network, ¿ves peticiones después del click?
   - [ ] Sí, URL: ___________
   - [ ] No, no veo peticiones nuevas

4. Si hay peticiones, ¿qué traen?
   - URL: ___________
   - Tipo de respuesta: JSON/HTML/XML/___________
   - Contiene datos: Sí/No

5. En DevTools → Elements, ¿ves los datos en el HTML?
   - [ ] Sí, selector del elemento: ___________
   - [ ] No, los datos NO están en el HTML

6. ¿Cuánto tiempo tarda en cargar?
   - ___ segundos

### SIMIT - Documento 1022394742

Mismas preguntas que arriba.

## CONCLUSIÓN

- [ ] Los datos están en HTML → Se pueden extraer con selectores
- [ ] Los datos vienen por AJAX → Se necesita interceptar petición
- [ ] Los datos NO aparecen → Usar fallback o buscar API

## SELECTORES ENCONTRADOS

RUNT:
- Input placa: input#mat-input-2
- Botón: button:has-text("Consultar Información")
- ¿Selector de datos?: ___________

SIMIT:
- Input documento: ___________
- Botón: ___________
- ¿Selector de datos?: ___________
```

---

## 📋 PASO 3: EVIDENCIA VISUAL

### Screenshots que debes tomar:

**RUNT:**
```bash
# Tomar desde el Chrome abierto
# Presiona F12 → pestaña "Elements" → selecciona un dato → PrintScreen

# Guardar como:
/tmp/runt_1_pagina_cargada.png
/tmp/runt_2_despues_click.png
/tmp/runt_3_devtools_elements.png
/tmp/runt_4_devtools_network.png
```

**SIMIT:**
```bash
/tmp/simit_1_pagina_cargada.png
/tmp/simit_2_despues_click.png
/tmp/simit_3_devtools_elements.png
/tmp/simit_4_devtools_network.png
```

---

## 🔍 LO QUE DEBES BUSCAR

### Si VES datos en la página:

1. **Click derecho en un dato** (ej: "MAZDA")
2. Click en "Inspeccionar"
3. **Anota el selector:**
   ```html
   <!-- Ejemplo de lo que verás -->
   <span class="marca">MAZDA</span>
   <!-- Selector: span.marca
   -->

   <mat-cell _ngcontent-c123>MAZDA</mat-cell>
   <!-- Selector: mat-cell
   -->

   <div class="vehiculo-data">MAZDA</div>
   <!-- Selector: div.vehiculo-data
   -->
   ```

### NO ves datos pero SÍ ves peticiones AJAX:

1. En DevTools → **Network**
2. Filtra por **"XHR"** o **"Fetch"**
3. Click en la petición
4. Ve a **"Response"**
5. **Anota:**
   - URL completa
   - Método (GET/POST)
   - Qué datos trae (JSON)

### NO ves NADA:

- Puede ser que la página esté bloqueando el scraper
- Puede ser que los datos tarden más de 15 segundos
- Puede ser que necesitemos una estrategia diferente

---

## ⏱️ TIEMPOS ESTIMADOS

- **Ejecutar observador RUNT:** 20 min
- **Ejecutar observador SIMIT:** 20 min
- **Investigar con DevTools:** 30 min
- **Documentar hallazgos:** 20 min

**Total:** 1.5 horas

---

## 🚀 EJECUCIÓN INMEDIATA

```bash
# PASO 1: Ir al directorio
cd /home/ubuntu/LABORATORIO/sarlaft-modern/backend/app/scrapers

# PASO 2: Ejecutar observador
python3 observar_en_vivo.py

# PASO 3: Seleccionar Opción 1 (RUNT)

# PASO 4: Seguir instrucciones en pantalla

# PASO 5: Repetir Opción 2 (SIMIT)

# PASO 6: Documentar en OBSERVACION_ANTIGRAVITY.md
```

---

## 📊 RESULTADO ESPERADO

Al terminar, debes poder responder:

1. **¿Los datos SON VISIBLES en el HTML después de consultar?**
   - Sí → Anota los selectores exactos
   - No → Anota las URLs de las peticiones AJAX

2. **¿QUÉ SELECTORES debo usar para extraer los datos?**
   - RUNT: ___________
   - SIMIT: ___________

3. **¿Hay peticiones AJAX que deba interceptar?**
   - RUNT: URL = ___________
   - SIMIT: URL = ___________

4. **Screenshots tomados:**
   - [ ] /tmp/runt_observacion_en_vivo.png
   - [ ] /tmp/simit_observacion_en_vivo.png

---

## ✅ CHECKLIST FINAL

Antes de terminar:

- [ ] Ejecuté `observar_en_vivo.py` para RUNT
- [ ] Ejecuté `observar_en_vivo.py` para SIMIT
- [ ] Abrí DevTools (F12) mientras se ejecutaba
- [ ] Observé la pestaña "Network"
- [ ] Observé la pestaña "Elements"
- [ ] Encontré los selectores de datos (o URLs de AJAX)
- [ ] Tomé screenshots
- [ ] Documenté todo en OBSERVACION_ANTIGRAVITY.md

---

## 📞 REPORTAR

Una vez tengas toda la información:

```bash
cat /home/ubuntu/LABORATORIO/sarlaft-modern/OBSERVACION_ANTIGRAVITY.md
```

Y me dices:

1. ¿Los datos están en el HTML o vienen por AJAX?
2. ¿Qué selectores debo usar?
3. ¿Qué necesitas cambiar en los scrapers?

---

**OBJETIVO:** VER para SABER, no adivinar.

**EMPIEZA AHORA:** `python3 observar_en_vivo.py`

**Buena suerte! 🚀**
