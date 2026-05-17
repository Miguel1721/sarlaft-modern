import requests
import json

def run_test(name, url, payload):
    print(f"\n--- {name} ---")
    print(f"URL: {url}")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    try:
        r = requests.post(url, json=payload, timeout=120)
        print(f"Status Code: {r.status_code}")
        data = r.json()
        print(f"Response: {json.dumps(data, indent=2)}")
        return data
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    # Prueba 1: Deep Search
    audit_data = run_test(
        "Prueba 1: Deep Search (Solo Cédula)",
        "http://localhost:8000/api/v1/auditar",
        {"cedula": "1026575786", "placa": "", "client_id": "test_backend_001"}
    )

    # Prueba 2: Onboarding Kit
    onboarding_data = run_test(
        "Prueba 2: Onboarding Kit (ZIP)",
        "http://localhost:8000/api/v1/onboarding/generar_kit",
        {
           "razon_social": "CDA BACKEND TEST",
           "nit": "900.999.999-1",
           "ciudad": "BOGOTA",
           "departamento": "CUNDINAMARCA",
           "direccion": "Calle 100 #15-30",
           "telefono": "3101234567",
           "correo": "contacto@backendtest.com",
           "regimen": "RESPONSABLE DE IVA",
           "representante_legal": "MIGUEL LOZANO",
           "cedula_representante": "1026575786",
           "nombre_oc": "GUSTAVO ADOLFO",
           "oc_cedula": "1111222333",
           "oc_correo": "cumplimiento@backendtest.com",
           "horas_formacion_oc": "120",
           "institucion_certificante_oc": "Universidad Javeriana",
           "oc_experiencia_meses": 28,
           "oc_suplente_nombre": "ANA MARIA",
           "oc_suplente_cedula": "444555666",
           "oc_suplente_correo": "ana@backendtest.com",
           "ingresos_anuales": 1500000000.0,
           "empleados": 25,
           "servicios": "CDA CLASE A, B, C, D",
           "zonas_operacion": "BOGOTA, SOACHA",
           "fecha_implementacion": "2026-05-16"
        }
    )
