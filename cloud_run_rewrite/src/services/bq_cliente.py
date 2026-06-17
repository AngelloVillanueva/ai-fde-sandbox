# `import asyncio
# import random

# class BigQuerySimulatedClient:
#     """Cliente simulado de BigQuery para desarrollo local en el Sandbox."""

#     def __init__(self):
#         # Simulamos una mini base de datos de tiendas en un diccionario
#         self.mock_database = {
#             "store_001": {"revenue": 150000, "discrepancies": 4200, "region": "Santiago"},
#             "store_002": {"revenue": 95000, "discrepancies": 0, "region": "Valparaíso"},
#             "store_045": {"revenue": 210000, "discrepancies": 12500, "region": "Concepción"}
#         }

#     async def get_store_financials(self, store_id: str) -> dict:
#         """Simula una query asíncrona a BigQuery con latencia de red."""
#         # Un FDE simula la latencia real de la nube (ej. 1.2 segundos de espera)
#         await asyncio.sleep(1.2) 
    
#         # Lógica de negocio simulada
#         if store_id in self.mock_database:
#             return {
#                 "store_id": store_id,
#                 "status": "success",
#                 "data": self.mock_database[store_id]
#             }
    
#         return {"store_id": store_id, "status": "error", "message": "Store data not found"}`

import asyncio
import random

class BigQuerySimulatedClient:
    """
    Simula una interfaz de cliente para BigQuery. 
    Encapsula tanto la generación de datos como la lógica de consulta asíncrona.
    """

    def __init__(self):
        # Inicializa el estado interno generando el dataset al momento de instanciar.
        self.mock_database = self._generate_mock_data(100)

    def _generate_mock_data(self, n: int) -> dict:
        """
        Método interno para poblar el diccionario con datos sintéticos.
        Establece la estructura del esquema de datos: (Ventas, Costos, OPEX, Comuna).
        """
        comunas = ["Santiago", "Providencia", "Las Condes", "Valparaíso", 
                   "Viña del Mar", "Concepción", "Antofagasta", "Temuco"]
        data = {}
        
        for i in range(1, n + 1):
            store_id = f"store_{i:03d}"
            
            # Lógica de cálculo para mantener consistencia financiera básica
            ventas = random.randint(5000000, 50000000)
            costos = int(ventas * random.uniform(0.4, 0.7))
            opex = random.randint(1000000, 5000000)
            opinc = ventas - costos - opex
            
            data[store_id] = {
                "ventas": ventas,
                "costos_ventas": costos,
                "opex": opex,
                "opinc": opinc,
                "comuna": random.choice(comunas)
            }
        return data

    async def get_store_financials(self, store_id: str) -> dict:
        """
        Simula una operación I/O de red (consulta a BigQuery).
        El uso de 'await' permite que el hilo principal no se bloquee durante la espera.
        """
        # Simulación de latencia de red (network overhead)
        await asyncio.sleep(0.1) 
        
        # Validación de existencia del recurso y retorno del payload de datos
        if store_id in self.mock_database:
            return {
                "store_id": store_id,
                "status": "success",
                "data": self.mock_database[store_id]
            }
        
        # Manejo de error para casos de misses (404 conceptual)
        return {"store_id": store_id, "status": "error", "message": "Store data not found"}

# Ejecución del event loop para procesar las llamadas asíncronas
async def main():
    client = BigQuerySimulatedClient()
    resultado = await client.get_store_financials("store_001")
    print(resultado)

if __name__ == "__main__":
    asyncio.run(main())