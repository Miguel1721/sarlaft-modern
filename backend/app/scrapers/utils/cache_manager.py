"""
CACHE MANAGER - Sistema de cache para evitar bans y mejorar performance
Autor: antigravity AI
"""

import asyncio
from datetime import datetime, timedelta
from typing import Dict, Optional
import hashlib
import json


class CacheManager:
    """Maneja cache de consultas"""

    def __init__(self, ttl_horas: int = 24):
        self.cache: Dict[str, Dict] = {}
        self.ttl = timedelta(hours=ttl_horas)
        self.lock = asyncio.Lock()

    def _generar_key(self, fuente: str, consulta: str) -> str:
        """Genera key única para cache"""
        texto = f"{fuente}:{consulta}"
        return hashlib.sha256(texto.encode()).hexdigest()

    async def obtener(self, fuente: str, consulta: str) -> Optional[Dict]:
        """Obtiene resultado cacheado si existe y no ha expirado"""
        async with self.lock:
            key = self._generar_key(fuente, consulta)

            if key in self.cache:
                entrada = self.cache[key]

                if datetime.now() - entrada['timestamp'] < self.ttl:
                    edad = (datetime.now() - entrada['timestamp']).total_seconds() / 3600
                    print(f"✅ CACHE HIT: {fuente} - {consulta} (edad: {edad:.1f}h)")
                    return entrada['datos']
                else:
                    # Expiró, eliminar
                    del self.cache[key]
                    print(f"⏰ CACHE EXPIRADO: {fuente} - {consulta}")

            return None

    async def guardar(self, fuente: str, consulta: str, datos: Dict):
        """Guarda resultado en cache"""
        async with self.lock:
            key = self._generar_key(fuente, consulta)

            self.cache[key] = {
                'datos': datos,
                'timestamp': datetime.now()
            }

            print(f"💾 CACHE GUARDADO: {fuente} - {consulta}")

    async def limpiar_expirados(self):
        """Limpia entradas expiradas del cache"""
        async with self.lock:
            ahora = datetime.now()

            keys_a_borrar = [
                key for key, entrada in self.cache.items()
                if ahora - entrada['timestamp'] >= self.ttl
            ]

            for key in keys_a_borrar:
                del self.cache[key]

            if keys_a_borrar:
                print(f"🧹 Limpiados {len(keys_a_borrar)} entries expirados")

    async def obtener_estadisticas(self) -> Dict:
        """Retorna estadísticas del cache"""
        total = len(self.cache)
        ahora = datetime.now()

        validos = sum(
            1 for entrada in self.cache.values()
            if ahora - entrada['timestamp'] < self.ttl
        )

        expirados = total - validos

        return {
            "total_entries": total,
            "validos": validos,
            "expirados": expirados,
            "ttl_horas": self.ttl.total_seconds() / 3600
        }


class RateLimiter:
    """Limita frecuencia de peticiones para evitar bans"""

    def __init__(self, peticiones_por_minuto: int = 10):
        self.ppm = peticiones_por_minuto
        self.peticiones = []
        self.lock = asyncio.Lock()

    async def acquire(self):
        """Espera si se excede el rate limit"""
        async with self.lock:
            ahora = datetime.now()

            # Eliminar peticiones antiguas (más de 1 minuto)
            self.peticiones = [
                p for p in self.peticiones
                if ahora - p < timedelta(minutes=1)
            ]

            # Si se excede el límite, esperar
            if len(self.peticiones) >= self.ppm:
                tiempo_espera = timedelta(minutes=1) / len(self.peticiones)
                print(f"⏸️ RATE LIMIT: Esperando {tiempo_espera.total_seconds():.1f}s...")
                await asyncio.sleep(tiempo_espera.total_seconds())

            # Registrar petición
            self.peticiones.append(ahora)

    async def obtener_info(self) -> Dict:
        """Retorna información del rate limiter"""
        ahora = datetime.now()

        peticuras_ultimo_minuto = [
            p for p in self.peticiones
            if ahora - p < timedelta(minutes=1)
        ]

        return {
            "peticiones_ultimo_minuto": len(peticuras_ultimo_minuto),
            "limite": self.ppm,
            "porcentaje_uso": len(peticuras_ultimo_minuto) / self.ppm * 100
        }
