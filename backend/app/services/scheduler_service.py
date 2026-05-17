import requests
import xml.etree.ElementTree as ET
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import ListaRestrictivaCache

# URLs de Listas
OFAC_SDN_URL = "https://www.treasury.gov/ofac/downloads/sdn.xml"
UN_SANCTIONS_URL = "https://scsanctions.un.org/resources/xml/en/consolidated.xml"

def sync_ofac_list():
    print(f"[{datetime.now()}] Iniciando sincronizaci?n OFAC SDN...")
    try:
        response = requests.get(OFAC_SDN_URL, timeout=60)
        response.raise_for_status()
        root = ET.fromstring(response.content)
        
        db: Session = SessionLocal()
        # Limpiar cache anterior de OFAC
        db.query(ListaRestrictivaCache).filter(ListaRestrictivaCache.lista_origen == "OFAC_SDN").delete()
        
        entries = []
        for entry in root.findall(".//{*}sdnEntry"):
            uid = entry.find("{*}uid").text if entry.find("{*}uid") is not None else ""
            last_name = entry.find("{*}lastName").text if entry.find("{*}lastName") is not None else ""
            first_name = entry.find("{*}firstName").text if entry.find("{*}firstName") is not None else ""
            
            nombre_completo = f"{first_name} {last_name}".strip()
            if nombre_completo:
                entries.append(ListaRestrictivaCache(
                    nombre=nombre_completo,
                    documento=uid,
                    lista_origen="OFAC_SDN"
                ))
        
        db.bulk_save_objects(entries)
        db.commit()
        db.close()
        print(f"[{datetime.now()}] OFAC SDN sincronizada: {len(entries)} registros.")
    except Exception as e:
        print(f"[{datetime.now()}] ERROR sincronizando OFAC: {str(e)}")

def sync_un_list():
    print(f"[{datetime.now()}] Iniciando sincronizaci?n ONU...")
    try:
        response = requests.get(UN_SANCTIONS_URL, timeout=60)
        response.raise_for_status()
        root = ET.fromstring(response.content)
        
        db: Session = SessionLocal()
        db.query(ListaRestrictivaCache).filter(ListaRestrictivaCache.lista_origen == "ONU_CONSOLIDATED").delete()
        
        entries = []
        
        # INDIVIDUALS
        for ind in root.findall(".//INDIVIDUAL"):
            dataid = ind.find("DATAID").text if ind.find("DATAID") is not None else ""
            f_name = ind.find("FIRST_NAME").text if ind.find("FIRST_NAME") is not None else ""
            s_name = ind.find("SECOND_NAME").text if ind.find("SECOND_NAME") is not None else ""
            t_name = ind.find("THIRD_NAME").text if ind.find("THIRD_NAME") is not None else ""
            
            nombre = f"{f_name} {s_name} {t_name}".strip()
            if nombre:
                entries.append(ListaRestrictivaCache(
                    nombre=nombre,
                    documento=dataid,
                    lista_origen="ONU_CONSOLIDATED"
                ))
                
        # ENTITIES
        for ent in root.findall(".//ENTITY"):
            dataid = ent.find("DATAID").text if ent.find("DATAID") is not None else ""
            nombre = ent.find("FIRST_NAME").text if ent.find("FIRST_NAME") is not None else ""
            
            if nombre:
                entries.append(ListaRestrictivaCache(
                    nombre=nombre,
                    documento=dataid,
                    lista_origen="ONU_CONSOLIDATED"
                ))

        db.bulk_save_objects(entries)
        db.commit()
        db.close()
        print(f"[{datetime.now()}] ONU sincronizada: {len(entries)} registros.")
    except Exception as e:
        print(f"[{datetime.now()}] ERROR sincronizando ONU: {str(e)}")

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(sync_ofac_list, 'cron', hour=2, minute=0)
    scheduler.add_job(sync_un_list, 'cron', hour=2, minute=30)
    
    scheduler.start()
    print("APScheduler iniciado. Sincronizaci?n programada a las 02:00 AM.")
    return scheduler

