import sys
from pathlib import Path


_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from fastmcp import FastMCP
from scripts.tool_registry import run_tool

mcp = FastMCP("pnl-tools")

# 5. @mcp.tool() consultar_tienda(tienda_id: int) -> str
@mcp.tool()
def consultar_tienda(tienda_id: int) -> str:
    """Consultar el P&L de una tienda por su ID (1-100)."""
    return run_tool("consultar_tienda", {"tienda_id": tienda_id})

# 6. @mcp.tool() consultar_comuna(comuna: str) -> str
@mcp.tool()
def consultar_comuna(comuna: str) -> str:
    """Listar tiendas y P&L filtradas por comuna."""
    return run_tool("consultar_comuna", {"comuna": comuna})


# 7. if __name__ == "__main__": mcp.run()

if __name__ == "__main__":
    mcp.run()