"""
Servicio de Gestión de Beneficiarios Finales y PEPs
Implementa requerimientos Resolución 2328 Circular 024
"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, validator

class BeneficiarioFinal(BaseModel):
    """Modelo de Beneficiario Final"""
    tipo_persona: str  # NATURAL / JURIDICA
    documento: str
    nombre: str
    porcentaje_propiedad: float  # > 25% debe reportarse
    rol: str  # ACCIONISTA / REPRESENTANTE / APODERADO
    es_pep: bool = False
    cargo_publico: Optional[str] = None
    vinculo_pep: Optional[str] = None  # Si es familiar de PEP

    @validator('porcentaje_propiedad')
    def validar_porcentaje(cls, v):
        if not (0 <= v <= 100):
            raise ValueError('Porcentaje debe estar entre 0 y 100')
        return v

class PersonaExpuestaPoliticamente(BaseModel):
    """Modelo de PEP"""
    documento: str
    nombre: str
    cargo_publico: str
    entidad: str
    nivel: str  # NACIONAL / DEPARTAMENTAL / MUNICIPAL / INTERNACIONAL
    ambito: str  # EJECUTIVO / LEGISLATIVO / JUDICIAL / OTRO
    fecha_vinculacion: Optional[datetime] = None
    vinculos_familiares: List[str] = []  # Documentos de familiares

class BeneficiariosService:
    """Servicio para gestión de beneficiarios finales y PEPs"""

    def __init__(self):
        self.lista_pep_cache = []  # TODO: Conectar a lista oficial
        self.umbral_propiedad = 25.0  # 25% mínimo para reportar

    def analizar_estructura_propiedad(self, accionistas: List[Dict]) -> Dict:
        """
        Analiza estructura accionaria para identificar beneficiarios finales

        Args:
            accionistas: Lista de {
                'documento': str,
                'nombre': str,
                'porcentaje': float,
                'tipo': str  # NATURAL/JURIDICA
            }
        """
        beneficiarios_finales = []
        alertas = []

        for accionista in accionistas:
            porcentaje = accionista.get('porcentaje', 0)

            # Si tiene > 25%, es beneficiario final
            if porcentaje > self.umbral_propiedad:
                bf = {
                    **accionista,
                    "es_beneficiario_final": True,
                    "requiere_verificacion": True,
                    "fecha_identificacion": datetime.now().isoformat()
                }

                # Si es persona jurídica, requiere desglose adicional
                if accionista.get('tipo') == 'JURIDICA':
                    bf["requiere_estructura_detallada"] = True
                    alertas.append({
                        "codigo": "BF-JUR-001",
                        "mensaje": f"Persona jurídica con {porcentaje}% requiere desglose de propiedad real"
                    })

                beneficiarios_finales.append(bf)

        # Validar que el total sume 100%
        total_propiedad = sum(a.get('porcentaje', 0) for a in accionistas)
        if abs(total_propiedad - 100.0) > 1.0:  # Tolerancia 1%
            alertas.append({
                "codigo": "BF-TOT-001",
                "mensaje": f"Estructura accionaria no suma 100% (actual: {total_propiedad}%)",
                "criticidad": "ALTA"
            })

        return {
            "beneficiarios_finales": beneficiarios_finales,
            "total_porcentaje_identificado": total_propiedad,
            "alertas": alertas,
            "requiere_investigacion_adicional": len(alertas) > 0
        }

    def verificar_pep(self, documento: str, nombre: str) -> Dict:
        """
        Verifica si una persona es PEP

        Args:
            documento: Cédula o documento de identidad
            nombre: Nombre completo
        """
        # TODO: Integrar con lista oficial PEP (no existe en Colombia)
        # Por ahora, devuelve resultado basado en parámetros

        # Simulación: buscar en cache
        pep_encontrado = next(
            (p for p in self.lista_pep_cache if p["documento"] == documento),
            None
        )

        if pep_encontrado:
            return {
                "es_pep": True,
                "detalle": pep_encontrado,
                "recomendacion": "APLICAR DEBIDA DILIGENCIA INTENSIFICADA",
                "requiere_monitoreo_continuo": True,
                "requiere_aprobacion_nivel_gerencial": True
            }

        return {
            "es_pep": False,
            "recomendacion": "PROCESO ESTÁNDAR",
            "requiere_monitoreo_continuo": False
        }

    def analizar_grupo_familiar(self, pep: PersonaExpuestaPoliticamente) -> Dict:
        """
        Analiza familiares de PEP que también deben considerarse PEP

        Circulo familiar PEP:
        - Cónyuge o compañero permanente
        - Hijos (incluidos adoptivos)
        - Padres
        - Hermanos
        """
        familia_expuesta = []

        # Por cada vinculo familiar, se debe aplicar DD intensificada
        for familiar_doc in pep.vinculos_familiares:
            familia_expuesta.append({
                "documento": familiar_doc,
                "vinculo": "FAMILIAR PEP",
                "nombre_pep_referente": pep.nombre,
                "cargo_pep_referente": pep.cargo_publico,
                "requiere_dd_intensificada": True
            })

        return {
            "pep_principal": pep.dict(),
            "familiares_expuestos": familia_expuesta,
            "total_personas_expuestas": 1 + len(familia_expuesta),
            "recomendacion": "Aplicar DD intensificada a todas las personas expuestas"
        }

    def generar_reporte_beneficiarios(self, estructura: Dict, peps: List[Dict]) -> str:
        """
        Genera reporte narrativo de beneficiarios y PEPs
        """
        reporte = []

        # Sección 1: Beneficiarios Finales
        reporte.append("## BENEFICIARIOS FINALES IDENTIFICADOS\n")

        for bf in estructura.get("beneficiarios_finales", []):
            reporte.append(f"- {bf['nombre']} ({bf['documento']})")
            reporte.append(f"  Porcentaje: {bf['porcentaje']}%")
            reporte.append(f"  Rol: {bf['rol']}")

            if bf.get("requiere_estructura_detallada"):
                reporte.append(f"  ⚠️ Requiere desglose de propiedad real (persona jurídica)")

        # Sección 2: Alertas
        if estructura.get("alertas"):
            reporte.append("\n## ALERTAS DE ESTRUCTURA\n")
            for alerta in estructura["alertas"]:
                reporte.append(f"⚠️ {alerta['mensaje']}")

        # Sección 3: PEPs
        if peps:
            reporte.append("\n## PERSONAS EXPUESTAS POLÍTICAMENTE\n")

            for pep_info in peps:
                if pep_info["es_pep"]:
                    pep = pep_info["detalle"]
                    reporte.append(f"- {pep['nombre']} - {pep['cargo_publico']}")
                    reporte.append(f"  Entidad: {pep['entidad']}")
                    reporte.append(f"  Nivel: {pep['nivel']}")

        # Sección 4: Recomendaciones
        reporte.append("\n## RECOMENDACIONES\n")

        if estructura.get("requiere_investigacion_adicional"):
            reporte.append("⚠️ Estructura accionaria requiere investigación adicional")

        if any(p["es_pep"] for p in peps):
            reporte.append("⚠️ Aplicar Debida Diligencia Intensificada por presencia de PEPs")

        return "\n".join(reporte)

# Instancia global
beneficiarios_service = BeneficiariosService()
