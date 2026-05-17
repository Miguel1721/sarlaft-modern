'use client';

import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Search, ShieldAlert, FileText, Loader2, AlertTriangle, ShieldCheck } from 'lucide-react';

export default function DeepSearchContent() {
  const [cedula, setCedula] = useState('');
  const [placa, setPlaca] = useState('');
  const [tipoConsulta, setTipoConsulta] = useState('SARLAFT_CDA');
  const [loading, setLoading] = useState(false);
  const [loadingText, setLoadingText] = useState('');
  const [result, setResult] = useState<any>(null);

  useEffect(() => {
    let interval: NodeJS.Timeout;
    if (loading) {
      const messages = [
        "Iniciando Deep Search...",
        "Consultando bases de datos...",
        "Verificando listas internacionales (OFAC, ONU)...",
        "Analizando hallazgos con Inteligencia Artificial...",
        "Redactando concepto jurídico final...",
        "Generando reporte PDF 4.0..."
      ];
      let i = 0;
      setLoadingText(messages[0]);
      interval = setInterval(() => {
        i++;
        if (i < messages.length) {
          setLoadingText(messages[i]);
        }
      }, 2500); // Cambia cada 2.5s
    }
    return () => clearInterval(interval);
  }, [loading]);

  const ejecutarAuditoria = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!cedula.trim()) {
      alert("Por favor ingrese la Cédula obligatoriamente.");
      return;
    }

    setLoading(true);
    setResult(null);
    try {
      const response = await fetch(`/api/v1/auditar`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          cedula: cedula.trim(),
          placa: tipoConsulta === 'SARLAFT_B2B' ? '' : placa.trim(),
          tipo_consulta: tipoConsulta,
          client_id: "cda_test_001"
        })
      });
      
      const data = await response.json();
      setResult(data);
    } catch (e) {
      console.error(e);
      alert("Error de conexión al servidor.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      <header className="mb-12 text-center">
        <div className="inline-flex items-center gap-4 mb-4">
          <div className="p-4 rounded-2xl bg-red-600/10 border border-red-600/20">
            <ShieldAlert className="h-10 w-10 text-red-600" />
          </div>
          <h1 className="text-4xl font-black tracking-tight text-white">Deep Search <span className="text-red-500">SARLAFT</span></h1>
        </div>
        <p className="text-gray-400 max-w-xl mx-auto text-lg">
          Auditoría en tiempo real de contrapartes en más de 50 listas restrictivas globales y nacionales.
        </p>
      </header>

      <section className="mb-12">
        <form onSubmit={ejecutarAuditoria} className="bg-gray-900 border border-gray-800 p-8 rounded-3xl shadow-2xl relative overflow-hidden">
          <div className="mb-6 space-y-2">
            <label className="text-sm font-bold text-gray-400 uppercase tracking-wider">Tipo de Perfil de Búsqueda</label>
            <select 
              value={tipoConsulta}
              onChange={(e) => setTipoConsulta(e.target.value)}
              disabled={loading}
              className="w-full bg-gray-950 border border-gray-800 rounded-2xl px-6 py-4 text-xl focus:outline-none focus:border-red-500 transition-all text-white disabled:opacity-50 appearance-none"
            >
              <option value="SARLAFT_CDA">SARLAFT CDA (Obliga Placa y Cédula)</option>
              <option value="SARLAFT_B2B">SARLAFT B2B (Proveedores/Empresas - Solo NIT/Cédula)</option>
              <option value="RRHH">Recursos Humanos (RRHH - Incluye Ley 1581)</option>
            </select>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
            <div className="space-y-2">
              <label className="text-sm font-bold text-gray-400 uppercase tracking-wider">Documento (Cédula / NIT)</label>
              <input 
                type="text" 
                value={cedula}
                onChange={(e) => setCedula(e.target.value)}
                placeholder="Ej: 1026575786"
                disabled={loading}
                className="w-full bg-gray-950 border border-gray-800 rounded-2xl px-6 py-4 text-xl focus:outline-none focus:border-red-500 transition-all text-white disabled:opacity-50"
              />
            </div>
            <div className="space-y-2">
              <label className="text-sm font-bold text-gray-400 uppercase tracking-wider">Placa del Vehículo</label>
              <input 
                type="text" 
                value={placa}
                onChange={(e) => setPlaca(e.target.value)}
                placeholder="Opcional: XXX000"
                disabled={loading || tipoConsulta === 'SARLAFT_B2B'}
                className="w-full bg-gray-950 border border-gray-800 rounded-2xl px-6 py-4 text-xl focus:outline-none focus:border-red-500 transition-all text-white uppercase disabled:opacity-50"
              />
            </div>
          </div>

          <button 
            type="submit"
            disabled={loading}
            className="w-full bg-red-600 hover:bg-red-700 py-5 rounded-2xl font-bold text-white text-lg transition-all disabled:opacity-50 flex items-center justify-center gap-3 relative overflow-hidden group"
          >
            {loading ? (
              <>
                <Loader2 className="animate-spin h-6 w-6" />
                <span>{loadingText}</span>
              </>
            ) : (
              <>
                <Search className="h-6 w-6" />
                <span>Ejecutar Auditoría SARLAFT</span>
              </>
            )}
          </button>
          
          {loading && (
            <div className="absolute bottom-0 left-0 h-1 bg-red-600 w-full animate-pulse"></div>
          )}
        </form>
      </section>

      <AnimatePresence mode="wait">
        {result && !loading && (
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="bg-gray-900 border border-gray-800 p-8 rounded-3xl shadow-2xl">
            
            <div className="flex flex-col items-center justify-center text-center mb-10">
              <div className={`p-6 rounded-full mb-6 ${
                result.summary?.status === 'ROJO' ? 'bg-red-500/10 text-red-500 border-2 border-red-500/20' : 
                'bg-green-500/10 text-green-500 border-2 border-green-500/20'
              }`}>
                {result.summary?.status === 'ROJO' ? <AlertTriangle className="h-16 w-16" /> : <ShieldCheck className="h-16 w-16" />}
              </div>
              
              <h2 className="text-3xl font-black mb-2 text-white">
                Dictamen: <span className={result.summary?.status === 'ROJO' ? 'text-red-500' : 'text-green-500'}>
                  {result.summary?.status === 'ROJO' ? 'RECHAZADO' : 'APROBADO'}
                </span>
              </h2>
              
              <p className="text-gray-400 text-lg max-w-2xl">
                {result.concepto_ia || "El análisis inteligente ha concluido y el dictamen jurídico ha sido redactado."}
              </p>
            </div>

            {result.summary?.alerts?.length > 0 && (
              <div className="bg-red-500/10 border border-red-500/20 p-6 rounded-2xl mb-8">
                <h3 className="text-red-500 font-bold mb-3 flex items-center gap-2"><AlertTriangle size={20} /> Alertas Críticas Detectadas</h3>
                <ul className="list-disc list-inside text-gray-300 space-y-1">
                  {result.summary.alerts.map((alerta: string, i: number) => (
                    <li key={i}>{alerta}</li>
                  ))}
                </ul>
              </div>
            )}

            {result.pdf_url && (
              <a 
                href={result.pdf_url} 
                target="_blank" 
                rel="noopener noreferrer"
                className="w-full bg-blue-600 hover:bg-blue-700 py-6 rounded-2xl font-bold text-white text-xl transition-all flex items-center justify-center gap-3 shadow-lg shadow-blue-900/20"
              >
                <FileText className="h-8 w-8" />
                <span>Descargar Reporte Oficial SARLAFT 4.0</span>
              </a>
            )}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
