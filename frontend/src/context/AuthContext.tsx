'use client';

import React, { createContext, useContext, useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';

interface User {
  id: number;
  nit: string;
  razon_social: string;
  email: string;
  representante_legal?: string;
}

interface AuthContextType {
  user: User | null;
  token: string | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<boolean>;
  register: (data: { nit: string; razon_social: string; email: string; password: string; representante_legal: string }) => Promise<boolean>;
  logout: () => void;
  error: string | null;
  setError: (err: string | null) => void;
}

const AuthContext = createContext<AuthContextType | null>(null);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

  // Restore session on load
  useEffect(() => {
    async function restoreSession() {
      if (typeof window === 'undefined') return;
      const storedToken = localStorage.getItem('access_token');
      if (!storedToken) {
        setLoading(false);
        return;
      }

      try {
        setToken(storedToken);
        const res = await fetch('https://sarlaf.agentesia.cloud/api/v1/auth/me', {
          headers: {
            'Authorization': `Bearer ${storedToken}`
          }
        });

        if (res.ok) {
          const userData = await res.json();
          setUser(userData);
        } else {
          // Token expired or invalid
          localStorage.removeItem('access_token');
          setToken(null);
          setUser(null);
        }
      } catch (err) {
        console.error('Error restoring session:', err);
      } finally {
        setLoading(false);
      }
    }

    restoreSession();
  }, []);

  const login = async (email: string, password: string): Promise<boolean> => {
    setError(null);
    setLoading(true);
    try {
      const res = await fetch('https://sarlaf.agentesia.cloud/api/v1/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      });

      if (!res.ok) {
        const data = await res.json();
        setError(data.detail || 'Email o contraseña incorrectos.');
        setLoading(false);
        return false;
      }

      const data = await res.json();
      const token = data.access_token;
      
      if (typeof window !== 'undefined') {
        localStorage.setItem('access_token', token);
      }
      setToken(token);

      // Fetch user info
      const meRes = await fetch('https://sarlaf.agentesia.cloud/api/v1/auth/me', {
        headers: { 'Authorization': `Bearer ${token}` }
      });

      if (meRes.ok) {
        const userData = await meRes.json();
        setUser(userData);
      }

      setLoading(false);
      return true;
    } catch (err) {
      setError('Error al conectar con el servidor.');
      setLoading(false);
      return false;
    }
  };

  const register = async (regData: { nit: string; razon_social: string; email: string; password: string; representante_legal: string }): Promise<boolean> => {
    setError(null);
    setLoading(true);
    try {
      const res = await fetch('https://sarlaf.agentesia.cloud/api/v1/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(regData)
      });

      if (!res.ok) {
        const data = await res.json();
        setError(data.detail || 'Error al registrar la empresa.');
        setLoading(false);
        return false;
      }

      const data = await res.json();
      const token = data.access_token;

      if (typeof window !== 'undefined') {
        localStorage.setItem('access_token', token);
      }
      setToken(token);

      // Fetch user info
      const meRes = await fetch('https://sarlaf.agentesia.cloud/api/v1/auth/me', {
        headers: { 'Authorization': `Bearer ${token}` }
      });

      if (meRes.ok) {
        const userData = await meRes.json();
        setUser(userData);
      }

      setLoading(false);
      return true;
    } catch (err) {
      setError('Error al registrar.');
      setLoading(false);
      return false;
    }
  };

  const logout = () => {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('access_token');
    }
    setToken(null);
    setUser(null);
    router.push('/login');
  };

  return (
    <AuthContext.Provider value={{ user, token, loading, login, register, logout, error, setError }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
