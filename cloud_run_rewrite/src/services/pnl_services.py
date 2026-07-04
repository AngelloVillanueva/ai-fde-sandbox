from typing import Dict, List, Optional
from src.services.bq_cliente import BigQuerySimulatedClient

# Importamos el modelo que creamos en el paso anterior
from src.models import TiendaPL

class PNLService:
    def __init__(self):
        # Aqui vive el diccionario de 100 tiendas simuladas
        # Lo ideal es generarlo una sola ves en una isntacia de servicio
        self._bq = BigQuerySimulatedClient()
        self._database = self._bq.mock_database

    def get_tienda_por_id(self, tienda_id: int) -> Optional[TiendaPL]:
        return self._database.get(tienda_id)
        
    def get_todas_las_tiendas(self) -> List[TiendaPL]:
        return list(self._database.values())
    
    async def get_tienda_por_id_async(self, tienda_id: int) -> dict:
        return await self._bq.get_tienda_por_id(tienda_id)
    
    def get_tiendas_por_comuna(self, comuna: str) -> List[TiendaPL]:
        return [t for t in self._database.values() if t.comuna.lower() == comuna.lower()]

    def get_opinc_por_id(self, tienda_id: int) -> Optional[float]:
        tienda = self.get_tienda_por_id(tienda_id)
        if tienda:
            return tienda.opinc
        return None
