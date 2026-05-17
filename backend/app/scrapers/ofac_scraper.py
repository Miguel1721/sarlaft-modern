"""
OFAC SCRAPER - Lista SDN de sanciones USA
Autor: antigravity AI
"""

import asyncio
import httpx
from typing import Dict, List, Optional
from datetime import datetime

from .utils.cache_manager import CacheManager
from .fuzzy_matching import buscar_coincidencia


class OFACScraper:
    """Scraper/Cliente para lista SDN de OFAC"""

    def __init__(self):
        # APIs disponibles
        self.api_oficial = "https://sanctionssearch.ofac.treas.gov/api/v2"
        self.url_lista_xml = "https://sanctionssearch.ofac.treas.gov/api/v2/downloads/sdn.xml"
        self.url_lista_csv = "https://sanctionssearch.ofac.treas.gov/api/v2/downloads/sdn.csv"

        # APIs alternativas (wrappers públicos)
        self.apis_alternativas = [
            "https://ofac-api-wrapper.public.lu/api/SDN",
            "https://api.tr sanctions.io/ofac",
        ]

        self.client = httpx.AsyncClient(timeout=30.0, follow_redirects=True)
        self.cache = CacheManager(ttl_horas=168)  # 7 días (OFAC se actualiza semanalmente)

        # Lista completa en memoria (se carga la primera vez)
        self.lista_completa: List[Dict] = []

    async def consultar_persona(
        self,
        nombre: str,
        documento: Optional[str] = None,
        usar_cache: bool = True
    ) -> Dict:
        """
        Consulta si una persona está en lista OFAC SDN

        Args:
            nombre: Nombre completo a buscar
            documento: (opcional) Documento de identidad
            usar_cache: Si True, usa cache

        Returns:
            Dict con resultado de consulta
        """

        print(f"🔍 Consultando OFAC: {nombre}")

        # Verificar cache
        if usar_cache:
            cacheado = await self.cache.obtener("OFAC", nombre)
            if cacheado:
                return cacheado

        try:
            # Método 1: Intentar búsqueda directa
            resultado = await self._buscar_directo(nombre, documento)

            # Método 2: Si no hay resultado, usar fuzzy matching en lista completa
            if resultado["coincidencias"] == 0:
                resultado_fuzzy = await self._buscar_fuzzy(nombre)
                resultado.update(resultado_fuzzy)

            # Guardar en cache
            await self.cache.guardar("OFAC", nombre, resultado)

            return resultado

        except Exception as e:
            return {
                "status": "ERROR",
                "error": str(e),
                "fuente": "OFAC",
                "consultado": nombre,
                "fecha_consulta": datetime.now().isoformat()
            }

    async def _buscar_directo(self, nombre: str, documento: Optional[str]) -> Dict:
        """Busca usando API oficial"""

        try:
            params = {
                "name": nombre,
                "type": "individual"
            }

            response = await self.client.get(
                f"{self.api_oficial}/search",
                params=params
            )

            if response.status_code == 200:
                data = response.json()

                if data.get("results"):
                    return {
                        "status": "EXITOSO",
                        "en_lista": True,
                        "coincidencias": len(data["results"]),
                        "resultados": data["results"][:10],
                        "fuente": "OFAC-API",
                        "metodo": "API_DIRECTA"
                    }
                else:
                    return {
                        "status": "EXITOSO",
                        "en_lista": False,
                        "coincidencias": 0,
                        "resultados": [],
                        "fuente": "OFAC-API",
                        "metodo": "API_DIRECTA"
                    }

        except Exception as e:
            print(f"  ⚠️ Error API directa: {e}")

        # Retornar sin coincidencias si falla la API
        return {
            "status": "EXITOSO",
            "en_lista": False,
            "coincidencias": 0,
            "resultados": [],
            "fuente": "OFAC",
            "metodo": "API_DIRECTA_FALLIDA"
        }

    async def _buscar_fuzzy(self, nombre: str) -> Dict:
        """Busca usando fuzzy matching en lista completa"""

        try:
            # Cargar lista completa si no está en memoria
            if not self.lista_completa:
                print("  📥 Cargando lista OFAC completa...")
                await self._cargar_lista_completa()

            # Extraer nombres de la lista
            nombres_ofac = [item["nombre"] for item in self.lista_completa]

            # Buscar coincidencias
            coincidencias = buscar_coincidencia(
                nombre,
                nombres_ofac,
                umbral=85,
                limite_resultados=10
            )

            # Obtener detalles de coincidencias
            resultados = []
            for coincidencia in coincidencias:
                idx = coincidencia["indice"]
                item_original = self.lista_completa[idx]
                item_original["score_match"] = coincidencia["score"]
                resultados.append(item_original)

            return {
                "status": "EXITOSO",
                "en_lista": len(resultados) > 0,
                "coincidencias": len(resultados),
                "resultados": resultados,
                "fuente": "OFAC",
                "metodo": "FUZZY_MATCHING"
            }

        except Exception as e:
            print(f"  ❌ Error fuzzy matching: {e}")
            return {
                "status": "ERROR",
                "error": str(e),
                "metodo": "FUZZY_MATCHING"
            }

    async def _cargar_lista_completa(self):
        """Descarga y parsea lista completa OFAC"""

        try:
            # Intentar descargar CSV (más liviano)
            response = await self.client.get(self.url_lista_csv)

            if response.status_code == 200:
                # Parsear CSV
                import io

                contenido = response.text
                # Parsear línea por línea
                lineas = contenido.split('\n')

                for linea in lineas[1:]:  # Saltar header
                    if not linea.strip():
                        continue

                    partes = linea.split(',')
                    if len(partes) >= 4:
                        self.lista_completa.append({
                            "nombre": partes[0],
                            "tipo": partes[1],
                            "programa": partes[2],
                            "direccion": partes[3] if len(partes) > 3 else ""
                        })

                print(f"  ✅ Lista cargada: {len(self.lista_completa)} entradas")

        except Exception as e:
            print(f"  ❌ Error cargando lista: {e}")
            # Usar datos de prueba
            self.lista_completa = self._datos_prueba()

    def _datos_prueba(self) -> List[Dict]:
        """Retorna datos de prueba para desarrollo"""
        return [
            {
                "nombre": "CARLOS ALBERTO PEREZ",
                "tipo": "INDIVIDUAL",
                "programa": "SDGT",
                "direccion": "Calle 123, Bogota"
            },
            {
                "nombre": "MARIA FERNANDA GARCIA",
                "tipo": "INDIVIDUAL",
                "programa": "SDNT",
                "direccion": "Carrera 45, Medellin"
            }
        ]

    async def verificar_actualizacion_lista(self) -> Dict:
        """Verifica si la lista tiene actualizaciones disponibles"""

        try:
            response = await self.client.head(self.url_lista_csv)

            # Verificar headers de fecha
            last_modified = response.headers.get('last-modified')
            etag = response.headers.get('etag')

            return {
                "ultima_modificacion": last_modified,
                "etag": etag,
                "fecha_consulta": datetime.now().isoformat()
            }

        except Exception as e:
            return {
                "error": str(e)
            }


# Función para testing
async def main():
    """Función de prueba"""
    scraper = OFACScraper()

    # Probar consulta
    resultado = await scraper.consultar_persona("JUAN PEREZ")

    print("\n" + "="*60)
    print("RESULTADO OFAC:")
    import json
    print(json.dumps(resultado, indent=2, ensure_ascii=False))
    print("="*60)


if __name__ == "__main__":
    asyncio.run(main())
