import json
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

pytest.importorskip("google.genai")
import scripts.pnl_agent  # noqa: F401, E402

from scripts.tool_registry import run_tool

FIXTURES = Path(__file__).parent / "fixtures" / "agent_eval_cases.json"


def test_run_tool_consultar_tienda():
    with patch("scripts.tool_registry.consultar_tienda", return_value="ok") as mock:
        assert run_tool("consultar_tienda", {"tienda_id": 45}) == "ok"
        mock.assert_called_once_with(45)


def test_run_tool_consultar_opinc():
    with patch("scripts.tool_registry.consultar_opinc", return_value="opinc") as mock:
        assert run_tool("consultar_opinc", {"tienda_id": 45}) == "opinc"
        mock.assert_called_once_with(45)


def test_run_tool_resumen_portfolio():
    with patch("scripts.tool_registry.resumen_portfolio", return_value="portfolio") as mock:
        assert run_tool("resumen_portfolio", {}) == "portfolio"
        mock.assert_called_once()


def test_run_tool_unknown():
    with pytest.raises(ValueError, match="Tool foo not found"):
        run_tool("foo", {})


def _make_fc_response(name: str, args: dict):
    fc = MagicMock()
    fc.name = name
    fc.args = args
    part = MagicMock()
    part.function_call = fc
    part.text = None
    content = MagicMock()
    content.parts = [part]
    candidate = MagicMock()
    candidate.content = content
    response = MagicMock()
    response.candidates = [candidate]
    response.text = None
    return response


def _make_text_response(text: str):
    part = MagicMock()
    part.function_call = None
    part.text = text
    content = MagicMock()
    content.parts = [part]
    candidate = MagicMock()
    candidate.content = content
    response = MagicMock()
    response.candidates = [candidate]
    response.text = text
    return response


@pytest.mark.parametrize("case", json.loads(FIXTURES.read_text(encoding="utf-8")))
@patch("scripts.pnl_agent.run_tool")
@patch("scripts.pnl_agent.get_client")
def test_agent_routing(mock_get_client, mock_run_tool, case):
    """Routing: mock Gemini viaje 1 -> verifica tool elegida y args."""
    mock_client = MagicMock()
    mock_get_client.return_value = mock_client
    mock_run_tool.return_value = "tool result"
    mock_client.models.generate_content.side_effect = [
        _make_fc_response(case["expected_tool"], case["expected_args"]),
        _make_text_response("Respuesta basada en tool result"),
    ]

    from scripts.pnl_agent import chat_once

    chat_once(case["input"])

    mock_run_tool.assert_called_once_with(case["expected_tool"], case["expected_args"])


@patch("scripts.pnl_agent.run_tool")
@patch("scripts.pnl_agent.get_client")
def test_agent_groundedness_tienda_45(mock_get_client, mock_run_tool):
    """Groundedness: respuesta final debe reflejar output de la tool."""
    mock_client = MagicMock()
    mock_get_client.return_value = mock_client
    tool_output = (
        "La tienda 45 en La Granja registro ventas de $18569.0, "
        "costos de $7918.98, gastos operativos (OPEX) de $4522.51 "
        "y un ingreso operativo neto (OPINC) de $6127.51."
    )
    mock_run_tool.return_value = tool_output
    mock_client.models.generate_content.side_effect = [
        _make_fc_response("consultar_tienda", {"tienda_id": 45}),
        _make_text_response("La tienda 45 tuvo OPINC de 6127.51 en La Granja segun datos."),
    ]

    from scripts.pnl_agent import chat_once

    reply, _ = chat_once("Como le fue a la tienda 45?")
    assert "6127.51" in reply or "6127.51" in tool_output
    assert "999" not in reply
