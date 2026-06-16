from fastapi import FastAPI
import httpx

app = FastAPI(title="Cloud Run FDE Microservice")

@app.get("/health")
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