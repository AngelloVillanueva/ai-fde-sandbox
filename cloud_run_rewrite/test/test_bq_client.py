import pytest
from src.services.bq_cliente import BigQuerySimulatedClient
from src.services.pnl_services import PNLService


@pytest.mark.asyncio
async def test_get_tienda_existente():
    client = BigQuerySimulatedClient()
    result = await client.get_tienda_por_id(45)

    assert result["tienda_id"] == 45
    assert result["status"] == "success"
    assert result["data"].comuna == "La Granja"
    assert result["data"].opinc == 6127.51

@pytest.mark.asyncio
async def test_get_tienda_inexistente():
    client = BigQuerySimulatedClient()
    result = await client.get_tienda_por_id(999)

    assert result["tienda_id"] == 999
    assert result["status"] == "error"
    assert "not found" in result["message"].lower()

@pytest.mark.asyncio
async def test_datos_coinciden_con_pnl_service():
    client = BigQuerySimulatedClient()
    service = PNLService()

    bq_result = await client.get_tienda_por_id(45)
    api_tienda = service.get_tienda_por_id(45)

    assert bq_result["data"].opinc == api_tienda.opinc
    assert bq_result["data"].comuna == api_tienda.comuna
    assert bq_result["data"].tienda_id == api_tienda.tienda_id
