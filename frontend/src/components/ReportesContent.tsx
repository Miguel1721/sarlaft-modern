'use client';

import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Download, 
  ShieldCheck, 
  AlertTriangle, 
  RefreshCw, 
  Clock, 
  FileText, 
  Search, 
  Trash2, 
  Eye, 
  ChevronLeft, 
  ChevronRight, 
  X, 
  ShieldAlert, 
  ListFilter,
  CheckCircle,
  Database,
  Calendar,
  AlertCircle
} from 'lucide-react';
import { useAuth } from '@/context/AuthContext';

interface HistorialItem {
  id: number;
  fecha_consulta: string;
  tipo_documento: string;
  numero_documento: string;
  nombre_contraparte: string;
  tipo_consulta: string;
  score_riesgo: number;
  nivel_riesgo: string;
  decision: string;
  en_lista_restrictiva: boolean;
  conectores_exitosos: number;
  conectores_fallidos: number;
  pdf_generado?: boolean;
  pdf_path?: string;
}

interface DetalleItem extends HistorialItem {
  resultados_json?: any;
  conectores_ejecutados?: string[];
  listas_restrictivas_encontradas?: string[];
  ip_origen?: string;
  tiempo_ejecucion_segundos?: number;
}

export default function ReportesContent() {
  const { token } = useAuth();
  const [items, setItems] = useState<HistorialItem[]>([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Filters State
  const [searchDoc, setSearchDoc] = useState('');
  const [searchName, setSearchName] = useState('');
  const [riskLevel, setRiskLevel] = useState('');
  const [decision, setDecision] = useState('');
  const [inList, setInList] = useState('');
  const [dateFrom, setDateFrom] = useState('');
  const [dateTo, setDateTo] = useState('');

  // Modals State
  const [selectedId, setSelectedId] = useState<number | null>(null);
  const [detailItem, setDetailItem] = useState<DetalleItem | null>(null);
  const [detailLoading, setDetailLoading] = useState(false);
  const [deleteConfirmId, setDeleteConfirmId] = useState<number | null>(null);
  const [deleting, setDeleting] = useState(false);

  const cargarHistorial = async (pageNum = page) => {
    setLoading(true);
    setError(null);
    try {
      const storedToken = token || localStorage.getItem('access_token');
      if (!storedToken) {
        setError('No autenticado. Por favor inicie sesión.');
        setLoading(false);
        return;
      }

      // Build Query String
      const params = new URLSearchParams();
      params.append('pagina', pageNum.toString());
      params.append('por_pagina', '10');
      
      if (searchDoc) params.append('numero_documento', searchDoc);
      if (searchName) params.append('nombre_contraparte', searchName);
      if (riskLevel) params.append('nivel_riesgo', riskLevel);
      if (decision) params.append('decision', decision);
      if (inList) params.append('en_lista_restrictiva', inList);
      if (dateFrom) params.append('fecha_desde', new Date(dateFrom).toISOString());
      if (dateTo) params.append('fecha_hasta', new Date(dateTo).toISOString());

      const res = await fetch(`https://sarlaf.agentesia.cloud/api/v1/historial?${params.toString()}`, {
        headers: {
          'Authorization': `Bearer ${storedToken}`
        }
      });

      if (!res.ok) {
        throw new Error('No se pudo cargar el historial de consultas.');
      }

      const data = await res.json();
      setItems(data.items ?? []);
      setTotal(data.total ?? 0);
      setTotalPages(data.total_paginas ?? 1);
      setPage(data.pagina ?? 1);
    } catch (err: any) {
      setError(err.message || 'Error de conexión con la API de cumplimiento.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    cargarHistorial(1);
  }, [searchDoc, searchName, riskLevel, decision, inList, dateFrom, dateTo]);

  // Load Detailed Consultation
  const verDetalle = async (id: number) => {
    setSelectedId(id);
    setDetailLoading(true);
    setDetailItem(null);
    try {
      const storedToken = token || localStorage.getItem('access_token');
      const res = await fetch(`https://sarlaf.agentesia.cloud/api/v1/historial/${id}`, {
        headers: {
          'Authorization': `Bearer ${storedToken}`
        }
      });

      if (!res.ok) throw new Error('Error al cargar detalle.');
      const data = await res.json();
      setDetailItem(data);
    } catch (err) {
      console.error(err);
    } finally {
      setDetailLoading(false);
    }
  };

  // Delete Record
  const ejecutarEliminar = async () => {
    if (!deleteConfirmId) return;
    setDeleting(true);
    try {
      const storedToken = token || localStorage.getItem('access_token');
      const res = await fetch(`https://sarlaf.agentesia.cloud/api/v1/historial/${deleteConfirmId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${storedToken}`
        }
      });

      if (res.ok) {
        setDeleteConfirmId(null);
        cargarHistorial(page);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setDeleting(false);
    }
  };

  const getRiskBadge = (level: string) => {
    switch ((level || '').toUpperCase()) {
      case 'CRITICO': return 'bg-red-950/40 text-red-400 border border-red-500/30';
      case 'ALTO': return 'bg-orange-950/40 text-orange-400 border border-orange-500/30';
      case 'MEDIO': return 'bg-yellow-950/40 text-yellow-400 border border-yellow-500/30';
      default: return 'bg-green-950/40 text-green-400 border border-green-500/30';
    }
  };

  const getDecisionBadge = (dec: string) => {
    switch ((dec || '').toUpperCase()) {
      case 'RECHAZADO': return 'bg-red-500/10 text-red-500 border border-red-500/20';
      case 'REVISION_MANUAL': return 'bg-yellow-500/10 text-yellow-500 border border-yellow-500/20';
      default: return 'bg-green-500/10 text-green-500 border border-green-500/20';
    }
  };

  return (
    <div className="max-w-6xl mx-auto pb-12">
      {/* Header */}
      <header className="mb-8 flex items-center justify-between">
        <div className="flex items-center gap-4">
          <div className="p-4 rounded-2xl bg-blue-600/10 border border-blue-600/20">
            <Clock className="h-8 w-8 text-blue-500" />
          </div>
          <div>
            <h1 className="text-3xl font-black tracking-tight text-white uppercase leading-none">
              Reportes / <span className="text-blue-500">Historial</span>
            </h1>
            <p className="text-foreground/50 text-sm mt-1">
              Registro histórico y auditoría E2E de debida diligencia de contrapartes.
            </p>
          </div>
        </div>
        <button
          onClick={() => cargarHistorial(page)}
          disabled={loading}
          className="flex items-center gap-2 bg-foreground/5 hover:bg-foreground/10 px-5 py-3 rounded-xl text-xs font-bold text-white transition-all border border-white/5 cursor-pointer disabled:opacity-50"
        >
          <RefreshCw className={`h-3.5 w-3.5 ${loading ? 'animate-spin' : ''}`} />
          Refrescar
        </button>
      </header>

      {/* Advanced Filters Panel */}
      <section className="glass rounded-3xl p-6 border border-white/10 mb-8">
        <div className="flex items-center gap-2 mb-4 text-xs font-bold uppercase tracking-wider text-blue-500">
          <ListFilter className="h-4 w-4" /> Panel de Filtrado Avanzado
        </div>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          {/* Document Search */}
          <div>
            <label className="block text-[9px] font-bold text-foreground/40 mb-1.5 uppercase tracking-wider">Documento</label>
            <div className="relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-3.5 w-3.5 text-foreground/30" />
              <input 
                type="text" 
                value={searchDoc} 
                onChange={(e) => setSearchDoc(e.target.value)}
                placeholder="CC, CE o NIT..."
                className="w-full bg-white/5 border border-white/10 focus:border-blue-500 rounded-xl pl-9 pr-3 py-2.5 text-xs text-white placeholder-foreground/30 focus:outline-none"
              />
            </div>
          </div>

          {/* Name Search */}
          <div>
            <label className="block text-[9px] font-bold text-foreground/40 mb-1.5 uppercase tracking-wider">Nombre Contraparte</label>
            <div className="relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-3.5 w-3.5 text-foreground/30" />
              <input 
                type="text" 
                value={searchName} 
                onChange={(e) => setSearchName(e.target.value)}
                placeholder="Nombre o Razón..."
                className="w-full bg-white/5 border border-white/10 focus:border-blue-500 rounded-xl pl-9 pr-3 py-2.5 text-xs text-white placeholder-foreground/30 focus:outline-none"
              />
            </div>
          </div>

          {/* Risk Level Selector */}
          <div>
            <label className="block text-[9px] font-bold text-foreground/40 mb-1.5 uppercase tracking-wider">Nivel de Riesgo</label>
            <select 
              value={riskLevel} 
              onChange={(e) => setRiskLevel(e.target.value)}
              className="w-full bg-white/5 border border-white/10 rounded-xl px-3 py-2.5 text-xs text-white focus:outline-none focus:border-blue-500"
            >
              <option className="bg-[#050505]" value="">Todos los Riesgos</option>
              <option className="bg-[#050505]" value="BAJO">Verde (Bajo)</option>
              <option className="bg-[#050505]" value="MEDIO">Amarillo (Medio)</option>
              <option className="bg-[#050505]" value="ALTO">Naranja (Alto)</option>
              <option className="bg-[#050505]" value="CRITICO">Rojo (Crítico)</option>
            </select>
          </div>

          {/* Decision Selector */}
          <div>
            <label className="block text-[9px] font-bold text-foreground/40 mb-1.5 uppercase tracking-wider">Decisión SARLAFT</label>
            <select 
              value={decision} 
              onChange={(e) => setDecision(e.target.value)}
              className="w-full bg-white/5 border border-white/10 rounded-xl px-3 py-2.5 text-xs text-white focus:outline-none focus:border-blue-500"
            >
              <option className="bg-[#050505]" value="">Todas las Decisiones</option>
              <option className="bg-[#050505]" value="APROBADO">Aprobado</option>
              <option className="bg-[#050505]" value="REVISION_MANUAL">Revisión Manual</option>
              <option className="bg-[#050505]" value="RECHAZADO">Rechazado</option>
            </select>
          </div>
        </div>

        {/* Date Ranges */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mt-4 pt-4 border-t border-white/5">
          <div className="md:col-span-2 grid grid-cols-2 gap-4">
            <div>
              <label className="block text-[9px] font-bold text-foreground/40 mb-1.5 uppercase tracking-wider">Desde Fecha</label>
              <input 
                type="date" 
                value={dateFrom} 
                onChange={(e) => setDateFrom(e.target.value)}
                className="w-full bg-white/5 border border-white/10 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-blue-500"
              />
            </div>
            <div>
              <label className="block text-[9px] font-bold text-foreground/40 mb-1.5 uppercase tracking-wider">Hasta Fecha</label>
              <input 
                type="date" 
                value={dateTo} 
                onChange={(e) => setDateTo(e.target.value)}
                className="w-full bg-white/5 border border-white/10 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-blue-500"
              />
            </div>
          </div>

          <div>
            <label className="block text-[9px] font-bold text-foreground/40 mb-1.5 uppercase tracking-wider">Presencia en Listas</label>
            <select 
              value={inList} 
              onChange={(e) => setInList(e.target.value)}
              className="w-full bg-white/5 border border-white/10 rounded-xl px-3 py-2.5 text-xs text-white focus:outline-none focus:border-blue-500"
            >
              <option className="bg-[#050505]" value="">Cualquiera</option>
              <option className="bg-[#050505]" value="true">Sí (En Lista Restrictiva)</option>
              <option className="bg-[#050505]" value="false">No (Paz y Salvo)</option>
            </select>
          </div>

          <div className="flex items-end">
            <button 
              onClick={() => {
                setSearchDoc('');
                setSearchName('');
                setRiskLevel('');
                setDecision('');
                setInList('');
                setDateFrom('');
                setDateTo('');
              }}
              className="w-full text-center text-xs font-bold text-foreground/40 hover:text-white py-2.5 transition-colors uppercase tracking-wider cursor-pointer"
            >
              Limpiar Filtros
            </button>
          </div>
        </div>
      </section>

      {/* Main Content Area */}
      {loading && items.length === 0 ? (
        <div className="text-center py-24 glass rounded-3xl border border-white/10 flex flex-col items-center">
          <RefreshCw className="h-10 w-10 animate-spin mb-4 text-blue-500" />
          <p className="text-foreground/70 font-semibold">Cargando consultas de cumplimiento...</p>
        </div>
      ) : error ? (
        <div className="bg-red-500/5 border border-red-500/20 p-8 rounded-3xl text-center">
          <AlertTriangle className="h-8 w-8 text-red-500 mx-auto mb-3" />
          <p className="text-red-400 font-bold">{error}</p>
        </div>
      ) : items.length === 0 ? (
        <div className="text-center py-24 glass rounded-3xl border border-white/10 flex flex-col items-center">
          <FileText className="h-16 w-16 mb-4 text-white/10" />
          <h3 className="text-lg font-bold">No se encontraron consultas</h3>
          <p className="text-sm text-foreground/40 mt-1 max-w-xs">
            Prueba ajustando los filtros de búsqueda o realiza una auditoría en Deep Search.
          </p>
        </div>
      ) : (
        <motion.div 
          initial={{ opacity: 0, y: 15 }} 
          animate={{ opacity: 1, y: 0 }}
          className="space-y-6"
        >
          {/* Audits Table */}
          <div className="glass border border-white/10 rounded-3xl overflow-hidden shadow-2xl">
            <div className="overflow-x-auto">
              <table className="w-full min-w-[900px]">
                <thead>
                  <tr className="border-b border-white/10 bg-white/[0.02]">
                    <th className="text-left p-4 text-[10px] font-bold text-foreground/40 uppercase tracking-wider">Fecha</th>
                    <th className="text-left p-4 text-[10px] font-bold text-foreground/40 uppercase tracking-wider">Documento</th>
                    <th className="text-left p-4 text-[10px] font-bold text-foreground/40 uppercase tracking-wider">Nombre Contraparte</th>
                    <th className="text-left p-4 text-[10px] font-bold text-foreground/40 uppercase tracking-wider">Score</th>
                    <th className="text-left p-4 text-[10px] font-bold text-foreground/40 uppercase tracking-wider">Riesgo</th>
                    <th className="text-left p-4 text-[10px] font-bold text-foreground/40 uppercase tracking-wider">Decisión</th>
                    <th className="text-center p-4 text-[10px] font-bold text-foreground/40 uppercase tracking-wider">Listas</th>
                    <th className="text-right p-4 text-[10px] font-bold text-foreground/40 uppercase tracking-wider">Acciones</th>
                  </tr>
                </thead>
                <tbody>
                  {items.map((row, i) => (
                    <motion.tr
                      key={row.id}
                      initial={{ opacity: 0, x: -10 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: i * 0.05 }}
                      className="border-b border-white/5 hover:bg-white/[0.02] transition-colors"
                    >
                      {/* Date */}
                      <td className="p-4 text-xs whitespace-nowrap font-medium text-foreground/75">
                        {new Date(row.fecha_consulta).toLocaleString('es-CO', {
                          day: '2-digit', month: '2-digit', year: 'numeric',
                          hour: '2-digit', minute: '2-digit'
                        })}
                      </td>

                      {/* Document */}
                      <td className="p-4 text-xs font-mono font-bold text-white whitespace-nowrap">
                        <span className="text-blue-500 text-[10px] font-black mr-1">{row.tipo_documento}</span>
                        {row.numero_documento}
                      </td>

                      {/* Name */}
                      <td className="p-4 text-xs font-semibold text-white whitespace-nowrap max-w-[200px] truncate">
                        {row.nombre_contraparte || 'S/N'}
                      </td>

                      {/* Score */}
                      <td className="p-4 text-xs font-mono font-bold text-foreground/80">
                        {row.score_riesgo}/100
                      </td>

                      {/* Risk */}
                      <td className="p-4">
                        <span className={`px-2.5 py-1 rounded-lg text-[10px] font-black uppercase tracking-wider ${getRiskBadge(row.nivel_riesgo)}`}>
                          {row.nivel_riesgo}
                        </span>
                      </td>

                      {/* Decision */}
                      <td className="p-4">
                        <span className={`px-2.5 py-1 rounded-lg text-[10px] font-black uppercase tracking-wider ${getDecisionBadge(row.decision)}`}>
                          {row.decision}
                        </span>
                      </td>

                      {/* Restricted Matches */}
                      <td className="p-4 text-center">
                        {row.en_lista_restrictiva ? (
                          <span className="px-2 py-0.5 rounded bg-red-500/10 text-red-500 text-[10px] font-bold border border-red-500/20">MATCH</span>
                        ) : (
                          <span className="px-2 py-0.5 rounded bg-green-500/10 text-green-400 text-[10px] font-bold border border-green-500/20">LIMPIO</span>
                        )}
                      </td>

                      {/* Actions */}
                      <td className="p-4 text-right whitespace-nowrap space-x-2">
                        {/* Audit Details */}
                        <button
                          onClick={() => verDetalle(row.id)}
                          className="p-2 rounded-lg bg-white/5 hover:bg-blue-600/20 hover:text-blue-400 text-foreground/60 border border-white/5 transition-all cursor-pointer"
                          title="Ver Detalle Técnico"
                        >
                          <Eye className="h-4 w-4" />
                        </button>

                        {/* Download PDF */}
                        {row.pdf_path || row.pdf_generado ? (
                          <a
                            href={row.pdf_path || `https://sarlaf.agentesia.cloud/api/v1/download/reporte_${row.numero_documento}.pdf`}
                            download
                            target="_blank"
                            rel="noopener noreferrer"
                            className="inline-block p-2 rounded-lg bg-blue-600/10 hover:bg-blue-600/30 text-blue-400 border border-blue-500/20 transition-all cursor-pointer"
                            title="Descargar Reporte PDF"
                          >
                            <Download className="h-4 w-4" />
                          </a>
                        ) : (
                          <span className="inline-block p-2 text-foreground/20 cursor-not-allowed">—</span>
                        )}

                        {/* Delete Audit */}
                        <button
                          onClick={() => setDeleteConfirmId(row.id)}
                          className="p-2 rounded-lg bg-white/5 hover:bg-red-600/20 hover:text-red-400 text-foreground/60 border border-white/5 transition-all cursor-pointer"
                          title="Eliminar del Historial"
                        >
                          <Trash2 className="h-4 w-4" />
                        </button>
                      </td>
                    </motion.tr>
                  ))}
                </tbody>
              </table>
            </div>

            {/* Pagination Controls */}
            <div className="flex items-center justify-between p-4 border-t border-white/10 bg-white/[0.01] text-xs">
              <span className="text-foreground/40 font-medium">Total: {total} consultas</span>
              
              <div className="flex items-center gap-3">
                <button
                  disabled={page <= 1 || loading}
                  onClick={() => cargarHistorial(page - 1)}
                  className="p-2 rounded-lg bg-white/5 hover:bg-white/10 disabled:opacity-30 disabled:cursor-not-allowed border border-white/5 text-white transition-all cursor-pointer"
                >
                  <ChevronLeft className="h-4 w-4" />
                </button>

                <span className="text-white font-bold">Página {page} de {totalPages}</span>

                <button
                  disabled={page >= totalPages || loading}
                  onClick={() => cargarHistorial(page + 1)}
                  className="p-2 rounded-lg bg-white/5 hover:bg-white/10 disabled:opacity-30 disabled:cursor-not-allowed border border-white/5 text-white transition-all cursor-pointer"
                >
                  <ChevronRight className="h-4 w-4" />
                </button>
              </div>
            </div>
          </div>
        </motion.div>
      )}

      {/* DETAIL MODAL PANEL */}
      <AnimatePresence>
        {selectedId && (
          <motion.div 
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-6"
            onClick={() => setSelectedId(null)}
          >
            <motion.div 
              initial={{ scale: 0.95, opacity: 0, y: 30 }}
              animate={{ scale: 1, opacity: 1, y: 0 }}
              exit={{ scale: 0.95, opacity: 0, y: 30 }}
              onClick={(e) => e.stopPropagation()}
              className="bg-[#0b0c10] border border-white/15 rounded-3xl w-full max-w-4xl max-h-[85vh] overflow-y-auto p-8 shadow-2xl relative custom-scrollbar"
            >
              {/* Close Button */}
              <button 
                onClick={() => setSelectedId(null)}
                className="absolute right-6 top-6 p-2 rounded-xl bg-white/5 hover:bg-white/10 border border-white/5 text-foreground/60 hover:text-white transition-all cursor-pointer"
              >
                <X className="h-4 w-4" />
              </button>

              {detailLoading ? (
                <div className="text-center py-20">
                  <RefreshCw className="h-10 w-10 animate-spin mx-auto mb-4 text-blue-500" />
                  <p className="text-foreground/50 text-sm font-bold uppercase tracking-widest">Cargando expediente técnico...</p>
                </div>
              ) : detailItem ? (
                <div className="space-y-6">
                  {/* Header Detail */}
                  <header className="border-b border-white/10 pb-6">
                    <div className="flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-blue-500 mb-2">
                      <ShieldCheck className="h-4 w-4" /> Dictamen Legal SARLAFT / Expediente #{detailItem.id}
                    </div>
                    <h2 className="text-2xl font-black text-white">{detailItem.nombre_contraparte || 'Persona Sin Nombre'}</h2>
                    <p className="text-xs text-foreground/40 mt-1 uppercase tracking-widest font-bold">
                      Consultado el {new Date(detailItem.fecha_consulta).toLocaleString('es-CO')}
                    </p>
                  </header>

                  {/* Summary Grid */}
                  <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                    <div className="bg-white/[0.02] border border-white/5 p-4 rounded-2xl">
                      <span className="text-[10px] font-bold text-foreground/40 uppercase tracking-widest block mb-1">Identificación</span>
                      <span className="text-xs font-mono font-bold text-white uppercase">{detailItem.tipo_documento} {detailItem.numero_documento}</span>
                    </div>

                    <div className="bg-white/[0.02] border border-white/5 p-4 rounded-2xl">
                      <span className="text-[10px] font-bold text-foreground/40 uppercase tracking-widest block mb-1">Score de Riesgo</span>
                      <span className="text-xs font-mono font-bold text-white block">{detailItem.score_riesgo} / 100</span>
                    </div>

                    <div className="bg-white/[0.02] border border-white/5 p-4 rounded-2xl">
                      <span className="text-[10px] font-bold text-foreground/40 uppercase tracking-widest block mb-1">Nivel de Riesgo</span>
                      <span className={`px-2 py-0.5 rounded text-[9px] font-black uppercase inline-block mt-0.5 ${getRiskBadge(detailItem.nivel_riesgo)}`}>
                        {detailItem.nivel_riesgo}
                      </span>
                    </div>

                    <div className="bg-white/[0.02] border border-white/5 p-4 rounded-2xl">
                      <span className="text-[10px] font-bold text-foreground/40 uppercase tracking-widest block mb-1">Decisión SARLAFT</span>
                      <span className={`px-2 py-0.5 rounded text-[9px] font-black uppercase inline-block mt-0.5 ${getDecisionBadge(detailItem.decision)}`}>
                        {detailItem.decision}
                      </span>
                    </div>
                  </div>

                  {/* Metrics and Sources */}
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    {/* Execution Audit */}
                    <div className="glass p-6 rounded-2xl border border-white/5 space-y-4">
                      <h4 className="text-xs font-bold text-blue-500 uppercase tracking-wider">Auditoría del Sistema</h4>
                      <div className="space-y-2 text-xs">
                        <div className="flex justify-between border-b border-white/5 pb-2">
                          <span className="text-foreground/40">IP Consultora:</span>
                          <span className="font-mono text-white">{detailItem.ip_origen || '127.0.0.1'}</span>
                        </div>
                        <div className="flex justify-between border-b border-white/5 pb-2">
                          <span className="text-foreground/40">Tiempo de Ejecución:</span>
                          <span className="font-mono text-white">{detailItem.tiempo_ejecucion_segundos || '—'} segundos</span>
                        </div>
                        <div className="flex justify-between border-b border-white/5 pb-2">
                          <span className="text-foreground/40">Conectores Exitosos:</span>
                          <span className="font-mono text-green-400 font-bold">{detailItem.conectores_exitosos}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-foreground/40">Conectores Fallidos:</span>
                          <span className="font-mono text-red-400 font-bold">{detailItem.conectores_fallidos}</span>
                        </div>
                      </div>
                    </div>

                    {/* Lists Log */}
                    <div className="glass p-6 rounded-2xl border border-white/5 space-y-4">
                      <h4 className="text-xs font-bold text-blue-500 uppercase tracking-wider">Listas Restrictivas Mapeadas</h4>
                      {detailItem.listas_restrictivas_encontradas && detailItem.listas_restrictivas_encontradas.length > 0 ? (
                        <div className="flex flex-wrap gap-2">
                          {detailItem.listas_restrictivas_encontradas.map((listName, idx) => (
                            <span key={idx} className="bg-red-500/10 text-red-500 text-[10px] font-black border border-red-500/20 px-2 py-1 rounded">
                              🚨 {listName.toUpperCase()}
                            </span>
                          ))}
                        </div>
                      ) : (
                        <p className="text-xs text-green-400 font-bold flex items-center gap-1.5 bg-green-500/5 p-4 rounded-xl border border-green-500/10">
                          <CheckCircle className="h-4 w-4" /> Paz y Salvo. No se encontraron coincidencias vinculantes de lavado de activos o listas vinculantes.
                        </p>
                      )}
                    </div>
                  </div>

                  {/* Connectors JSON Dump */}
                  <div className="space-y-2">
                    <h4 className="text-xs font-bold text-foreground/40 uppercase tracking-wider">Expediente Raw JSON (Network Audit)</h4>
                    <pre className="bg-black/40 border border-white/5 p-5 rounded-2xl overflow-x-auto text-[10px] font-mono text-foreground/75 max-h-[250px] custom-scrollbar">
                      {JSON.stringify(detailItem.resultados_json ?? {}, null, 2)}
                    </pre>
                  </div>

                  {/* PDF Download Direct */}
                  {(detailItem.pdf_path || detailItem.pdf_generado) && (
                    <div className="pt-4 border-t border-white/10 flex justify-end">
                      <a
                        href={detailItem.pdf_path || `https://sarlaf.agentesia.cloud/api/v1/download/reporte_${detailItem.numero_documento}.pdf`}
                        download
                        target="_blank"
                        rel="noopener noreferrer"
                        className="flex items-center gap-2 bg-blue-600 hover:bg-blue-500 text-white font-bold px-6 py-3.5 rounded-xl text-xs transition-all shadow-lg shadow-blue-900/20 cursor-pointer"
                      >
                        <Download className="h-4 w-4" /> Descargar Certificado de Consulta PDF
                      </a>
                    </div>
                  )}
                </div>
              ) : null}
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* CONFIRM DELETE MODAL */}
      <AnimatePresence>
        {deleteConfirmId && (
          <motion.div 
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-6"
          >
            <motion.div 
              initial={{ scale: 0.95, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.95, opacity: 0 }}
              className="glass border border-red-500/20 rounded-3xl p-8 max-w-sm w-full text-center space-y-6 shadow-2xl relative overflow-hidden"
            >
              <div className="absolute top-0 left-0 w-full h-[2px] bg-red-500/30" />
              <div className="h-12 w-12 rounded-full bg-red-500/10 border border-red-500/20 flex items-center justify-center mx-auto text-red-500">
                <AlertCircle className="h-6 w-6" />
              </div>

              <div>
                <h3 className="text-lg font-bold text-white">¿Eliminar Consulta?</h3>
                <p className="text-xs text-foreground/50 mt-2">
                  Esta acción eliminará de forma permanente el registro del historial de cumplimiento de la base de datos de auditoría. Esta operación es irreversible.
                </p>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <button
                  onClick={() => setDeleteConfirmId(null)}
                  disabled={deleting}
                  className="py-3 rounded-xl bg-white/5 hover:bg-white/10 border border-white/5 text-xs font-bold text-foreground/60 hover:text-white transition-all cursor-pointer"
                >
                  Cancelar
                </button>
                <button
                  onClick={ejecutarEliminar}
                  disabled={deleting}
                  className="py-3 rounded-xl bg-red-600 hover:bg-red-500 disabled:opacity-50 text-xs font-bold text-white transition-all shadow-lg shadow-red-900/10 cursor-pointer"
                >
                  {deleting ? 'Eliminando...' : 'Sí, Eliminar'}
                </button>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
