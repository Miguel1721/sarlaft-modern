'use client';
import React, { useState } from 'react';
import Sidebar from '@/components/Sidebar';
import { Swords, Zap, AlertTriangle, Database } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

export default function WarRoomPage() {
  const [loading, setLoading] = useState(false);
  const [criminalPlan, setCriminalPlan] = useState<string | null>(null);
  const [monto, setMonto] = useState(5000000);
  const [ecosistema, setEcosistema] = useState('Banca & Economía Real');
  const [evidencia, setEvidencia] = useState<any[]>([]);

  const handleSimulate = async () => {
    setLoading(true);
    setCriminalPlan(null);
    try {
      const response = await fetch('/api/war-room/simulate/red-team', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ecosistema, monto })
      });
      const data = await response.json();
      setCriminalPlan(data.plan_criminal);
      setEvidencia(data.evidencia_tactica || []);
    } catch (e) { console.error(e); }
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
            <h1 className="text-4xl font-bold tracking-tight">War Room <span className="text-white/40">/ Laboratorio Adversario</span></h1>
          </div>
        </header>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <section className="lg:col-span-1 glass rounded-3xl p-8 border border-white/10 h-fit">
            <h2 className="text-xl font-semibold mb-6 flex items-center gap-2"><Zap className="h-5 w-5 text-yellow-500" /> Parámetros</h2>
            <div className="space-y-6">
              <div>
                <label className="block text-sm font-medium text-white/40 mb-2 uppercase">Ecosistema</label>
                <select value={ecosistema} onChange={(e) => setEcosistema(e.target.value)} className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white">
                  <option className="bg-[#050505]">Banca & Economía Real</option>
                  <option className="bg-[#050505]">Criptoactivos & DeFi</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-white/40 mb-2 uppercase">Monto</label>
                <input type="number" value={monto} onChange={(e) => setMonto(Number(e.target.value))} className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3" />
              </div>
              <button onClick={handleSimulate} disabled={loading} className="w-full bg-red-600 hover:bg-red-500 py-4 rounded-2xl font-bold flex items-center justify-center gap-2">
                {loading ? "Simulando..." : "Iniciar Simulación"}
              </button>
            </div>
          </section>

          <section className="lg:col-span-2">
            {criminalPlan ? (
              <div className="glass rounded-3xl p-8 border border-red-500/20">
                <div className="whitespace-pre-wrap text-white/80 font-mono text-sm bg-black/40 p-6 rounded-2xl border border-white/5">{criminalPlan}</div>
              </div>
            ) : (
              <div className="h-full flex flex-col items-center justify-center border-2 border-dashed border-white/5 rounded-3xl p-12 text-white/10">
                <Database className="h-12 w-12 mb-4" /><p>Configura y lanza la simulación.</p>
              </div>
            )}
          </section>
        </div>
      </div>
    </Sidebar>
  );
}
