"""
Tool del agente P&L: CLIENTE que llama la API (servidor en Cloud Run) y devuelve texto humano.
Uso: python scripts/pnl_tool.py --tienda_id 45
"""
import sys
from pathlib import Path
import argparse
from urllib.parse import quote

import httpx

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from config.settings import settings

_API_ERROR = (
    "No puedo consultar la API. Verifica que la API este corriendo y que la URL sea correcta."
)


def _get(url: str) -> httpx.Response | None:
    try:
        return httpx.get(url, timeout=30.0)
    except httpx.RequestError:
        return None


def consultar_tienda(tienda_id: int) -> str:
    """GET /api/v1/pnl/{id} -> str legible. Errores -> mensajes, nunca excepciones."""
    url_base = settings.api_base_url.rstrip("/")
    response = _get(f"{url_base}/api/v1/pnl/{tienda_id}")
    if response is None:
        return _API_ERROR
    if response.status_code == 200:
        return formatear_tienda(response.json())
    if response.status_code == 404:
        return f"La tienda {tienda_id} no existe."
    return f"Error inesperado al consultar la API. Codigo de estado: {response.status_code}"


def consultar_comuna(comuna: str) -> str:
    """GET /api/v1/pnl?comuna= -> str legible."""
    url_base = settings.api_base_url.rstrip("/")
    response = _get(f"{url_base}/api/v1/pnl?comuna={quote(comuna)}")
    if response is None:
        return _API_ERROR
    if response.status_code == 200:
        return formatear_comuna(comuna, response.json())
    if response.status_code == 404:
        return f"La comuna {comuna} no existe."
    return f"Error inesperado al consultar la API. Codigo de estado: {response.status_code}"


def consultar_opinc(tienda_id: int) -> str:
    """GET /api/v1/pnl/{id}/opinc -> solo ingreso operativo neto."""
    url_base = settings.api_base_url.rstrip("/")
    response = _get(f"{url_base}/api/v1/pnl/{tienda_id}/opinc")
    if response is None:
        return _API_ERROR
    if response.status_code == 200:
        opinc = response.json()["opinc"]
        return f"La tienda {tienda_id} tiene un OPINC de ${opinc}."
    if response.status_code == 404:
        return f"La tienda {tienda_id} no existe."
    return f"Error inesperado al consultar la API. Codigo de estado: {response.status_code}"


def resumen_portfolio() -> str:
    """GET /api/v1/pnl -> resumen agregado del portfolio completo."""
    url_base = settings.api_base_url.rstrip("/")
    response = _get(f"{url_base}/api/v1/pnl")
    if response is None:
        return _API_ERROR
    if response.status_code != 200:
        return f"Error inesperado al consultar la API. Codigo de estado: {response.status_code}"
    tiendas = response.json()
    if not tiendas:
        return "No hay tiendas en el portfolio."
    return formatear_portfolio(tiendas)


def comparar_tiendas(comuna: str) -> str:
    """Ranking de tiendas por OPINC dentro de una comuna."""
    url_base = settings.api_base_url.rstrip("/")
    response = _get(f"{url_base}/api/v1/pnl?comuna={quote(comuna)}")
    if response is None:
        return _API_ERROR
    if response.status_code == 200:
        tiendas = response.json()
        if not tiendas:
            return f"No hay tiendas en la comuna {comuna}."
        return formatear_ranking_comuna(comuna, tiendas)
    if response.status_code == 404:
        return f"La comuna {comuna} no existe."
    return f"Error inesperado al consultar la API. Codigo de estado: {response.status_code}"


def analizar_tienda(tienda_id: int) -> str:
    """GET /api/v1/pnl/{id}/analisis -> margen y comparacion vs promedio del portfolio."""
    url_base = settings.api_base_url.rstrip("/")
    response = _get(f"{url_base}/api/v1/pnl/{tienda_id}/analisis")
    if response is None:
        return _API_ERROR
    if response.status_code == 200:
        return formatear_analisis(response.json())
    if response.status_code == 404:
        return f"La tienda {tienda_id} no existe."
    return f"Error inesperado al consultar la API. Codigo de estado: {response.status_code}"


def formatear_tienda(data: dict) -> str:
    """JSON (TiendaPL) -> prosa."""
    return (
        f"La tienda {data['tienda_id']} en {data['comuna']} registro ventas de ${data['ventas']}, "
        f"costos de ${data['costos']}, gastos operativos (OPEX) de ${data['opex']} "
        f"y un ingreso operativo neto (OPINC) de ${data['opinc']}."
    )


def formatear_comuna(comuna: str, tiendas: list) -> str:
    if not tiendas:
        return f"No hay tiendas en la comuna {comuna}."
    ids = [str(t["tienda_id"]) for t in tiendas]
    return (
        f"Las tiendas {', '.join(ids)} en {comuna} registran ventas totales de "
        f"${sum(t['ventas'] for t in tiendas)}, costos de ${sum(t['costos'] for t in tiendas)}, "
        f"OPEX de ${sum(t['opex'] for t in tiendas)} y OPINC total de ${sum(t['opinc'] for t in tiendas)}."
    )


def formatear_portfolio(tiendas: list) -> str:
    n = len(tiendas)
    total_opinc = sum(t["opinc"] for t in tiendas)
    avg_opinc = round(total_opinc / n, 2)
    comunas = len({t["comuna"] for t in tiendas})
    return (
        f"Portfolio: {n} tiendas en {comunas} comunas. "
        f"OPINC total ${round(total_opinc, 2)}, promedio ${avg_opinc} por tienda."
    )


def formatear_ranking_comuna(comuna: str, tiendas: list) -> str:
    ordenadas = sorted(tiendas, key=lambda t: t["opinc"], reverse=True)
    lineas = [f"Ranking OPINC en {comuna} ({len(ordenadas)} tiendas):"]
    for i, t in enumerate(ordenadas, 1):
        lineas.append(f"  {i}. Tienda {t['tienda_id']}: OPINC ${t['opinc']}")
    mejor, peor = ordenadas[0], ordenadas[-1]
    lineas.append(
        f"Mejor: tienda {mejor['tienda_id']} (${mejor['opinc']}). "
        f"Peor: tienda {peor['tienda_id']} (${peor['opinc']})."
    )
    return "\n".join(lineas)


def formatear_analisis(data: dict) -> str:
    above = "por encima" if data["diff_opinc_vs_promedio"] >= 0 else "por debajo"
    return (
        f"Analisis tienda {data['tienda_id']} ({data['comuna']}): "
        f"OPINC ${data['opinc']}, margen {data['margen_pct']}% sobre ventas. "
        f"Promedio portfolio: OPINC ${data['promedio_portfolio_opinc']}, "
        f"margen {data['promedio_portfolio_margen_pct']}%. "
        f"Esta tienda esta {above} del promedio en "
        f"${abs(data['diff_opinc_vs_promedio'])} ({abs(data['diff_pct_vs_promedio'])}%)."
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Consulta el P&L de una tienda")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--tienda_id", type=int, help="ID de tienda (1-100)")
    group.add_argument("--comuna", type=str, help="Filtrar por comuna")
    group.add_argument("--opinc", type=int, help="Solo OPINC de una tienda")
    group.add_argument("--portfolio", action="store_true", help="Resumen del portfolio")
    group.add_argument("--ranking", type=str, help="Ranking OPINC por comuna")
    group.add_argument("--analisis", type=int, help="Analisis vs promedio portfolio")
    args = parser.parse_args()
    if args.tienda_id is not None:
        print(consultar_tienda(args.tienda_id))
    elif args.comuna is not None:
        print(consultar_comuna(args.comuna))
    elif args.opinc is not None:
        print(consultar_opinc(args.opinc))
    elif args.portfolio:
        print(resumen_portfolio())
    elif args.ranking is not None:
        print(comparar_tiendas(args.ranking))
    elif args.analisis is not None:
        print(analizar_tienda(args.analisis))


if __name__ == "__main__":
    main()
