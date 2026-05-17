'use client';

import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import Sidebar from '@/components/Sidebar';
import {
  BankingTransaction,
  DigitalContext,
  BeneficiaryInfo,
  DueDiligence,
  BankingAnalysisRequest,
  RiskAssessment
} from '@/types/analytics';

export default function BankingAnalyticsPage() {
  // Estados del formulario
  const [transaction, setTransaction] = useState<BankingTransaction>({
    tipo_operacion: 'TRANSFER',
    monto: 5000000.0,
    saldo_disponible_origen: 10000000.0
  });

  const [digitalContext, setDigitalContext] = useState<DigitalContext>({
    dispositivo: '📱 iPhone 14 (Conocido)',
    ip_origen: '🇨🇴 Colombia (Local)',
    hora_transaccion: 14
  });

  const [beneficiary, setBeneficiary] = useState<BeneficiaryInfo>({
    id_cuenta_destino: 'C-9999999',
    relacion_beneficiario: 'Proveedor Frecuente'
  });

  const [dueDiligence, setDueDiligence] = useState<DueDiligence>({
    actividad_economica_ciiu: 'Servicios Informáticos (J620)',
    origen_fondos: 'Salario/Nómina',
    es_pep: false,
    traza_mixer_darknet: false,
    antiguedad_wallet_dias: 365
  });

  // Estados de análisis
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [assessment, setAssessment] = useState<RiskAssessment | null>(null);
  const [error, setError] = useState<string | null>(null);

  // Animaciones
  const fadeIn = {
    initial: { opacity: 0, y: 20 },
    animate: { opacity: 1, y: 0, transition: { duration: 0.5 } }
  };

  const slideUp = {
    initial: { opacity: 0, y: 30 },
    animate: { opacity: 1, y: 0, transition: { duration: 0.6, delay: 0.1 } }
  };

  // Manejar envío del formulario
  const handleAnalyze = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsAnalyzing(true);
    setError(null);
    setAssessment(null);

    try {
      const requestData: BankingAnalysisRequest = {
        transaccion: transaction,
        contexto_digital: digitalContext,
        beneficiario: beneficiary,
        debida_diligence: dueDiligence
      };

      const response = await fetch('/api/analytics/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestData),
      });

      if (!response.ok) {
        throw new Error('Error en el análisis de la transacción');
      }

      const result = await response.json();
      setAssessment(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error desconocido');
    } finally {
      setIsAnalyzing(false);
    }
  };

  // Renderizar semáforo de riesgo
  const renderRiskGauge = (riskScore: number) => {
    const riskPercentage = riskScore * 100;

    let barColor, bgColor, textColor, statusText, actionText;

    if (riskScore > 0.8) {
      barColor = '#dc2626';
      bgColor = '#fee2e2';
      textColor = '#dc2626';
      statusText = '🚨 RIESGO CRÍTICO';
      actionText = 'BLOQUEAR';
    } else if (riskScore > 0.5) {
      barColor = '#f59e0b';
      bgColor = '#fef3c7';
      textColor = '#f59e0b';
      statusText = '⚠️ RIESGO MEDIO';
      actionText = 'REVISAR';
    } else {
      barColor = '#16a34a';
      bgColor = '#d1fae5';
      textColor = '#16a34a';
      statusText = '✅ TRANSACCIÓN SEGURA';
      actionText = 'APROBAR';
    }

    return (
      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        className="w-full max-w-md mx-auto"
      >
        <div className="relative">
          {/* Gauge */}
          <div className={`w-full h-8 rounded-full overflow-hidden bg-gray-200 dark:bg-gray-800`}>
            <div
              className="h-full rounded-full transition-all duration-1000 ease-out"
              style={{
                width: `${riskPercentage}%`,
                backgroundColor: barColor
              }}
            />
          </div>

          {/* Porcentaje */}
          <div className="absolute top-0 left-0 w-full h-full flex items-center justify-center">
            <span className={`font-bold text-lg ${riskScore > 0.5 ? 'text-white' : 'text-gray-700 dark:text-gray-300'}`}>
              {riskPercentage.toFixed(1)}%
            </span>
          </div>
        </div>

        {/* Estado y Acción */}
        <div className={`text-center mt-4 p-4 rounded-lg ${bgColor} border border-l-4 ${barColor}`}>
          <p className={`font-bold text-lg ${textColor}`}>
            {statusText}
          </p>
          <p className={`mt-2 font-semibold ${textColor}`}>
            Acción: {actionText}
          </p>
        </div>
      </motion.div>
    );
  };

  // Renderizar factores de riesgo
  const renderRiskFactors = (factors: string[]) => {
    if (!factors.length) {
      return (
        <div className="text-green-500 bg-green-50 dark:bg-green-900/20 p-4 rounded-lg">
          ✅ No se detectaron factores de riesgo. La transacción presenta comportamientos normales.
        </div>
      );
    }

    return (
      <div className="space-y-3">
        <h3 className="text-lg font-semibold text-red-600 dark:text-red-400">
          🚩 Factores de Riesgo Detectados
        </h3>
        <div className="space-y-2">
          {factors.map((factor, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.1 }}
              className="bg-red-50 dark:bg-red-900/20 border-l-4 border-red-400 p-3 rounded-r-lg"
            >
              <p className="text-red-700 dark:text-red-300">{factor}</p>
            </motion.div>
          ))}
        </div>
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-gray-100">
      <Sidebar>
        <div className="p-6 max-w-7xl mx-auto">
          {/* Título */}
          <motion.div initial={fadeIn.initial} animate={fadeIn.animate}>
            <h1 className="text-4xl font-bold mb-2 bg-gradient-to-r from-green-600 to-emerald-600 bg-clip-text text-transparent">
              🏦 Análisis Bancario Multidimensional
            </h1>
            <p className="text-gray-600 dark:text-gray-400 mb-8">
              Sistema de detección de riesgo de lavado de activos transaccional
            </p>
          </motion.div>

          {/* Banner informativo */}
          <motion.div
            initial={fadeIn.initial}
            animate={fadeIn.animate}
            className="mb-8 p-6 bg-gradient-to-r from-green-600 to-emerald-600 rounded-xl text-white"
          >
            <h2 className="text-xl font-semibold mb-2">⚖️ Sistema de Cumplimiento SARLAFT</h2>
            <p className="opacity-90">
              Análisis financiero + contexto digital + debida diligencia para cumplir con Circular Básica Jurídica SFC
            </p>
          </motion.div>

          <div className="grid lg:grid-cols-3 gap-8">
            {/* Panel de formulario */}
            <div className="lg:col-span-2">
              <motion.div
                initial={fadeIn.initial}
                animate={fadeIn.animate}
                className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6"
              >
                <form onSubmit={handleAnalyze} className="space-y-8">
                  {/* Sección 1: Datos Financieros */}
                  <div className="space-y-4">
                    <h3 className="text-xl font-semibold flex items-center">
                      💰 1. Dimensión Financiera
                      <span className="ml-2 text-sm text-gray-500">(Modelo matemático + Reglas SARLAFT)</span>
                    </h3>
                    <div className="grid md:grid-cols-3 gap-4">
                      <div>
                        <label className="block text-sm font-medium mb-2 dark:text-gray-300">
                          Tipo de Operación
                        </label>
                        <select
                          value={transaction.tipo_operacion}
                          onChange={(e) => setTransaction({...transaction, tipo_operacion: e.target.value})}
                          className="w-full p-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 dark:text-white"
                          required
                        >
                          <option value="TRANSFER">TRANSFER</option>
                          <option value="CASH_OUT">CASH_OUT</option>
                          <option value="PAYMENT">PAYMENT</option>
                          <option value="CASH_IN">CASH_IN</option>
                          <option value="DEBIT">DEBIT</option>
                        </select>
                      </div>
                      <div>
                        <label className="block text-sm font-medium mb-2 dark:text-gray-300">
                          Monto ($ USD)
                        </label>
                        <input
                          type="number"
                          value={transaction.monto}
                          onChange={(e) => setTransaction({...transaction, monto: parseFloat(e.target.value) || 0})}
                          min="0"
                          step="10000"
                          className="w-full p-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 dark:text-white"
                          required
                        />
                      </div>
                      <div>
                        <label className="block text-sm font-medium mb-2 dark:text-gray-300">
                          Saldo Origen ($ USD)
                        </label>
                        <input
                          type="number"
                          value={transaction.saldo_disponible_origen}
                          onChange={(e) => setTransaction({...transaction, saldo_disponible_origen: parseFloat(e.target.value) || 0})}
                          min="0"
                          step="10000"
                          className="w-full p-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 dark:text-white"
                          required
                        />
                      </div>
                    </div>
                  </div>

                  <div className="h-px bg-gray-200 dark:bg-gray-700"></div>

                  {/* Sección 2: Contexto Digital */}
                  <div className="space-y-4">
                    <h3 className="text-xl font-semibold flex items-center">
                      📡 2. Huella Digital y Dispositivo
                      <span className="ml-2 text-sm text-gray-500">(Geolocalización + Dispositivo)</span>
                    </h3>
                    <div className="grid md:grid-cols-3 gap-4">
                      <div>
                        <label className="block text-sm font-medium mb-2 dark:text-gray-300">
                          Dispositivo
                        </label>
                        <select
                          value={digitalContext.dispositivo}
                          onChange={(e) => setDigitalContext({...digitalContext, dispositivo: e.target.value})}
                          className="w-full p-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 dark:text-white"
                          required
                        >
                          <option>📱 iPhone 14 (Conocido)</option>
                          <option>💻 Windows PC (Conocido)</option>
                          <option>🤖 Android Genérico (NUEVO)</option>
                          <option>🌐 Tor Browser (SOSPECHOSO)</option>
                        </select>
                      </div>
                      <div>
                        <label className="block text-sm font-medium mb-2 dark:text-gray-300">
                          Geolocalización IP
                        </label>
                        <select
                          value={digitalContext.ip_origen}
                          onChange={(e) => setDigitalContext({...digitalContext, ip_origen: e.target.value})}
                          className="w-full p-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 dark:text-white"
                          required
                        >
                          <option>🇨🇴 Colombia (Local)</option>
                          <option>🇺🇸 USA (Miami)</option>
                          <option>🇪🇺 Unión Europea</option>
                          <option>🇷🇺 Rusia (Alto Riesgo)</option>
                          <option>🇰🇵 Corea del Norte (Sancionado)</option>
                          <option>🇨🇳 China</option>
                        </select>
                      </div>
                      <div>
                        <label className="block text-sm font-medium mb-2 dark:text-gray-300">
                          Hora (24h)
                        </label>
                        <input
                          type="range"
                          min="0"
                          max="23"
                          value={digitalContext.hora_transaccion}
                          onChange={(e) => setDigitalContext({...digitalContext, hora_transaccion: parseInt(e.target.value)})}
                          className="w-full"
                        />
                        <div className="text-center mt-2 font-semibold">{digitalContext.hora_transaccion}:00</div>
                      </div>
                    </div>
                  </div>

                  <div className="h-px bg-gray-200 dark:bg-gray-700"></div>

                  {/* Sección 3: Beneficiario */}
                  <div className="space-y-4">
                    <h3 className="text-xl font-semibold flex items-center">
                      👤 3. Datos del Beneficiario
                      <span className="ml-2 text-sm text-gray-500">(Relación + Cuenta)</span>
                    </h3>
                    <div className="grid md:grid-cols-2 gap-4">
                      <div>
                        <label className="block text-sm font-medium mb-2 dark:text-gray-300">
                          ID Cuenta Destino
                        </label>
                        <input
                          type="text"
                          value={beneficiary.id_cuenta_destino}
                          onChange={(e) => setBeneficiary({...beneficiary, id_cuenta_destino: e.target.value})}
                          className="w-full p-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 dark:text-white"
                          required
                        />
                      </div>
                      <div>
                        <label className="block text-sm font-medium mb-2 dark:text-gray-300">
                          Relación Beneficiario
                        </label>
                        <select
                          value={beneficiary.relacion_beneficiario}
                          onChange={(e) => setBeneficiary({...beneficiary, relacion_beneficiario: e.target.value})}
                          className="w-full p-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 dark:text-white"
                          required
                        >
                          <option>Proveedor Frecuente</option>
                          <option>Empleado</option>
                          <option>Cuenta Nueva (Sin historial)</option>
                          <option>Lista Clinton/OFAC</option>
                        </select>
                      </div>
                    </div>
                  </div>

                  <div className="h-px bg-gray-200 dark:bg-gray-700"></div>

                  {/* Botón de análisis */}
                  <motion.div
                    initial={fadeIn.initial}
                    animate={fadeIn.animate}
                    whileTap={{ scale: 0.98 }}
                  >
                    <button
                      type="submit"
                      disabled={isAnalyzing}
                      className="w-full py-4 px-6 bg-gradient-to-r from-green-600 to-emerald-600 text-white font-semibold rounded-lg hover:from-green-700 hover:to-emerald-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
                    >
                      {isAnalyzing ? (
                        <div className="flex items-center justify-center">
                          <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-white mr-3"></div>
                          Analizando transacción...
                        </div>
                      ) : (
                        '🔍 EJECUTAR ANÁLISIS MULTIDIMENSIONAL'
                      )}
                    </button>
                  </motion.div>
                </form>
              </motion.div>
            </div>

            {/* Panel de resultados */}
            <div className="lg:col-span-1">
              <motion.div
                initial={slideUp.initial}
                animate={slideUp.animate}
                className="sticky top-6"
              >
                {/* Indicador de carga */}
                {isAnalyzing && (
                  <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-8 mb-6">
                    <div className="text-center">
                      <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-green-600 mx-auto mb-4"></div>
                      <p className="text-gray-600 dark:text-gray-400">Realizando análisis multidimensional...</p>
                    </div>
                  </div>
                )}

                {/* Error */}
                {error && (
                  <div className="bg-red-50 dark:bg-red-900/20 border-l-4 border-red-400 p-4 rounded-lg mb-6">
                    <p className="text-red-700 dark:text-red-400">❌ {error}</p>
                  </div>
                )}

                {/* Resultado del análisis */}
                {assessment && (
                  <div className="space-y-6">
                    {/* Gauge de riesgo */}
                    {renderRiskGauge(assessment.risk_score)}

                    {/* Factores de riesgo */}
                    {renderRiskFactors(assessment.factors_detected)}

                    {/* Explicación */}
                    <motion.div
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 p-4 rounded-lg"
                    >
                      <h3 className="font-semibold text-blue-800 dark:text-blue-400 mb-2">
                        📖 Explicación Técnica
                      </h3>
                      <p className="text-sm text-blue-700 dark:text-blue-300">
                        {assessment.explanation}
                      </p>
                    </motion.div>

                    {/* Información adicional */}
                    <div className="bg-gray-100 dark:bg-gray-800 p-4 rounded-lg">
                      <h3 className="font-semibold mb-3">📊 Metodología del Análisis</h3>
                      <ul className="text-sm space-y-2 text-gray-600 dark:text-gray-400">
                        <li>• Modelo XGBoost para detección de patrones</li>
                        <li>• Reglas de negocio bancario</li>
                        <li>• Deuda diligencia ampliada</li>
                        <li>• Cross-referencing con listas restrictivas</li>
                      </ul>
                    </div>
                  </div>
                )}

                {!assessment && !isAnalyzing && (
                  <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-8 text-center">
                    <div className="text-gray-400 mb-4">
                      <svg className="w-16 h-16 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                      </svg>
                    </div>
                    <h3 className="text-lg font-semibold mb-2">Análisis de Riesgo</h3>
                    <p className="text-gray-600 dark:text-gray-400">
                      Ingresa los datos de la transacción para obtener una evaluación completa del riesgo.
                    </p>
                  </div>
                )}
              </motion.div>
            </div>
          </div>
        </div>
      </Sidebar>
    </div>
  );
}