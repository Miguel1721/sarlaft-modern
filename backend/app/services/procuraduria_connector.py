
import asyncio

async def consultar_async(placa, cedula):
    await asyncio.sleep(0.5)
    return {"status": "LIMPIO", "mensaje": "Sin sanciones vigentes."}
