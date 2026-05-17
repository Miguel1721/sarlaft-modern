'use client';

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { FileText, Loader2, CheckCircle, Download, AlertCircle } from 'lucide-react';

const CAMPOS = [
  // --- Datos de la Empresa ---
  { section: "Datos del CDA", fields: [
    { name: "razon_social",          label: "Razón Social",              type: "text",   placeholder: "Ej: CDA Autodiagnósticos S.A.S." },
    { name: "nit",                   label: "NIT",                       type: "text",   placeholder: "Ej: 900.123.456-7" },
    { name: "ciudad",                label: "Ciudad",                    type: "text",   placeholder: "Ej: Bogotá" },
    { name: "departamento",          label: "Departamento",              type: "text",   placeholder: "Ej: Cundinamarca" },
    { name: "direccion",             label: "Dirección",                 type: "text",   placeholder: "Ej: Calle 100 # 15-30" },
    { name: "telefono",              label: "Teléfono",                  type: "text",   placeholder: "Ej: 3101234567" },
    { name: "correo",                label: "Correo Electrónico",        type: "email",  placeholder: "contacto@cda.com" },
    { name: "regimen",               label: "Régimen Tributario",        type: "select", options: ["RESPONSABLE DE IVA", "NO RESPONSABLE DE IVA", "GRAN CONTRIBUYENTE"] },
    { name: "ingresos_anuales",      label: "Ingresos Anuales (COP)",   type: "number", placeholder: "Ej: 1500000000" },
    { name: "empleados",             label: "Número de Empleados",       type: "number", placeholder: "Ej: 25" },
    { name: "servicios",             label: "Servicios (Clases CDA)",    type: "text",   placeholder: "Ej: CDA CLASE A, B, C" },
    { name: "zonas_operacion",       label: "Zonas de Operación",        type: "text",   placeholder: "Ej: Bogotá, Soacha" },
    { name: "fecha_implementacion",  label: "Fecha de Implementación",   type: "date",   placeholder: "" },
  ]},
  // --- Representante Legal ---
  { section: "Representante Legal", fields: [
    { name: "representante_legal",   label: "Nombre Completo",           type: "text",   placeholder: "Ej: CARLOS ALBERTO PÉREZ" },
    { name: "cedula_representante",  label: "Cédula",                    type: "text",   placeholder: "Ej: 1026575786" },
  ]},
  // --- Oficial de Cumplimiento ---
  { section: "Oficial de Cumplimiento (Principal)", fields: [
    { name: "nombre_oc",                  label: "Nombre y Apellido(s) Completos", type: "text",   placeholder: "Ej: GUSTAVO ADOLFO RODRÍGUEZ" },
    { name: "oc_cedula",                  label: "Cédula",                         type: "text",   placeholder: "Ej: 1111222333" },
    { name: "oc_correo",                  label: "Correo",                          type: "email",  placeholder: "cumplimiento@cda.com" },
    { name: "horas_formacion_oc",         label: "Horas de Formación SARLAFT",     type: "number", placeholder: "Ej: 120" },
    { name: "institucion_certificante_oc",label: "Institución Certificante",        type: "text",   placeholder: "Ej: Universidad Javeriana" },
    { name: "oc_experiencia_meses",       label: "Experiencia (Meses)",            type: "number", placeholder: "Ej: 24" },
  ]},
  // --- Oficial Suplente ---
  { section: "Oficial de Cumplimiento (Suplente)", fields: [
    { name: "oc_suplente_nombre",  label: "Nombre y Apellido(s) Completos", type: "text",  placeholder: "Ej: ANA MARÍA GÓMEZ" },
    { name: "oc_suplente_cedula",  label: "Cédula",                         type: "text",  placeholder: "Ej: 444555666" },
    { name: "oc_suplente_correo",  label: "Correo",                          type: "email", placeholder: "suplente@cda.com" },
  ]},
];

const INITIAL_STATE: Record<string, string | number> = {
  razon_social: '', nit: '', ciudad: '', departamento: '', direccion: '', telefono: '',
  correo: '', regimen: 'RESPONSABLE DE IVA', ingresos_anuales: 0, empleados: 0,
  servicios: '', zonas_operacion: '', fecha_implementacion: new Date().toISOString().split('T')[0],
  representante_legal: '', cedula_representante: '',
  nombre_oc: '', oc_cedula: '', oc_correo: '', horas_formacion_oc: 0,
  institucion_certificante_oc: '', oc_experiencia_meses: 0,
  oc_suplente_nombre: '', oc_suplente_cedula: '', oc_suplente_correo: '',
};

export default function FabricaLegalContent() {
  const [formData, setFormData] = useState<Record<string, string | number>>(INITIAL_STATE);
  const [loading, setLoading] = useState(false);
  const [zipUrl, setZipUrl] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value, type } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'number' ? (value === '' ? 0 : Number(value)) : value,
    }));
  };

  const generarKit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setZipUrl(null);

    try {
      const response = await fetch('/api/v1/onboarding/generar_kit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      });

      const data = await response.json();

      if (response.ok && data.status === 'Exito') {
        setZipUrl(data.zip_url);
      } else {
        const detalle = data?.detail;
        if (Array.isArray(detalle)) {
          setError(detalle.map((d: any) => d.msg).join(' | '));
        } else {
          setError(typeof detalle === 'string' ? detalle : 'Error al generar el kit. Revise los campos requeridos.');
        }
      }
    } catch (err) {
      setError('No se pudo conectar con el servidor. Intente de nuevo.');
    } finally {
      setLoading(false);
    }
  };

  if (zipUrl) {
    return (
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        className="max-w-xl mx-auto text-center py-24"
      >
        <div className="p-6 rounded-full bg-green-500/10 border-2 border-green-500/20 inline-flex mb-8">
          <CheckCircle className="h-20 w-20 text-green-500" />
        </div>
        <h2 className="text-4xl font-black text-white mb-4">¡Kit Normativo Generado!</h2>
        <p className="text-gray-400 text-lg mb-10">
          Sus 7 documentos SARLAFT han sido compilados, sellados con los datos del CDA y empaquetados en un archivo seguro.
        </p>
        <div className="space-y-4">
          <a
            href={zipUrl}
            download
            className="w-full bg-green-600 hover:bg-green-700 text-white font-bold py-5 px-8 rounded-2xl flex items-center justify-center gap-3 text-lg transition-all shadow-lg shadow-green-900/20"
          >
            <Download className="h-6 w-6" />
            Descargar Kit Completo (.ZIP)
          </a>
          <button
            onClick={() => { setZipUrl(null); setFormData(INITIAL_STATE); }}
            className="w-full bg-gray-800 hover:bg-gray-700 text-white font-bold py-4 px-8 rounded-2xl transition-all"
          >
            Generar otro Kit
          </button>
        </div>
      </motion.div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto">
      <header className="mb-12">
        <div className="flex items-center gap-4 mb-4">
          <div className="p-4 rounded-2xl bg-blue-600/10 border border-blue-600/20">
            <FileText className="h-10 w-10 text-blue-500" />
          </div>
          <div>
            <h1 className="text-4xl font-black tracking-tight text-white">
              Fábrica Legal <span className="text-blue-500">SARLAFT</span>
            </h1>
            <p className="text-gray-400 mt-1">
              Complete los datos del CDA para generar los 7 documentos normativos requeridos por Supertransporte.
            </p>
          </div>
        </div>
      </header>

      {error && (
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8 bg-red-500/10 border border-red-500/30 p-5 rounded-2xl flex items-start gap-3"
        >
          <AlertCircle className="h-5 w-5 text-red-500 mt-0.5 shrink-0" />
          <p className="text-red-400 text-sm font-medium">{error}</p>
        </motion.div>
      )}

      <form onSubmit={generarKit} className="space-y-8">
        {CAMPOS.map((seccion) => (
          <div key={seccion.section} className="bg-gray-900 border border-gray-800 p-8 rounded-3xl">
            <h2 className="text-lg font-bold text-blue-400 uppercase tracking-wider mb-6 pb-3 border-b border-gray-800">
              {seccion.section}
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
              {seccion.fields.map((field) => (
                <div key={field.name} className={field.name === 'direccion' || field.name === 'servicios' ? 'md:col-span-2' : ''}>
                  <label className="block text-xs font-bold text-gray-400 uppercase tracking-wider mb-2">
                    {field.label}
                  </label>
                  {field.type === 'select' ? (
                    <select
                      name={field.name}
                      value={formData[field.name] as string}
                      onChange={handleChange}
                      className="w-full bg-gray-950 border border-gray-800 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-blue-500 transition-all appearance-none"
                    >
                      {field.options?.map(opt => (
                        <option key={opt} value={opt}>{opt}</option>
                      ))}
                    </select>
                  ) : (
                    <input
                      name={field.name}
                      type={field.type}
                      value={formData[field.name] as string}
                      onChange={handleChange}
                      placeholder={field.placeholder}
                      className="w-full bg-gray-950 border border-gray-800 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-blue-500 transition-all placeholder-gray-600"
                    />
                  )}
                </div>
              ))}
            </div>
          </div>
        ))}

        <button
          type="submit"
          disabled={loading}
          className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-6 rounded-2xl text-xl transition-all disabled:opacity-50 flex items-center justify-center gap-3 shadow-lg shadow-blue-900/20"
        >
          {loading ? (
            <>
              <Loader2 className="animate-spin h-6 w-6" />
              <span>Compilando Documentos Legales...</span>
            </>
          ) : (
            <>
              <FileText className="h-6 w-6" />
              <span>Generar Kit Normativo SARLAFT (7 Docs)</span>
            </>
          )}
        </button>
      </form>
    </div>
  );
}
