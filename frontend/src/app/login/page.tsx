'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { ShieldCheck, Mail, Lock, AlertCircle, Sparkles } from 'lucide-react';
import { motion } from 'framer-motion';
import { useAuth } from '@/context/AuthContext';

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const { login, error, setError, user } = useAuth();
  const router = useRouter();

  // Redirect if already authenticated
  useEffect(() => {
    if (user) {
      router.push('/cda');
    }
  }, [user, router]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!email || !password) {
      setError('Por favor complete todos los campos.');
      return;
    }

    setSubmitting(true);
    const success = await login(email, password);
    setSubmitting(false);

    if (success) {
      router.push('/cda');
    }
  };

  const handleFillDemo = () => {
    setEmail('test@cda.com');
    setPassword('Test123!');
    setError(null);
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
        className="w-full max-w-md"
      >
        {/* Brand Header */}
        <div className="flex flex-col items-center mb-8 text-center">
          <div className="h-12 w-12 rounded-2xl bg-blue-600 flex items-center justify-center shadow-lg shadow-blue-500/30 mb-4 border border-blue-400/20">
            <ShieldCheck className="h-6 w-6 text-white" />
          </div>
          <h1 className="text-3xl font-black tracking-tight bg-gradient-to-r from-white via-white to-blue-400 bg-clip-text text-transparent">
            PORTAL SARLAFT
          </h1>
          <p className="text-foreground/50 text-sm mt-1 uppercase tracking-widest font-bold text-[10px]">
            Edición Corporativa CDA
          </p>
        </div>

        {/* Login Glassmorphic Card */}
        <div className="glass p-8 rounded-3xl border border-white/10 shadow-2xl relative overflow-hidden">
          <div className="absolute top-0 left-0 w-full h-[2px] bg-gradient-to-r from-transparent via-blue-500/50 to-transparent" />
          
          <h2 className="text-xl font-bold mb-6 text-center">Iniciar Sesión</h2>

          <form onSubmit={handleSubmit} className="space-y-5">
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

            {/* Email Field */}
            <div>
              <label className="block text-[10px] font-bold text-foreground/40 mb-2 uppercase tracking-wider">Correo Electrónico</label>
              <div className="relative">
                <span className="absolute left-4 top-1/2 -translate-y-1/2 text-foreground/30">
                  <Mail className="h-4 w-4" />
                </span>
                <input 
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="ejemplo@cda.com"
                  className="w-full bg-white/5 border border-white/10 hover:border-white/20 focus:border-blue-500 rounded-xl pl-11 pr-4 py-3.5 focus:outline-none transition-all text-sm text-white"
                />
              </div>
            </div>

            {/* Password Field */}
            <div>
              <label className="block text-[10px] font-bold text-foreground/40 mb-2 uppercase tracking-wider">Contraseña</label>
              <div className="relative">
                <span className="absolute left-4 top-1/2 -translate-y-1/2 text-foreground/30">
                  <Lock className="h-4 w-4" />
                </span>
                <input 
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="••••••••"
                  className="w-full bg-white/5 border border-white/10 hover:border-white/20 focus:border-blue-500 rounded-xl pl-11 pr-4 py-3.5 focus:outline-none transition-all text-sm text-white"
                />
              </div>
            </div>

            {/* Action Buttons */}
            <button 
              type="submit"
              disabled={submitting}
              className="w-full bg-blue-600 hover:bg-blue-500 disabled:opacity-50 text-white font-bold py-3.5 rounded-xl transition-all shadow-lg shadow-blue-900/20 flex items-center justify-center gap-2 text-sm font-semibold mt-6 cursor-pointer"
            >
              {submitting ? (
                <>
                  <div className="h-4 w-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                  Ingresando...
                </>
              ) : (
                'Iniciar Sesión'
              )}
            </button>

            {/* Autocompleter Demo Button */}
            <button 
              type="button"
              onClick={handleFillDemo}
              className="w-full flex items-center justify-center gap-2 py-3 rounded-xl border border-dashed border-blue-500/20 hover:border-blue-500/40 bg-blue-500/5 hover:bg-blue-500/10 text-blue-400 text-xs font-bold transition-all mt-4 cursor-pointer"
            >
              <Sparkles className="h-3.5 w-3.5 text-blue-400 animate-pulse" />
              Autocompletar CDA Demo (test@cda.com)
            </button>
          </form>

          {/* Redirection Link */}
          <div className="text-center mt-6 pt-6 border-t border-white/5 text-xs text-foreground/40">
            ¿No tiene una cuenta corporativa?{' '}
            <Link href="/register" className="text-blue-500 hover:text-blue-400 font-bold transition-colors">
              Registrar CDA
            </Link>
          </div>
        </div>
      </motion.div>
    </div>
  );
}
