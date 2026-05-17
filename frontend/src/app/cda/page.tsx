'use client';

import React from 'react';
import { ShieldCheck, Activity, Users, FileText } from 'lucide-react';
import { motion } from 'framer-motion';

export default function CDADashboard() {
  return (
    <div className="max-w-6xl mx-auto">
      <header className="mb-12">
        <h1 className="text-4xl font-bold tracking-tight mb-2">Bienvenido al Portal de Cumplimiento</h1>
        <p className="text-foreground/60 max-w-2xl text-lg">
          Gestione las validaciones normativas y requerimientos SARLAFT de su entidad de manera centralizada.
        </p>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
        {[
          { icon: ShieldCheck, title: "Consultas Realizadas", val: "124", color: "text-blue-500", bg: "bg-blue-500/10" },
          { icon: Activity, title: "Alertas Activas", val: "2", color: "text-red-500", bg: "bg-red-500/10" },
          { icon: Users, title: "Contrapartes", val: "89", color: "text-purple-500", bg: "bg-purple-500/10" },
          { icon: FileText, title: "Reportes Emitidos", val: "124", color: "text-green-500", bg: "bg-green-500/10" },
        ].map((stat, i) => (
          <motion.div 
            key={i}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.1 }}
            className="glass p-6 rounded-3xl border border-foreground/10 hover:border-blue-500/30 transition-all"
          >
            <div className={`p-3 rounded-xl ${stat.bg} w-max mb-4`}>
              <stat.icon className={`h-6 w-6 ${stat.color}`} />
            </div>
            <h3 className="text-sm font-bold text-foreground/40 uppercase tracking-wider mb-1">{stat.title}</h3>
            <p className="text-3xl font-black">{stat.val}</p>
          </motion.div>
        ))}
      </div>
      
      <div className="bg-blue-600/10 border border-blue-600/20 rounded-3xl p-8 flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-blue-500 mb-2">Deep Search Disponible</h2>
          <p className="text-foreground/80">Realice auditorías de contrapartes y vehículos contra más de 50 listas restrictivas globales en tiempo real.</p>
        </div>
        <a href="/cda/deep-search" className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-4 rounded-xl font-bold transition-all shadow-lg shadow-blue-900/20 whitespace-nowrap">
          Iniciar Auditoría
        </a>
      </div>
    </div>
  );
}
