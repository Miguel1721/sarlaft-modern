'use client';
import React from 'react';
import Sidebar from '@/components/Sidebar';
import { Settings, Shield, User, Bell, Database, Lock } from 'lucide-react';
import { motion } from 'framer-motion';

export default function SettingsPage() {
  return (
    <Sidebar>
      <div className="max-w-4xl mx-auto">
        <header className="mb-12">
          <div className="flex items-center gap-4 mb-2">
            <div className="p-3 rounded-2xl bg-blue-500/10 border border-blue-500/20">
              <Settings className="h-8 w-8 text-blue-500" />
            </div>
            <h1 className="text-4xl font-bold tracking-tight">Configuración <span className="text-white/40">/ Sistema</span></h1>
          </div>
          <p className="text-white/60">
            Gestiona los parámetros de seguridad, modelos de IA y preferencias del oficial de cumplimiento.
          </p>
        </header>

        <div className="space-y-6">
          {[
            { icon: User, title: 'Perfil de Usuario', desc: 'Gestiona tus datos personales y roles de acceso.' },
            { icon: Shield, title: 'Seguridad SARLAFT', desc: 'Ajusta los umbrales de riesgo y reglas de bloqueo automático.', active: true },
            { icon: Bell, title: 'Notificaciones', desc: 'Configura alertas por WhatsApp, Email y Slack.' },
            { icon: Database, title: 'Modelos de IA', desc: 'Verifica el estado de los modelos XGBoost y Anthropic.' },
            { icon: Lock, title: 'API & Integraciones', desc: 'Gestión de llaves API y Webhooks externos.' },
          ].map((item, i) => (
            <motion.div 
              key={i}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.1 }}
              className={`glass p-6 rounded-3xl border ${item.active ? 'border-blue-500/30 bg-blue-500/5' : 'border-white/5'} flex items-center justify-between group cursor-pointer hover:bg-white/[0.02] transition-all`}
            >
              <div className="flex items-center gap-4">
                <div className={`p-3 rounded-xl ${item.active ? 'bg-blue-500/20 text-blue-500' : 'bg-white/5 text-white/40 group-hover:text-white transition-colors'}`}>
                  <item.icon className="h-6 w-6" />
                </div>
                <div>
                  <h3 className="font-bold">{item.title}</h3>
                  <p className="text-xs text-white/40">{item.desc}</p>
                </div>
              </div>
              <button className="text-xs font-bold text-white/20 uppercase tracking-widest group-hover:text-blue-500 transition-colors">Configurar</button>
            </motion.div>
          ))}
        </div>
      </div>
    </Sidebar>
  );
}
