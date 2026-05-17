# 🔄 DIAGRAMA DE FLUJO COMPLETO - SISTEMA SARLAFT CDA

## ESCENARIO 1: VINCULACIÓN NUEVO CLIENTE

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      1. USUARIO: CDA                                    │
└─────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  Portal: /cda/deep-search                                               │
│                                                                         │
│  Campos requeridos:                                                     │
│  ┌────────────────────────────────────────────────────────────────┐     │
│  │ 📄 Documento: [________________]                            │     │
│  │ 📛 Nombre:     [________________]                            │     │
│  │ 🏢 Actividad:  [________________]                            │     │
│  │ 🚗 Placa (opc): [____]                                      │     │
│  └────────────────────────────────────────────────────────────────┘     │
│                                                                         │
│                    [🔍 INICIAR AUDITORÍA]                              │
└─────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────┐
│              2. BACKEND: ORCHESTRADOR (orchestrator_service_v2.py)    │
└─────────────────────────────────────────────────────────────────────────┘
                                      │
                    ┌─────────────────┴─────────────────┐
                    │                                       │
                    ▼                                       ▼
        ┌───────────────────────┐           ┌───────────────────────┐
        │  VALIDAR DATOS        │           │  CREAR SESIÓN         │
        │  - Formato documento  │           │  - ID auditoría       │
        │  - Campos obligatorios│           │  - Timestamp          │
        └───────────────────────┘           └───────────────────────┘
                    │                                       │
                    └─────────────────┬─────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────┐
│           3. EJECUCIÓN PARALELA DE CONSULTAS (asyncio.gather)          │
└─────────────────────────────────────────────────────────────────────────┘
                                      │
        ┌─────────────────────────────┼─────────────────────────────┐
        │                             │                             │
        ▼                             ▼                             ▼
┌───────────────┐         ┌───────────────┐         ┌───────────────┐
│ LISTAS        │         │ ANTECEDENTES  │         │ VEHÍCULO      │
│ RESTRICTIVAS  │         │ NACIONALES    │         │ (si placa)    │
├───────────────┤         ├───────────────┤         ├───────────────┤
│• OFAC         │         │• Policía      │         │• RUNT         │
│• ONU          │         │• Procuraduría │         │• SIMIT        │
│• UE           │         │• Contraloría  │         │               │
│• +40 listas   │         │• Otros        │         │               │
└───────────────┘         └───────────────┘         └───────────────┘
        │                             │                             │
        └─────────────────────────────┼─────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────┐
│              4. AGREGAR RESULTADOS (wait all)                          │
└─────────────────────────────────────────────────────────────────────────┘
                                      │
                    ┌─────────────────┴─────────────────┐
                    │                                       │
                    ▼                                       ▼
        ┌───────────────────────┐           ┌───────────────────────┐
        │  ¿ALERTAS LEGALES?    │           │  ¿ALERTAS LISTAS?     │
        │  (Policía/Proc/etc)   │           │  (OFAC/ONU/etc)       │
        └───────────────────────┘           └───────────────────────┘
                    │                               │
        ┌───────────┴───────────┐       ┌───────────┴───────────┐
        │ SÍ: STATUS = ROJO     │       │ SÍ: STATUS = ROJO     │
        │ NO: Continuar         │       │ NO: Continuar         │
        └───────────────────────┘       └───────────────────────┘
                    │                               │
                    └─────────────────┬─────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────┐
│            5. MOTOR DE REGLAS (motor_reglas_service.py)                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  Entrada: Datos del cliente + resultados consultas                     │
│                                                                         │
│  Reglas evaluadas:                                                     │
│  • ¿Fraccionamiento de efectivo?                                      │
│  • ¿Sin relación con actividad económica?                             │
│  • ¿Cliente sin histórico?                                            │
│  • ¿Cambio repentino de comportamiento?                               │
│  • ¿Operaciones simultáneas?                                          │
│                                                                         │
│  Salida: Lista de alertas + Score (0-100)                              │
└─────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────┐
│            6. IA ANALYZER (llm_evaluator.py)                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  Modelo: Claude 3.5 Sonnet + contexto normativo                        │
│                                                                         │
│  Tarea: Generar concepto jurídico justificado                          │
│                                                                         │
│  Entrada:                                                              │
│  • Resultados de consultas                                             │
│  • Alertas del motor de reglas                                         │
│  • Historial del cliente                                               │
│                                                                         │
│  Salida:                                                               │
│  • Explicación en lenguaje natural                                     │
│  • Referencias normativas                                              │
│  • Recomendación fundamentada                                          │
└─────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                  7. DICTAMEN FINAL                                     │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌────────────────────────────────────────────────────────────────┐    │
│  │  DECISIÓN: [APROBAR / RECHAZAR / REVISAR MANUAL]              │    │
│  │                                                                 │    │
│  │  NIVEL RIESGO: [BAJO / MEDIO / ALTO / CRÍTICO]                │    │
│  │                                                                 │    │
│  │  SCORE: [0-100]                                                 │    │
│  │                                                                 │    │
│  │  JUSTIFICACIÓN:                                                 │    │
│  │  "... El cliente no presenta alertas en listas restrictivas   │    │
│  │   ni antecedentes. El motor de reglas detectó operación       │    │
│  │   sin relación con actividad económica, pero justificada      │    │
│  │   por [razón]. Recomiendo APROBAR con monitoreo."            │    │
│  │                                                                 │    │
│  │  ALERTAS ENCONTRADAS: [N]                                      │    │
│  │  1. [Código] - [Descripción]                                   │    │
│  │  2. [Código] - [Descripción]                                   │    │
│  └────────────────────────────────────────────────────────────────┘    │
│                                                                         │
│                    [📥 DESCARGAR PDF]    [🔍 VER DETALLES]            │
└─────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────┐
│              8. PERSISTENCIA (database.py)                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  Tablas afectadas:                                                     │
│  • contrapartes_kyc (INSERT/UPDATE)                                    │
│  • evidencias_log (INSERT)                                             │
│  • lista_restrictiva_cache (UPDATE si es necesario)                    │
│                                                                         │
│  Datos guardados:                                                      │
│  • Dictamen completo (JSON)                                            │
│  • URL del PDF                                                         │
│  • Fecha de próxima revisión (hoy + 2 años)                           │
│  • Usuario que autoriza                                               │
└─────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────┐
│              9. PROGRAMAR TAREAS FUTURAS                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  APScheduler Jobs:                                                     │
│                                                                         │
│  ┌────────────────────────────────────────────────────────────────┐    │
│  │  Job: "monitoreo_continuo"                                     │    │
│  │  Frecuencia: DIARIA a las 02:00 AM                            │    │
│  │  Acción: Reconsultar listas restrictivas                       │    │
│  └────────────────────────────────────────────────────────────────┘    │
│                                                                         │
│  ┌────────────────────────────────────────────────────────────────┐    │
│  │  Job: "reevaluacion_bianual"                                   │    │
│  │  Frecuencia: MENSUAL (día 1)                                  │    │
│  │  Acción: Identificar clientes +2 años y reevaluar             │    │
│  └────────────────────────────────────────────────────────────────┘    │
│                                                                         │
│  Proxima revisión programada: 2028-05-17                                │
└─────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                      10. FRONTEND: RESULTADO                           │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌────────────────────────────────────────────────────────────────┐    │
│  │  ✅ AUDITORÍA COMPLETADA                                        │    │
│  │                                                                 │    │
│  │  ⏱️  Tiempo total: 45 segundos                                  │    │
│  │  📊 Consultas realizadas: 50                                   │    │
│  │                                                                 │    │
│  │  🎯 DICTAMEN: APROBAR                                          │    │
│  │  📈 Nivel Riesgo: BAJO (15/100)                                │    │
│  │                                                                 │    │
│  │  [📄 Descargar PDF]    [🔄 Nueva Consulta]    [📋 Historial]  │    │
│  └────────────────────────────────────────────────────────────────┘    │
│                                                                         │
│  ┌────────────────────────────────────────────────────────────────┐    │
│  │  📋 DETALLES DE CONSULTAS                                       │    │
│  │                                                                 │    │
│  │  ✓ OFAC - SDN List              LIMPIO                         │    │
│  │  ✓ ONU - Consolidated List      LIMPIO                         │    │
│  │  ✓ EU - Financial Sanctions      LIMPIO                         │    │
│  │  ✓ Policía Judicial             LIMPIO                         │    │
│  │  ✓ Procuraduría                 LIMPIO                         │    │
│  │  ✓ Contraloría                  LIMPIO                         │    │
│  │  ✓ RUNT                         No aplica                      │    │
│  │  ✓ SIMIT                        No aplica                      │    │
│  │  ... +42 listas más                                             │    │
│  └────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## ESCENARIO 2: MONITOREO CONTINUO (AUTOMÁTICO)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  CRON JOB: Todos los días a las 02:00 AM                               │
└─────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  monitoring_service_v2.py.tarea_monitoreo_continuo()                  │
└─────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  1. OBTENER CLIENTES ACTIVOS                                            │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  SELECT * FROM contrapartes_kyc                                        │
│  WHERE estado = 'ACTIVO'                                               │
│  AND ultima_revision < NOW() - INTERVAL '1 day'                        │
│                                                                         │
│  Resultado: 1,240 clientes para reconsultar                            │
└─────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  2. RECONSULTAR LISTAS RESTRICTIVAS (por lote de 10)                   │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  Para cada lote de 10 clientes:                                        │
│    - Ejecutar listas_restrictivas_service.py                           │
│    - Comparar resultado con último cache                               │
│    - Si DIFERENTE → Marcar como cambio                                 │
│                                                                         │
│  Progreso: [████████░░] 80% (992/1240)                                │
└─────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  3. ¿HAY CAMBIOS?                                                       │
└─────────────────────────────────────────────────────────────────────────┘
                                      │
                    ┌─────────────────┴─────────────────┐
                    │                                       │
            ▼ SÍ (3 clientes)                     ▼ NO (1,237 clientes)
                    │                                       │
                    ▼                                       │
┌───────────────────────────────────────────┐                   │
│  4. GENERAR ALERTAS                       │                   │
├───────────────────────────────────────────┤                   │
│                                           │                   │
│  Cliente: JUAN PÉREZ (1026575786)        │                   │
│  ⚠️  NUEVA COINCIDENCIA EN LISTA OFAC    │                   │
│                                           │                   │
│  Estado anterior: LIMPIO (2026-05-16)    │                   │
│  Estado actual: ALERTA (2026-05-17)      │                   │
│                                           │                   │
│  Acciones:                                │                   │
│  • PDF de novedad generado                │                   │
│  • Email enviado al CDA                   │                   │
│  • Dashboard actualizado                  │                   │
│                                           │                   │
│  Recomendación:                           │                   │
│  "Considerar rescisión de contrato       │                   │
│   y reportar a UIAF si se confirma LA/FT"│                   │
└───────────────────────────────────────────┘                   │
                    │                                       │
                    └─────────────────┬─────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  5. REGISTRAR EN BITÁCORA                                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  INSERT INTO evidencias_log (                                          │
│    tipo: "MONITOREO_CONTINUO",                                         │
│    cliente_id: 1026575786,                                             │
│    novedad: "NUEVA_ALERTA_LISTA",                                      │
│    severidad: "CRITICA",                                               │
│    fecha: NOW()                                                        │
│  )                                                                     │
│                                                                         │
│  ✓ 3 alertas críticas registradas                                      │
│  ✓ 1,237 clientes sin cambios                                          │
└─────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  6. ENVIAR RESUMEN AL CDA                                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  Email: compliance@cda.com                                             │
│  Asunto: "Reporte Monitoreo Diario - 2026-05-17"                       │
│                                                                         │
│  Resumen:                                                              │
│  • Clientes monitoreados: 1,240                                        │
│  • Novedades detectadas: 3                                             │
│  • Acción requerida: Revisar urgentes                                  │
│                                                                         │
│  Acceso: https://sarlaf.agentesia.cloud/cda/alertas                   │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## ESCENARIO 3: REEVALUACIÓN BIANUAL (AUTOMÁTICA)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  CRON JOB: Día 1 de cada mes a las 03:00 AM                            │
└─────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  monitoring_service_v2.py.tarea_reevaluacion_bianual()                 │
└─────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  1. IDENTIFICAR CLIENTES VENCIDOS                                       │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  SELECT * FROM contrapartes_kyc                                        │
│  WHERE proxima_revision <= NOW()                                       │
│  AND estado = 'ACTIVO'                                                 │
│                                                                         │
│  Resultado: 47 clientes requieren reevaluación                         │
└─────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  2. EJECUTAR DEBIDA DILIGENCIA COMPLETA (automático)                   │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  Para cada cliente:                                                    │
│    • Ejecutar orquestador_service_v2.py                               │
│    • Generar dictamen actualizado                                      │
│    • Comparar con dictamen anterior                                    │
│                                                                         │
│  Progreso: [████████░░] 85% (40/47)                                    │
└─────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  3. ANALIZAR CAMBIOS DE RIESGO                                         │
└─────────────────────────────────────────────────────────────────────────┘
                                      │
                    ┌─────────────────┴─────────────────┐
                    │                                       │
        ▼ RIESGO AUMENTÓ (5)                   ▼ RIESGO IGUAL/MENOR (42)
                    │                                       │
                    ▼                                       ▼
┌───────────────────────────────────────────┐       ┌───────────────────┐
│  4. NOTIFICAR CAMBIO DE RIESGO            │       │  5. ACTUALIZAR   │
├───────────────────────────────────────────┤       │     Y ARCHIVAR   │
│                                           │       └───────────────────┘
│  Cliente: TRANSPORTES ABC (900.123.456)  │                   │
│  ⚠️  RIESGO AUMENTÓ                      │                   │
│                                           │                   │
│  Anterior (2024-05-17):                   │                   │
│  • Nivel: BAJO (15/100)                  │                   │
│  • Dictamen: APROBAR                     │                   │
│                                           │                   │
│  Actual (2026-05-17):                     │                   │
│  • Nivel: MEDIO (55/100)                 │                   │
│  • Dictamen: REVISAR                     │                   │
│                                           │                   │
│  Motivo del cambio:                       │                   │
│  "Nueva coincidencia en SIMIT por         │                   │
│   multas acumuladas > $5M COP"           │                   │
│                                           │                   │
│  Recomendación:                           │                   │
│  "Revisar relación comercial y           │                   │
│   considerar monitoreo intensificado"    │                   │
│                                           │                   │
│  [Ver PDF Comparativo]                    │                   │
└───────────────────────────────────────────┘                   │
                    │                                       │
                    └─────────────────┬─────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  6. PROGRAMAR PRÓXIMA REVISIÓN                                           │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  UPDATE contrapartes_kyc                                                │
│  SET ultima_revision = NOW(),                                           │
│      proxima_revision = NOW() + INTERVAL '2 years',                    │
│      nivel_riesgo_actual = 'MEDIO'                                      │
│  WHERE cliente_id = 900123456                                           │
│                                                                         │
│  ✓ 47 clientes reevaluados                                             │
│  ✓ Próximas revisiones programadas: 2028-05-17                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## ESCENARIO 4: DETECCIÓN DE OPERACIÓN INUSUAL

```
┌─────────────────────────────────────────────────────────────────────────┐
│  EVENTO: Cliente realiza transacción                                   │
└─────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  1. CAPTURAR TRANSACCIÓN                                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  POST /api/v1/transacciones/evaluar                                    │
│                                                                         │
│  {                                                                     │
│    "cliente_id": "1026575786",                                          │
│    "monto": 45000000,                                                  │
│    "forma_pago": "EFECTIVO",                                           │
│    "fecha": "2026-05-17T10:30:00",                                     │
│    "actividad_economica": "TRANSPORTE DE CARGA",                       │
│    "descripcion": "Servicio de inspección vehículo"                    │
│  }                                                                     │
└─────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  2. MOTOR DE REGLAS (Tiempo Real)                                      │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  motor_reglas_service.evaluar_transaccion()                            │
│                                                                         │
│  Reglas evaluadas:                                                     │
│  ✓ Fraccionamiento de efectivo → 3 ops en 7 días                      │
│  ✓ Monto vs actividad → $45M > umbral ($50M) = NORMAL                 │
│  ✓ Cambio de comportamiento → +400% vs histórico                      │
│  ✓ Cliente sin histórico → FALSO (tiene histórico)                    │
│  ✓ Operaciones simultáneas → 2 ops en 2 horas                        │
│                                                                         │
│  SCORE: 75/100                                                         │
└─────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  3. ¿REQUIERE ROS?                                                      │
└─────────────────────────────────────────────────────────────────────────┘
                                      │
                    ┌─────────────────┴─────────────────┐
                    │                                       │
              ▼ SÍ (Score > 70)                   ▼ NO (Score ≤ 70)
                    │                                       │
                    ▼                                       │
┌───────────────────────────────────────────┐                   │
│  4. ALERTAR Y PREPARAR ROS                │                   │
├───────────────────────────────────────────┤                   │
│                                           │                   │
│  ⚠️  ALERTA: Operación inusual            │                   │
│      detectada                            │                   │
│                                           │                   │
│  Cliente: JUAN PÉREZ (1026575786)        │                   │
│  Score: 75/100                            │                   │
│                                           │                   │
│  Señales de alerta:                       │                   │
│  1. [EFR-001] Fraccionamiento efectivo   │                   │
│  2. [CAM-001] Cambio repentino +400%     │                   │
│                                           │                   │
│  Requiere ROS: SÍ                         │                   │
│                                           │                   │
│  Formato ROS prellenado:                  │                   │
│  • Consecutivo: ROS-2026-0042            │                   │
│  • Fecha reporte: 2026-05-17             │                   │
│  • Datos cliente: pre-cargados           │                   │
│  • Señales alerta: documentadas          │                   │
│                                           │                   │
│  [Completar ROS]    [Ver evidencia]      │                   │
└───────────────────────────────────────────┘                   │
                    │                                       │
                    └─────────────────┬─────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  5. CDA REVISA Y APRUEBA ROS                                            │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  El CDA:                                                                │
│  • Revisa el formato prellenado                                        │
│  • Agrega descripción manual                                           │
│  • Justifica la sospecha                                                │
│  • Aprueba envío                                                        │
│                                                                         │
│  Tiempo: 10 minutos (vs 2 horas manual)                                │
└─────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  6. SISTEMA ARCHIVA Y REGISTRA                                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  • ROS archivado en PDF (5 años)                                       │
│  • Registrado en tabla ros_enviados                                    │
│  • Estado de cliente actualizado a "EN REVISIÓN"                       │
│  • Email de confirmación al CDA                                        │
│                                                                         │
│  ✓ ROS-2026-0042 archivado correctamente                               │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 📊 RESUMEN DE TIEMPOS

| Proceso | Manual | Automatizado | Ahorro |
|---------|--------|--------------|--------|
| Vinculación cliente | 2-3 horas | 3-5 minutos | **95%** |
| Monitoreo diario | 4-8 horas | 0 min (automático) | **100%** |
| Reevaluación bianual | 8-12 horas | 0 min (automático) | **100%** |
| Reporte ROS | 2-4 horas | 10 minutos | **92%** |
| **TOTAL POR CLIENTE/AÑO** | **~40 horas** | **~20 minutos** | **99%** |

---

## 🎯 IMPACTO EN CDA TÍPICO

**CDA con 100 clientes:**

- **Antes:** 4,000 horas/año en SARLAFT (2 personas tiempo completo)
- **Después:** 33 horas/año (1 persona 1 día/mes)
- **Ahorro:** 3,967 horas/año
- **Costo laboral ahorrado:** ~$120M COP/año

**ROI del sistema:**
- Inversión: $15M COP (implementación)
- Ahorro primer año: $120M COP
- **ROI: 800% primer año**

---

**FIN DEL DIAGRAMA**
