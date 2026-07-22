# Paridad obligatoria al agregar tools: pnl_tool.py -> tool_registry.py -> mcp_server.py

from scripts.pnl_tool import (
    analizar_tienda,
    comparar_tiendas,
    consultar_comuna,
    consultar_opinc,
    consultar_tienda,
    resumen_portfolio,
)

TOOL_SCHEMAS = [
    {
        "name": "consultar_tienda",
        "description": (
            "Full P&L for one store: sales, costs, OPEX, OPINC, comuna. "
            "Use when the user asks how a specific store performed overall. "
            "Example: tienda_id 45."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "tienda_id": {
                    "type": "integer",
                    "description": "Store ID (1-100). Example: 45",
                }
            },
            "required": ["tienda_id"],
        },
    },
    {
        "name": "consultar_opinc",
        "description": (
            "Only the OPINC (operating income) for one store. "
            "Use when the user asks specifically for OPINC or net operating income, "
            "not the full breakdown."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "tienda_id": {
                    "type": "integer",
                    "description": "Store ID (1-100). Example: 45",
                }
            },
            "required": ["tienda_id"],
        },
    },
    {
        "name": "consultar_comuna",
        "description": (
            "Aggregate P&L for all stores in a comuna (district). "
            "Use when the user asks about a zone or lists stores in an area."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "comuna": {
                    "type": "string",
                    "description": "Comuna name. Example: La Granja",
                }
            },
            "required": ["comuna"],
        },
    },
    {
        "name": "comparar_tiendas",
        "description": (
            "Rank stores by OPINC within one comuna. "
            "Use when the user asks which store is best or worst in an area, "
            "or wants a comparison/ranking."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "comuna": {
                    "type": "string",
                    "description": "Comuna name. Example: La Granja",
                }
            },
            "required": ["comuna"],
        },
    },
    {
        "name": "resumen_portfolio",
        "description": (
            "Summary of all 100 stores: count, comunas, total and average OPINC. "
            "Use when the user asks about the whole portfolio or overall performance."
        ),
        "parameters": {"type": "object", "properties": {}, "required": []},
    },
    {
        "name": "analizar_tienda",
        "description": (
            "Margin analysis and comparison vs portfolio average for one store. "
            "Use when the user asks if a store is above/below average, margin, "
            "or wants insights beyond raw numbers."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "tienda_id": {
                    "type": "integer",
                    "description": "Store ID (1-100). Example: 45",
                }
            },
            "required": ["tienda_id"],
        },
    },
]


def run_tool(name: str, args: dict) -> str:
    if name == "consultar_tienda":
        return consultar_tienda(args["tienda_id"])
    if name == "consultar_opinc":
        return consultar_opinc(args["tienda_id"])
    if name == "consultar_comuna":
        return consultar_comuna(args["comuna"])
    if name == "comparar_tiendas":
        return comparar_tiendas(args["comuna"])
    if name == "resumen_portfolio":
        return resumen_portfolio()
    if name == "analizar_tienda":
        return analizar_tienda(args["tienda_id"])
    raise ValueError(f"Tool {name} not found")


def get_tool_registry() -> list[dict]:
    return TOOL_SCHEMAS
