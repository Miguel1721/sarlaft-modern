import random
import time
from datetime import datetime
from typing import Generator

class MonitoringService:
    def __init__(self):
        self.tecnicas_cripto = [
            "Pitufeo (Smurfing)",
            "Mezclador (Tumbler) detectado",
            "Transacción con Wallet sancionada",
            "Salto de cadena (Chain Hopping)",
            "Estructuración de montos",
            "Uso de Exchange de alto riesgo"
        ]
        self.tecnicas_banca = [
            "Fraccionamiento de efectivo",
            "Transferencias internacionales rápidas",
            "Inconsistencia en perfil transaccional",
            "Uso de cuentas puente",
            "Depósitos en efectivo inusuales",
            "Retiros masivos inmediatos"
        ]

    def stream_alerts(self, ecosystem: str) -> Generator[str, None, None]:
        alert_id = 1000
        while True:
            alert_id += 1
            monto = random.randint(1000, 50000)
            riesgo = random.randint(5, 98)
            
            tecnicas = self.tecnicas_cripto if ecosystem == "Cripto" else self.tecnicas_banca
            tecnica = random.choice(tecnicas)
            
            # Formato SSE
            data = {
                "id": f"TX-{alert_id}",
                "tipo": tecnica,
                "monto": f"${monto:,}",
                "riesgo": riesgo,
                "hora": datetime.now().strftime("%H:%M:%S")
            }
            
            import json
            yield f"data: {json.dumps(data)}\n\n"
            
            # Velocidad de simulación (aleatoria para realismo)
            time.sleep(random.uniform(0.5, 3.0))

monitoring_service = MonitoringService()
