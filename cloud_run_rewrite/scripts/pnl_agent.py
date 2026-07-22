"""
Agente P&L: pregunta en espanol -> Gemini elige tool -> API -> respuesta en prosa.
Uso: python scripts/pnl_agent.py
Comandos REPL: salir, reset
"""
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from google import genai
from google.genai import types

try:
    from google.genai.errors import ClientError
except ImportError:
    ClientError = type("ClientError", (Exception,), {})

from config.settings import settings
from scripts.agent_prompt import SYSTEM_PROMPT
from scripts.tool_registry import TOOL_SCHEMAS, run_tool

MODEL = "gemini-3.1-flash-lite"

_client: genai.Client | None = None


def get_client() -> genai.Client:
    """Lazy init: permite importar el modulo en tests sin GEMINI_API_KEY."""
    global _client
    if _client is None:
        if not settings.gemini_api_key:
            raise ValueError(
                "GEMINI_API_KEY no configurada. Agregala en cloud_run_rewrite/.env"
            )
        _client = genai.Client(api_key=settings.gemini_api_key)
    return _client


_tool_config = [types.Tool(
    function_declarations=[types.FunctionDeclaration(**schema) for schema in TOOL_SCHEMAS]
)]

_generate_config = types.GenerateContentConfig(
    tools=_tool_config,
    system_instruction=SYSTEM_PROMPT,
)


def _extract_function_call(response) -> types.FunctionCall | None:
    if not response.candidates:
        return None
    for part in response.candidates[0].content.parts:
        if part.function_call:
            return part.function_call
    return None


def _format_error(exc: Exception) -> str:
    if isinstance(exc, ClientError):
        msg = str(exc).lower()
        if "429" in msg or "limit" in msg or "quota" in msg:
            return (
                "Cuota de Gemini agotada o limite alcanzado. "
                "Revisa AI Studio -> limites por modelo y usa uno con RPD > 0."
            )
        if "401" in msg or "403" in msg or "api key" in msg:
            return "API key invalida o sin permisos. Revisa GEMINI_API_KEY en .env."
    if isinstance(exc, ValueError) and "Tool" in str(exc):
        return f"Tool desconocida: {exc}"
    return f"Error inesperado: {exc}"


def chat_once(pregunta: str, history: list | None = None) -> tuple[str, list]:
    """Un turno: pregunta -> respuesta. Retorna (texto, history actualizado)."""
    contents = list(history or [])
    contents.append(types.Content(role="user", parts=[types.Part(text=pregunta)]))

    response = get_client().models.generate_content(
        model=MODEL,
        contents=contents,
        config=_generate_config,
    )

    fc = _extract_function_call(response)
    if not fc:
        reply = response.text or "No pude generar una respuesta."
        contents.append(response.candidates[0].content)
        return reply, contents

    tool_result = run_tool(fc.name, dict(fc.args))

    contents.append(response.candidates[0].content)
    contents.append(
        types.Content(
            role="user",
            parts=[
                types.Part(
                    function_response=types.FunctionResponse(
                        name=fc.name,
                        response={"result": tool_result},
                    )
                )
            ],
        )
    )

    response2 = get_client().models.generate_content(
        model=MODEL,
        contents=contents,
        config=_generate_config,
    )
    reply = response2.text or tool_result
    contents.append(response2.candidates[0].content)
    return reply, contents


def main():
    print("Agente P&L · escribe 'salir' para terminar · 'reset' para nueva conversacion")
    history: list = []
    while True:
        pregunta = input("\nTu: ").strip()
        if not pregunta:
            continue
        if pregunta.lower() in ("salir", "exit", "q"):
            print("Chao.")
            break
        if pregunta.lower() == "reset":
            history = []
            print("Conversacion reiniciada.")
            continue
        try:
            reply, history = chat_once(pregunta, history)
            print("Agente:", reply)
        except Exception as e:
            print("Error:", _format_error(e))


if __name__ == "__main__":
    main()
