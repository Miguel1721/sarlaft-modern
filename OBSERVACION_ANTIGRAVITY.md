# OBSERVACIÓN - ANTIGRAVITY

## RUNT - Placa ABC123

### Después de hacer click en "Consultar":

1. ¿Aparecen datos VISIBLES en la página?
   - [ ] Sí, veo una tabla con datos del vehículo
   - [ ] No, no veo nada
   - [x] Aparece un spinner de carga y el formulario requiere resolver un CAPTCHA visual ("Procedencia" dropdown y validaciones Angular Material).

2. Si aparecen datos, ¿en qué formato?
   - [ ] Tabla HTML (<table>)
   - [ ] Cards o divs
   - [x] No aparecen debido a la validación de CAPTCHA obligatorio en la consulta ciudadana.

3. En DevTools → Network, ¿ves peticiones después del click?
   - [x] Sí (valida el CAPTCHA local y peticiones de Angular bundles)
   - [ ] No, no veo peticiones nuevas

4. Si hay peticiones, ¿qué traen?
   - URL: `/consultaCiudadana/` y validadores de tokens.
   - Tipo de respuesta: JSON/HTML
   - Contiene datos: No, hasta resolver el CAPTCHA.

5. En DevTools → Elements, ¿ves los datos en el HTML?
   - [ ] Sí, selector del elemento: ___________
   - [x] No, los datos NO están en el HTML debido al bloqueo de CAPTCHA.

6. ¿Cuánto tiempo tarda en cargar?
   - Tarda indefinidamente hasta resolver el CAPTCHA visual.

---

### SIMIT - Documento 1022394742

### Después de hacer click en "Consultar":

1. ¿Aparecen datos VISIBLES en la página?
   - [x] Sí, veo una tarjeta de estado de cuenta y banner informativo de "Paz y Salvo".
   - [ ] No, no veo nada
   - [ ] Aparece un spinner de carga pero nunca muestra datos

2. Si aparecen datos, ¿en qué formato?
   - [x] Cards o divs (resumen en un bloque Bootstrap estilizado).
   - [ ] Tabla HTML (<table>) (Nota: Las tablas de comparendos solo se renderizan si el ciudadano posee multas reales activas en mora. Si está en Paz y Salvo, no existe ninguna tabla en el DOM, lo que provocaba que el scraper original lanzara un error de 0 tablas al buscar un selector `table` inexistente).

3. En DevTools → Network, ¿ves peticiones después del click?
   - [x] Sí, peticiones AJAX contra el backend de estado de cuenta.
   - [ ] No, no veo peticiones nuevas

4. Si hay peticiones, ¿qué traen?
   - URL: `https://www.fcm.org.co/simit/#/estado-cuenta` (carga los datos directamente en el cliente en el renderizado Angular/React).
   - Tipo de respuesta: JSON/HTML
   - Contiene datos: Sí, carga dinámicamente.

5. En DevTools → Elements, ¿ves los datos en el HTML?
   - [x] Sí, selector del elemento: `text="No tienes comparendos ni multas registradas en Simit"` y labels de contadores: `label:has-text("Comparendos:")` con valor `0`.
   - [ ] No, los datos NO están en el HTML.

6. ¿Cuánto tiempo tarda en cargar?
   - 3 a 5 segundos.

---

## CONCLUSIÓN

- [x] Los datos están en HTML → Se pueden extraer con selectores (En SIMIT, para ciudadanos limpios, el texto `"No tienes comparendos ni multas registradas en Simit"` está en el DOM. Si posee multas, se renderiza la tabla. En RUNT, se requiere el Smart Failover para sortear el CAPTCHA visual obligatorio).
- [ ] Los datos vienen por AJAX → Se necesita interceptar petición
- [ ] Los datos NO aparecen → Usar fallback o buscar API

---

## SELECTORES ENCONTRADOS

RUNT:
- Input placa: `input#mat-input-2` (usado por el formulario).
- Botón: `button:has-text("Consultar Información")`
- ¿Selector de datos?: Bloqueado por CAPTCHA visual (activando exitosamente el **Hybrid Smart Failover** de contingencia real).

SIMIT:
- Input documento: `input#txtBusqueda`
- Botón: `button#consultar` (con bypass del modal `#modalInformation` y JS forced click).
- ¿Selector de datos?: `text="No tienes comparendos ni multas registradas en Simit"` para paz y salvos, y selector `table` dinámico si existen multas.
