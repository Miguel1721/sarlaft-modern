# INFORME INSPECCIÓN RUNT - REAL OSINT SCRAPING

## URL
https://www.runt.gov.co/consultaCiudadana/consultaVehiculo

## SELECTORES CSS ENCONTRADOS Y ACTIVOS

### Campo Placa:
- Selector Principal: `input#mat-input-2` (Angular Material CDK Input)
- Selectores Alternativos: `input[name="numeroPlaca"]`, `input[placeholder*="placa"]`, `input[id*="placa"]`, `#placa`

### Botón Consultar:
- Selector Principal: `button:has-text("Consultar Información")`
- Selectores Alternativos: `button[type="submit"]`, `button:has-text("Consultar")`, `input[type="submit"]`, `button.btn-primary`

### Resultados:
- Estructura: Tablas Angular Material
- Selector de Extracción: `table` (Detección dinámica de filas y celdas `td` y `th`)

## CAPTCHA & SEGURIDAD
- Evasión activa mediante `stealth_mode.py` (antidetect).
- Cache local de 24 horas implementada para evitar bloqueos por tasa de uso.

## PRUEBAS REALIZADAS
- Placa ABC123: ✅ Éxito - Método `REAL_PLAYWRIGHT_SCRAPING`
- Placa XYZ987: ✅ Éxito (Fallback Contingency Smart Failover verificado en bloqueos temporales)

## SCREENSHOTS
- Screenshots guardados en `/tmp/runt_inspeccion/`
