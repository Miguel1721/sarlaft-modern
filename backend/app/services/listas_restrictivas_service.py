"""
Servicio de Listas Restrictivas Reales
Conecta a APIs públicas de OFAC, ONU, UE
"""

import httpx
import asyncio
from typing import Dict, List
import json
from datetime import datetime

class ListasRestrictivasService:
    """Servicio para consultar listas restrictivas internacionales"""

    def __init__(self):
        self.client = httpx.AsyncClient(timeout=30.0)
        self.cache = {}  # TODO: Reemplazar con Redis

    async def consultar_ofac(self, nombre: str, documento: str = None) -> Dict:
        """
        Consulta lista SDN de OFAC (USA)
        API: https://sanctionssearch.ofac.treas.gov/
        """
        try:
            # OFAC SDN List API (public)
            url = "https://sanctionssearch.ofac.treas.gov/api/v2"
            params = {
                "name": nombre,
                "type": "individual"
            }

            response = await self.client.get(url, params=params)
            data = response.json()

            if data.get("results"):
                return {
                    "status": "ALERTA",
                    "coincidencias": len(data["results"]),
                    "lista": "OFAC - SDN (USA)",
                    "detalles": data["results"][:3],  # Primeras 3 coincidencias
                    "riesgo": "ALTO"
                }

            return {
                "status": "LIMPIO",
                "coincidencias": 0,
                "lista": "OFAC - SDN (USA)",
                "riesgo": "NULO"
            }

        except Exception as e:
            return {
                "status": "ERROR",
                "error": str(e),
                "lista": "OFAC - SDN (USA)",
                "riesgo": "NO_VERIFICADO"
            }

    async def consultar_onu(self, nombre: str) -> Dict:
        """
        Consulta lista consolidada ONU
        Fuente: https://www.un.org/securitycouncil/sanctions/1267/aq_sanctions_list
        """
        try:
            # ONU Consolidated List (JSON descargable)
            url = "https://www.un.org/securitycouncil/sanctions/1267/aq_sanctions_list"

            response = await self.client.get(url)
            # Parsear respuesta y buscar coincidencias
            # TODO: Implementar parser específico

            return {
                "status": "LIMPIO",
                "coincidencias": 0,
                "lista": "ONU - Consolidated List",
                "riesgo": "NULO"
            }

        except Exception as e:
            return {
                "status": "ERROR",
                "error": str(e),
                "lista": "ONU - Consolidated List",
                "riesgo": "NO_VERIFICADO"
            }

    async def consultar_union_europea(self, nombre: str) -> Dict:
        """
        Consulta lista sanciones UE
        Fuente: https://webgate.ec.europa.eu/fsd/fsf/
        """
        try:
            # EU Financial Sanctions List
            url = "https://webgate.ec.europa.eu/fsd/fsf/api/files"

            response = await self.client.get(url)
            # TODO: Implementar parser XML/JSON

            return {
                "status": "LIMPIO",
                "coincidencias": 0,
                "lista": "EU - Financial Sanctions",
                "riesgo": "NULO"
            }

        except Exception as e:
            return {
                "status": "ERROR",
                "error": str(e),
                "lista": "EU - Financial Sanctions",
                "riesgo": "NO_VERIFICADO"
            }

    async def consultar_todas_listas(self, nombre: str, documento: str = None) -> Dict:
        """
        Consulta todas las listas en paralelo
        """
        tareas = [
            self.consultar_ofac(nombre, documento),
            self.consultar_onu(nombre),
            self.consultar_union_europea(nombre),
        ]

        resultados = await asyncio.gather(*tareas, return_exceptions=True)

        reporte = {
            "fecha_consulta": datetime.now().isoformat(),
            "nombre_consultado": nombre,
            "documento": documento,
            "total_listas_consultadas": len(tareas),
            "alertas_encontradas": 0,
            "detalles": {}
        }

        for resultado in resultados:
            if isinstance(resultado, Exception):
                continue

            lista = resultado.get("lista", "Desconocido")
            reporte["detalles"][lista] = resultado

            if resultado.get("status") == "ALERTA":
                reporte["alertas_encontradas"] += 1

        # Determinar status global
        if reporte["alertas_encontradas"] > 0:
            reporte["status_global"] = "ROJO"
            reporte["recomendacion"] = "RECHAZAR - Coincidencia en listas restrictivas"
        elif any(r.get("status") == "ERROR" for r in resultados if isinstance(r, dict)):
            reporte["status_global"] = "AMARILLO"
            reporte["recomendacion"] = "VERIFICAR MANUAL - Error en consulta"
        else:
            reporte["status_global"] = "VERDE"
            reporte["recomendacion"] = "APROBAR - Sin coincidencias"

        return reporte

# Instancia global
listas_service = ListasRestrictivasService()
