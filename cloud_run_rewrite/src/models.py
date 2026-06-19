from pydantic import BaseModel

class TiendaPL(BaseModel):
    tienda_id: int
    ventas: float
    costos: float
    opex: float
    opinc: float
    comuna: str