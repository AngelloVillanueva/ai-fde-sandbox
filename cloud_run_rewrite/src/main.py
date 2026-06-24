from fastapi import FastAPI, HTTPException, Query
from typing import List, Optional
from src.models import TiendaPL
from src.services.pnl_services import PNLService

app = FastAPI(title="FDE P&L Dashboard & Agent API")

# Inicializamos el servicio una sola vez (Singleton conceptual)
pnl_service = PNLService()

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "ai-fde-balancer"}


@app.get("/api/v1/pnl", response_model=List[TiendaPL])
def get_pnl(comuna: Optional[str] = Query(None, description="Filtrar tiendas por comuna")):
    """
    Este endpoint lo usará tanto tu Dashboard (para listar) 
    como el Agente (cuando le pregunten por una zona/comuna).
    """
    if comuna:
        return pnl_service.get_tiendas_por_comuna(comuna)
    return pnl_service.get_todas_las_tiendas()

@app.get("/api/v1/pnl/{tienda_id}", response_model=TiendaPL)
def get_tienda_pnl(tienda_id: int):
    """
    Endpoint clave para el agente: si el usuario pregunta '¿Cómo le fue a la tienda 45?',
    el agente extraerá el ID 45 y llamará a esta herramienta.
    """
    tienda = pnl_service.get_tienda_por_id(tienda_id)
    if not tienda:
        raise HTTPException(status_code=404, detail=f"La tienda {tienda_id} no existe")
    return tienda


@app.get("/api/v1/pnl/{tienda_id}/opinc", response_model=dict)
def get_opinc_por_id(tienda_id: int):
    opinc = pnl_service.get_opinc_por_id(tienda_id)
    if not opinc:
        raise HTTPException(status_code=404, detail=f"La tienda {tienda_id} no existe")
    return {"opinc": opinc}