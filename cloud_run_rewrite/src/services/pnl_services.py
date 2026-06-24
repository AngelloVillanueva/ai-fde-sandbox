import random
from typing import Dict, List, Optional

# Importamos el modelo que creamos en el paso anterior
from src.models import TiendaPL

class PNLService:
    def __init__(self):
        # Aqui vive el diccionario de 100 tiendas simuladas
        # Lo ideal es generarlo una sola ves en una isntacia de servicio
        self._comunas = ["Santiago","Providencia","Las Condes", "Ñuñoa", "Vitacura", "Cerrillos", "La Florida", "La Granja", "San Miguel"]
        self._database: Dict[int, TiendaPL] = self._generador_datos_sinteticos()

    def _generador_datos_sinteticos(self) -> Dict[int, TiendaPL]:
        random.seed(42)
        db = {}
        for i in range(1, 101):
            ventas = round(random.uniform(10000,50000))
            costos = round(ventas * random.uniform(0.4,0.6),2)
            opex = round(ventas* random.uniform(0.15,0.25),2)
            opinc = round(ventas-costos-opex,2)
            comuna = random.choice(self._comunas)

            # Guardaremos cada tienda ya formateada como el modelo Pydantic
            db[i] = TiendaPL(
                tienda_id=i,
                ventas=ventas,
                costos=costos,
                opex=opex,
                opinc=opinc,
                comuna=comuna
            )
        return db
    
    def get_todas_las_tiendas(self) -> List[TiendaPL]:
        return list(self._database.values())
    
    def get_tienda_por_id(self, tienda_id: int) -> Optional[TiendaPL]:
        return self._database.get(tienda_id)
    
    def get_tiendas_por_comuna(self, comuna: str) -> List[TiendaPL]:
        return [t for t in self._database.values() if t.comuna.lower() == comuna.lower()]

    def get_opinc_por_id(self, tienda_id: int) -> Optional[float]:
        tienda = self.get_tienda_por_id(tienda_id)
        if tienda:
            return tienda.opinc
        return None
