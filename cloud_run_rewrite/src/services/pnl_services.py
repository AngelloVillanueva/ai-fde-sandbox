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

    def analizar_tienda(self, tienda_id: int) -> Optional[dict]:
        tienda = self.get_tienda_por_id(tienda_id)
        if not tienda:
            return None
        todas = self.get_todas_las_tiendas()
        avg_opinc = sum(t.opinc for t in todas) / len(todas)
        avg_margen = sum(t.opinc / t.ventas for t in todas if t.ventas) / len(todas)
        margen = tienda.opinc / tienda.ventas if tienda.ventas else 0.0
        diff_opinc = tienda.opinc - avg_opinc
        diff_pct = (diff_opinc / avg_opinc * 100) if avg_opinc else 0.0
        return {
            "tienda_id": tienda_id,
            "comuna": tienda.comuna,
            "opinc": tienda.opinc,
            "margen_pct": round(margen * 100, 2),
            "promedio_portfolio_opinc": round(avg_opinc, 2),
            "promedio_portfolio_margen_pct": round(avg_margen * 100, 2),
            "diff_opinc_vs_promedio": round(diff_opinc, 2),
            "diff_pct_vs_promedio": round(diff_pct, 1),
        }
