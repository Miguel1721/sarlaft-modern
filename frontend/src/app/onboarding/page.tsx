"use client";
import { useState } from 'react';

export default function CDAOnboardingWizard() {
  const [loading, setLoading] = useState(false);
  const [zipUrl, setZipUrl] = useState<string | null>(null);
  
  // Estado con las variables críticas que exigió el backend
  const [formData, setFormData] = useState({
    razon_social: '',
    nit: '',
    ciudad: '',
    departamento: '',
    direccion: '',
    telefono: '',
    correo: '',
    regimen: 'Simplificado',
    representante_legal: '',
    rep_cedula: '',
    nombre_oc: '',
    oc_cedula: '',
    oc_correo: '',
    ingresos_anuales: 0,
    empleados: 0,
    servicios: '',
    zonas_operacion: '',
    fecha_implementacion: new Date().toISOString().split('T')[0]
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const generarKit = async () => {
    setLoading(true);
    try {
      const response = await fetch('/api/v1/onboarding/generar_kit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });
      
      const data = await response.json();
      
      if (data.status === 'Exito') {
        setZipUrl(data.zip_url);
      } else {
        alert("Hubo un error al generar los documentos.");
      }
    } catch (error) {
      console.error(error);
      alert("Hubo un error de conexión al servidor.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-8 bg-gray-900 rounded-xl shadow-2xl text-white mt-10">
      <h2 className="text-3xl font-bold mb-6 text-red-500">Configuración SARLAFT 4.0</h2>
      
      {!zipUrl ? (
        <div className="space-y-6 animate-fade-in">
          {/* Aquí puedes dividir visualmente en pasos o poner una cuadrícula de inputs */}
          <div className="grid grid-cols-2 gap-4">
            <input name="razon_social" placeholder="Razón Social del CDA" onChange={handleChange} className="p-3 bg-gray-800 rounded border border-gray-700 w-full focus:outline-none focus:border-red-500" />
            <input name="nit" placeholder="NIT" onChange={handleChange} className="p-3 bg-gray-800 rounded border border-gray-700 w-full focus:outline-none focus:border-red-500" />
            <input name="representante_legal" placeholder="Nombre Rep. Legal" onChange={handleChange} className="p-3 bg-gray-800 rounded border border-gray-700 w-full focus:outline-none focus:border-red-500" />
            <input name="rep_cedula" placeholder="Cédula Rep. Legal" onChange={handleChange} className="p-3 bg-gray-800 rounded border border-gray-700 w-full focus:outline-none focus:border-red-500" />
            <input name="nombre_oc" placeholder="Nombre Oficial Cumplimiento" onChange={handleChange} className="p-3 bg-gray-800 rounded border border-gray-700 w-full focus:outline-none focus:border-red-500" />
            <input name="oc_cedula" placeholder="Cédula OC" onChange={handleChange} className="p-3 bg-gray-800 rounded border border-gray-700 w-full focus:outline-none focus:border-red-500" />
            <input name="ciudad" placeholder="Ciudad de Operación" onChange={handleChange} className="p-3 bg-gray-800 rounded border border-gray-700 w-full focus:outline-none focus:border-red-500" />
            <input name="servicios" placeholder="Servicios (Ej: Revisión Gases)" onChange={handleChange} className="p-3 bg-gray-800 rounded border border-gray-700 w-full focus:outline-none focus:border-red-500" />
            <input name="departamento" placeholder="Departamento" onChange={handleChange} className="p-3 bg-gray-800 rounded border border-gray-700 w-full focus:outline-none focus:border-red-500" />
            <input name="direccion" placeholder="Dirección" onChange={handleChange} className="p-3 bg-gray-800 rounded border border-gray-700 w-full focus:outline-none focus:border-red-500" />
            <input name="telefono" placeholder="Teléfono" onChange={handleChange} className="p-3 bg-gray-800 rounded border border-gray-700 w-full focus:outline-none focus:border-red-500" />
            <input name="correo" placeholder="Correo Electrónico" onChange={handleChange} className="p-3 bg-gray-800 rounded border border-gray-700 w-full focus:outline-none focus:border-red-500" />
            <input name="ingresos_anuales" placeholder="Ingresos Anuales (COP)" type="number" onChange={handleChange} className="p-3 bg-gray-800 rounded border border-gray-700 w-full focus:outline-none focus:border-red-500" />
            <input name="empleados" placeholder="Número de Empleados" type="number" onChange={handleChange} className="p-3 bg-gray-800 rounded border border-gray-700 w-full focus:outline-none focus:border-red-500" />
            <input name="zonas_operacion" placeholder="Zonas de Operación" onChange={handleChange} className="p-3 bg-gray-800 rounded border border-gray-700 w-full focus:outline-none focus:border-red-500" />
          </div>

          <button 
            onClick={generarKit} 
            disabled={loading}
            className="w-full bg-red-600 hover:bg-red-700 text-white font-bold py-4 rounded-lg mt-6 transition-all"
          >
            {loading ? 'Compilando Documentos Legales...' : 'Generar Kit Normativo'}
          </button>
        </div>
      ) : (
        <div className="text-center py-12 animate-fade-in">
          <div className="text-green-400 text-6xl mb-4">✓</div>
          <h3 className="text-2xl font-bold mb-4">¡Fábrica Legal Completada!</h3>
          <p className="text-gray-400 mb-8">Tus 7 manuales han sido generados e inyectados con los datos del CDA.</p>
          <a 
            href={zipUrl} 
            download
            className="bg-green-600 hover:bg-green-700 text-white font-bold py-4 px-8 rounded-lg inline-block"
          >
            Descargar Archivo .ZIP
          </a>
        </div>
      )}
    </div>
  );
}
