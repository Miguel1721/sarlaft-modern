'use client';

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Swords, Zap, Database, ShieldAlert } from 'lucide-react';
import Sidebar from '@/components/Sidebar';

export default function Dashboard() {
  const [loading, setLoading] = useState(false);
  const [criminalPlan, setCriminalPlan] = useState<string | null>(null);
  const [ecosistema, setEcosistema] = useState('Banca & Economía Real');
  const [monto, setMonto] = useState('5000000');

  const handleSimulate = async () => {
    setLoading(true);
    try {
      const response = await fetch('/api/war-room/simulate/red-team', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ecosistema, monto: parseFloat(monto) })
      });
      const data = await response.json();
      setCriminalPlan(data.plan_criminal);
    } catch (e) {
      console.error(e);
      setCriminalPlan("Error al conectar con el servidor de IA. Por favor, intente de nuevo.");
    }
    setLoading(false);
  };

  return (
    <Sidebar>
      <div className="max-w-6xl mx-auto">
        <header className="mb-12">
          <div className="flex items-center gap-4 mb-2">
            <div className="p-3 rounded-2xl bg-red-500/10 border border-red-500/20">
              <Swords className="h-8 w-8 text-red-500" />
            </div>
            <h1 className="text-4xl font-bold tracking-tight">Dashboard <span className="text-foreground/40">/ Resumen Ejecutivo</span></h1>
          </div>
          <p className="text-foreground/60 max-w-2xl">
            Centro de mando para la simulación y detección de amenazas financieras avanzadas.
          </p>
        </header>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-12">
          {/* Panel de Configuración */}
          <section className="lg:col-span-1 glass rounded-3xl p-8 border border-white/10 h-fit">
            <h2 className="text-xl font-semibold mb-6 flex items-center gap-2">
              <Zap className="h-5 w-5 text-yellow-500" /> Parámetros
            </h2>
            
            <div className="space-y-6">
              <div>
                <label className="block text-sm font-medium text-foreground/40 mb-2 uppercase tracking-wider">Ecosistema</label>
                <select 
                  value={ecosistema}
                  onChange={(e) => setEcosistema(e.target.value)}
                  className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 focus:outline-none focus:border-red-500 transition-colors text-white"
                >
                  <option className="bg-[#050505]">Banca & Economía Real</option>
                  <option className="bg-[#050505]">Criptoactivos & DeFi</option>
                  <option className="bg-[#050505]">Comercio Exterior</option>
                  <option className="bg-[#050505]">Inmobiliario</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-foreground/40 mb-2 uppercase tracking-wider">Monto de Simulación</label>
                <input 
                  type="number"
                  value={monto}
                  onChange={(e) => setMonto(e.target.value)}
                  className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 focus:outline-none focus:border-red-500 transition-colors text-white"
                />
              </div>

              <button 
                onClick={handleSimulate}
                disabled={loading}
                className="w-full bg-red-600 hover:bg-red-500 disabled:opacity-50 disabled:cursor-not-allowed text-white font-bold py-4 rounded-2xl transition-all shadow-lg shadow-red-900/20 flex items-center justify-center gap-2 mt-4"
              >
                {loading ? (
                  <>
                    <div className="h-4 w-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                    Simulando...
                  </>
                ) : (
                  <>
                    <Swords className="h-5 w-5" />
                    Iniciar Simulación
                  </>
                )}
              </button>
            </div>
          </section>

          {/* Panel de Resultados */}
          <section className="lg:col-span-2">
            <AnimatePresence mode="wait">
              {criminalPlan ? (
                <motion.div 
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -20 }}
                  className="glass rounded-3xl p-8 border border-red-500/20 relative overflow-hidden"
                >
                  <div className="flex items-center gap-3 mb-6">
                    <div className="h-2 w-2 rounded-full bg-red-500 animate-pulse" />
                    <h3 className="text-red-500 font-bold uppercase tracking-tighter italic flex items-center gap-2">
                      <ShieldAlert className="h-4 w-4" /> IA CRIMINAL GENERADA
                    </h3>
                  </div>

                  <div className="prose prose-invert max-w-none">
                    <div className="whitespace-pre-wrap text-foreground/80 leading-relaxed font-mono text-sm bg-black/40 p-6 rounded-2xl border border-white/5">
                      {criminalPlan}
                    </div>
                  </div>
                </motion.div>
              ) : (
                <motion.div 
                  className="h-full flex flex-col items-center justify-center border-2 border-dashed border-white/5 rounded-3xl p-12 text-center"
                >
                  <Database className="h-12 w-12 text-foreground/10 mb-4" />
                  <p className="text-foreground/30 font-medium">Configura los parámetros y lanza la simulación para ver los resultados.</p>
                </motion.div>
              )}
            </AnimatePresence>
          </section>
        </div>
      </div>
    </Sidebar>
  );
}
