from scripts.pnl_tool import consultar_tienda, consultar_comuna


TOOL_SCHEMAS = [
    {
        "name": "consultar_tienda",
        "description": "Consultar la información de una tienda en especifico",
        "parameters": {
            "type": "object",
            "properties": {
                "tienda_id": {
                    "type": "integer",
                    "description": "El ID de la tienda a consultar, debe ser un número entero"
                    }
            },
            "required": ["tienda_id"]
        }
    },
    {
        "name": "consultar_comuna",
        "description": "Consultar la información de una comuna en especifico",
        "parameters": {
            "type": "object",
            "properties": {
                "comuna": {
                    "type": "string",
                    "description": "El nombre de la comuna a consultar, debe ser un string"
                }
            },
            "required": ["comuna"]
        }
    }
]


def run_tool(name: str, args: dict) -> str:
    if name == "consultar_tienda":
        return consultar_tienda(args["tienda_id"])
    elif name == "consultar_comuna":
        return consultar_comuna(args["comuna"])
    else:
        raise ValueError(f"Tool {name} not found")
    

def get_tool_registry() -> list[dict]:
    return TOOL_SCHEMAS