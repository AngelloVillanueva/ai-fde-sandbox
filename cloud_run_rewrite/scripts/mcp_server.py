import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from fastmcp import FastMCP
from scripts.tool_registry import run_tool

mcp = FastMCP("pnl-tools")


@mcp.tool()
def consultar_tienda(tienda_id: int) -> str:
    """Full P&L for one store (sales, costs, OPEX, OPINC). Store ID 1-100."""
    return run_tool("consultar_tienda", {"tienda_id": tienda_id})


@mcp.tool()
def consultar_opinc(tienda_id: int) -> str:
    """Only OPINC for one store. Use when user asks specifically for operating income."""
    return run_tool("consultar_opinc", {"tienda_id": tienda_id})


@mcp.tool()
def consultar_comuna(comuna: str) -> str:
    """Aggregate P&L for all stores in a comuna."""
    return run_tool("consultar_comuna", {"comuna": comuna})


@mcp.tool()
def comparar_tiendas(comuna: str) -> str:
    """Rank stores by OPINC within a comuna."""
    return run_tool("comparar_tiendas", {"comuna": comuna})


@mcp.tool()
def resumen_portfolio() -> str:
    """Summary of all 100 stores: totals and average OPINC."""
    return run_tool("resumen_portfolio", {})


@mcp.tool()
def analizar_tienda(tienda_id: int) -> str:
    """Margin and comparison vs portfolio average for one store."""
    return run_tool("analizar_tienda", {"tienda_id": tienda_id})


if __name__ == "__main__":
    mcp.run()
