# 🚀 PLAN DE IMPLEMENTACIÓN COMPLETA - TRABAJO PARALELO

**Fecha:** Mayo 17, 2026
**Estrategia:** Claude + antigravity trabajando simultáneamente
**Objetivo:** Sistema empresarial completo en 2 semanas

---

## 📋 ESTRUCTURA DE TRABAJO PARALELO

### Arquitectura de Independencia:

```
Claude (Backend + Infraestructura)
├── Autenticación JWT
├── Histórico DB
├── API endpoints adicionales
└── Configuración servidor

antigravity (Frontend + Integración)
├── Conectar frontend a backend
├── Dashboard admin
├── Panel de consultas
└── Documentación
```

**Coordinación:**
- Commits a ramas separadas
- Merge diario de avances
- Comunicación cada 2-3 horas

---

## 📅 SEMANA 1 - FUNDAMENTOS (Días 1-5)

### DÍA 1 - Mañana (Claude)

**Tareas Claude:**
- [x] Crear estructura de autenticación
- [ ] Implementar sistema de login
- [ ] Configurar JWT tokens
- [ ] Crear endpoints auth

**Archivos:**
- `backend/app/auth/`
  - `__init__.py`
  - `security.py`
  - `dependencies.py`
  - `router.py`

**Tiempo:** 4 horas

### DÍA 1 - Tarde (antigravity)

**Tareas antigravity:**
- [ ] Crear página de login en frontend
- [ ] Crear página de registro
- [ ] Conectar frontend a API de auth
- [ ] Implementar manejo de sesiones

**Archivos:**
- `frontend/src/app/login/`
- `frontend/src/app/register/`
- `frontend/src/components/auth/`

**Tiempo:** 4 horas

---

### DÍA 2 - Mañana (Claude)

**Tareas Claude:**
- [ ] Implementar guardado de histórico en DB
- [ ] Modificar orchestrator para guardar consultas
- [ ] Crear endpoints de consultas históricas
- [ ] Panel de historial API

**Archivos:**
- `backend/app/services/historial_service.py`
- `backend/app/routers/historial_router.py`

**Tiempo:** 4 horas

### DÍA 2 - Tarde (antigravity)

**Tareas antigravity:**
- [ ] Crear panel de consultas históricas
- [ ] Tabla de auditorías realizadas
- [ ] Filtros por fecha, resultado
- [ ] Descarga de PDFs anteriores

**Archivos:**
- `frontend/src/app/history/`
- `frontend/src/components/consultas/`

**Tiempo:** 4 horas

---

### DÍA 3 - Mañana (Claude)

**Tareas Claude:**
- [ ] Implementar sistema de notificaciones por email
- [ ] Configurar SendGrid/AWS SES
- [ ] Crear templates de emails
- [ ] Email service con PDF adjunto

**Archivos:**
- `backend/app/services/email_service.py`
- `backend/app/templates/`
- Configurar variable de entorno `SMTP_*`

**Tiempo:** 4 horas

### DÍA 3 - Tarde (antigravity)

**Tareas antigravity:**
- [ ] Crear dashboard de administración
- [ ] Panel de estadísticas
- [ ] Métricas de uso
- [ ] Gráficos y visualizaciones

**Archivos:**
- `frontend/src/app/admin/`
- `frontend/src/components/admin/`

**Tiempo:** 4 horas

---

### DÍA 4 - Mañana (Claude)

**Tareas Claude:**
- [ ] Gestión de contrapartes (CRUD)
- [ ] API de contrapartes
- [ ] Validaciones y reglas de negocio
- [ ] Endpoints adicionales

**Archivos:**
- `backend/app/routers/contrapartes_router.py`
- `backend/app/services/contrapartes_service.py`

**Tiempo:** 4 horas

### DÍA 4 - Tarde (antigravity)

**Tareas antigravity:**
- [ ] Formulario de registro de contrapartes
- [ ] Lista de contrapartes
- [ ] Edición de contrapartes
- [ ] Validación de formularios

**Archivos:**
- `frontend/src/app/contrapartes/`
- `frontend/src/components/contrapartes/`

**Tiempo:** 4 horas

---

### DÍA 5 - Integración y Testing (Ambos)

**Mañana (Claude):**
- [ ] Tests unitarios de scrapers
- [ ] Tests de integración API
- [ ] Corregir bugs encontrados
- [ ] Optimizar queries de DB

**Tarde (antigravity):**
- [ ] Tests E2E del frontend
- [ ] Corregir bugs UI
- [ ] Optimizar rendimiento
- [ ] Responsive design

**Coordinación:**
- Merge de cambios
- Testing conjunto
- Documentación de bugs

---

## 📅 SEMANA 2 - PROFESIONALIZACIÓN

### DÍA 6-7 - Facturación (Claude)

**Tareas:**
- [ ] Integrar Stripe/Wompi
- [ ] Sistema de suscripciones
- [ ] Generación de facturas
- [ ] Webhooks de pagos
- [ ] Dashboard de ingresos

**Tiempo:** 12 horas

### DÍA 6-7 - Tests y Optimización (antigravity)

**Tareas:**
- [ ] Suite completa de tests
- [ ] Tests de carga (Locust)
- [ ] Optimización de assets
- [ ] Cache de React Query
- [ ] PWA y offline

**Tiempo:** 12 horas

---

### DÍA 8-9 - Formato CDA Exacto (Claude)

**Tareas:**
- [ ] Revisar Resolución 2325 detalladamente
- [ ] Formato exacto de certificado
- [ ] Campos adicionales requeridos
- [ ] Cadena de custodia
- [ **NO** incluir certificación final (diplomado)

**Tiempo:** 10 horas

### DÍA 8-9 - Documentación Completa (antigravity)

**Tareas:**
- [ ] Manual de usuario para CDAs
- [ ] Video tutorial de onboarding
- [ ] FAQ completa
- [ ] Términos y condiciones
- [ ] Política de privacidad
- [ ] Guía de API

**Tiempo:** 10 horas

---

## 🔧 CÓORDINACIÓN DEL TRABAJO

### Comunicación:

**Cada 2-3 horas:**
- Checkpoint de avance
- Merge de ramas
- Resolución de conflicts
- Ajuste de prioridades

### Git Workflow:

```bash
# Ramas separadas
git checkout -b feature/auth-claude    # Claude
git checkout -b feature/frontend-antigravity  # antigravity

# Cada uno trabaja en su rama

# Merge diario al final del día
git checkout main
git merge feature/auth-claude
git merge feature/frontend-antigravity
git push
```

### Canales de Comunicación:

**Archivo de coordinación:**
- `COORDINACION.md` - Estado de cada tarea
- Actualizado cada 2-3 horas

**Formato:**
```markdown
## [FECHA/HORA] - CHECKPOINT

### Claude:
- ✅ Completado: Autenticación JWT
- 🔄 En progreso: Histórico DB
- ⏸️ Pendiente: Email service

### antigravity:
- ✅ Completado: Login page
- 🔄 En progreso: Register page
- ⏸️ Pendiente: Connect to API

### Bloqueos:
- Ninguno

### Próximo checkpoint: 3 horas
```

---

## 📋 TAREAS ESPECÍFICAS PARA HOY (DÍA 1)

### 🔵 CLAUDE - AUTENTICACIÓN BACKEND

#### Archivo 1: `backend/app/auth/dependencies.py`

```python
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Optional
from pydantic import BaseModel

# Configuración
SECRET_KEY = "tu-clave-secreta-aqui-cambiar"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 horas
REFRESH_TOKEN_EXPIRE_DAYS = 7

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    username: Optional[str] = None
    user_id: Optional[int] = None
    exp: Optional[int] = None
```

#### Archivo 2: `backend/app/auth/security.py`

```python
from passlib.context import CryptContext
from .dependencies import pwd_context, SECRET_KEY, ALGORITHM

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica password"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hashea password"""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    """Crea token de acceso"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
```

#### Archivo 3: `backend/app/auth/router.py`

```python
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import CDAEmpresa
from .security import verify_password, get_password_hash, create_access_token
from pydantic import BaseModel, EmailStr

router = APIRouter(prefix="/auth", tags=["Autenticación"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class RegisterRequest(BaseModel):
    nit: str
    razon_social: str
    email: EmailStr
    password: str
    representante_legal: str

@router.post("/register")
async def register(req: RegisterRequest, db: Session = Depends(get_db)):
    """Registra un nuevo CDA"""
    # Verificar si ya existe
    existing = db.query(CDAEmpresa).filter(CDAEmpresa.nit == req.nit).first()
    if existing:
        raise HTTPException(status_code=400, detail="NIT ya registrado")
    
    # Crear nuevo CDA
    nuevo_cda = CDAEmpresa(
        nit=req.nit,
        razon_social=req.razon_social,
        email=req.email,
        password_hash=get_password_hash(req.password),
        representante_legal=req.representante_legal
    )
    
    db.add(nuevo_cda)
    db.commit()
    db.refresh(nuevo_cda)
    
    # Crear token
    token_data = {"sub": nuevo_cda.nit, "id": nuevo_cda.id}
    access_token = create_access_token(token_data)
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login")
async def login(req: LoginRequest, db: Session = Depends(get_db)):
    """Login de CDA"""
    # Buscar por email
    cda = db.query(CDAEmpresa).filter(CDAEmpresa.email == req.email).first()
    
    if not cda or not verify_password(req.password, cda.password_hash):
        raise HTTPException(
            status_code=401,
            detail="Email o password incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Crear token
    token_data = {"sub": cda.nit, "id": cda.id}
    access_token = create_access_token(token_data)
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me")
async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Obtiene usuario actual"""
    # TODO: Implementar decodificación de token
    return {"message": "Endpoint me"}
```

#### Instalar dependencias:

```bash
pip install python-jose[cryptography] passlib[bcrypt] python-multipart
```

---

### 🟢 ANTIGRAVITY - FRONTEND AUTENTICACIÓN

#### Archivo 1: `frontend/src/app/login/page.tsx`

```typescript
"use client"

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'

export default function LoginPage() {
  const router = useRouter()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError('')

    try {
      const response = await fetch('https://sarlaf.agentesia.cloud/api/v1/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      })

      if (!response.ok) {
        throw new Error('Credenciales inválidas')
      }

      const data = await response.json()
      
      // Guardar token en localStorage
      localStorage.setItem('token', data.access_token)
      localStorage.setItem('user', JSON.stringify({ email }))
      
      // Redirigir al dashboard
      router.push('/cda')
      
    } catch (err: any) {
      setError(err.message || 'Error al iniciar sesión')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="max-w-md w-full space-y-8 p-8">
        <div>
          <h2 className="text-3xl font-bold text-center">Iniciar Sesión</h2>
          <p className="text-center text-gray-600">Portal de Cumplimiento SARLAFT</p>
        </div>

        <form onSubmit={handleSubmit} className="mt-8 space-y-6">
          {error && (
            <div className="bg-red-50 border border-red-200 text-red-600 px-4 py-3 rounded">
              {error}
            </div>
          )}

          <div>
            <label htmlFor="email" className="block text-sm font-medium text-gray-700">
              Email
            </label>
            <input
              id="email"
              type="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            />
          </div>

          <div>
            <label htmlFor="password" className="block text-sm font-medium text-gray-700">
              Contraseña
            </label>
            <input
              id="password"
              type="password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full flex justify-center py-3 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
          >
            {loading ? 'Iniciando sesión...' : 'Iniciar Sesión'}
          </button>

          <div className="text-center">
            <Link href="/cda/register" className="text-indigo-600 hover:text-indigo-500">
              ¿No tienes cuenta? Regístrate
            </Link>
          </div>
        </form>
      </div>
    </div>
  )
}
```

#### Archivo 2: `frontend/src/app/register/page.tsx`

```typescript
"use client"

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'

export default function RegisterPage() {
  const router = useRouter()
  const [formData, setFormData] = useState({
    nit: '',
    razon_social: '',
    email: '',
    password: '',
    confirm_password: '',
    representante_legal: ''
  })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value })
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError('')

    if (formData.password !== formData.confirm_password) {
      setError('Las contraseñas no coinciden')
      setLoading(false)
      return
    }

    try {
      const response = await fetch('https://sarlaf.agentesia.cloud/api/v1/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      })

      if (!response.ok) {
        throw new Error('Error al registrar')
      }

      const data = await response.json()
      
      // Guardar token
      localStorage.setItem('token', data.access_token)
      
      // Redirigir al dashboard
      router.push('/cda')
      
    } catch (err: any) {
      setError(err.message || 'Error al registrar')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="max-w-md w-full space-y-8 p-8">
        <div>
          <h2 className="text-3xl font-bold text-center">Crear Cuenta</h2>
          <p className="text-center text-gray-600">Registro para Centros de Diagnóstico</p>
        </div>

        <form onSubmit={handleSubmit} className="mt-8 space-y-6">
          {error && (
            <div className="bg-red-50 border border-red-200 text-red-600 px-4 py-3 rounded">
              {error}
            </div>
          )}

          <div>
            <label htmlFor="nit" className="block text-sm font-medium text-gray-700">
              NIT
            </label>
            <input
              id="nit"
              name="nit"
              type="text"
              required
              value={formData.nit}
              onChange={handleChange}
              className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            />
          </div>

          <div>
            <label htmlFor="razon_social" className="block text-sm font-medium text-gray-700">
              Razón Social
            </label>
            <input
              id="razon_social"
              name="razon_social"
              type="text"
              required
              value={formData.razon_social}
              onChange={handleChange}
              className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            />
          </div>

          <div>
            <label htmlFor="email" className="block text-sm font-medium text-gray-700">
              Email
            </label>
            <input
              id="email"
              name="email"
              type="email"
              required
              value={formData.email}
              onChange={handleChange}
              className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            />
          </div>

          <div>
            <label htmlFor="password" className="block text-sm font-medium text-gray-700">
              Contraseña
            </label>
            <input
              id="password"
              name="password"
              type="password"
              required
              value={formData.password}
              onChange={handleChange}
              className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            />
          </div>

          <div>
            <label htmlFor="confirm_password" className="block text-sm font-medium text-gray-700">
              Confirmar Contraseña
            </label>
            <input
              id="confirm_password"
              name="confirm_password"
              type="password"
              required
              value={formData.confirm_password}
              onChange={handleChange}
              className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            />
          </div>

          <div>
            <label htmlFor="representante_legal" className="block text-sm font-medium text-gray-700">
              Representante Legal
            </label>
            <input
              id="representante_legal"
              name="representante_legal"
              type="text"
              required
              value={formData.representante_legal}
              onChange={handleChange}
              className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full flex justify-center py-3 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
          >
            {loading ? 'Registrando...' : 'Registrarse'}
          </button>

          <div className="text-center">
            <Link href="/cda/login" className="text-indigo-600 hover:text-indigo-500">
              ¿Ya tienes cuenta? Inicia sesión
            </Link>
          </div>
        </form>
      </div>
    </div>
  )
}
```

---

## 🎯 CHECKPOINTS DEL DÍA

### Checkpoint 1 (11:00 AM - 3 horas):
**Claude:**
- ✅ Autenticación backend implementada
- ✅ Dependencias instaladas
- ✅ Tests de login/register

**antigravity:**
- ✅ Página login creada
- ✅ Página register creada
- ✅ Conexión a API probada

**Merge:** Integrar frontend con backend

---

### Checkpoint 2 (3:00 PM - 6 horas):
**Claude:**
- ✅ Histórico en DB
- ✅ Endpoints de consultas

**antigravity:**
- ✅ Panel de historial
- ✅ Tabla de consultas

**Merge:** Integrar

---

### Checkpoint 3 (6:00 PM - 9 horas):
**Claude:**
- ✅ Email service básico
- ✅ Templates

**antigravity:**
- ✅ Dashboard admin estructura
- ✅ Componentes base

**Merge:** Integrar

---

## 📋 ARCHIVO DE COORDINACIÓN

Crear `/home/ubuntu/LABORATORIO/sarlaft-modern/COORDINACION.md`:

```markdown
# COORDINACIÓN CLAUDE + ANTIGRAVITY

## DÍA 1 - 2026-05-17

### Checkpoint 1 - 11:00 AM

#### ✅ Claude Completado:
- [ ] Autenticación JWT
- [ ] Endpoints /auth/login y /auth/register
- [ ] Pruebas de autenticación

#### ✅ antigravity Completado:
- [ ] Páginas login y register
- [ ] Conexión a API
- [ ] Manejo de errores

#### 🔧 Merge necesario:
- Actualizar router en main.py
- Probar flujo completo login→dashboard

#### ⏸️ Siguiente checkpoint: 3:00 PM
```

---

## 🚀 INICIO AHORA

### Para Claude (Backend):

```bash
cd /home/ubuntu/LABORATORIO/sarlaft-modern/backend

# Crear rama de trabajo
git checkout -b feature/auth-claude

# Instalar dependencias
pip install python-jose[cryptography] passlib[bcrypt] python-multipart

# Crear estructura
mkdir -p app/auth
touch app/auth/__init__.py
touch app/auth/dependencies.py
touch app/auth/security.py
touch app/auth/router.py

# Empezar a implementar
# Usar código de arriba
```

### Para antigravity (Frontend):

```bash
cd /home/ubuntu/LABORATORIO/sarlaft-modern/frontend

# Crear rama de trabajo
git checkout -b feature/auth-frontend

# Crear estructura
mkdir -p src/app/login
mkdir -p src/app/register

# Crear archivos
touch src/app/login/page.tsx
touch src/app/register/page.tsx

# Implementar usando código de arriba
```

---

## 📞 COMUNICACIÓN

**Cada 2-3 horas:**
- Actualizar COORDINACION.md
- Reportar avances
- Merge de cambios si es seguro
- Resolver conflicts si hay

**Fin del día:**
- Merge final a main
- Push a producción
- Testing conjunto

---

**¿Listos para empezar?**

**Claude:** Autenticación backend
**antigravity:** Frontend login/register

**Primer checkpoint en 3 horas** 🚀
