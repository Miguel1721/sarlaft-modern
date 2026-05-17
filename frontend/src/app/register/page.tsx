'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { ShieldCheck, Mail, Lock, Building2, User, Landmark, AlertCircle } from 'lucide-react';
import { motion } from 'framer-motion';
import { useAuth } from '@/context/AuthContext';

export default function RegisterPage() {
  const [nit, setNit] = useState('');
  const [razonSocial, setRazonSocial] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [representanteLegal, setRepresentanteLegal] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const { register, error, setError, user } = useAuth();
  const router = useRouter();

  // Redirect if already authenticated
  useEffect(() => {
    if (user) {
      router.push('/cda');
    }
  }, [user, router]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!nit || !razonSocial || !email || !password || !representanteLegal) {
      setError('Por favor complete todos los campos obligatorios.');
      return;
    }

    setSubmitting(true);
    const success = await register({
      nit,
      razon_social: razonSocial,
      email,
      password,
      representante_legal: representanteLegal
    });
    setSubmitting(false);

    if (success) {
      router.push('/cda');
    }
  };

  return (
    <div className="min-h-screen bg-[#050508] text-foreground flex items-center justify-center p-6 relative overflow-hidden">
      {/* Decorative Radial Gradients */}
      <div className="absolute top-1/4 left-1/4 w-[500px] h-[500px] bg-blue-600/10 rounded-full blur-[120px] pointer-events-none" />
      <div className="absolute bottom-1/4 right-1/4 w-[400px] h-[400px] bg-indigo-600/10 rounded-full blur-[100px] pointer-events-none" />

      <motion.div 
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="w-full max-w-lg"
      >
        {/* Brand Header */}
        <div className="flex flex-col items-center mb-6 text-center">
          <div className="h-12 w-12 rounded-2xl bg-blue-600 flex items-center justify-center shadow-lg shadow-blue-500/30 mb-4 border border-blue-400/20">
            <ShieldCheck className="h-6 w-6 text-white" />
          </div>
          <h1 className="text-3xl font-black tracking-tight bg-gradient-to-r from-white via-white to-blue-400 bg-clip-text text-transparent">
            REGISTRO CORPORATIVO
          </h1>
          <p className="text-foreground/50 text-sm mt-1 uppercase tracking-widest font-bold text-[10px]">
            Creación de Cuenta SARLAFT 4.0
          </p>
        </div>

        {/* Register Glassmorphic Card */}
        <div className="glass p-8 rounded-3xl border border-white/10 shadow-2xl relative overflow-hidden">
          <div className="absolute top-0 left-0 w-full h-[2px] bg-gradient-to-r from-transparent via-blue-500/50 to-transparent" />
          
          <h2 className="text-xl font-bold mb-6 text-center">Registro de CDA / Empresa</h2>

          <form onSubmit={handleSubmit} className="space-y-4">
            {error && (
              <motion.div 
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: 'auto' }}
                className="p-4 rounded-xl bg-red-500/10 border border-red-500/20 text-red-400 text-xs flex items-start gap-2.5"
              >
                <AlertCircle className="h-4 w-4 shrink-0 mt-0.5" />
                <span>{error}</span>
              </motion.div>
            )}

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {/* NIT Field */}
              <div>
                <label className="block text-[10px] font-bold text-foreground/40 mb-2 uppercase tracking-wider">NIT de la Empresa *</label>
                <div className="relative">
                  <span className="absolute left-4 top-1/2 -translate-y-1/2 text-foreground/30">
                    <Landmark className="h-4 w-4" />
                  </span>
                  <input 
                    type="text"
                    value={nit}
                    onChange={(e) => setNit(e.target.value)}
                    placeholder="900123456-1"
                    className="w-full bg-white/5 border border-white/10 hover:border-white/20 focus:border-blue-500 rounded-xl pl-11 pr-4 py-3 focus:outline-none transition-all text-xs text-white"
                  />
                </div>
              </div>

              {/* Razon Social Field */}
              <div>
                <label className="block text-[10px] font-bold text-foreground/40 mb-2 uppercase tracking-wider">Razón Social *</label>
                <div className="relative">
                  <span className="absolute left-4 top-1/2 -translate-y-1/2 text-foreground/30">
                    <Building2 className="h-4 w-4" />
                  </span>
                  <input 
                    type="text"
                    value={razonSocial}
                    onChange={(e) => setRazonSocial(e.target.value)}
                    placeholder="CDA de Prueba SAS"
                    className="w-full bg-white/5 border border-white/10 hover:border-white/20 focus:border-blue-500 rounded-xl pl-11 pr-4 py-3 focus:outline-none transition-all text-xs text-white"
                  />
                </div>
              </div>
            </div>

            {/* Representante Legal Field */}
            <div>
              <label className="block text-[10px] font-bold text-foreground/40 mb-2 uppercase tracking-wider">Representante Legal *</label>
              <div className="relative">
                <span className="absolute left-4 top-1/2 -translate-y-1/2 text-foreground/30">
                  <User className="h-4 w-4" />
                </span>
                <input 
                  type="text"
                  value={representanteLegal}
                  onChange={(e) => setRepresentanteLegal(e.target.value)}
                  placeholder="Nombre del Representante"
                  className="w-full bg-white/5 border border-white/10 hover:border-white/20 focus:border-blue-500 rounded-xl pl-11 pr-4 py-3 focus:outline-none transition-all text-xs text-white"
                />
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {/* Email Field */}
              <div>
                <label className="block text-[10px] font-bold text-foreground/40 mb-2 uppercase tracking-wider">Correo Electrónico *</label>
                <div className="relative">
                  <span className="absolute left-4 top-1/2 -translate-y-1/2 text-foreground/30">
                    <Mail className="h-4 w-4" />
                  </span>
                  <input 
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="correo@empresa.com"
                    className="w-full bg-white/5 border border-white/10 hover:border-white/20 focus:border-blue-500 rounded-xl pl-11 pr-4 py-3 focus:outline-none transition-all text-xs text-white"
                  />
                </div>
              </div>

              {/* Password Field */}
              <div>
                <label className="block text-[10px] font-bold text-foreground/40 mb-2 uppercase tracking-wider">Contraseña *</label>
                <div className="relative">
                  <span className="absolute left-4 top-1/2 -translate-y-1/2 text-foreground/30">
                    <Lock className="h-4 w-4" />
                  </span>
                  <input 
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="••••••••"
                    className="w-full bg-white/5 border border-white/10 hover:border-white/20 focus:border-blue-500 rounded-xl pl-11 pr-4 py-3 focus:outline-none transition-all text-xs text-white"
                  />
                </div>
              </div>
            </div>

            {/* Action Submit Button */}
            <button 
              type="submit"
              disabled={submitting}
              className="w-full bg-blue-600 hover:bg-blue-500 disabled:opacity-50 text-white font-bold py-3.5 rounded-xl transition-all shadow-lg shadow-blue-900/20 flex items-center justify-center gap-2 text-sm font-semibold mt-6 cursor-pointer"
            >
              {submitting ? (
                <>
                  <div className="h-4 w-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                  Registrando Empresa...
                </>
              ) : (
                'Registrarse y Crear Cuenta'
              )}
            </button>
          </form>

          {/* Redirection Link */}
          <div className="text-center mt-6 pt-6 border-t border-white/5 text-xs text-foreground/40">
            ¿Ya tiene una cuenta corporativa?{' '}
            <Link href="/login" className="text-blue-500 hover:text-blue-400 font-bold transition-colors">
              Iniciar Sesión
            </Link>
          </div>
        </div>
      </motion.div>
    </div>
  );
}
