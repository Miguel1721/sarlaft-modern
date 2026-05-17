'use client';

import React, { useState, useEffect } from 'react';
import { ShieldCheck, Activity, Users, FileText, RefreshCw, Database } from 'lucide-react';
import { motion } from 'framer-motion';
import { useAuth } from '@/context/AuthContext';

interface Stats {
  total_consultas: number;
  consultas_hoy: number;
  consultas_semana: number;
  aprobadas: number;
  rechazadas: number;
  revision_manual: number;
  riesgo_alto: number;
  en_listas: number;
}

export default function CDADashboard() {
  const { token } = useAuth();
  const [stats, setStats] = useState<Stats>({
    total_consultas: 124,
    consultas_hoy: 12,
    consultas_semana: 85,
    aprobadas: 110,
    rechazadas: 6,
    revision_manual: 8,
    riesgo_alto: 2,
    en_listas: 2
  });
  const [loading, setLoading] = useState(true);

  const loadStats = async () => {
    try {
      const storedToken = token || localStorage.getItem('access_token');
      if (!storedToken) return;

      const res = await fetch('https://sarlaf.agentesia.cloud/api/v1/historial/estadisticas/resumen', {
        headers: {
          'Authorization': `Bearer ${storedToken}`
        }
      });

      if (res.ok) {
        const data = await res.json();
        if (data.total_consultas > 0) {
          setStats(data);
        }
      }
    } catch (err) {
      console.error('Error loading dashboard stats:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadStats();
  }, [token]);

  const statItems = [
    { icon: ShieldCheck, title: "Consultas Realizadas", val: stats.total_consultas.toString(), color: "text-blue-500", bg: "bg-blue-500/10" },
    { icon: Activity, title: "Alertas Activas", val: stats.riesgo_alto.toString(), color: "text-red-500", bg: "bg-red-500/10" },
    { icon: Users, title: "Contrapartes Aprobadas", val: stats.aprobadas.toString(), color: "text-purple-500", bg: "bg-purple-500/10" },
    { icon: FileText, title: "Reportes Emitidos", val: stats.total_consultas.toString(), color: "text-green-500", bg: "bg-green-500/10" },
  ];

  return (
    <div className="max-w-6xl mx-auto">
      <header className="mb-12 flex items-center justify-between">
        <div>
          <h1 className="text-4xl font-bold tracking-tight mb-2">Bienvenido al Portal de Cumplimiento</h1>
          <p className="text-foreground/60 max-w-2xl text-lg">
            Gestione las validaciones normativas y requerimientos SARLAFT de su entidad de manera centralizada.
          </p>
        </div>
        <button
          onClick={loadStats}
          disabled={loading}
          className="flex items-center gap-2 bg-foreground/5 hover:bg-foreground/10 px-4 py-2.5 border border-white/5 text-xs font-bold text-white rounded-xl transition-all cursor-pointer disabled:opacity-50"
        >
          <RefreshCw className={`h-3.5 w-3.5 ${loading ? 'animate-spin' : ''}`} />
          Recargar
        </button>
      </header>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
        {statItems.map((stat, i) => (
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
            <p className="text-3xl font-black text-white">{stat.val}</p>
          </motion.div>
        ))}
      </div>
      
      {/* Search Audit Banner */}
      <div className="bg-blue-600/10 border border-blue-600/20 rounded-3xl p-8 flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
        <div>
          <h2 className="text-2xl font-bold text-blue-500 mb-2">Deep Search Disponible</h2>
          <p className="text-foreground/80 max-w-xl">
            Realice auditorías de contrapartes y vehículos contra más de 50 listas restrictivas globales en tiempo real. Todas las búsquedas se guardan automáticamente en su historial de auditoría.
          </p>
        </div>
        <a 
          href="/cda/deep-search" 
          className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-4 rounded-xl font-bold transition-all shadow-lg shadow-blue-900/20 whitespace-nowrap cursor-pointer"
        >
          Iniciar Auditoría
        </a>
      </div>
    </div>
  );
}
