from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()

# Datos de conexión a Odoo
url = "https://ansaproyectos.odoo.com"
db = "ansaproyectos"
username = "js@ansaproyectos.com"
password = "Ansa_1492?"

# Función para autenticar y obtener la cookie de sesión
def authenticate():
    auth_payload = {
        "jsonrpc": "2.0",
        "params": {
            "db": db,
            "login": username,
            "password": password
        }
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(url + "/web/session/authenticate", json=auth_payload, headers=headers)
    if response.status_code == 200 and "result" in response.json():
        return response.cookies.get("session_id")
    else:
        raise HTTPException(status_code=401, detail="Authentication failed")

# Endpoint para obtener clientes
@app.get("/clientes")
def get_clientes():
    session_id = authenticate()
    query_payload = {
        "jsonrpc": "2.0",
        "method": "call",
        "params": {
            "model": "res.partner",
            "method": "search_read",
            "args": [[["customer_rank", ">", 0]]],
            "kwargs": {
                "fields": ["id", "name", "email", "phone", "company_type", "is_company"],
                "limit": 50
            }
        }
    }
    headers = {
        "Content-Type": "application/json",
        "Cookie": f"session_id={session_id}"
    }
    response = requests.post(url + "/web/dataset/call_kw", json=query_payload, headers=headers)
    if response.status_code == 200 and "result" in response.json():
        return response.json()["result"]
    else:

        print("Error al consultar Odoo:")
        print(response.status_code)
        print(response.text)
        raise HTTPException(status_code=400, detail=response.text)

# Ejecutar la aplicación
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
