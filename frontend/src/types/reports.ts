/**
 * Tipos para el módulo de Reportes
 */

export interface AlertDetail {
  id: string;
  transaction_type: string;
  user_id?: string;
  amount: number;
  risk_score: number;
  is_fraud: boolean;
  is_suspicious: boolean;
  model_version: string;
  status: string;
  created_at: string;
}

export interface ROSReportRequest {
  entity_name: string;
  entity_nit: string;
  contact_person: string;
  contact_email: string;
  phone: string;
  alerts: AlertDetail[];
}

export interface ReportMetadata {
  report_id: string;
  report_type: string;
  generated_at: string;
  entity_name: string;
  total_alerts: number;
  high_risk_count: number;
  medium_risk_count: number;
  detection_rate: number;
  file_size: number;
}

export interface ReportsSummary {
  total_reports: number;
  reports_this_month: number;
  average_detection_rate: number;
  high_risk_operations: number;
  pending_review: number;
}

export interface ReportTemplate {
  name: string;
  type: string;
  authority: string;
  description: string;
  fields_required: string[];
  format: string;
  file_extension: string;
}

export interface ReportData {
  id: string;
  type: 'ROS' | 'ROC' | 'RTE';
  created_at: string;
  status: 'PENDING' | 'APPROVED' | 'REJECTED';
  risk_score: number;
  transaction_data: any;
  assessment: any;
}