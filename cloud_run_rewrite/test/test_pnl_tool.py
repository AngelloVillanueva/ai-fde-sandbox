from scripts.pnl_tool import (
    formatear_analisis,
    formatear_comuna,
    formatear_portfolio,
    formatear_ranking_comuna,
    formatear_tienda,
)
from unittest.mock import patch, MagicMock
from scripts.pnl_tool import (
    analizar_tienda,
    comparar_tiendas,
    consultar_comuna,
    consultar_opinc,
    consultar_tienda,
    resumen_portfolio,
)

TIENDA_45 = {
    "tienda_id": 45,
    "ventas": 18569.0,
    "costos": 7918.98,
    "opex": 4522.51,
    "opinc": 6127.51,
    "comuna": "La Granja",
}

ANALISIS_45 = {
    "tienda_id": 45,
    "comuna": "La Granja",
    "opinc": 6127.51,
    "margen_pct": 32.99,
    "promedio_portfolio_opinc": 8500.0,
    "promedio_portfolio_margen_pct": 33.0,
    "diff_opinc_vs_promedio": -2372.49,
    "diff_pct_vs_promedio": -27.9,
}


def test_formatear_tienda_seed_42():
    texto = formatear_tienda(TIENDA_45)
    assert "45" in texto
    assert "La Granja" in texto
    assert "6127.51" in texto


def test_formatear_comuna_vacia():
    resultado = formatear_comuna("comunaFake", [])
    assert "No hay tiendas en la comuna comunaFake" in resultado


def test_formatear_portfolio():
    texto = formatear_portfolio([TIENDA_45, {**TIENDA_45, "tienda_id": 12}])
    assert "2 tiendas" in texto
    assert "OPINC total" in texto


def test_formatear_ranking_comuna():
    tiendas = [
        {**TIENDA_45, "tienda_id": 12, "opinc": 3000.0},
        TIENDA_45,
    ]
    texto = formatear_ranking_comuna("La Granja", tiendas)
    assert "Ranking OPINC" in texto
    assert "Tienda 45" in texto
    assert "Mejor: tienda 45" in texto


def test_formatear_analisis():
    texto = formatear_analisis(ANALISIS_45)
    assert "45" in texto
    assert "por debajo" in texto


@patch("scripts.pnl_tool.httpx.get")
def test_consultar_tienda_200(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = TIENDA_45
    mock_get.return_value = mock_response

    resultado = consultar_tienda(45)
    assert "La Granja" in resultado
    mock_get.assert_called_once()


@patch("scripts.pnl_tool.httpx.get")
def test_consultar_tienda_404(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_get.return_value = mock_response

    assert consultar_tienda(999) == "La tienda 999 no existe."


@patch("scripts.pnl_tool.httpx.get")
def test_consultar_comuna_200(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [TIENDA_45]
    mock_get.return_value = mock_response

    resultado = consultar_comuna("La Granja")
    assert "45" in resultado
    assert "La Granja" in resultado


@patch("scripts.pnl_tool.httpx.get")
def test_consultar_opinc_200(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"opinc": 6127.51}
    mock_get.return_value = mock_response

    resultado = consultar_opinc(45)
    assert "6127.51" in resultado
    assert "OPINC" in resultado


@patch("scripts.pnl_tool.httpx.get")
def test_resumen_portfolio_200(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [TIENDA_45]
    mock_get.return_value = mock_response

    resultado = resumen_portfolio()
    assert "Portfolio" in resultado
    assert "1 tiendas" in resultado


@patch("scripts.pnl_tool.httpx.get")
def test_comparar_tiendas_200(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [TIENDA_45]
    mock_get.return_value = mock_response

    resultado = comparar_tiendas("La Granja")
    assert "Ranking OPINC" in resultado


@patch("scripts.pnl_tool.httpx.get")
def test_analizar_tienda_200(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = ANALISIS_45
    mock_get.return_value = mock_response

    resultado = analizar_tienda(45)
    assert "Analisis tienda 45" in resultado
    assert "margen" in resultado
