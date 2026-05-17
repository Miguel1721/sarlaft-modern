/**
 * Tipos para el módulo de Analytics
 */

// Tipos básicos de transacción
export interface BankingTransaction {
  tipo_operacion: string;
  monto: number;
  saldo_disponible_origen: number;
}

export interface DigitalContext {
  dispositivo: string;
  ip_origen: string;
  hora_transaccion: number;
}

export interface BeneficiaryInfo {
  id_cuenta_destino: string;
  relacion_beneficiario: string;
}

export interface DueDiligence {
  actividad_economica_ciiu?: string;
  origen_fondos?: string;
  es_pep: boolean;
  traza_mixer_darknet: boolean;
  antiguedad_wallet_dias: number;
}

// Tipos complejos
export interface BankingAnalysisRequest {
  transaccion: BankingTransaction;
  contexto_digital: DigitalContext;
  beneficiario: BeneficiaryInfo;
  debida_diligence: DueDiligence;
}

export interface RiskAssessment {
  risk_score: number;
  risk_percentage: number;
  risk_level: 'BAJO' | 'MEDIO' | 'ALTO';
  action_required: 'APROBAR' | 'REVISAR' | 'BLOQUEAR';
  factors_detected: string[];
  explanation: string;
}

export interface SearchResult {
  transaction_id: string;
  risk_score: number;
  amount: number;
  timestamp: string;
  status: string;
  factors: string[];
}

export interface SearchFilters {
  monto_min?: number;
  monto_max?: number;
  fecha_inicio?: string;
  fecha_fin?: string;
  riesgo_min?: number;
  riesgo_max?: number;
  tipo_operacion?: string;
}

// Tipos para gráficos
export interface ChartData {
  name: string;
  value: number;
  color?: string;
}

export interface TimeSeriesData {
  date: string;
  value: number;
  risk_level?: 'BAJO' | 'MEDIO' | 'ALTO';
}

// Tipos de API
export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
  timestamp: string;
}

export interface AnalyticsSummary {
  total_transactions: number;
  high_risk_count: number;
  medium_risk_count: number;
  low_risk_count: number;
  average_risk_score: number;
  top_risk_factors: string[];
}

// Tipos para reportes
export interface ReportData {
  id: string;
  type: 'ROS' | 'ROC' | 'RTE';
  created_at: string;
  status: 'PENDING' | 'APPROVED' | 'REJECTED';
  risk_score: number;
  transaction_data: BankingTransaction;
  assessment: RiskAssessment;
}