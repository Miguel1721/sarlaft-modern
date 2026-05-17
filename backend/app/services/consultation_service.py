import asyncio
from typing import List, Dict, Optional
import random
from datetime import datetime

class ConsultationService:
    async def search(self, query: str) -> List[Dict]:
        # Simulamos una búsqueda en listas restrictivas y bases de datos
        await asyncio.sleep(1.5) # Simular latencia
        
        results = [
            {
                "id": f"CONS_{random.randint(1000, 9999)}",
                "nombre": "JUAN PEREZ GARCIA",
                "documento": query if query.isdigit() else "12345678",
                "tipo": "Persona Natural",
                "riesgo": "BAJO",
                "score": 0.12,
                "coincidencias": ["OFAC (No)", "Interpol (No)", "Rama Judicial (1)"],
                "created_at": datetime.now().isoformat()
            },
            {
                "id": f"CONS_{random.randint(1000, 9999)}",
                "nombre": "INVERSIONES ALPHA S.A.S",
                "documento": query if not query.isdigit() else "900.123.456-7",
                "tipo": "Persona Jurídica",
                "riesgo": "MEDIO",
                "score": 0.45,
                "coincidencias": ["Prensa Negativa (2)", "Panama Papers (No)"],
                "created_at": datetime.now().isoformat()
            }
        ]
        
        # Si el query es específico, filtramos o generamos algo más relevante
        if "80" in query:
            results[0]["riesgo"] = "ALTO"
            results[0]["score"] = 0.89
            results[0]["coincidencias"].append("Lista Clinton (SI)")
            
        return results

    async def get_details(self, consulta_id: str) -> Optional[Dict]:
        return {
            "id": consulta_id,
            "detalles_completos": "Esta es una simulación de los detalles de la consulta migrada del sistema anterior."
        }

consultation_service = ConsultationService()
