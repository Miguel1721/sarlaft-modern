# 🚀 GUÍA DE IMPLEMENTACIÓN COMPLETA - SARLAFT PARA CDAs
## Sistema 100% Automatizado de Debida Diligencia

**Fecha:** Mayo 17, 2026
**Versión:** 1.0
**Objetivo:** Implementar flujo completo automatizado que haga **absolutamente todo** por el CDA

---

## 📋 ÍNDICE

1. [Visión General del Sistema Automatizado](#1-visión-general)
2. [Arquitectura del Flujo Completo](#2-arquitectura)
3. [Módulos a Implementar](#3-módulos)
4. [Plan de Trabajo por Fases](#4-plan-de-trabajo)
5. [Procedimientos Operativos](#5-procedimientos)
6. [Métricas de Éxito](#6-métricas)

---

## 1. VISIÓN GENERAL DEL SISTEMA AUTOMATIZADO

### 🎯 **OBJETIVO FINAL**
El sistema debe permitir que un CDA realice **TODA** la debida diligencia con **MÍNIMA** intervención humana:

```
┌───────────────────────────────────────────────────────────────┐
│               FLUJO IDEAL AUTOMATIZADO                        │
├───────────────────────────────────────────────────────────────┤
│                                                               │
│  1. CDA ingresa documento del cliente                        │
│         ↓                                                    │
│  2. Sistema consulta automáticamente 50+ fuentes             │
│         ↓                                                    │
│  3. Sistema analiza riesgos con IA                          │
│         ↓                                                    │
│  4. Sistema genera dictamen con recomendación               │
│         ↓                                                    │
│  5. Sistema archiva evidencia (5 años)                      │
│         ↓                                                    │
│  6. Sistema alerta cambios en listas (24/7)                 │
│         ↓                                                    │
│  7. Sistema reevalúa cada 2 años automáticamente            │
│                                                               │
│       ❌ INTERACCIÓN HUMANA: Solo aprobación final           │
└───────────────────────────────────────────────────────────────┘
```

---

## 2. ARQUITECTURA DEL FLUJO COMPLETO

### 🏗️ **DIAGRAMA DE COMPONENTES**

```
┌─────────────────────────────────────────────────────────────────┐
│                    PORTAL CDA (/cda)                            │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌──────────────┐  ┌────────────────────┐    │
│  │   Dashboard │  │ Deep Search  │  │  Fábrica Legal     │    │
│  │   Métricas  │  │ Consultas    │  │  Docs PDF          │    │
│  └─────────────┘  └──────────────┘  └────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
                            ↓ API REST
┌─────────────────────────────────────────────────────────────────┐
│                     BACKEND ORCHESTRATOR                        │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              MOTOR DE ORQUESTACIÓN                        │  │
│  │  - Consulta paralela a todas las fuentes                 │  │
│  │  - Agrega resultados                                     │  │
│  │  - Ejecuta motor de reglas                               │  │
│  │  - Genera dictamen                                       │  │
│  └──────────────────────────────────────────────────────────┘  │
│           ↓              ↓              ↓                      │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐          │
│  │ Conectores   │ │ Motor Reglas │ │ IA Analyzer  │          │
│  │ 50+ fuentes  │ │ Señales UIAF │ │ Concepto     │          │
│  └──────────────┘ └──────────────┘ └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│                       CAPA DE DATOS                             │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────────┐      │
│  │ PostgreSQL  │  │ Cache Redis  │  │ Storage S3/Local  │      │
│  │ + Modelos   │  │ Listas       │  │ PDFs, Evidencias  │      │
│  └─────────────┘  └──────────────┘  └──────────────────┘      │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│                    SERVICIOS EXTERNOS                            │
├─────────────────────────────────────────────────────────────────┤
│  RUNT | SIMIT | Policía | Procuraduría | Contraloría | OFAC    │
│  ONU | UE | FBI | Interpol | +40 listas internacionales         │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. MÓDULOS A IMPLEMENTAR

### ✅ **MÓDULOS YA LISTOS (100%)**

| Módulo | Estado | Archivo | Funcionalidad |
|--------|--------|---------|---------------|
| Fábrica Legal | ✅ | `document_factory.py` | Genera 7 PDFs normativos |
| Consecutivos ROS | ✅ | `onboarding_router.py` | Secuencia atómica por tenant |
| Templates PDF | ✅ | `templates/sarlaft_docs/` | 7 documentos SARLAFT |
| Portal Frontend | ✅ | `frontend/src/app/cda/` | UI completa Next.js |
| Modelo de Datos | ✅ | `models.py` | Tablas PostgreSQL |

---

### 🔨 **MÓDULOS PENDIENTES (PRIORIDAD ALTA)**

#### **A. MOTOR DE ORQUESTACIÓN COMPLETO**
**Archivo:** `orchestrator_service_v2.py`

**Funcionalidad:**
```python
async def orquestar_debida_diligencia_completa(
    cedula: str,
    placa: str = None,
    cliente_id: str,
    tipo_consulta: str = "SARLAFT_CDA"
) -> Dict:
    """
    Ejecuta el flujo completo de debida diligencia automáticamente

    Returns:
        {
            "estado": "COMPLETO",
            "cliente": {...},
            "consultas_realizadas": 50,
            "tiempo_total_segundos": 45,
            "dictamen": {
                "decision": "APROBAR/RECHAZAR/REVISAR",
                "nivel_riesgo": "BAJO/MEDIO/ALTO/CRITICO",
                "score": 0-100,
                "justificacion": "...",
                "alertas": [...]
            },
            "evidencia": {
                "pdf_url": "...",
                "json_raw": {...},
                "fecha_archivo": "..."
            },
            "proxima_revision": "2028-05-17"  # 2 años
        }
    """
```

**Pasos del orquestador:**
1. Validar datos de entrada
2. Consultar listas restrictivas (43 fuentes)
3. Consultar antecedentes nacionales (Policía, Procuraduría, etc.)
4. Ejecutar motor de reglas
5. Analizar con IA
6. Generar dictamen
7. Crear PDF de evidencia
8. Guardar en base de datos
9. Programar próxima revisión (2 años)

---

#### **B. MONITOREO CONTINUO (Background Jobs)**
**Archivo:** `monitoring_service_v2.py`

**Funcionalidad:**
```python
async def tarea_monitoreo_continuo():
    """
    Se ejecuta DIARIAMENTE a las 2 AM

    1. Reconsultar listas restrictivas para todos los clientes activos
    2. Si hay COINCIDENCIA NUEVA → Alerta inmediata al CDA
    3. Generar reporte de cambios
    """
    pass

async def tarea_reevaluacion_bianual():
    """
    Se ejecuta MENSUALMENTE

    1. Identificar clientes con 2 años desde última revisión
    2. Ejecutar debida diligencia completa automáticamente
    3. Actualizar score de riesgo
    4. Notificar al CDA
    """
    pass
```

---

#### **C. GESTIÓN DE BENEFICIARIOS FINALES**
**Archivo:** `beneficiarios_service.py` ✅ **YA CREADO**

**Funcionalidad:**
- Analizar estructura accionaria
- Identificar PEPs
- Detectar familiares de PEP
- Generar reporte de propiedad real

---

#### **D. MOTOR DE REGLAS UIAF**
**Archivo:** `motor_reglas_service.py` ✅ **YA CREADO**

**Funcionalidad:**
- Detectar operaciones inusuales
- Fraccionamiento de efectivo
- Cambios de comportamiento
- Operaciones simultáneas
- Sin relación con actividad económica

---

#### **E. LISTAS RESTRICTIVAS REALES**
**Archivo:** `listas_restrictivas_service.py` ✅ **YA CREADO**

**Funcionalidad:**
- Consulta a APIs OFAC, ONU, UE
- Cache de resultados
- Actualización automática diaria

---

## 4. PLAN DE TRABAJO POR FASES

### 📅 **FASE 1: CONECTORES REALES (Semana 1-2)**

#### **Día 1-2: Listas Restrictivas**
- [ ] Implementar `listas_restrictivas_service.py`
- [ ] Configurar integración OFAC API
- [ ] Configurar integración ONU API
- [ ] Configurar integración UE API
- [ ] Implementar cache Redis
- [ ] Tests unitarios

#### **Día 3-5: Conectores Nacionales**
- [ ] RUNT real (API MinTransporte)
- [ ] SIMIT real (API Fiscalía)
- [ ] Configurar límites de tasa
- [ ] Implementar reintentos
- [ ] Tests de integración

#### **Día 6-7: Documentación**
- [ ] Documentar APIs usadas
- [ ] Crear diagramas de secuencia
- [ ] Actualizar README

---

### 📅 **FASE 2: MOTOR DE INTELIGENCIA (Semana 3-4)**

#### **Semana 3: Reglas y Análisis**
- [ ] Integrar `motor_reglas_service.py`
- [ ] Integrar `beneficiarios_service.py`
- [ ] Crear evaluador de riesgo compuesto
- [ ] Implementar matriz de riesgo dinámica
- [ ] Tests con casos de prueba reales

#### **Semana 4: IA y Concepto**
- [ ] Mejorar `llm_evaluator.py`
- [ ] Agregar contexto normativo
- [ ] Generar explicaciones justificadas
- [ ] Validar con abogado experto

---

### 📅 **FASE 3: AUTOMATIZACIÓN COMPLETA (Semana 5-6)**

#### **Semana 5: Orquestador V2**
- [ ] Crear `orchestrator_service_v2.py`
- [ ] Implementar flujo unificado
- [ ] Manejo de errores robusto
- [ ] Logging y auditoría
- [ ] Tests end-to-end

#### **Semana 6: Monitoreo y Alertas**
- [ ] Implementar `monitoring_service_v2.py`
- [ ] Configurar APScheduler
- [ ] Sistema de notificaciones
- [ ] Dashboard de monitoreo
- [ ] Tests de carga

---

### 📅 **FASE 4: FRONTEND COMPLETO (Semana 7-8)**

#### **Semana 7: UI Avanzada**
- [ ] Dashboard de monitoreo
- [ ] Vista de alertas en tiempo real
- [ ] Historial de reevaluaciones
- [ ] Reportes programados
- [ ] Filtros avanzados

#### **Semana 8: UX Final**
- [ ] Onboarding guiado
- [ ] Tutoriales interactivos
- [ ] Ayuda contextual
- [ ] Validaciones en tiempo real
- [ ] Tests E2E con Playwright

---

### 📅 **FASE 5: PRUEBAS Y LANZAMIENTO (Semana 9-10)**

#### **Semana 9: Piloto**
- [ ] Seleccionar 3 CDAs piloto
- [ ] Implementar con datos reales
- [ ] Recopilar feedback
- [ ] Ajustar según uso
- [ ] Documentar casos

#### **Semana 10: Producción**
- [ ] Deploy en producción
- [ ] Configurar backups
- [ ] Monitoreo 24/7
- [ ] Soporte usuario
- [ ] Plan de contingencia

---

## 5. PROCEDIMIENTOS OPERATIVOS

### 📋 **PO-01: VINCULACIÓN DE NUEVO CLIENTE**

**Objetivo:** Vincular nuevo cliente con intervención mínima del CDA

**Tiempo estimado:** 3-5 minutos (vs 2-3 horas manual)

**Pasos:**

1. **CDA ingresa datos básicos (1 min)**
   - Nombre completo
   - Documento
   - Actividad económica
   - (Opcional) Placa si es cliente vehículo

2. **Sistema ejecuta automáticamente (2-3 min)**
   - Consulta 50+ fuentes en paralelo
   - Ejecuta motor de reglas
   - Genera dictamen con IA
   - Crea PDF de evidencia

3. **CDA revisa dictamen (1 min)**
   - Ve decisión recomendada
   - Revisa justificación
   - Aprueba o rechaza

4. **Sistema archiva automáticamente**
   - Guarda PDF (5 años)
   - Programa próxima revisión (2 años)
   - Envía confirmación

**Resultado:** Cliente vinculado con evidencia completa archivada

---

### 📋 **PO-02: MONITOREO CONTINUO**

**Objetivo:** Detectar cambios en estatus de clientes existentes

**Frecuencia:** Diaria (2:00 AM)

**Pasos automáticos:**

1. **Sistema obtiene lista de clientes activos**
2. **Reconsultar listas restrictivas**
3. **Comparar con resultado anterior**
4. **Si hay cambio:**
   - Generar alerta
   - Notificar al CDA (email + dashboard)
   - Crear PDF de novedad
   - Sugerir acción (ej: "Considerar rescisión contrato")

**Resultado:** CDA siempre al tanto de cambios de riesgo

---

### 📋 **PO-03: REEVALUACIÓN BIANUAL**

**Objetivo:** Actualizar debida diligencia cada 2 años

**Frecuencia:** Mensual (revisa vencidos)

**Pasos automáticos:**

1. **Sistema identifica clientes vencidos (2 años sin revisión)**
2. **Ejecuta debida diligencia completa automáticamente**
3. **Genera nuevo dictamen comparado con anterior**
4. **Notifica al CDA:**
   - "Cliente [NOMBRE] requiere reevaluación"
   - "Dictamen anterior: VERDE"
   - "Dictamen actual: [COLOR]"
   - "Recomendación: [ACCION]"
5. **CDA aprueba actualización**

**Resultado:** Cumplimiento normativo sin esfuerzo manual

---

### 📋 **PO-04: REPORTE DE OPERACIÓN SOSPECHOSA (ROS)**

**Objetivo:** Generar ROS cuando se detecta operación inusual

**Trigger:** Motor de reglas detecta patrón sospechoso

**Pasos:**

1. **Sistema detecta operación inusual**
   - Motor de reglas evalúa transacción
   - Si score > 80 → Alerta de posible ROS

2. **Sistema prepara ROS (automático)**
   - Formato UIAF prellenado
   - Consecutivo automático
   - Evidencia adjunta

3. **CDA revisa y aprueba ROS**
   - Verifica información
   - Agrega descripción manual
   - Aprueba envío

4. **Sistema:**
   - Archiva ROS
   - Registra en SIREL (si está integrado)
   - Programa seguimiento

**Resultado:** ROS generado en 10 minutos (vs 2 horas manual)

---

## 6. MÉTRICAS DE ÉXITO

### 📊 **MÉTRICAS TÉCNICAS**

| Métrica | Objetivo | Medición |
|---------|----------|----------|
| Tiempo respuesta consulta | < 60 segundos | Prometheus |
| Disponibilidad sistema | 99.5% uptime | Uptime Robot |
| Tasa de falsos positivos | < 10% | Feedback usuario |
| Cobertura listas restrictivas | 43/43 fuentes | Checklist |
| Precisión clasificación riesgo | > 85% | Validación experto |

---

### 📊 **MÉTRICAS DE NEGOCIO**

| Métrica | Objetivo | Medición |
|---------|----------|----------|
| Ahorro tiempo CDA | 90% (3h → 18min) | Encuesta satisfacción |
| Reducción errores humanos | 95% | Comparación pre/post |
| Cumplimiento normativo | 100% | Auditorías externas |
| Costo por consulta | < $20k COP | Contabilidad |
| Satisfacción cliente | > 4.5/5 | NPS |

---

### 📊 **MÉTRICAS DE IMPACTO**

| Métrica | Línea base | Objetivo 6 meses |
|---------|------------|------------------|
| CDAs usando sistema | 0 | 50 |
| Consultas mensuales | 0 | 5,000 |
| Alertas generadas | 0 | 200 |
| ROS reportados | 0 | 20 |
| Ingresos MRR | $0 | $15M COP |

---

## 🚀 **PRÓXIMOS PASOS INMEDIATOS**

### **HOY (Día 1)**
1. ✅ Revisar archivos creados hoy
2. [ ] Decidir: ¿Implementar conector RUNT real primero?
3. [ ] Crear repositorio de tareas con issues
4. [ ] Configurar proyecto Jira/Trello

### **ESTA SEMANA**
1. [ ] Implementar conector RUNT real
2. [ ] Implementar conector SIMIT real
3. [ ] Integrar listas restrictivas servicio
4. [ ] Crear tests de integración

### **PRÓXIMA SEMANA**
1. [ ] Iniciar desarrollo orquestador V2
2. [ ] Integrar motor de reglas
3. [ ] Crear frontend de monitoreo
4. [ ] Documentar arquitectura

---

## 📞 **SOPORTE Y CONTACTO**

**Desarrollador Principal:** Claude AI Assistant
**Repositorio:** `/home/ubuntu/LABORATORIO/sarlaft-modern`
**URL Producción:** https://sarlaf.agentesia.cloud/cda
**Documentación:** `SARLAFT_COMPLIANCE_HANDOFF.md`

---

## 📚 **REFERENCIAS NORMATIVAS**

- Resolución 2328 de 2025 (SuperTransporte)
- Circular Externa 024 de 2026 (Implementación)
- Resolución 4607 de 2026 (Simplificación)
- Guía UIAF Transaction Monitoring
- Guía SARLAFT sector transporte

---

**FIN DE LA GUÍA**

¿Listo para comenzar la implementación?
