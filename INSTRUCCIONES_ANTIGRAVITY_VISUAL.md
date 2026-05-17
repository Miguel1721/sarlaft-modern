# 🔍 INSTRUCCIONES PARA ANTIGRAVITY - INVESTIGACIÓN VISUAL EN VIVO

**Objetivo:** Ver con tus propios ojos qué pasa en RUNT y SIMIT
**Método:** Observación real en navegador + DevTools
**Duración:** 1-2 horas

---

## 🎯 LO QUE DEBES HACER

### PASO 1: Abrir RUNT y OBSERVAR (30 min)

```bash
# Abrir Chrome en la página de RUNT
google-chrome https://www.runt.gov.co/consultaCiudadana/consultaVehiculo &
```

#### 1.1 Presiona F12 para abrir DevTools

#### 1.2 Click en pestaña "Network" (Red)

#### 1.3 Ingresa una placa de prueba: `ABC123`

#### 1.4 Click en "Consultar Información"

#### 1.5 **OBSERVA ATENTAMENTE:**

**A) ¿Aparece una tabla de resultados INMEDIATAMENTE?**
- Sí → Ve al paso 2
- No → ¿Aparece un spinner de carga? ¿Cuánto tiempo tarda?

**B) En la pestaña "Network" de DevTools:**
- ¿Ves peticiones XHR/Fetch después de hacer click?
- ¿Cuál es la URL de esas peticiones?
- ¿Qué respuesta traen (JSON, HTML, XML)?

**C) Cuando aparece la información:**
- ¿En qué FORMATO está? (Tabla, Cards, Divs)
- ¿Qué CLASS o ID tienen los elementos que contienen los datos?
- ¿Los datos están visibles en el HTML?

#### 1.6 Inspecciona un dato visible

1. Click derecho en un dato visible (ej: "MAZDA")
2. Click en "Inspeccionar"
3. **Anota TODO lo que veas:**
   ```html
   <!-- EJEMPLO de lo que buscarás -->
   <span class="marca-vehiculo">MAZDA</span>
   <!-- O -->
   <div _ngcontent-c123>MAZDA</div>
   <!-- O -->
   <mat-cell _ngcontent-c123>MAZDA</mat-cell>
   ```

**DOCUMENTA:**
- [ ] ¿La tabla aparece? Sí/No
- [ ] ¿Cuántos segundos tarda en aparecer? ___ seg
- [ ] ¿URL de petición AJAX (si existe): ___________
- [ ] ¿Selector de elemento con datos: ___________
- [ ] Screenshot del resultado: `/tmp/runt_visible.png`

---

### PASO 2: Abrir SIMIT y OBSERVAR (30 min)

```bash
# Abrir Chrome en SIMIT
google-chrome https://www.fcm.org.co/simit/ &
```

#### 2.1 Presiona F12 para abrir DevTools

#### 2.2 Click en pestaña "Network" (Red)

#### 2.3 Ingresa documento: `1022394742`

#### 2.4 Click en "Consultar"

#### 2.5 **OBSERVA LO MISMO QUE EN RUNT:**

**A) ¿Aparece una tabla de multas?**
- Sí → Ve al paso 2.6
- No → ¿Dice "Paz y Salvo"? ¿Hay un mensaje?

**B) En la pestaña "Network":**
- ¿Ves peticiones XHR/Fetch?
- ¿Cuál es la URL?
- ¿Qué respuesta traen?

**C) Si aparecen multas:**
- Inspecciona una multa (click derecho → Inspeccionar)
- Anota el selector del elemento

**DOCUMENTA:**
- [ ] ¿La tabla aparece? Sí/No
- [ ] ¿Dice "Paz y Salvo"? Sí/No
- [ ] ¿URL de petición AJAX: ___________
- [ ] ¿Selector de elemento con datos: ___________
- [ ] Screenshot del resultado: `/tmp/simit_visible.png`

---

### PASO 3: PROBAR CON EL SCRIPT DE AYUDA (30 min)

```bash
cd /home/ubuntu/LABORATORIO/sarlaft-modern/backend/app/scrapers
python3 ayuda_inspeccion.py
```

#### Opción 1: "Inspeccionar RUNT (automático)"

Este script:
1. Abre RUNT en navegador visible
2. Ingresa placa automáticamente
3. Hace click en consultar
4. **PAUSA para que veas el resultado**
5. Toma screenshots

**Mientras está Pausado:**
- Abre DevTools (F12)
- Observa qué aparece en la pantalla
- Inspecciona elementos visibles
- Anota selectores

#### Opción 5: "Modo interactivo (exploración libre)"

Este te permite:
- Navegar libremente por RUNT o SIMIT
- Probar diferentes placas/documentos
- Ver qué pasa en tiempo real
- Inspeccionar elementos con DevTools

---

### PASO 4: SI NO HAY DATOS VISIBLES - INVESTIGAR AJAX

Si después de consultar NO ves datos en el HTML:

#### 4.1 Interceptar peticiones de red

En DevTools → Pestaña "Network":
1. Filtra por "XHR" y "Fetch"
2. Haz click en "Consultar"
3. Busca peticiones que aparezcan DESPUÉS del click
4. Click en cada petición
5. Ve a la pestaña "Response"

**Anota:**
- URL de la petición: ___________
- Método: GET/POST/___________
- Response type: JSON/HTML/XML/___________
- Datos que trae: ___________

#### 4.2 Probar replicar la petición

```bash
# Ejemplo de cómo replicar petición AJAX
curl -X POST 'URL_DE_LA_PETICION' \
  -H 'Content-Type: application/json' \
  -d '{"placa": "ABC123"}'
```

---

### PASO 5: DOCUMENTAR TODO LO QUE VISTE

Crear archivo:

```bash
nano /home/ubuntu/LABORATORIO/sarlaft-modern/OBSERVACION_VISUAL_RUNT.md
```

**Contenido:**

```markdown
# OBSERVACIÓN VISUAL RUNT

## URL
https://www.runt.gov.co/consultaCiudadana/consultaVehiculo

## PROCESO OBSERVADO

### Paso 1: Ingresar placa ABC123
- [ ] El campo acepta la placa: Sí/No
- [ ] Selector del campo: ___________

### Paso 2: Click en "Consultar Información"
- [ ] El botón responde: Sí/No
- [ ] Selector del botón: ___________

### Paso 3: Espera de resultados
- [ ] ¿Aparece spinner de carga? Sí/No
- [ ] ¿Cuántos segundos tarda? ___ seg
- [ ] ¿La pantalla cambia? Sí/No

### Paso 4: Resultados
- [ ] ¿Aparecen datos del vehículo? Sí/No
- [ ] ¿En qué formato? (Tabla/Cards/Divs): ___________
- [ ] ¿Los datos son visibles en HTML (F12)? Sí/No

### Paso 5: Selectores observados

**Si hay datos visibles:**
- Selector de contenedor: ___________
- Selector de cada fila: ___________
- Selector de celda marca: ___________
- Selector de celda modelo: ___________

**Si NO hay datos visibles:**
- ¿URL de petición AJAX? ___________
- ¿Tipo de respuesta? (JSON/HTML): ___________
- ¿Se puede replicar? Sí/No

### Screenshots
- [ ] /tmp/runt_visible.png
- [ ] /tmp/runt_devtools_inspector.png
- [ ] /tmp/runt_network_tab.png

## CONCLUSIÓN

- [ ] Los datos están en HTML → Se puede extraer con selectores
- [ ] Los datos vienen por AJAX → Se necesita interceptar petición
- [ ] Los datos NO aparecen → Usar API o fallback

## SELECTORES FINALES

Input placa: ___________
Botón consultar: ___________
Contenedor resultados: ___________
Fila de datos: ___________
Celda marca: ___________
```

**Repetir para SIMIT:**
```bash
nano /home/ubuntu/LABORATORIO/sarlaft-modern/OBSERVACION_VISUAL_SIMIT.md
```

---

## 🎯 CHECKLIST DE OBSERVACIÓN

Antes de terminar, asegúrate de haber observado:

### RUNT:
- [ ] Abrí la página en navegador
- [ ] Ingresé una placa real (ABC123 o similar)
- [ ] Hice click en consultar
- [ ] Esperé a que aparecieran resultados (o confirmé que NO aparecen)
- [ ] Abrí DevTools (F12)
- [ ] Inspeccioné un dato visible
- [ ] Verifiqué pestaña "Network" para peticiones AJAX
- [ ] Tomé screenshots
- [ ] Documenté selectores observados

### SIMIT:
- [ ] Abrí la página en navegador
- [ ] Ingresé un documento real
- [ ] Hice click en consultar
- [ ] Esperé resultados (o mensaje de "Paz y Salvo")
- [ ] Abrí DevTools (F12)
- [ ] Inspeccioné elementos
- [ ] Verifiqué pestaña "Network"
- [ ] Tomé screenshots
- [ ] Documenté selectores observados

---

## 📞 REPORTAR HALLAZGOS

Una vez hayas observado todo, reporta:

1. **¿Los datos son VISIBLES en el HTML?**
   - Sí → Anota los selectores exactos
   - No → Anota las URLs de las peticiones AJAX

2. **¿Cuánto tiempo tardan en aparecer?**
   - ___ segundos para RUNT
   - ___ segundos para SIMIT

3. **¿Qué selectores usan los datos?**
   - RUNT: ___________
   - SIMIT: ___________

4. **Screenshots de evidencia**
   - `/tmp/runt_visible.png`
   - `/tmp/simit_visible.png`

---

## 🚀 EJECUCIÓN

```bash
# PASO 1: Abrir RUNT manualmente
google-chrome https://www.runt.gov.co/consultaCiudadana/consultaVehiculo &

# PASO 2: Observar y documentar (30 min)

# PASO 3: Abrir SIMIT manualmente
google-chrome https://www.fcm.org.co/simit/ &

# PASO 4: Observar y documentar (30 min)

# PASO 5: Probar con script de ayuda
cd /home/ubuntu/LABORATORIO/sarlaft-modern/backend/app/scrapers
python3 ayuda_inspeccion.py

# PASO 6: Documentar hallazgos
nano /home/ubuntu/LABORATORIO/sarlaft-modern/OBSERVACION_VISUAL_RUNT.md
nano /home/ubuntu/LABORATORIO/sarlaft-modern/OBSERVACION_VISUAL_SIMIT.md
```

---

**TIEMPO TOTAL:** 1.5 - 2 horas

**OBJETIVO:** Ver con tus propios ojos qué pasa, no adivinar.
