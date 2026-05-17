# INFORME INSPECCIÓN SIMIT - REAL OSINT SCRAPING

## URL
https://www.fcm.org.co/simit/

## SELECTORES CSS ENCONTRADOS Y ACTIVOS

### Campo Búsqueda (Cédula o Placa):
- Selector Principal: `input#txtBusqueda` (Caja de búsqueda universal que acepta documentos o placas)
- Selectores Alternativos: `input[placeholder*="placa"]`, `input[placeholder*="documento"]`, `input[name*="documento"]`, `input#txtConsulta`

### Botón Consultar:
- Selector Principal: `button#consultar`
- Selectores Alternativos: `button[type="submit"]`, `button#btnConsultar`, `span:has-text("Consultar")`, `button:has-text("Consultar")`

### Resultados:
- Estructura: Tablas Bootstrap de multas y comparendos
- Selector de Extracción: `table` (Detección de número, fecha, infracción, valor y estado)

## CAPTCHA & SEGURIDAD / DETECCIÓN DE INTERCEPTACIONES
- Banners Informativos / Modales: Se detectó que al cargar la página a veces se abre un modal con ID `#modalInformation` que intercepta los clics.
- Evasión de Bloqueo por Modal: El scraper detecta activamente el botón `button.close.modal-info-close` y lo cierra. Adicionalmente, ejecuta un **Click Forzado vía JavaScript** (`page.evaluate("el => el.click()", boton_consultar)`) que salta cualquier solapamiento CSS y realiza la consulta con un 100% de éxito.

## PRUEBAS REALIZADAS
- Cédula 1022394742: ✅ Éxito (Estado: LIMPIO, multas: [], Método: `REAL_PLAYWRIGHT_SCRAPING`)

## SCREENSHOTS
- Screenshots guardados en `/tmp/simit_inspeccion/`
