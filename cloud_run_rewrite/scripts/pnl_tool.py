"""
Tool del agente P&L: CLIENTE que llama la API (servidor en Cloud Run) y devuelve texto humano.
Uso: python scripts/pnl_tool.py --tienda_id 45
Fase 2: el LLM invocará consultar_tienda() directamente.
"""
import sys
from pathlib import Path
import argparse

import httpx  # Cliente HTTP (GET a la API, como un navegador en código)

# Python no encuentra config/ al correr desde scripts/ — agregamos cloud_run_rewrite/ al path
_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from config.settings import settings  # API_BASE_URL desde env var (12-factor)


def consultar_tienda(tienda_id: int) -> str:
    """GET /api/v1/pnl/{id} → str legible. Errores → mensajes, nunca excepciones."""
    url_base = settings.api_base_url.rstrip("/")  # evita doble slash en la URL
    endpoint = f"{url_base}/api/v1/pnl/{tienda_id}"

    try:
        response = httpx.get(endpoint, timeout=15.0)
    except httpx.RequestError:
        return "No puedo consulta la API. Verifica que la API esté corriendo y que la URL sea correcta."

    if response.status_code == 200:
        return formatear_tienda(response.json())

    if response.status_code == 404:
        return f"La tienda {tienda_id} no existe."

    return f"Error inesperado al consultar la API. Codigo de estado: {response.status_code}"

def consultar_comuna(comuna: str) -> str:
    """GET /api/v1/pnl?{comuna} → str legible. Errores → mensajes, nunca excepciones."""
    url_base = settings.api_base_url.rstrip("/")  # evita doble slash en la URL
    endpoint = f"{url_base}/api/v1/pnl?comuna={comuna}"

    try:
        response = httpx.get(endpoint, timeout=15.0)
    except httpx.RequestError:
        return "No puedo consulta la API. Verifica que la API esté corriendo y que la URL sea correcta."

    if response.status_code == 200:
        return formatear_comuna(comuna,response.json())

    if response.status_code == 404:
        return f"La comuna {comuna} no existe."

    return f"Error inesperado al consultar la API. Codigo de estado: {response.status_code}"



def formatear_tienda(data: dict) -> str:
    """JSON (TiendaPL) → prosa. Separado de HTTP para testear y alimentar al LLM sin JSON crudo."""
    return (
        f"La tienda {data['tienda_id']} {data['comuna']} registro unas ventas de ${data['ventas']}, "
        f"unos costos de ${data['costos']}, unos gastos opertaivos u opex de {data['opex']} "
        f"y unos ingresos operativos netos de ${data['opinc']}"
    )

def formatear_comuna(comuna: str, tienda: list) -> str:
    if not tienda:
        return f"No hay tiendas en la comuna {comuna}."

    ids = [str(t['tienda_id']) for t in tienda]
    return (f"Las tiendas {', '.join(ids)} en {comuna} registran unas ventas de ${sum(t['ventas'] for t in tienda)}, "
        f"unos costos de ${sum(t['costos'] for t in tienda)}, unos gastos operativos u opex de {sum(t['opex'] for t in tienda)} "
        f"y unos ingresos operativos netos de ${sum(t['opinc'] for t in tienda)}")

def main() -> None:
    """CLI: simula al orquestador del agente pasando tienda_id por terminal."""
    parser = argparse.ArgumentParser(description="Consulta el P&L de una tienda")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--tienda_id", type=int, help="ID de tienda (1-100)")
    group.add_argument("--comuna", type=str, help="Filtrar por comuna")
    args = parser.parse_args()
    if args.tienda_id is not None:
        print(consultar_tienda(args.tienda_id))
    else:
        print(consultar_comuna(args.comuna))


if __name__ == "__main__":
    main()
