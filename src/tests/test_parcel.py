import pytest


@pytest.mark.asyncio
async def test_create_parcel(async_client):
    response = await async_client.post(
        "/parcels/",
        json={
            "name": "Тестовая посылка",
            "weight": 2.5,
            "parcel_price_usd": 50,
            "type_id": 1,
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["name"] == "Тестовая посылка"


@pytest.mark.asyncio
async def test_get_parcels(async_client):
    response = await async_client.get("/parcels/")
    assert response.status_code == 200
    parcels = response.json()
    assert isinstance(parcels, list)


@pytest.mark.asyncio
async def test_get_parcel_by_id(async_client):
    # сначала создаём посылку
    create_response = await async_client.post(
        "/parcels/",
        json={
            "name": "Посылка для ID теста",
            "weight": 1.0,
            "parcel_price_usd": 10,
            "type_id": 1,
        },
    )
    parcel_id = create_response.json()["id"]

    # теперь достаём по ID
    response = await async_client.get(f"/parcels/{parcel_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Посылка для ID теста"
    assert "delivery_price_rub" in data
