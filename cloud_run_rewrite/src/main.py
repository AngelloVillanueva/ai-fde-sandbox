from fastapi import FastAPI, Request, Query, From #fastapi es uina libreria que te permite crear APis y poder consultarlas
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# HTTPX es un modo de consulta cerrado con mayor seguridad que la consulta tradicional HTTP
import httpx 

app = FastAPI(title="Cloud Run FDE Microservice")

# desde el modulo de app obtenemos el health
@app.get("/health")

# async def sse usar para funciones que puedan ser pausada y luego volver a ser invocada para completarse. A diferencia del def normal que es secuencial
# Esto es muy util si queremos hacer otras cosas mientas "esperamos" la respuesta del servidor o la app
async def health_check():
    """Endpoint básico de monitoreo para Cloud Run."""
    return {"status": "healthy", "service": "ai-fde-balancer"}

@app.get("/fetch-data")
async def fetch_external_data():
    """Ejemplo de consumo asíncrono de API externa usando HTTPX."""
    async with httpx.AsyncClient() as client:
        # Simulamos una llamada asíncrona a un microservicio externo
        response = await client.get("https://httpbin.org/delay/1")
        return {"network_status": response.status_code, "data": "processed"}