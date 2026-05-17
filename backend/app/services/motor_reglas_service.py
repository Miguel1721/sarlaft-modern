"""
Motor de Reglas SARLAFT - Detección de Operaciones Inusuales
Implementa señales de alerta UIAF para CDAs
"""

from typing import Dict, List, Any
from datetime import datetime, timedelta
from enum import Enum

class NivelRiesgo(Enum):
    BAJO = "BAJO"
    MEDIO = "MEDIO"
    ALTO = "ALTO"
    CRITICO = "CRITICO"

class SenialAlerta(Enum):
    """Señales de alerta UIAF para sector transporte"""
    FRACCIONAMIENTO_EFECTIVO = "EFR-001"
    EFECTIVO_GRANDES_MONTOS = "EFR-002"
    NO_RELACION_ACTIVIDAD = "ACT-001"
    GEOGRAFIA_INUSUAL = "GEO-001"
    COMPORTAMIENTO_ATIPICO = "COM-001"
    SIN_HISTORIAL = "HIS-001"
    CAMBIO_REPENTINO = "CAM-001"
    OPERACIONES_SIMULTANEAS = "SIM-001"

class MotorReglasSARLAFT:
    """Motor de reglas para detección de operaciones inusuales"""

    def __init__(self):
        self.umbrales = {
            "efectivo_diario_max": 10000000,  # $10M COP
            "efectivo_mensual_max": 30000000,  # $30M COP
            "operaciones_sin_relacion": 2,
            "dias_inactividad_alerta": 180,  # 6 meses
            "cambio_porcentaje_alerta": 300,  # 300% aumento
        }

    def evaluar_transaccion(self, transaccion: Dict, historial: List[Dict] = None) -> Dict:
        """
        Evalúa una transacción contra todas las reglas

        Args:
            transaccion: Dict con {
                'monto': float,
                'forma_pago': str,
                'fecha': datetime,
                'cliente_id': str,
                'actividad_economica': str,
                'descripcion': str
            }
            historial: Lista de transacciones previas del cliente
        """
        alertas = []
        nivel_riesgo = NivelRiesgo.BAJO

        # REGLA 1: Fraccionamiento de Efectivo
        alerta_efectivo = self._detectar_fraccionamiento_efectivo(transaccion, historial)
        if alerta_efectivo:
            alertas.append(alerta_efectivo)
            nivel_riesgo = max(nivel_riesgo, NivelRiesgo.ALTO)

        # REGLA 2: No relación con actividad económica
        alerta_actividad = self._detectar_sin_relacion_actividad(transaccion)
        if alerta_actividad:
            alertas.append(alerta_actividad)
            nivel_riesgo = max(nivel_riesgo, NivelRiesgo.MEDIO)

        # REGLA 3: Cliente sin histórico
        alerta_historial = self._detectar_sin_historial(transaccion, historial)
        if alerta_historial:
            alertas.append(alerta_historial)
            nivel_riesgo = max(nivel_riesgo, NivelRiesgo.MEDIO)

        # REGLA 4: Cambio repentino de comportamiento
        alerta_cambio = self._detectar_cambio_repentino(transaccion, historial)
        if alerta_cambio:
            alertas.append(alerta_cambio)
            nivel_riesgo = max(nivel_riesgo, NivelRiesgo.ALTO)

        # REGLA 5: Operaciones simultáneas
        alerta_simultaneas = self._detectar_operaciones_simultaneas(transaccion, historial)
        if alerta_simultaneas:
            alertas.append(alerta_simultaneas)
            nivel_riesgo = max(nivel_riesgo, NivelRiesgo.CRITICO)

        # Calcular score de riesgo (0-100)
        score = self._calcular_score_riesgo(nivel_riesgo, alertas)

        return {
            "estado": "ALERTA" if alertas else "NORMAL",
            "nivel_riesgo": nivel_riesgo.value,
            "score_riesgo": score,
            "alertas": alertas,
            "recomendacion": self._generar_recomendacion(nivel_riesgo, alertas),
            "requiere_ros": len([a for a in alertas if a.get("criticidad") == "ALTA"]) > 0,
            "fecha_evaluacion": datetime.now().isoformat()
        }

    def _detectar_fraccionamiento_efectivo(self, tx: Dict, historial: List[Dict]) -> Dict:
        """Detecta estructuración de efectivo por debajo del umbral"""
        if tx.get("forma_pago") != "EFECTIVO":
            return None

        # Buscar múltiples transacciones en efectivo en últimos días
        if not historial:
            return None

        ultimos_7_dias = [
            h for h in historial
            if h.get("forma_pago") == "EFECTIVO" and
            datetime.fromisoformat(h["fecha"]) > datetime.now() - timedelta(days=7)
        ] + [tx]

        if len(ultimos_7_dias) >= 3:
            total_efectivo = sum(h.get("monto", 0) for h in ultimos_7_dias)

            if total_efectivo > self.umbrales["efectivo_mensual_max"]:
                return {
                    "codigo": SenialAlerta.FRACCIONAMIENTO_EFECTIVO.value,
                    "descripcion": "Fraccionamiento de efectivo",
                    "detalle": f"{len(ultimos_7_dias)} operaciones en efectivo últimos 7 días. Total: ${total_efectivo:,.0f} COP",
                    "criticidad": "ALTA",
                    "referencia_uiaf": "UIAF Guía Transaction Monitoring - Estructuración"
                }

        return None

    def _detectar_sin_relacion_actividad(self, tx: Dict) -> Dict:
        """Detecta operaciones sin relación con actividad económica declarada"""
        monto = tx.get("monto", 0)
        actividad = tx.get("actividad_economica", "").lower()
        descripcion = tx.get("descripcion", "").lower()

        # Reglas por actividad económica
        umbrales_actividad = {
            "transporte": 50000000,  # $50M
            "comerciario": 30000000,  # $30M
            "profesional": 15000000,  # $15M
            "otro": 10000000,  # $10M
        }

        umbral = umbrales_actividad.get("otro")
        if "transport" in actividad:
            umbral = umbrales_actividad["transporte"]
        elif "comerc" in actividad:
            umbral = umbrales_actividad["comerciario"]

        if monto > umbral:
            return {
                "codigo": SenialAlerta.NO_RELACION_ACTIVIDAD.value,
                "descripcion": "Operación sin relación con actividad económica",
                "detalle": f"Monto ${monto:,.0f} COP supera umbral razonable para actividad '{actividad}' (${umbral:,.0f})",
                "criticidad": "MEDIA",
                "referencia_uiaf": "UIAF Guía Debida Diligencia - Conocimiento Cliente"
            }

        return None

    def _detectar_sin_historial(self, tx: Dict, historial: List[Dict]) -> Dict:
        """Detecta transacciones de clientes sin histórico"""
        if not historial or len(historial) == 0:
            monto = tx.get("monto", 0)
            if monto > self.umbrales["efectivo_diario_max"]:
                return {
                    "codigo": SenialAlerta.SIN_HISTORIAL.value,
                    "descripcion": "Primera operación de alto monto",
                    "detalle": f"Cliente sin histórico transaccional. Monto: ${monto:,.0f} COP",
                    "criticidad": "MEDIA",
                    "referencia_uiaf": "UIAF Guía KYC - Cliente Nuevo"
                }

        return None

    def _detectar_cambio_repentino(self, tx: Dict, historial: List[Dict]) -> Dict:
        """Detecta cambios repentinos en comportamiento transaccional"""
        if not historial or len(historial) < 3:
            return None

        # Calcular promedio histórico
        montos_historicos = [h.get("monto", 0) for h in historial[-10:]]
        promedio_historico = sum(montos_historicos) / len(montos_historicos)

        monto_actual = tx.get("monto", 0)

        if promedio_historico > 0:
            cambio_porcentaje = ((monto_actual - promedio_historico) / promedio_historico) * 100

            if cambio_porcentaje > self.umbrales["cambio_porcentaje_alerta"]:
                return {
                    "codigo": SenialAlerta.CAMBIO_REPENTINO.value,
                    "descripcion": "Cambio repentino en comportamiento",
                    "detalle": f"Aumento del {cambio_porcentaje:.0f}% vs promedio histórico (${promedio_historico:,.0f} COP)",
                    "criticidad": "ALTA",
                    "referencia_uiaf": "UIAF Guía Transaction Monitoring - Cambio Patrón"
                }

        return None

    def _detectar_operaciones_simultaneas(self, tx: Dict, historial: List[Dict]) -> Dict:
        """Detecta operaciones simultáneas (posible coordinación)"""
        if not historial:
            return None

        tx_datetime = datetime.fromisoformat(tx["fecha"])

        # Buscar operaciones en misma ventana de 2 horas
        simultaneas = [
            h for h in historial
            if abs((datetime.fromisoformat(h["fecha"]) - tx_datetime).total_seconds()) <= 7200  # 2 horas
        ]

        if len(simultaneas) >= 3:
            return {
                "codigo": SenialAlerta.OPERACIONES_SIMULTANEAS.value,
                "descripcion": "Múltiples operaciones simultáneas",
                "detalle": f"{len(simultaneas)} operaciones en ventana de 2 horas. Posible coordinación.",
                "criticidad": "ALTA",
                "referencia_uiaf": "UIAF Guía Transaction Monitoring - Layering"
            }

        return None

    def _calcular_score_riesgo(self, nivel: NivelRiesgo, alertas: List[Dict]) -> int:
        """Calcula score numérico de riesgo (0-100)"""
        base_scores = {
            NivelRiesgo.BAJO: 10,
            NivelRiesgo.MEDIO: 40,
            NivelRiesgo.ALTO: 70,
            NivelRiesgo.CRITICO: 95
        }

        score = base_scores[nivel]

        # Ajustar por cantidad de alertas
        score += len(alertas) * 5

        return min(score, 100)

    def _generar_recomendacion(self, nivel: NivelRiesgo, alertas: List[Dict]) -> str:
        """Genera recomendación de acción"""
        if nivel == NivelRiesgo.BAJO:
            return "PROCESAR NORMAL - Sin alertas"

        if nivel == NivelRiesgo.MEDIO:
            return "REVISAR - Documentar justificación cliente"

        if nivel == NivelRiesgo.ALTO:
            return "ALERTA - Considerar reporte ROS si se confirma sospecha"

        if nivel == NivelRiesgo.CRITICO:
            return "CRÍTICO - Requiere análisis inmediato y posible ROS"

        return "REVISAR MANUAL"

# Instancia global
motor_reglas = MotorReglasSARLAFT()
