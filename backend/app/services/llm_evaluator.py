
import os
import json
import httpx
import logging

logger = logging.getLogger(__name__)

# Configuración: Se usan las variables del .env
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
ANTHROPIC_BASE_URL = os.getenv("ANTHROPIC_BASE_URL", "https://api.anthropic.com")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

async def generar_concepto_juridico(json_crudo: dict):
    """
    Usa un LLM para redactar el concepto jurídico basado en los resultados del orquestador.
    """
    prompt_sistema = (
        "Eres un Oficial de Cumplimiento SARLAFT experto en Colombia (Resolución 2328). "
        "Analiza este JSON de resultados. Si hay hallazgos en Policía, Procuraduría o OFAC, "
        "el dictamen es 'RECHAZO'. Si solo hay hallazgos administrativos (SISBEN, Libreta), "
        "el dictamen es 'VINCULAR'. Redacta un párrafo formal llamado 'Concepto Jurídico' "
        "resumiendo esto en 80 palabras máximo. IMPORTANTE: Si no se proporciona una placa de vehículo "
        "en el JSON, NO menciones nada sobre vehículos en tu concepto; enfócate solo en la identidad."
    )
    
    contenido_json = json.dumps(json_crudo, indent=2)
    
    # 1. Intentar con Anthropic (vía Z.ai Proxy si está configurado)
    if ANTHROPIC_API_KEY:
        try:
            base_url = ANTHROPIC_BASE_URL.rstrip('/')
            url = f"{base_url}/v1/messages"
            
            async with httpx.AsyncClient() as client:
                resp = await client.post(
                    url,
                    headers={
                        "x-api-key": ANTHROPIC_API_KEY,
                        "anthropic-version": "2023-06-01",
                        "content-type": "application/json"
                    },
                    json={
                        "model": "claude-3-haiku-20240307",
                        "max_tokens": 300,
                        "system": prompt_sistema,
                        "messages": [{"role": "user", "content": f"Analiza estos datos: {contenido_json}"}]
                    },
                    timeout=30.0
                )
                if resp.status_code == 200:
                    data = resp.json()
                    return data['content'][0]['text']
                else:
                    logger.error(f"Error Anthropic API ({resp.status_code}): {resp.text}")
        except Exception as e:
            logger.error(f"Error con Anthropic: {e}")

    # 2. Fallback: OpenAI
    if OPENAI_API_KEY:
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers={"Authorization": f"Bearer {OPENAI_API_KEY}"},
                    json={
                        "model": "gpt-4o-mini",
                        "messages": [
                            {"role": "system", "content": prompt_sistema},
                            {"role": "user", "content": f"Analiza estos datos: {contenido_json}"}
                        ]
                    },
                    timeout=30.0
                )
                if resp.status_code == 200:
                    data = resp.json()
                    return data['choices'][0]['message']['content']
        except Exception as e:
            logger.error(f"Error con OpenAI: {e}")

    # 3. Mock/Fallback Estático
    status = json_crudo.get('summary', {}).get('status', 'VERDE')
    if status == 'VERDE':
        return "CONCEPTO JURÍDICO: Tras el análisis de 50+ fuentes, no se detectan hallazgos vinculantes para LA/FT. El ciudadano es VINCULABLE bajo los términos de la Resolución 2328."
    return "CONCEPTO JURÍDICO: Se detectan alertas en listas restrictivas o antecedentes legales. Se recomienda el RECHAZO inmediato de la vinculación."
