import asyncio
import random

class BigQuerySimulatedClient:
    """Cliente simulado de BigQuery para desarrollo local en el Sandbox."""

    def __init__(self):
        # Simulamos una mini base de datos de tiendas en un diccionario
        self.mock_database = {
            "store_001": {"revenue": 150000, "discrepancies": 4200, "region": "Santiago"},
            "store_002": {"revenue": 95000, "discrepancies": 0, "region": "Valparaíso"},
            "store_045": {"revenue": 210000, "discrepancies": 12500, "region": "Concepción"}
        }

    async def get_store_financials(self, store_id: str) -> dict:
        """Simula una query asíncrona a BigQuery con latencia de red."""
        # Un FDE simula la latencia real de la nube (ej. 1.2 segundos de espera)
        await asyncio.sleep(1.2) 
        
        # Lógica de negocio simulada
        if store_id in self.mock_database:
            return {
                "store_id": store_id,
                "status": "success",
                "data": self.mock_database[store_id]
            }
        
        return {"store_id": store_id, "status": "error", "message": "Store data not found"}