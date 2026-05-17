'use client';

import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { FileText, Download, ShieldAlert, CheckCircle2 } from 'lucide-react';
import Sidebar from '@/components/Sidebar';

export default function ReportsPage() {
  const [loading, setLoading] = useState(false);
  const [generated, setGenerated] = useState(false);

  const handleGenerate = () => {
    setLoading(true);
    setTimeout(() => {
      setLoading(false);
      setGenerated(true);
    }, 1500);
  };

  return (
    <Sidebar>
      <div className="max-w-6xl mx-auto">
        <header className="mb-12">
          <div className="flex items-center gap-4 mb-2">
            <div className="p-3 rounded-2xl bg-blue-500/10 border border-blue-500/20">
              <FileText className="h-8 w-8 text-blue-500" />
            </div>
            <h1 className="text-4xl font-bold tracking-tight">Reportes <span className="text-foreground/40">/ Cumplimiento UIAF</span></h1>
          </div>
          <p className="text-foreground/60 max-w-2xl">
            Generación de reportes oficiales ROS y auditorías de cumplimiento normativo.
          </p>
        </header>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div className="lg:col-span-1 space-y-6">
            <section className="glass rounded-3xl p-8 border border-white/10">
              <h2 className="text-xl font-semibold mb-6 flex items-center gap-2">Configuración</h2>
              <div className="space-y-4">
                <div>
                  <label className="block text-xs font-bold opacity-40 uppercase mb-2 tracking-widest">Tipo de Reporte</label>
                  <select className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-blue-500 transition-colors">
                    <option className="bg-background">Reporte ROS (Operación Sospechosa)</option>
                    <option className="bg-background">Reporte de Ausencia de ROS</option>
                    <option className="bg-background">Auditoría Interna</option>
                  </select>
                </div>
                <div>
                  <label className="block text-xs font-bold opacity-40 uppercase mb-2 tracking-widest">Periodo</label>
                  <input type="month" className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-blue-500 transition-colors" />
                </div>
                <button 
                  onClick={handleGenerate}
                  disabled={loading}
                  className="w-full bg-blue-600 hover:bg-blue-500 disabled:opacity-50 text-white font-bold py-4 rounded-2xl transition-all shadow-lg shadow-blue-900/20 flex items-center justify-center gap-2"
                >
                  {loading ? 'Generando...' : 'Generar Reporte'}
                </button>
              </div>
            </section>
          </div>

          <div className="lg:col-span-2">
            <section className="glass rounded-3xl p-8 border border-white/10 min-h-[400px] flex flex-col items-center justify-center text-center">
              {generated ? (
                <motion.div initial={{ opacity: 0, scale: 0.9 }} animate={{ opacity: 1, scale: 1 }} className="space-y-6">
                  <div className="h-20 w-20 bg-green-500/20 border border-green-500/30 rounded-full flex items-center justify-center mx-auto">
                    <CheckCircle2 className="h-10 w-10 text-green-500" />
                  </div>
                  <div>
                    <h3 className="text-2xl font-bold mb-2">Reporte Generado con Éxito</h3>
                    <p className="text-foreground/60 mb-8 max-w-sm mx-auto">
                      El reporte ROS para el periodo seleccionado ha sido validado y está listo para su envío.
                    </p>
                    <div className="flex flex-wrap gap-4 justify-center">
                      <button className="bg-white/10 hover:bg-white/20 px-6 py-3 rounded-xl font-bold flex items-center gap-2 transition-all">
                        <Download className="h-5 w-5" /> Descargar PDF
                      </button>
                      <button className="bg-white/10 hover:bg-white/20 px-6 py-3 rounded-xl font-bold flex items-center gap-2 transition-all">
                        <ShieldAlert className="h-5 w-5" /> Enviar a UIAF
                      </button>
                    </div>
                  </div>
                </motion.div>
              ) : (
                <div className="space-y-4">
                  <div className="h-16 w-16 bg-white/5 border border-white/10 rounded-2xl flex items-center justify-center mx-auto opacity-20">
                    <FileText className="h-8 w-8" />
                  </div>
                  <p className="text-foreground/20 font-medium max-w-xs">
                    Selecciona los parámetros para generar el reporte de cumplimiento.
                  </p>
                </div>
              )}
            </section>
          </div>
        </div>
      </div>
    </Sidebar>
  );
}
