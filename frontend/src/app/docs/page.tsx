'use client';

import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import Sidebar from '@/components/Sidebar';

// Tipos para documentos
interface DocumentMetadata {
  id: string;
  name: string;
  category: string;
  file_type: string;
  file_size: number;
  created_at: string;
  last_modified: string;
  description?: string;
  tags: string[];
}

export default function DocsPage() {
  // Estado de documentos
  const [documents, setDocuments] = useState<DocumentMetadata[]>([]);
  const [filteredDocuments, setFilteredDocuments] = useState<DocumentMetadata[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [searchTerm, setSearchTerm] = useState('');

  // Estado de vista previa
  const [selectedDocument, setSelectedDocument] = useState<DocumentMetadata | null>(null);
  const [previewContent, setPreviewContent] = useState<string>('');
  const [isPreviewOpen, setIsPreviewOpen] = useState(false);

  // Animaciones
  const fadeIn = {
    initial: { opacity: 0, y: 20 },
    animate: { opacity: 1, y: 0, transition: { duration: 0.5 } }
  };

  // Cargar documentos
  useEffect(() => {
    loadDocuments();
  }, []);

  // Filtrar documentos cuando cambian los filtros
  useEffect(() => {
    filterDocuments();
  }, [documents, selectedCategory, searchTerm]);

  const loadDocuments = async () => {
    setLoading(true);
    try {
      const response = await fetch('/api/documents/');
      if (response.ok) {
        const data = await response.json();
        setDocuments(data);
      } else {
        // Usar documentos de ejemplo si la API no está disponible
        setDocuments(getSampleDocuments());
      }
    } catch (error) {
      console.error('Error al cargar documentos:', error);
      setDocuments(getSampleDocuments());
    } finally {
      setLoading(false);
    }
  };

  const getSampleDocuments = (): DocumentMetadata[] => [
    {
      id: 'DOC_001',
      name: 'Manual de Autocontrol y Gestión del Riesgo',
      category: 'manuales',
      file_type: 'pdf',
      file_size: 2048576,
      created_at: '2026-01-09T00:00:00Z',
      last_modified: '2026-01-09T00:00:00Z',
      description: 'Procedimientos de control interno para operaciones cripto',
      tags: ['SARLAFT', 'Riesgo', 'Procedimientos']
    },
    {
      id: 'DOC_002',
      name: 'Política AML Actualizada',
      category: 'politicas',
      file_type: 'pdf',
      file_size: 1024000,
      created_at: '2026-01-15T00:00:00Z',
      last_modified: '2026-01-20T00:00:00Z',
      description: 'Política actualizada de prevención de lavado',
      tags: ['AML', 'Política', '2024']
    },
    {
      id: 'DOC_003',
      name: 'Acta Comité de Cumplimiento - Enero 2026',
      category: 'actas',
      file_type: 'docx',
      file_size: 512000,
      created_at: '2026-01-30T00:00:00Z',
      last_modified: '2026-01-30T00:00:00Z',
      description: 'Acta de la reunión mensual del comité',
      tags: ['Comité', 'Reunión', 'Enero']
    },
    {
      id: 'DOC_004',
      name: 'Programa de Capacitación SARLAFT',
      category: 'programas',
      file_type: 'pdf',
      file_size: 3072000,
      created_at: '2026-02-01T00:00:00Z',
      last_modified: '2026-02-01T00:00:00Z',
      description: 'Programa anual de capacitación para empleados',
      tags: ['Capacitación', 'Anual', 'Empleados']
    }
  ];

  const filterDocuments = () => {
    let filtered = documents;

    // Filtrar por categoría
    if (selectedCategory !== 'all') {
      filtered = filtered.filter(doc => doc.category === selectedCategory);
    }

    // Filtrar por término de búsqueda
    if (searchTerm) {
      const term = searchTerm.toLowerCase();
      filtered = filtered.filter(doc =>
        doc.name.toLowerCase().includes(term) ||
        (doc.description && doc.description.toLowerCase().includes(term)) ||
        doc.tags.some(tag => tag.toLowerCase().includes(term))
      );
    }

    setFilteredDocuments(filtered);
  };

  const categories = [
    { key: 'all', label: 'Todos', icon: '📁' },
    { key: 'manuales', label: 'Manuales', icon: '📖' },
    { key: 'politicas', label: 'Políticas', icon: '📋' },
    { key: 'actas', label: 'Actas', icon: '📝' },
    { key: 'programas', label: 'Programas', icon: '🎯' }
  ];

  const formatFileSize = (bytes: number): string => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const formatDate = (dateString: string): string => {
    return new Date(dateString).toLocaleDateString('es-CO', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  const handlePreview = async (document: DocumentMetadata) => {
    setSelectedDocument(document);

    try {
      const response = await fetch(`/api/documents/${document.id}`);
      if (response.ok) {
        const data = await response.json();
        setPreviewContent(data.content || 'Contenido no disponible');
      } else {
        // Contenido de ejemplo para demostración
        setPreviewContent(getPreviewContent(document));
      }
    } catch (error) {
      setPreviewContent(getPreviewContent(document));
    }

    setIsPreviewOpen(true);
  };

  const getPreviewContent = (document: DocumentMetadata): string => {
    return `DOCUMENTO: ${document.name}
CATEGORÍA: ${document.category}
FECHA: ${formatDate(document.created_at)}

DESCRIPCIÓN:
${document.description || 'Sin descripción disponible'}

ETIQUETAS:
${document.tags.join(', ')}

Este es un documento de ejemplo en la plataforma de gestión de cumplimiento.
El contenido real del documento se mostraría aquí en un sistema completo.
`;
  };

  const renderDocumentCard = (document: DocumentMetadata) => {
    const categoryInfo = categories.find(cat => cat.key === document.category);
    const fileIcon = getFileIcon(document.file_type);

    return (
      <motion.div
        key={document.id}
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="bg-white dark:bg-gray-800 rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 border border-gray-200 dark:border-gray-700"
      >
        <div className="p-6">
          {/* Encabezado */}
          <div className="flex items-start justify-between mb-4">
            <div className="flex items-center gap-3">
              <div className="text-3xl">{fileIcon}</div>
              <div>
                <h3 className="font-semibold text-lg text-gray-900 dark:text-gray-100">
                  {document.name}
                </h3>
                <p className="text-sm text-gray-500 dark:text-gray-400">
                  {categoryInfo?.icon} {categoryInfo?.label} • {document.file_type.toUpperCase()}
                </p>
              </div>
            </div>
            <button
              onClick={() => handlePreview(document)}
              className="px-4 py-2 bg-blue-100 text-blue-700 rounded-lg hover:bg-blue-200 transition-colors text-sm font-medium"
            >
              Ver
            </button>
          </div>

          {/* Descripción */}
          {document.description && (
            <p className="text-gray-600 dark:text-gray-300 mb-4 text-sm">
              {document.description}
            </p>
          )}

          {/* Tags */}
          {document.tags.length > 0 && (
            <div className="flex flex-wrap gap-2 mb-4">
              {document.tags.map((tag, index) => (
                <span
                  key={index}
                  className="px-2 py-1 bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300 text-xs rounded-full"
                >
                  #{tag}
                </span>
              ))}
            </div>
          )}

          {/* Información del archivo */}
          <div className="flex items-center justify-between text-xs text-gray-500 dark:text-gray-400">
            <span>📊 {formatFileSize(document.file_size)}</span>
            <span>📅 {formatDate(document.created_at)}</span>
          </div>
        </div>
      </motion.div>
    );
  };

  const getFileIcon = (fileType: string): string => {
    switch (fileType.toLowerCase()) {
      case 'pdf':
        return '📄';
      case 'doc':
      case 'docx':
        return '📝';
      case 'txt':
        return '📃';
      default:
        return '📄';
    }
  };

  // Resumen por categorías
  const getCategorySummary = () => {
    const summary = {
      total: documents.length,
      manuales: documents.filter(d => d.category === 'manuales').length,
      politicas: documents.filter(d => d.category === 'politicas').length,
      actas: documents.filter(d => d.category === 'actas').length,
      programas: documents.filter(d => d.category === 'programas').length
    };

    return summary;
  };

  const categorySummary = getCategorySummary();

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-gray-100">
      <Sidebar>
        <div className="p-6 max-w-7xl mx-auto">
          {/* Título */}
          <motion.div initial={fadeIn.initial} animate={fadeIn.animate}>
            <h1 className="text-4xl font-bold mb-2 bg-gradient-to-r from-indigo-600 to-blue-600 bg-clip-text text-transparent">
              📚 Centro de Documentos de Cumplimiento
            </h1>
            <p className="text-gray-600 dark:text-gray-400 mb-8">
              Gestión centralizada de manuales, políticas y actas SARLAFT
            </p>
          </motion.div>

          {/* Banner informativo */}
          <motion.div
            initial={fadeIn.initial}
            animate={fadeIn.animate}
            className="mb-8 p-6 bg-gradient-to-r from-indigo-600 to-blue-600 rounded-xl text-white"
          >
            <h2 className="text-xl font-semibold mb-2">🏛️ Documentación Normativa</h2>
            <p className="opacity-90">
              Acceso a toda la documentación de cumplimiento requerida por la Superintendencia Financiera
            </p>
          </motion.div>

          {/* Resumen de categorías */}
          <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mb-8">
            <div className="bg-white dark:bg-gray-800 rounded-lg p-4 text-center border border-gray-200 dark:border-gray-700">
              <div className="text-3xl mb-2">📁</div>
              <p className="text-sm text-gray-600 dark:text-gray-400">Total</p>
              <p className="text-2xl font-bold text-indigo-600">{categorySummary.total}</p>
            </div>
            <div className="bg-white dark:bg-gray-800 rounded-lg p-4 text-center border border-gray-200 dark:border-gray-700">
              <div className="text-3xl mb-2">📖</div>
              <p className="text-sm text-gray-600 dark:text-gray-400">Manuales</p>
              <p className="text-2xl font-bold text-blue-600">{categorySummary.manuales}</p>
            </div>
            <div className="bg-white dark:bg-gray-800 rounded-lg p-4 text-center border border-gray-200 dark:border-gray-700">
              <div className="text-3xl mb-2">📋</div>
              <p className="text-sm text-gray-600 dark:text-gray-400">Políticas</p>
              <p className="text-2xl font-bold text-purple-600">{categorySummary.politicas}</p>
            </div>
            <div className="bg-white dark:bg-gray-800 rounded-lg p-4 text-center border border-gray-200 dark:border-gray-700">
              <div className="text-3xl mb-2">📝</div>
              <p className="text-sm text-gray-600 dark:text-gray-400">Actas</p>
              <p className="text-2xl font-bold text-green-600">{categorySummary.actas}</p>
            </div>
            <div className="bg-white dark:bg-gray-800 rounded-lg p-4 text-center border border-gray-200 dark:border-gray-700">
              <div className="text-3xl mb-2">🎯</div>
              <p className="text-sm text-gray-600 dark:text-gray-400">Programas</p>
              <p className="text-2xl font-bold text-orange-600">{categorySummary.programas}</p>
            </div>
          </div>

          {/* Filtros */}
          <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6 mb-8">
            <div className="flex flex-col md:flex-row gap-4 items-center">
              {/* Búsqueda */}
              <div className="flex-1 w-full">
                <div className="relative">
                  <input
                    type="text"
                    placeholder="Buscar documentos por nombre, descripción o etiquetas..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="w-full pl-10 pr-4 py-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 dark:text-white"
                  />
                  <div className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400">
                    🔍
                  </div>
                </div>
              </div>

              {/* Categorías */}
              <div className="flex gap-2 flex-wrap">
                {categories.map(category => (
                  <button
                    key={category.key}
                    onClick={() => setSelectedCategory(category.key)}
                    className={`px-4 py-2 rounded-lg transition-all ${
                      selectedCategory === category.key
                        ? 'bg-indigo-600 text-white'
                        : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600'
                    }`}
                  >
                    <span className="mr-2">{category.icon}</span>
                    {category.label}
                  </button>
                ))}
              </div>
            </div>
          </div>

          {/* Resultados */}
          {loading ? (
            <div className="text-center py-12">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto mb-4"></div>
              <p className="text-gray-600 dark:text-gray-400">Cargando documentos...</p>
            </div>
          ) : (
            <>
              {filteredDocuments.length === 0 ? (
                <div className="text-center py-12 bg-white dark:bg-gray-800 rounded-xl">
                  <div className="text-gray-400 mb-4">
                    <svg className="w-16 h-16 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                  </div>
                  <h3 className="text-lg font-semibold mb-2">No se encontraron documentos</h3>
                  <p className="text-gray-600 dark:text-gray-400">
                    {searchTerm ? 'Prueba con otro término de búsqueda' : 'No hay documentos en esta categoría'}
                  </p>
                </div>
              ) : (
                <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {filteredDocuments.map(renderDocumentCard)}
                </div>
              )}
            </>
          )}

          {/* Modal de vista previa */}
          {isPreviewOpen && selectedDocument && (
            <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
              <div className="bg-white dark:bg-gray-800 rounded-xl shadow-2xl max-w-4xl w-full max-h-[90vh] overflow-hidden">
                {/* Encabezado del modal */}
                <div className="p-6 border-b border-gray-200 dark:border-gray-700">
                  <div className="flex items-center justify-between">
                    <div>
                      <h2 className="text-xl font-semibold">{selectedDocument.name}</h2>
                      <p className="text-sm text-gray-500">
                        {selectedDocument.file_type.toUpperCase()} • {formatFileSize(selectedDocument.file_size)}
                      </p>
                    </div>
                    <button
                      onClick={() => setIsPreviewOpen(false)}
                      className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
                    >
                      <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
                      </svg>
                    </button>
                  </div>
                </div>

                {/* Contenido del modal */}
                <div className="p-6 overflow-y-auto max-h-[calc(90vh-120px)]">
                  <pre className="whitespace-pre-wrap text-sm text-gray-700 dark:text-gray-300 font-mono">
                    {previewContent}
                  </pre>
                </div>

                {/* Pie del modal */}
                <div className="p-6 border-t border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-900">
                  <div className="flex items-center justify-between">
                    <div className="text-sm text-gray-500">
                      📅 {formatDate(selectedDocument.created_at)}
                    </div>
                    <div className="flex gap-2">
                      <button className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors">
                        Descargar
                      </button>
                      <button className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors">
                        Imprimir
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </Sidebar>
    </div>
  );
}