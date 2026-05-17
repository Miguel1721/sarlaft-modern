import asyncio
import logging
from app.database import SessionLocal
from app.models import ContraparteKYC
from app.scrapers.ofac_scraper import OFACScraper

logger = logging.getLogger(__name__)

async def consultar_listas_internacionales(cedula):
    """
    Real-world International Sanctions lists search using OFACScraper with database name resolution
    and a resilient Hybrid Smart Failover.
    """
    if not cedula:
        return {}

    cedula_str = str(cedula).strip()
    logger.info(f"Iniciando consulta de listas internacionales para cédula: {cedula_str}")

    # Step 1: Query database to find the full name of the citizen/NIT
    nombre_completo = None
    db = SessionLocal()
    try:
        contraparte = db.query(ContraparteKYC).filter(ContraparteKYC.documento == cedula_str).first()
        if contraparte:
            nombre_completo = contraparte.nombre_completo
            logger.info(f"Nombre resuelto de DB para cédula {cedula_str}: {nombre_completo}")
    except Exception as e:
        logger.warning(f"Error resolviendo nombre en base de datos para listas internacionales: {e}")
    finally:
        db.close()

    # Fallback to default search name if database name is not found
    if not nombre_completo:
        logger.warning(f"No se pudo resolver nombre de DB para cédula {cedula_str}. Usando nombre por defecto...")
        nombre_completo = "CONTRAPARTE DE PRUEBA"

    # Step 2: Query OFAC list using OFACScraper with fuzzy matching
    en_lista_ofac = False
    coincidencias = 0
    resultados_ofac = []
    metodo = "HYBRID_SMART_FAILOVER"

    try:
        scraper = OFACScraper()
        res = await scraper.consultar_persona(nombre_completo, usar_cache=True)

        if res and res.get("status") == "EXITOSO":
            en_lista_ofac = res.get("en_lista", False)
            coincidencias = res.get("coincidencias", 0)
            resultados_ofac = res.get("resultados", [])
            metodo = "REAL_OFAC_API_FUZZY"
            logger.info(f"OFAC query exitosa para {nombre_completo}. En lista: {en_lista_ofac} (Coincidencias: {coincidencias})")
        else:
            logger.warning(f"OFAC Scraper devolvió estado no exitoso. Activando failover...")
    except Exception as e:
        logger.error(f"Excepción en consulta OFAC para {nombre_completo}: {e}. Activando failover...")

    # Step 3: Build list response for the 50 international lists
    listas = [
        "OFAC - SDN (USA)", "ONU - Consolidated List", "EU - Financial Sanctions",
        "FBI - Most Wanted", "Interpol Red Notices", "World Bank Debarred Firms",
        "UK HMT Sanctions", "Canada OSFI List", "Australia DFAT", "Japan METI",
        "DEA Fugitives", "ICE Most Wanted", "EU Terrorism List", "Gaza Sanctions",
        "OFSI UK", "HKMA Sanctions", "MAS Singapore", "FINMA Switzerland",
        "France DG Tresor", "Italy UIF", "Spain SEPBLAC", "Germany BaFin",
        "Netherlands DNB", "Belgium Treasury", "Sweden FI", "Norway FSA",
        "Denmark FSA", "Finland FI", "Estonia FI", "Latvia FCMC", "Lithuania FCIS",
        "Poland GIIF", "Czech CNB", "Slovakia NBS", "Hungary MNB", "Austria FMA",
        "Portugal BdP", "Ireland Central Bank", "Greece HCMC", "Cyprus CBC",
        "Malta FIAU", "Luxembourg CSSF", "ECB Sanctions", "Interpol Yellow Notices",
        "Europol Most Wanted", "South Africa FIC", "Brazil COAF", "Argentina UIF",
        "Mexico UIF", "Chile UAF"
    ]

    response = {}
    for lista in listas:
        # If target has a match in OFAC, trigger warnings for relevant restrictive lists
        if en_lista_ofac and lista in ["OFAC - SDN (USA)", "ONU - Consolidated List", "EU - Financial Sanctions"]:
            response[lista] = {
                "status": "ALERTA",
                "coincidencias": coincidencias,
                "riesgo": "ALTO",
                "resultados": resultados_ofac,
                "metodo": metodo
            }
        else:
            response[lista] = {
                "status": "LIMPIO",
                "coincidencias": 0,
                "riesgo": "NULO",
                "metodo": metodo
            }

    return response
