from scripts.pnl_tool import formatear_tienda, formatear_comuna
from unittest.mock import patch, MagicMock
from scripts.pnl_tool import consultar_tienda, consultar_comuna

def test_formatear_tienda_seed_42():
    data = {
        "tienda_id": 45,
        "ventas": 18569.0,
        "costos": 7918.98,
        "opex": 4522.51,
        "opinc": 6127.51,
        "comuna": "La Granja",
    }
    
    texto = formatear_tienda(data)
    assert "45" in texto
    assert "La Granja" in texto
    assert "6127.51" in texto

def test_formatear_comuna_vacia():
    resultado = formatear_comuna("comunaFake", [])
    assert "No hay tiendas en la comuna comunaFake" in resultado


@patch("scripts.pnl_tool.httpx.get")
def test_consultar_tienda_200(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "tienda_id": 45,
        "ventas": 18569.0,
        "costos": 7918.98,
        "opex": 4522.51,
        "opinc": 6127.51,
        "comuna": "La Granja"
    }
    mock_get.return_value = mock_response

    resultado = consultar_tienda(45)
    assert "La Granja" in resultado
    mock_get.assert_called_once()

@patch("scripts.pnl_tool.httpx.get")
def test_consultar_tienda_404(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_get.return_value = mock_response

    resultado = consultar_tienda(999)

    assert resultado == "La tienda 999 no existe."

@patch("scripts.pnl_tool.httpx.get")
def test_consultar_comuna_200(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [
        {
            "tienda_id": 45,
            "ventas": 18569.0,
            "costos": 7918.98,
            "opex": 4522.51,
            "opinc": 6127.51,
            "comuna": "La Granja"
        }
    ]
    mock_get.return_value = mock_response

    resultado = consultar_comuna("La Granja")

    assert "45" in resultado
    assert "La Granja" in resultado