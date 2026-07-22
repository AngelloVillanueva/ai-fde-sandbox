import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.services.pnl_services import PNLService

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "service": "fde-pnl-api"}


def test_happy_path_get_pnl():
    response = client.get("/api/v1/pnl/45")
    assert response.status_code == 200
    assert response.json() == {
        "tienda_id": 45,
        "ventas": 18569.0,
        "costos": 7918.98,
        "opex": 4522.51,
        "opinc": 6127.51,
        "comuna": "La Granja",
    }


def test_not_found_get_pnl():
    response = client.get("/api/v1/pnl/999")
    assert response.status_code == 404


def test_filter_by_comuna():
    response = client.get("/api/v1/pnl?comuna=La+Granja")
    assert response.status_code == 200
    tiendas = response.json()
    assert len(tiendas) > 0
    assert all(t["comuna"] == "La Granja" for t in tiendas)
    assert 45 in [t["tienda_id"] for t in tiendas]


def test_get_opinc():
    response = client.get("/api/v1/pnl/45/opinc")
    assert response.status_code == 200
    assert response.json() == {"opinc": 6127.51}


def test_get_opinc_not_found():
    response = client.get("/api/v1/pnl/999/opinc")
    assert response.status_code == 404


def test_list_all_tiendas():
    response = client.get("/api/v1/pnl")
    assert response.status_code == 200
    tiendas = response.json()
    assert len(tiendas) == 100


def test_analisis_tienda_45():
    response = client.get("/api/v1/pnl/45/analisis")
    assert response.status_code == 200
    data = response.json()
    assert data["tienda_id"] == 45
    assert data["comuna"] == "La Granja"
    assert data["opinc"] == 6127.51
    assert "margen_pct" in data
    assert "diff_opinc_vs_promedio" in data


def test_analisis_not_found():
    response = client.get("/api/v1/pnl/999/analisis")
    assert response.status_code == 404


def test_pnl_service_analizar_consistency():
    service = PNLService()
    analisis = service.analizar_tienda(45)
    tienda = service.get_tienda_por_id(45)
    assert analisis is not None
    assert analisis["opinc"] == tienda.opinc
