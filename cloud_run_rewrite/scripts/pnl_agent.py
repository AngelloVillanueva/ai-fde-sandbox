"""
Agente P&L: pregunta en español → Gemini elige tool → API → respuesta en prosa.
Uso: python scripts/pnl_agent.py
"""
import sys
from pathlib import Path

# Permite importar config/ y scripts/ desde cloud_run_rewrite/
_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from google import genai
from google.genai import types
from config.settings import settings
from scripts.tool_registry import TOOL_SCHEMAS, run_tool

MODEL = "gemini-2.0-flash"

client = genai.Client(api_key=settings.gemini_api_key)

_tool_config = [types.Tool(
    function_declarations=[types.FunctionDeclaration(**schema) for schema in TOOL_SCHEMAS]
)]


def chat_once(pregunta: str) -> str:
    # Viaje 1: Gemini decide qué tool usar
    response = client.models.generate_content(
        model=MODEL,
        contents=pregunta,
        config=types.GenerateContentConfig(tools=_tool_config),
    )

    part = response.candidates[0].content.parts[0]

    if not part.function_call:
        return response.text

    fc = part.function_call
    tool_result = run_tool(fc.name, dict(fc.args))

    # Viaje 2: devolver resultado de la tool a Gemini para respuesta en prosa
    response2 = client.models.generate_content(
        model=MODEL,
        contents=[
            types.Content(role="user", parts=[types.Part(text=pregunta)]),
            types.Content(role="model", parts=[types.Part(function_call=fc)]),
            types.Content(
                role="user",
                parts=[types.Part(
                    function_response=types.FunctionResponse(
                        name=fc.name,
                        response={"result": tool_result},
                    )
                )],
            ),
        ],
        config=types.GenerateContentConfig(tools=_tool_config),
    )
    return response2.text


def main():
    print("Agente P&L · escribe 'salir' para terminar")
    while True:
        pregunta = input("\nTú: ").strip()
        if not pregunta or pregunta.lower() in ("salir", "exit", "q"):
            print("Chao.")
            break
        try:
            print("Agente:", chat_once(pregunta))
        except Exception as e:
            print("Error:", e)


if __name__ == "__main__":
    main()
