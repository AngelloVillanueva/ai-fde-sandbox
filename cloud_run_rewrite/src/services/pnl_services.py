import random
from typing import Dict, List, Optimal

# Importamos el modelo que creamos en el paso anterior
from src.models import TiendaPL

class PNLServices:
    def __init__(self):
        # Aqui vive el diccionario de 100 tiendas simuladas
        # Lo ideal es generarlo una sola ves en una isntacia de servicio
        self._comunas = ["Santiago","Providencia","Las Condes", "Ñuñoa", "Vitacura", "Cerrillos", "La Florida", "La Granja", "San Miguel"]
        self._database: Dict[int, TiendaPL] = self._generador_datos_sinteticos()

    def _generador_datos_sinteticos(self) -> Dict[int, TiendaPL]:
        db = {}
        for i in range(1, 101):
            ventas = round(random.uniform(10000,50000))