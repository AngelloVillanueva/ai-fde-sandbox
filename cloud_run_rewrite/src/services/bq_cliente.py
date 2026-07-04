import asyncio
import random
from src.models import TiendaPL
from typing import Dict, Optional


class BigQuerySimulatedClient:
    """
    Simula una interfaz de cliente para BigQuery. 
    Encapsula tanto la generación de datos como la lógica de consulta asíncrona.
    """

# Definimos una funcion de inicio para generan 100 datos aleatorios
    def __init__(self):
        # Inicializa el estado interno generando el dataset al momento de instanciar.
        self._comunas = ["Santiago","Providencia","Las Condes", "Ñuñoa", "Vitacura", "Cerrillos", "La Florida", "La Granja", "San Miguel"]
        self.mock_database: Dict[int, TiendaPL]  = self._generate_mock_data(100)
        
# Funcion real de datos aleatorios 
    def _generate_mock_data(self, n: int) -> Dict[int, TiendaPL]:
        """
        Método interno para poblar el diccionario con datos sintéticos.
        Establece la estructura del esquema de datos: (Ventas, Costos, OPEX, Comuna).
        """
        random.seed(42)
        data = {}
        for i in range(1, 101):
           
            ventas = round(random.uniform(10000,50000))
            costos = round(ventas * random.uniform(0.4,0.6),2)
            opex = round(ventas* random.uniform(0.15,0.25),2)
            opinc = round(ventas-costos-opex,2)
            comuna = random.choice(self._comunas)
            
            data[i] = TiendaPL(
                tienda_id=i,
                ventas=ventas,
                costos=costos,
                opex=opex,
                opinc=opinc,
                comuna=comuna
            )
        return data

    async def get_tienda_por_id(self, tienda_id: int) -> TiendaPL:
        """
        Simula una operación I/O de red (consulta a BigQuery).
        El uso de 'await' permite que el hilo principal no se bloquee durante la espera.
        """
        # Simulación de latencia de red (network overhead)
        await asyncio.sleep(0.5) 
        
        # Validación de existencia del recurso y retorno del payload de datos
        if tienda_id in self.mock_database:
            return {
                "tienda_id": tienda_id,
                "status": "success",
                "data": self.mock_database[tienda_id]
            }
        
        # Manejo de error para casos de misses (404 conceptual)
        # error
        return {
            "tienda_id": tienda_id,
            "status": "error",
            "message": "Store data not found",
        }

# Ejecución del event loop para procesar las llamadas asíncronas
async def main():
    client = BigQuerySimulatedClient()
    resultado = await client.get_tienda_por_id(tienda_id=45)
    print(resultado)

if __name__ == "__main__":
    asyncio.run(main())