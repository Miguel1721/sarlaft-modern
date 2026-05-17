# COORDINACIÓN CLAUDE - ANTIGRAVITY
# Sistema SARLAFT 4.0 - Desarrollo Paralelo
# Fecha inicio: 2026-05-17

## ESTADO DEL PROYECTO

**Backend (Claude):** ✅ Autenticación COMPLETADA
- JWT tokens (24 horas validez)
- Endpoints: /api/v1/auth/register, /api/v1/auth/login, /api/v1/auth/me
- Modelo actualizado: CDAEmpresa con email y password_hash
- Probado: 200 OK en producción

**Frontend (antigravity):** ✅ Autenticación COMPLETADA
- AuthContext con gestión de tokens JWT
- Páginas premium: /login y /register
- Diseño glassmorphism con Framer Motion
- Botón autocompletar demo (test@cda.com / Test123!)
- Conectado a API: https://sarlaf.agentesia.cloud
- Probado: Flujo login → dashboard funcionando

**Progreso General:** 30% → 50% (2026-05-17 23:00)

## RAMAS GIT

**Claude:** `feature/auth-claude` (Backend)
**antigravity:** `feature/auth-frontend` (Frontend - POR CREAR)

## CHECKPOINTS

### Diario: 9:00 AM y 6:00 PM (Colombia)
- Sincronizar avances
- Merge de branches
- Resolver conflictos

### urgente: Cuando alguien bloquee
- Reportar inmediatamente
- Coordinar solución

---

## TAREAS CLAUDE (BACKEND)

### Día 1 (Hoy - 2026-05-17) ✅ COMPLETADO
- [x] Crear sistema autenticación (JWT, endpoints)
- [x] Probar endpoints en contenedor Docker
- [x] Migración BD para agregar email/password_hash
- [x] Documentar API (INSTRUCCIONES_ANTIGRAVITY.md)
- [x] Coordinar con antigravity para frontend

### Día 2 (Mañana - 2026-05-18) ✅ COMPLETADO
- [x] Implementar logging de consultas históricas en BD
- [x] Crear modelo HistorialConsulta con todos los campos
- [x] Agregar endpoint GET /api/v1/historial (listado con paginación)
- [x] Agregar filtros (por fecha, por tipo, por contraparte, por riesgo)
- [x] Agregar endpoint GET /api/v1/historial/{id} (detalle)
- [x] Agregar endpoint DELETE /api/v1/historial/{id} (eliminar)
- [x] Agregar endpoint GET /api/v1/historial/estadisticas/resumen
- [x] Integrar con endpoint /api/v1/auditar para guardar automáticamente

### Semana 1 (Día 2-7)
- [ ] Servicio de notificaciones por email
- [ ] Sistema de facturación básico
- [ ] Endpoints CRUD contrapartes
- [ ] Panel admin API endpoints
- [ ] Testing de endpoints

---

## TAREAS ANTIGRAVITY (FRONTEND)

### Día 1 (Hoy - 2026-05-17) ✅ COMPLETADO
- [x] Crear rama `feature/auth-claude` (compartida)
- [x] Crear AuthContext con useAuth hook
- [x] Crear página Login: `/login/page.tsx`
- [x] Crear página Register: `/register/page.tsx`
- [x] Conectar con API backend (https://sarlaf.agentesia.cloud)
- [x] Testing de login/register en navegador
- [x] Diseño premium glassmorphism + animaciones
- [x] Botón autocompletar demo credentials

### Día 2 (Mañana - 2026-05-18)
- [ ] Crear página historial: `/cda/historial/page.tsx`
- [ ] Tabla con filtros (fecha, tipo, contraparte)
- [ ] Paginación de resultados
- [ ] Exportar a PDF/Excel

### Semana 1 (Día 2-7)
- [ ] Dashboard admin con métricas
- [ ] Formulario CRUD contrapartes
- [ ] Sistema de notificaciones UI (toast/notifications)
- [ ] Panel de facturación
- [ ] Reportes y estadísticas

---

## ESPECIFICACIONES TÉCNICAS

### Backend API (Claude)
**URL Base:** `http://localhost:8002` (development)

**Endpoints Autenticación:**
```bash
# Registro
POST /api/v1/auth/register
Content-Type: application/json

{
  "nit": "900123456-7",
  "razon_social": "Mi CDA S.A.",
  "email": "admin@micda.com",
  "password": "Password123!",
  "representante_legal": "Juan Pérez"
}

# Login
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "admin@micda.com",
  "password": "Password123!"
}

# Obtener usuario actual
GET /api/v1/auth/me
Authorization: Bearer <token>
```

**Respuestas:**
```json
// Registro/Login exitoso
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}

// Obtener usuario
{
  "nit": "900123456-7",
  "razon_social": "Mi CDA S.A.",
  "email": "admin@micda.com",
  "representante_legal": "Juan Pérez"
}
```

### Frontend (antigravity)

**Stack:**
- Next.js 14 (App Router)
- TypeScript
- Tailwind CSS
- Axios para HTTP requests

**Estructura:**
```
cda/
├── login/
│   └── page.tsx
├── register/
│   └── page.tsx
├── dashboard/
│   └── page.tsx
└── layout.tsx
```

---

## COMUNICACIÓN

**Ubicación:** /home/ubuntu/LABORATORIO/sarlaft-modern

**Archivos compartidos:**
- `COORDINACION.md` (este archivo - actualizar estado)
- `backend-api-spec.json` (especificación API - Claude mantenerá)

**Método:**
- Actualizar este archivo con avances
- Commit con mensajes descriptivos
- Merge diario en main

---

## METAS

**Semana 1:** MVP funcional + autenticación + historial
**Semana 2:** Facturación + admin + testing
**Fin:** Sistema completo 100% listo para comercializar

---

## PRIORIDADES

1. **HIGH:** Autenticación funcionando (Claude ✓, antigravity hoy)
2. **HIGH:** Historial de consultas (Claude: BD, antigravity: UI)
3. **MEDIUM:** Notificaciones (Claude: email, antigravity: UI)
4. **MEDIUM:** Admin panel (antigravity: UI, Claude: API)
5. **LOW:** Facturación (Claude: integración, antigravity: UI)

---

**ÚLTIMA ACTUALIZACIÓN:** 2026-05-17 10:00 AM (Colombia)
**PRÓXIMO CHECKPOINT:** 2026-05-17 6:00 PM (Colombia)
