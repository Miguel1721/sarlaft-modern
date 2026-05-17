# INSTRUCCIONES PARA ANTIGRAVITY
# Frontend Autenticación SARLAFT 4.0
# Fecha: 2026-05-17

## OBJETIVO

Crear las páginas de autenticación (Login y Registro) del frontend que se conecten con el backend API que ya implementé.

---

## PASO 1: CONFIGURAR ENTORNO

### 1.1 Crear rama de trabajo

```bash
cd /home/ubuntu/LABORATORIO/sarlaft-modern

# Crear rama para frontend auth
git checkout -b feature/auth-frontend

# Verificar que estás en la rama correcta
git branch
```

### 1.2 Instalar dependencias necesarias

```bash
cd /home/ubuntu/LABORATORIO/sarlaft-modern/frontend

# Instalar Axios para HTTP requests
npm install axios

# Instalar hooks de React si no están
npm install react-hook-form @hookform/resolvers zod
```

---

## PASO 2: CREAR SERVICIO API

### 2.1 Crear archivo para configuración de Axios

**Archivo:** `/home/ubuntu/LABORATORIO/sarlaft-modern/frontend/src/lib/api.ts`

```typescript
import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8002';

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para agregar token JWT
api.interceptors.request.use((config) => {
  if (typeof window !== 'undefined') {
    const token = localStorage.getItem('sarlaft_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
  }
  return config;
});

// Interceptor para manejar errores
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expirado o inválido
      if (typeof window !== 'undefined') {
        localStorage.removeItem('sarlaft_token');
        window.location.href = '/cda/login';
      }
    }
    return Promise.reject(error);
  }
);

// Tipo de respuesta de autenticación
export interface AuthResponse {
  access_token: string;
  token_type: string;
}

// Tipo de usuario
export interface CDAUser {
  nit: string;
  razon_social: string;
  email: string;
  representante_legal: string;
}

// API de autenticación
export const authAPI = {
  register: async (data: {
    nit: string;
    razon_social: string;
    email: string;
    password: string;
    representante_legal: string;
  }): Promise<AuthResponse> => {
    const response = await api.post<AuthResponse>('/api/v1/auth/register', data);
    return response.data;
  },

  login: async (email: string, password: string): Promise<AuthResponse> => {
    const response = await api.post<AuthResponse>('/api/v1/auth/login', {
      email,
      password,
    });
    return response.data;
  },

  me: async (): Promise<CDAUser> => {
    const response = await api.get<CDAUser>('/api/v1/auth/me');
    return response.data;
  },
};
```

---

## PASO 3: CREAR PÁGINA DE REGISTRO

### 3.1 Crear archivo de registro

**Archivo:** `/home/ubuntu/LABORATORIO/sarlaft-modern/frontend/src/app/cda/register/page.tsx`

```typescript
'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { authAPI } from '@/lib/api';

export default function RegisterPage() {
  const router = useRouter();
  const [formData, setFormData] = useState({
    nit: '',
    razon_social: '',
    email: '',
    password: '',
    confirmPassword: '',
    representante_legal: '',
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    // Validaciones
    if (formData.password !== formData.confirmPassword) {
      setError('Las contraseñas no coinciden');
      return;
    }

    if (formData.password.length < 8) {
      setError('La contraseña debe tener al menos 8 caracteres');
      return;
    }

    setLoading(true);

    try {
      const response = await authAPI.register({
        nit: formData.nit,
        razon_social: formData.razon_social,
        email: formData.email,
        password: formData.password,
        representante_legal: formData.representante_legal,
      });

      // Guardar token
      localStorage.setItem('sarlaft_token', response.access_token);

      // Redirigir al dashboard
      router.push('/cda/dashboard');
    } catch (err: any) {
      setError(
        err.response?.data?.detail || 'Error al registrar. Verifica los datos.'
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
            Registro CDA - SARLAFT 4.0
          </h2>
          <p className="mt-2 text-center text-sm text-gray-600">
            Sistema de Debida Diligencia Automotriz
          </p>
        </div>

        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
          {error && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
              {error}
            </div>
          )}

          <div className="space-y-4">
            <div>
              <label htmlFor="nit" className="block text-sm font-medium text-gray-700">
                NIT *
              </label>
              <input
                id="nit"
                name="nit"
                type="text"
                required
                className="mt-1 appearance-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm"
                placeholder="900123456-7"
                value={formData.nit}
                onChange={handleChange}
              />
            </div>

            <div>
              <label htmlFor="razon_social" className="block text-sm font-medium text-gray-700">
                Razón Social *
              </label>
              <input
                id="razon_social"
                name="razon_social"
                type="text"
                required
                className="mt-1 appearance-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm"
                placeholder="Mi CDA S.A."
                value={formData.razon_social}
                onChange={handleChange}
              />
            </div>

            <div>
              <label htmlFor="representante_legal" className="block text-sm font-medium text-gray-700">
                Representante Legal *
              </label>
              <input
                id="representante_legal"
                name="representante_legal"
                type="text"
                required
                className="mt-1 appearance-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm"
                placeholder="Juan Pérez"
                value={formData.representante_legal}
                onChange={handleChange}
              />
            </div>

            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-700">
                Email *
              </label>
              <input
                id="email"
                name="email"
                type="email"
                required
                className="mt-1 appearance-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm"
                placeholder="admin@micda.com"
                value={formData.email}
                onChange={handleChange}
              />
            </div>

            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-700">
                Contraseña *
              </label>
              <input
                id="password"
                name="password"
                type="password"
                required
                className="mt-1 appearance-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm"
                placeholder="Mínimo 8 caracteres"
                value={formData.password}
                onChange={handleChange}
              />
            </div>

            <div>
              <label htmlFor="confirmPassword" className="block text-sm font-medium text-gray-700">
                Confirmar Contraseña *
              </label>
              <input
                id="confirmPassword"
                name="confirmPassword"
                type="password"
                required
                className="mt-1 appearance-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm"
                placeholder="Repite tu contraseña"
                value={formData.confirmPassword}
                onChange={handleChange}
              />
            </div>
          </div>

          <div>
            <button
              type="submit"
              disabled={loading}
              className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? 'Registrando...' : 'Registrarse'}
            </button>
          </div>

          <div className="text-center">
            <span className="text-sm text-gray-600">
              ¿Ya tienes cuenta?{' '}
              <Link href="/cda/login" className="font-medium text-blue-600 hover:text-blue-500">
                Inicia sesión
              </Link>
            </span>
          </div>
        </form>
      </div>
    </div>
  );
}
```

---

## PASO 4: CREAR PÁGINA DE LOGIN

### 4.1 Crear archivo de login

**Archivo:** `/home/ubuntu/LABORATORIO/sarlaft-modern/frontend/src/app/cda/login/page.tsx`

```typescript
'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { authAPI } from '@/lib/api';

export default function LoginPage() {
  const router = useRouter();
  const [formData, setFormData] = useState({
    email: '',
    password: '',
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await authAPI.login(
        formData.email,
        formData.password
      );

      // Guardar token
      localStorage.setItem('sarlaft_token', response.access_token);

      // Redirigir al dashboard
      router.push('/cda/dashboard');
    } catch (err: any) {
      setError(
        err.response?.data?.detail || 'Email o contraseña incorrectos'
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
            Iniciar Sesión - SARLAFT 4.0
          </h2>
          <p className="mt-2 text-center text-sm text-gray-600">
            Sistema de Debida Diligencia Automotriz
          </p>
        </div>

        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
          {error && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
              {error}
            </div>
          )}

          <div className="space-y-4">
            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-700">
                Email
              </label>
              <input
                id="email"
                name="email"
                type="email"
                required
                className="mt-1 appearance-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm"
                placeholder="admin@micda.com"
                value={formData.email}
                onChange={handleChange}
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
                className="mt-1 appearance-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm"
                placeholder="Tu contraseña"
                value={formData.password}
                onChange={handleChange}
              />
            </div>
          </div>

          <div>
            <button
              type="submit"
              disabled={loading}
              className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? 'Iniciando sesión...' : 'Iniciar Sesión'}
            </button>
          </div>

          <div className="text-center">
            <span className="text-sm text-gray-600">
              ¿No tienes cuenta?{' '}
              <Link href="/cda/register" className="font-medium text-blue-600 hover:text-blue-500">
                Regístrate aquí
              </Link>
            </span>
          </div>
        </form>
      </div>
    </div>
  );
}
```

---

## PASO 5: PROBAR LOCALMENTE

### 5.1 Iniciar servidor de desarrollo

```bash
cd /home/ubuntu/LABORATORIO/sarlaft-modern/frontend

# Asegurarse de que el backend esté corriendo
# El backend debe estar en: http://localhost:8002

# Iniciar frontend
npm run dev
```

### 5.2 Probar registro

1. Abrir navegador: `http://localhost:3000/cda/register`
2. Llenar formulario:
   - NIT: 900123456-7
   - Razón Social: CDA de Prueba S.A.
   - Representante Legal: Juan Pérez
   - Email: test@micda.com
   - Contraseña: Password123!
3. Click en "Registrarse"
4. Debería redirigir a `/cda/dashboard`

### 5.3 Probar login

1. Abrir navegador: `http://localhost:3000/cda/login`
2. Ingresar:
   - Email: test@micda.com
   - Contraseña: Password123!
3. Click en "Iniciar Sesión"
4. Debería redirigir a `/cda/dashboard`

---

## PASO 6: COMMITEAR CAMBIOS

```bash
cd /home/ubuntu/LABORATORIO/sarlaft-modern

# Agregar cambios
git add frontend/src/lib/api.ts
git add frontend/src/app/cda/register/page.tsx
git add frontend/src/app/cda/login/page.tsx

# Commitear
git commit -m "feat(frontend): Add authentication pages (login + register)

- Create API service with Axios
- Implement login page (/cda/login)
- Implement register page (/cda/register)
- Connect to backend API endpoints
- Add JWT token management in localStorage
- Add form validation
- Add error handling

Co-Authored-By: antigravity <antigravity@antigravity.com>"

# Hacer push a remoto
git push origin feature/auth-frontend
```

---

## PASO 7: NOTIFICAR A CLAUDE

Una vez terminado:

1. **Actualizar COORDINACION.md** marcando tareas completadas
2. **Notificar** a Claude que el frontend está listo
3. **Hacer merge** de ambas ramas a main

---

## DUDAS O PROBLEMAS

**Backend no responde:**
- Verificar que el contenedor `sarlaft-ocr-api` esté corriendo
- Verificar que el puerto 8002 esté disponible
- Revisar logs: `docker logs sarlaft-ocr-api`

**Error de CORS:**
- Claude ya agregó CORS middleware en backend
- Si persiste, reportar a Claude

**Tokens no funcionan:**
- Verificar que el backend tenga la misma SECRET_KEY
- Revisar localStorage del navegador
- Usar DevTools > Application > Local Storage

---

## SIGUIENTES PASOS (DESPUÉS DE AUTH)

Una vez autenticación funcionando:

1. Crear `/cda/dashboard/page.tsx` (panel principal)
2. Crear `/cda/historial/page.tsx` (historial de consultas)
3. Crear `/cda/admin/page.tsx` (panel administrativo)
4. Integrar con los scrapers existentes

---

**ÉXITO ANTIGRAVITY!** 🚀

Cualquier duda, revisar COORDINACION.md o preguntar a Claude.
