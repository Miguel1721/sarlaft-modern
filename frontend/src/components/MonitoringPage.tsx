'use client';
import React, { useState, useEffect } from 'react';
import Sidebar from '@/components/Sidebar';
import { Activity, ShieldAlert, TrendingUp, Clock, Search, Database } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

export default function MonitoringPage({ ecosystem }: { ecosystem: string }) {
  const [alerts, setAlerts] = useState<any[]>([]);

  useEffect(() => {
    const eventSource = new EventSource(`/api/monitoring/stream/${ecosystem}`);
    eventSource.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setAlerts((prev) => [data, ...prev].slice(0, 50));
    };
    return () => eventSource.close();
  }, [ecosystem]);

  return (
    <Sidebar>
      <div className="max-w-6xl mx-auto">
        <header className="mb-12 flex justify-between items-end">
          <div>
            <div className="flex items-center gap-4 mb-2">
              <div className="p-3 rounded-2xl bg-blue-500/10 border border-blue-500/20">
                <Activity className="h-8 w-8 text-blue-500" />
              </div>
              <h1 className="text-4xl font-bold tracking-tight">Monitoreo en Vivo <span className="text-foreground/40">/ {ecosystem}</span></h1>
            </div>
          </div>
        </header>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-12">
          {[
            { label: 'Transacciones', value: '1,240', icon: Database, color: 'text-blue-500' },
            { label: 'Alertas Altas', value: alerts.filter(a => a.riesgo > 80).length, icon: ShieldAlert, color: 'text-red-500' },
            { label: 'Riesgo Promedio', value: '14.2%', icon: TrendingUp, color: 'text-yellow-500' },
            { label: 'Uptime Sistema', value: '99.9%', icon: Clock, color: 'text-green-500' },
          ].map((stat, i) => (
            <div key={i} className="glass p-6 rounded-3xl border border-white/5">
              <stat.icon className={`h-6 w-6 ${stat.color} mb-4`} />
              <div className="text-2xl font-bold">{stat.value}</div>
              <div className="text-xs text-foreground/40 uppercase tracking-tighter mt-1">{stat.label}</div>
            </div>
          ))}
        </div>

        <section className="glass rounded-3xl border border-white/5 overflow-hidden">
          <div className="px-8 py-6 border-b border-white/5 flex justify-between items-center bg-white/[0.02]">
            <h3 className="font-bold flex items-center gap-2"><Search className="h-4 w-4 text-foreground/40" /> Flujo de Alertas</h3>
          </div>
          <table className="w-full text-left text-sm">
            <thead>
              <tr className="text-foreground/40 uppercase text-[10px] tracking-widest border-b border-white/5">
                <th className="px-8 py-4">ID</th><th className="px-8 py-4">Patrón</th><th className="px-8 py-4">Monto</th><th className="px-8 py-4">Riesgo</th>
              </tr>
            </thead>
            <tbody>
              <AnimatePresence initial={false}>
                {alerts.map((alert) => (
                  <motion.tr key={alert.id} initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }} className="border-b border-white/5 hover:bg-white/[0.02] transition-colors">
                    <td className="px-8 py-4 font-mono text-xs text-foreground/40">{alert.id}</td>
                    <td className="px-8 py-4 font-semibold">{alert.tipo}</td>
                    <td className="px-8 py-4 text-foreground/80">{alert.monto}</td>
                    <td className="px-8 py-4 font-bold">{alert.riesgo}%</td>
                  </motion.tr>
                ))}
              </AnimatePresence>
            </tbody>
          </table>
        </section>
      </div>
    </Sidebar>
  );
}
