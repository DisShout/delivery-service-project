import pytest


@pytest.mark.asyncio
async def test_get_parcel_types(async_client):
    response = await async_client.get("/parcel-types/")
    assert response.status_code == 200
    parcel_types = response.json()

    assert isinstance(parcel_types, list)
    assert any(pt["name"] == "одежда" for pt in parcel_types)
    assert any(pt["name"] == "электроника" for pt in parcel_types)
    assert any(pt["name"] == "разное" for pt in parcel_types)
