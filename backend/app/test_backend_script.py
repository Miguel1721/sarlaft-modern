import requests
import json

def test_audit():
    url = "http://localhost:8000/api/v1/auditar"
    payload = {
        "cedula": "1026575786",
        "placa": "",
        "client_id": "cda_test_001"
    }
    print(f"Testing Audit with payload: {payload}")
    try:
        r = requests.post(url, json=payload, timeout=60)
        print(f"Status Code: {r.status_code}")
        data = r.json()
        print(f"Full Response: {json.dumps(data, indent=2)}")
        if "pdf_url" in data:
            print(f"SUCCESS: PDF URL generated: {data['pdf_url']}")
            return data['pdf_url']
        else:
            print(f"FAILURE: No pdf_url in response. pdf_error: {data.get('pdf_error')}")
    except Exception as e:
        print(f"Error: {e}")
    return None

def test_download(pdf_url):
    if not pdf_url:
        print("Skipping download test (no URL)")
        return
    
    # Extract filename from URL (e.g., /api/v1/download/filename.pdf)
    filename = pdf_url.split("/")[-1]
    url = f"http://localhost:8000/api/v1/download/{filename}"
    print(f"Testing Download for: {url}")
    
    try:
        r = requests.get(url, stream=True)
        print(f"Status Code: {r.status_code}")
        print(f"Headers: {json.dumps(dict(r.headers), indent=2)}")
        
        content_disposition = r.headers.get("Content-Disposition", "")
        content_type = r.headers.get("Content-Type", "")
        
        if "attachment" in content_disposition and "application/pdf" in content_type:
            print("SUCCESS: Correct headers detected!")
        else:
            print("FAILURE: Headers missing or incorrect.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    pdf_url = test_audit()
    test_download(pdf_url)
