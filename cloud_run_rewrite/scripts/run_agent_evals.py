"""
Eval manual contra Gemini live. No corre en CI.

Uso:
  cd cloud_run_rewrite
  python scripts/run_agent_evals.py
"""
import json
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from scripts.pnl_agent import chat_once, _extract_function_call
from google import genai
from google.genai import types
from config.settings import settings
from scripts.tool_registry import TOOL_SCHEMAS

FIXTURES = _ROOT / "test" / "fixtures" / "agent_eval_cases.json"
MODEL = "gemini-3.1-flash-lite"

_tool_config = [types.Tool(
    function_declarations=[types.FunctionDeclaration(**schema) for schema in TOOL_SCHEMAS]
)]


def route_only(pregunta: str) -> tuple[str | None, dict]:
    client = genai.Client(api_key=settings.gemini_api_key)
    response = client.models.generate_content(
        model=MODEL,
        contents=pregunta,
        config=types.GenerateContentConfig(tools=_tool_config),
    )
    fc = _extract_function_call(response)
    if not fc:
        return None, {}
    return fc.name, dict(fc.args)


def main():
    cases = json.loads(FIXTURES.read_text(encoding="utf-8"))
    passed = 0
    print(f"Eval live: {len(cases)} casos (routing + respuesta)\n")
    for i, case in enumerate(cases, 1):
        print(f"[{i}/{len(cases)}] {case['input']}")
        try:
            name, args = route_only(case["input"])
            routing_ok = name == case["expected_tool"] and args == case["expected_args"]
            print(f"  routing: {name}({args}) -> {'OK' if routing_ok else 'FAIL expected ' + case['expected_tool']}")
            reply, _ = chat_once(case["input"])
            grounded_ok = all(
                t.lower() in reply.lower() for t in case.get("grounded_contains", [])
            ) if case.get("grounded_contains") else True
            print(f"  grounded: {'OK' if grounded_ok else 'FAIL'}")
            print(f"  reply: {reply[:120]}...")
            if routing_ok and grounded_ok:
                passed += 1
        except Exception as e:
            print(f"  ERROR: {e}")
        print()
    print(f"Resultado: {passed}/{len(cases)} passed")


if __name__ == "__main__":
    main()
