# pytest is a libery that contains test for your code
import pytest

#Test client is a util to make simulated HTTP requests to your API
from fastapi.testclient import TestClient

# My app from the main.py
from src.main import app

# client is the aplication of the TestClient with my app
client = TestClient(app)

def test_health_check():
    """Prueba que el endpoint de salud responda correctamente."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "service": "ai-fde-balancer"}


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