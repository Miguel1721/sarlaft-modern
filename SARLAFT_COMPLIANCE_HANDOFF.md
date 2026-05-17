# DOSSIER DE TRASPASO: SARLAFT 4.0 COMPLIANCE ENGINE
## Documento de Contexto y Estado del Arte (Para Continuación de Sesión)

Este documento ha sido estructurado meticulosamente para ser entregado a la Inteligencia Artificial al inicio de la nueva conversación. Permite reanudar el desarrollo con **cero pérdida de contexto**, alineación inmediata de la arquitectura y mapeo total del sistema actual.

---

## 1. CONTEXTO GENERAL DEL SISTEMA
El **SARLAFT 4.0 Compliance Engine** es una plataforma multitenant de prevención de lavado de activos y financiación del terrorismo, diseñada específicamente para cumplir con las regulaciones de la **Supertransporte** y la **UIAF** en Colombia.

### Arquitectura Técnica
*   **Servidor**: Oracle Cloud (`sarlaf.agentesia.cloud` / IP: `157.137.232.7`).
*   **Capa Backend**: FastAPI (Python 3) monolítico robustecido con Pydantic V2 y SQLAlchemy, encargado de la orquestación asíncrona de listas, análisis jurídico con Inteligencia Artificial, y generación/sellado de PDFs con Jinja2 y Playwright (headless).
*   **Capa Frontend**: Next.js 16 (App Router) en TypeScript y Tailwind CSS, utilizando animaciones fluidas con Framer Motion y una estética premium en modo oscuro con acentos de color contextuales.
*   **Capa de Datos**: PostgreSQL alojado de forma aislada en Docker.
*   **Orquestación**: Docker Compose administrado bajo Traefik para enrutamiento reverso HTTPS.

---

## 2. HITOS COMPLETADOS (FASES DE ESTABILIZACIÓN)

### Fase 1: Capa de Presentación (Jinja2 Estático) - 100% Normativo
*   **Problema original**: Existencia de bucles dinámicos `{% for %}` en plantillas Jinja2 que causaban que inspectores de entes de control invalidaran el sistema al ver tablas vacías de matrices de riesgo o señales de alerta si los datos no cargaban del onboarding.
*   **Solución**: Se removieron todos los bucles dinámicos y se **hardcodearon estáticamente** las definiciones normativas y tablas estáticas de la ley directo en el código HTML de los 7 documentos core. Las definiciones de la ley no cambian por cliente y ahora son 100% sólidas.
*   **Documentos Modificados**:
    1.  `1_manual_politica.html`: Matriz de medición de riesgo y señales de alerta UIAF estáticas.
    2.  `4_procedimiento_dd.html`: Tabla estática con las listas de verificación obligatorias.
    3.  `5_acta_nombramiento.html`: Cálculos de experiencia legibles y dinámicos.
    4.  `6_plan_capacitacion.html`: Módulo estático normativo.
    5.  `7_formato_ros.html`: Formulario UIAF en blanco auto-consecutivo.

### Fase 2: Capa de Negocio (Pydantic & Validación)
*   **Validación de Nombres (OC)**: Se implementó un validador estricto en Pydantic (`debe_tener_apellido`) que obliga al Oficial de Cumplimiento a ingresar nombre **Y** apellido completos (mínimo 2 palabras) para evitar reportes inválidos en SIREL.
*   **Experiencia**: Se añadió el campo `oc_experiencia_meses: int` en el esquema de datos y se programó la lógica en la plantilla `5_acta_nombramiento.html` para convertir meses de manera elegante a años y meses (ej: *2 año(s) y 3 mes(es)*).

### Fase 3: Capa de Datos (Consecutivo Atómico ROS por Tenant)
*   **Problema original**: Riesgo de colisión de consecutivos de Reporte de Operaciones Sospechosas (ROS) al generarse de forma aleatoria o no secuencial.
*   **Solución**: 
    *   Se creó una tabla dedicada `ros_consecutivos` en PostgreSQL con clave primaria compuesta por `(tenant_id, anio)`.
    *   Se implementó una consulta atómica `INSERT ... ON CONFLICT DO UPDATE` en el servicio que autogenera e incrementa el consecutivo en cada llamada en tiempo real, garantizando la unicidad y evitando colisiones de transacciones simultáneas.
    *   El backend inyecta dinámicamente al contexto de Jinja2 los campos `consecutivo_ros` (ej: `ROS-2026-0001`) y `fecha_reporte`.

### Fase 4: Entorno Aislado B2B (`/cda`) y White-Labeling
*   **Problema original**: Ruido e inseguridad en la interfaz al exponer herramientas internas administrativas ("War Room", "Monitoreo Cripto", "Monitoreo Bancario") al cliente final (CDA o Aseguradora).
*   **Solución**:
    1.  **CDALayout**: Se creó una barra de navegación lateral completamente sanitizada con tonos azules corporativos, bajo el banner **"Portal de Cumplimiento SARLAFT - Edición Corporativa"**.
    2.  **Modularización de Deep Search**: Se extrajo el core lógico del buscador a `DeepSearchContent.tsx` para poder reutilizarlo tanto en la vista administrativa como en la corporativa sin duplicar código.
    3.  **Habeas Data (Exclusión de SISBEN)**: Se refinó el orquestador backend para soportar `tipo_consulta` (`SARLAFT_CDA`, `SARLAFT_B2B`, `RRHH`). En consultas comerciales (B2B), se excluye y sanitiza cualquier consulta a SISBEN (resguardando Habeas Data Ley 1581) y RUNT/SIMIT para no generar secciones en blanco en los reportes de empresas.
    4.  **Fábrica Legal (`/cda/onboarding`)**: Se implementó el formulario completo de Onboarding CDA que compila los 7 manuales normativos y descarga nativamente el archivo `Kit_Cumplimiento_SARLAFT_[NIT].zip`.
    5.  **Reportes Historial (`/cda/reports`)**: Se montó la tabla del historial de reportes con filtros por tenant, badges de colores según nivel de riesgo e inicialización de descargas en formato `.pdf`.

### Fase 5: Publicación Segura en GitHub
*   **Repositorio**: Se creó el repositorio público oficial en GitHub: [https://github.com/Miguel1721/sarlaft-modern](https://github.com/Miguel1721/sarlaft-modern).
*   **Seguridad**: Se realizó limpieza quirúrgica de historial desvinculando de forma segura el archivo `backend/.env` del control de versiones usando una rama limpia (`clean-main` ahora renombrada a `main`), previniendo fugas de secretos y bypass de GitHub Secret Scanning mientras el `.env` físico se mantiene intacto y operativo en el servidor de producción.

---

## 3. MAPA DE ARCHIVOS CLAVE Y UBICACIONES
Todos los archivos modificados y creados se encuentran en sus respectivas ubicaciones en el servidor dentro de `/home/ubuntu/LABORATORIO/sarlaft-modern`:

### Capa de Negocio & Controladores (FastAPI)
*   **Onboarding & ROS**: `backend/app/routers/onboarding_router.py`
    *   *Lógica*: Esquema `OnboardingCDA`, validador de apellidos, creación de tabla `ros_consecutivos` y la función atómica `generar_consecutivo_ros`.
*   **Orquestador Multiuso**: `backend/app/services/orchestrator_service.py`
    *   *Lógica*: Mapeo de `tipo_consulta` en la matriz de conectores para omitir dinámicamente SISBEN, SIMIT y RUNT en el flujo B2B.
*   **Generador PDF**: `backend/app/services/pdf_generator.py`
    *   *Lógica*: Inyección de disclaimers de Habeas Data condicionales para perfiles de RRHH.
*   **Ruta API Core**: `backend/app/main.py`
    *   *Lógica*: Mapeo del parámetro `tipo_consulta` en el esquema de request `/api/v1/auditar`.

### Documentación Estática (HTML Templates)
*   Ubicación: `backend/app/templates/sarlaft_docs/`
    *   `1_manual_politica.html` (Manual de Políticas SARLAFT)
    *   `4_procedimiento_dd.html` (Debida Diligencia Estática)
    *   `5_acta_nombramiento.html` (Acta del Oficial con lógica de experiencia de meses a años)
    *   `6_plan_capacitacion.html` (Plan de Capacitación)
    *   `7_formato_ros.html` (ROS automatizado en blanco)

### Capa Frontend (Next.js 16 - App Router)
*   **Layout del CDA**: `frontend/src/components/CDALayout.tsx` *(Menú corporativo sanitizado, color azul).*
*   **Core Reutilizable Deep Search**: `frontend/src/components/DeepSearchContent.tsx` *(Formulario de búsqueda y dictamen inteligente).*
*   **Fábrica Legal (Formulario)**: `frontend/src/components/FabricaLegalContent.tsx` *(Campos completos de CDA, OC, suplente y validación).*
*   **Historial de Consultas**: `frontend/src/components/ReportesContent.tsx` *(Tabla de reportes con descarga y badges).*
*   **Wrapper Layout `/cda`**: `frontend/src/app/cda/layout.tsx`
*   **Dashboard `/cda`**: `frontend/src/app/cda/page.tsx`
*   **Deep Search `/cda/deep-search`**: `frontend/src/app/cda/deep-search/page.tsx`
*   **Onboarding `/cda/onboarding`**: `frontend/src/app/cda/onboarding/page.tsx`
*   **Reportes `/cda/reports`**: `frontend/src/app/cda/reports/page.tsx`

---

## 4. COMANDOS ÚTILES PARA EL MANTENIMIENTO
Todos los comandos deben ejecutarse desde la raíz del proyecto `/home/ubuntu/LABORATORIO/sarlaft-modern` en el servidor:

*   **Verificar logs del frontend**:
    ```bash
    sudo docker compose logs -f frontend --tail=50
    ```
*   **Verificar logs del backend**:
    ```bash
    sudo docker compose logs -f backend --tail=50
    ```
*   **Reconstruir y desplegar cambios en caliente**:
    ```bash
    sudo docker compose up -d --build
    ```
*   **Estado general de contenedores**:
    ```bash
    sudo docker compose ps
    ```

---

## 5. INSTRUCCIONES PARA LA PRÓXIMA SESIÓN (IA INSTRUCTION)
> [!IMPORTANT]
> **Mensaje Directo para el Siguiente Contexto de IA**:
> "Hola. Has sido inicializado en una nueva sesión para continuar el desarrollo del **SARLAFT 4.0 Compliance Engine**. Lee atentamente este archivo `SARLAFT_COMPLIANCE_HANDOFF.md` ubicado en la raíz del proyecto para comprender toda la arquitectura actual y los hitos completados. No alteres las tablas estáticas normativas de los manuales en Jinja2. Respeta la modularidad del `CDALayout` y el componente de `DeepSearchContent` compartido. La API de producción está operativa y respondiendo. Pregúntale al usuario cuál es el siguiente paso del backlog."
